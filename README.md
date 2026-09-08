# Bible Quiz Live

A projector-friendly, host-operated Bible quiz built with Python and Streamlit. Teams answer verbally while the host controls reveal, scoring, pacing, and language.

## Run locally

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Features

- 2-10 dynamically named teams, with live rankings and leader highlighting.
- 10/20/30/50/custom question counts, category and difficulty filters, configurable points, and optional countdown timer.
- English and Nepali question banks with stable shared IDs.
- Light and dark themes with an optional Bible-manga background texture for the host screen.
- Language switching during an active question preserves question ID, progress, scores, used IDs, reveal state, and timer timestamp.
- Validation for required fields, exactly four unique options, valid answers, duplicate IDs, and missing translations.
- No database or paid service. All state is local to the Streamlit session.

## Question bank format

Add records to each `data/questions_*.json` file using the same ID in all languages:

```json
{
  "id": "JHN002",
  "question": "What did Jesus turn water into?",
  "options": ["Oil", "Wine", "Milk", "Juice"],
  "correct_answer": "Wine",
  "category": "Miracles",
  "difficulty": "Easy",
  "bible_reference": "John 2:7-11",
  "explanation": "At Cana, Jesus turned water into wine."
}
```

The English bank is the canonical pool used for filtering and randomization. A missing Nepali record falls back to English with a visible warning and never changes the current question.

## Streamlit Community Cloud

Push this folder to GitHub, choose `app.py` as the main file, and Streamlit Community Cloud will install `requirements.txt`. The app requires no secrets or external services.

The theme controls live in the sidebar and persist through Streamlit reruns. The manga background is a local SVG asset in `assets/bible_manga_background.svg`, so it does not depend on an external image host.

## Generate a large question bank

The optional generator uses the `XAI_API_KEY` from `.streamlit/secrets.toml` or the environment. It is run before the event, not during live play. Install dependencies and preview the plan first:

```powershell
pip install -r requirements.txt
python tools\generate_question_bank.py --per-category 100 --batch-size 5 --dry-run
```

When the plan looks right, run without `--dry-run`:

```powershell
python tools\generate_question_bank.py --per-category 100 --batch-size 5
```

This generates questions for each named category in English and Nepali, balances the three difficulty levels toward Medium and Hard, validates the structured output, assigns stable shared IDs, and appends the results to the existing JSON banks. The API call can use credits, so review the generated files before committing them.

### Free local generation with Ollama

If Ollama is installed locally, no API key or paid service is needed. Check the installed model with `ollama list`, then use the local provider:

```powershell
python tools\generate_question_bank.py --provider ollama --model qwen3:4b --per-category 100 --batch-size 1
```

Ollama generation can take a long time on a small local model. Start with `--per-category 1 --batch-size 1` to verify the model, then increase the target after checking the output. The app itself remains fully local and reads the generated JSON files.

## State model

`st.session_state` stores the screen, language, settings, team names, scores, randomized question IDs, used question IDs, current question, reveal/award state, and timer timestamps. Navigation actions mutate only the relevant state and rerun the app, so Streamlit reruns do not restart an active quiz.
