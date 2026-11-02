"""Keep shared filtering metadata identical across English and Nepali banks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    en_path = ROOT / "data" / "questions_en.json"
    ne_path = ROOT / "data" / "questions_ne.json"
    english = json.loads(en_path.read_text(encoding="utf-8"))
    nepali = json.loads(ne_path.read_text(encoding="utf-8"))
    english_by_id = {record["id"]: record for record in english}
    for record in nepali:
        source = english_by_id[record["id"]]
        record["category"] = source["category"]
        record["difficulty"] = source["difficulty"]
    ne_path.write_text(json.dumps(nepali, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Synchronized metadata for {len(nepali)} Nepali records.")


if __name__ == "__main__":
    main()
