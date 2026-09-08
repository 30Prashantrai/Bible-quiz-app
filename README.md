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
- English, Hindi, and Nepali question banks with stable shared IDs.
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

The English bank is the canonical pool used for filtering and randomization. A missing Hindi or Nepali record falls back to English with a visible warning and never changes the current question.

## Streamlit Community Cloud

Push this folder to GitHub, choose `app.py` as the main file, and Streamlit Community Cloud will install `requirements.txt`. The app requires no secrets or external services.

The theme controls live in the sidebar and persist through Streamlit reruns. The manga background is a local SVG asset in `assets/bible_manga_background.svg`, so it does not depend on an external image host.

## State model

`st.session_state` stores the screen, language, settings, team names, scores, randomized question IDs, used question IDs, current question, reveal/award state, and timer timestamps. Navigation actions mutate only the relevant state and rerun the app, so Streamlit reruns do not restart an active quiz.
