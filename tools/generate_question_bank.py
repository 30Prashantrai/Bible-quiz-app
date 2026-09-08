"""Generate a large, validated multilingual Bible question bank with xAI/Grok.

This is an opt-in offline preparation tool. It never runs from the live quiz.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"
LANGUAGES = ("en", "ne")
CATEGORIES = ("Old Testament", "New Testament", "People", "Places", "Miracles", "Parables", "Books", "Events", "Teachings", "Mixed")
DIFFICULTIES = ("Easy", "Medium", "Hard")
# Keep the bank challenging while retaining enough accessible questions for
# mixed groups. At 50 questions per category this becomes 10/18/22.
DIFFICULTY_WEIGHTS = {"Easy": 0.20, "Medium": 0.36, "Hard": 0.44}

LOCALIZED_FIELDS = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "question": {"type": "string"},
        "options": {"type": "array", "items": {"type": "string"}, "minItems": 4, "maxItems": 4},
        "correct_answer": {"type": "string"},
        "explanation": {"type": "string"},
        "bible_reference": {"type": "string"},
    },
    "required": ["question", "options", "correct_answer", "explanation", "bible_reference"],
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "category": {"type": "string", "enum": list(CATEGORIES)},
                    "difficulty": {"type": "string", "enum": list(DIFFICULTIES)},
                    "en": LOCALIZED_FIELDS,
                    "ne": LOCALIZED_FIELDS,
                },
                "required": ["category", "difficulty", "en", "ne"],
            },
        }
    },
    "required": ["questions"],
}


def load_key() -> str:
    if os.getenv("XAI_API_KEY"):
        return os.environ["XAI_API_KEY"]
    secrets_path = ROOT / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        with secrets_path.open("rb") as handle:
            secrets = tomllib.load(handle)
        key = secrets.get("XAI_API_KEY") or secrets.get("xai", {}).get("api_key")
        if key:
            return str(key)
    raise SystemExit("XAI_API_KEY was not found in .streamlit/secrets.toml or the environment.")


def load_banks() -> dict[str, list[dict]]:
    banks = {}
    for lang in LANGUAGES:
        path = DATA / f"questions_{lang}.json"
        banks[lang] = json.loads(path.read_text(encoding="utf-8"))
    return banks


def plan(per_category: int) -> list[tuple[str, str]]:
    targets = []
    easy_count = max(1, round(per_category * DIFFICULTY_WEIGHTS["Easy"]))
    medium_count = max(1, round(per_category * DIFFICULTY_WEIGHTS["Medium"]))
    hard_count = per_category - easy_count - medium_count
    if hard_count < 1:
        hard_count = 1
        medium_count = max(1, per_category - easy_count - hard_count)
    difficulty_slots = (["Easy"] * easy_count + ["Medium"] * medium_count + ["Hard"] * hard_count)
    for category in CATEGORIES[:-1]:
        targets.extend((category, difficulty) for difficulty in difficulty_slots)
    return targets


def validate_batch(batch: list[dict], expected: list[tuple[str, str]]) -> None:
    if len(batch) != len(expected):
        raise ValueError(f"Model returned {len(batch)} questions; expected {len(expected)}")
    for item, (category, difficulty) in zip(batch, expected):
        if item["category"] != category or item["difficulty"] != difficulty:
            raise ValueError("Model changed the requested category or difficulty")
        for lang in LANGUAGES:
            localized = item[lang]
            if len(localized["options"]) != 4 or len(set(localized["options"])) != 4:
                raise ValueError(f"{lang}: options must contain exactly four unique values")
            if localized["correct_answer"] not in localized["options"]:
                raise ValueError(f"{lang}: correct answer is not one of the options")
            if lang != "en":
                if localized["question"].strip() == item["en"]["question"].strip():
                    raise ValueError(f"{lang}: question was returned in English instead of being translated")
                if localized["options"] == item["en"]["options"]:
                    raise ValueError(f"{lang}: answer options were returned in English instead of being translated")
                if localized["explanation"].strip() == item["en"]["explanation"].strip():
                    raise ValueError(f"{lang}: explanation was returned in English instead of being translated")


def request_batch(client, targets: list[tuple[str, str]], model: str, provider: str, ollama_url: str) -> list[dict]:
    target_text = "\n".join(f"{index + 1}. category={category}; difficulty={difficulty}" for index, (category, difficulty) in enumerate(targets))
    messages = [
        {"role": "system", "content": "You create accurate Christian Bible quiz questions. Use canonical Bible facts, avoid duplicates, trick wording, denominational controversy, and invented citations. Return only the requested JSON schema."},
        {"role": "user", "content": f"Generate exactly one question for each requested slot below. Produce natural English and Nepali versions. Each language needs four translated options, a translated correct answer, explanation, and Bible reference.\n\nRequested slots:\n{target_text}"},
    ]
    batch_schema = {**SCHEMA, "properties": {"questions": {**SCHEMA["properties"]["questions"], "minItems": len(targets), "maxItems": len(targets)}}}
    if provider == "ollama":
        # Qwen3 can spend a long time in its internal reasoning mode. The task
        # already has a strict schema, so disable that extra reasoning pass.
        request_body = json.dumps({
            "model": model,
            "messages": messages,
            "stream": False,
            "think": False,
            # Full schema-constrained decoding is very slow on small local
            # models. JSON mode is faster; validate_batch still enforces the
            # required shape before anything is written to disk.
            "format": "json",
            "keep_alive": "10m",
            "options": {"temperature": 0.2, "num_predict": 1400},
        }).encode("utf-8")
        request = urllib.request.Request(f"{ollama_url.rstrip('/')}/api/chat", data=request_body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=900) as response:
            result = json.loads(response.read().decode("utf-8"))
        payload = json.loads(result["message"]["content"])
    else:
        response = client.chat.completions.create(
            model=model,
            temperature=0.4,
            messages=messages,
            response_format={"type": "json_schema", "json_schema": {"name": "bible_question_batch", "strict": True, "schema": batch_schema}},
        )
        payload = json.loads(response.choices[0].message.content)
    batch = payload["questions"]
    validate_batch(batch, targets)
    return batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-category", type=int, default=100, help="Questions required for each named category")
    parser.add_argument("--batch-size", type=int, default=5, help="Questions generated per API call")
    parser.add_argument("--model", default="grok-4.6", help="xAI model name")
    parser.add_argument("--provider", choices=["xai", "ollama"], default="xai", help="Question generation provider")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434", help="Ollama server URL")
    parser.add_argument("--dry-run", action="store_true", help="Show the generation plan without calling the API")
    args = parser.parse_args()
    if args.per_category < 1 or args.batch_size < 1:
        raise SystemExit("per-category and batch-size must be positive")
    targets = plan(args.per_category)
    print(f"Plan: {len(targets)} unique questions across {len(CATEGORIES) - 1} categories and three difficulty levels.")
    if args.dry_run:
        return
    client = None
    if args.provider == "xai":
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise SystemExit("Install requirements.txt first: pip install -r requirements.txt") from exc
        client = OpenAI(api_key=load_key(), base_url="https://api.x.ai/v1")
    banks = load_banks()
    existing_ids = {record["id"] for record in banks["en"]}
    next_number = 1
    generated = []
    for start in range(0, len(targets), args.batch_size):
        batch_targets = targets[start:start + args.batch_size]
        print(f"Requesting batch {start // args.batch_size + 1} ({len(batch_targets)} question(s))...", flush=True)
        for attempt in range(3):
            try:
                generated.extend(request_batch(client, batch_targets, args.model, args.provider, args.ollama_url))
                break
            except Exception as exc:
                if attempt == 2:
                    raise SystemExit(f"Batch {start + 1} failed after three attempts: {exc}") from exc
                print(f"Retrying batch {start + 1}: {exc}", file=sys.stderr)
                time.sleep(2 ** attempt)
        print(f"Generated {len(generated)}/{len(targets)}")

    for item in generated:
        while f"AI{next_number:05d}" in existing_ids:
            next_number += 1
        qid = f"AI{next_number:05d}"
        existing_ids.add(qid)
        for lang in LANGUAGES:
            localized = item[lang]
            banks[lang].append({"id": qid, "question": localized["question"], "options": localized["options"], "correct_answer": localized["correct_answer"], "category": item["category"], "difficulty": item["difficulty"], "bible_reference": localized["bible_reference"], "explanation": localized["explanation"]})
        next_number += 1

    for lang in LANGUAGES:
        (DATA / f"questions_{lang}.json").write_text(json.dumps(banks[lang], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(generated)} new questions to both language files.")


if __name__ == "__main__":
    main()
