from __future__ import annotations

import base64
import html
import json
import random
import time
from pathlib import Path
from typing import Any

import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


ROOT = Path(__file__).parent
LANGUAGES = ["en", "ne"]
LANGUAGE_NAMES = {"en": "English", "ne": "नेपाली"}
REQUIRED_FIELDS = {"id", "question", "options", "correct_answer", "category", "difficulty", "bible_reference", "explanation"}
CATEGORIES = ["Old Testament", "New Testament", "People", "Places", "Miracles", "Parables", "Books", "Events", "Teachings", "Mixed"]
DIFFICULTIES = ["Easy", "Medium", "Hard", "Mixed"]
LABELS = {
    "en": {"Old Testament":"Old Testament", "New Testament":"New Testament", "People":"People", "Places":"Places", "Miracles":"Miracles", "Parables":"Parables", "Books":"Books", "Events":"Events", "Teachings":"Teachings", "Mixed":"Mixed", "Easy":"Easy", "Medium":"Medium", "Hard":"Hard"},
    "hi": {"Old Testament":"पुराना नियम", "New Testament":"नया नियम", "People":"लोग", "Places":"स्थान", "Miracles":"चमत्कार", "Parables":"दृष्टान्त", "Books":"पुस्तकें", "Events":"घटनाएँ", "Teachings":"शिक्षाएँ", "Mixed":"मिश्रित", "Easy":"आसान", "Medium":"मध्यम", "Hard":"कठिन"},
    "ne": {"Old Testament":"पुरानो नियम", "New Testament":"नयाँ नियम", "People":"व्यक्तिहरू", "Places":"स्थानहरू", "Miracles":"चमत्कारहरू", "Parables":"दृष्टान्तहरू", "Books":"पुस्तकहरू", "Events":"घटनाहरू", "Teachings":"शिक्षाहरू", "Mixed":"मिश्रित", "Easy":"सजिलो", "Medium":"मध्यम", "Hard":"गाह्रो"},
}

COPY = {
    "en": {
        "home": "Bible Quiz Live", "tagline": "A joyful, projector-ready Bible challenge for teams.", "host": "HOST CONSOLE",
        "start": "Start a new quiz", "setup": "Quiz setup", "teams": "Team setup", "continue": "Continue",
        "back": "Back", "language": "Language", "projector": "Projector-friendly mode", "questions": "Questions",
        "difficulty": "Difficulty", "category": "Category", "points": "Points per question", "timer": "Timer",
        "seconds": "seconds", "disabled": "Disabled", "custom": "Custom", "team_count": "Number of teams",
        "team_names": "Team names", "team_hint": "Give each team a name your host can call out.", "launch": "Launch quiz",
        "question": "Question", "of": "of", "reveal": "Reveal answer", "correct": "Correct answer",
        "reference": "Bible reference", "explanation": "Explanation", "award": "Award points", "no_points": "No points",
        "next": "Next question", "scoreboard": "Live scoreboard", "leader": "Current leader", "time_up": "TIME'S UP",
        "remaining": "remaining", "final": "Final results", "winner": "Winner", "played": "questions played",
        "play_again": "Play again", "new_quiz": "New quiz", "home_btn": "Home", "rank": "Rank", "score": "Score",
        "points_awarded": "points awarded", "missing": "Translation unavailable. Showing English for this question.",
        "bank_limit": "Only {available} matching questions are available for this filter; the quiz will use all of them.",
        "setup_note": "Choose the pace and feel of your game. You can switch the quiz language at any time once play begins.",
        "team_note": "Teams answer verbally. The host reveals the answer, then awards points manually.",
        "start_over": "Start over", "validation": "Question bank validation", "available": "available",
        "same_answer": "Correct answer", "question_number": "Question number", "settings": "Game settings",
        "theme": "Theme", "light": "Light", "dark": "Dark", "manga_background": "Bible manga background",
        "matching": "{count} questions match the selected filters.",
    },
    "hi": {
        "home": "बाइबल क्विज लाइव", "tagline": "टीमों के लिए आनंदमय, प्रोजेक्टर-रेडी बाइबल चुनौती।", "host": "होस्ट कंसोल",
        "start": "नई क्विज़ शुरू करें", "setup": "क्विज़ सेटअप", "teams": "टीम सेटअप", "continue": "आगे बढ़ें",
        "back": "वापस", "language": "भाषा", "projector": "प्रोजेक्टर मोड", "questions": "प्रश्न",
        "difficulty": "कठिनाई", "category": "श्रेणी", "points": "प्रति प्रश्न अंक", "timer": "टाइमर",
        "seconds": "सेकंड", "disabled": "बंद", "custom": "कस्टम", "team_count": "टीमों की संख्या",
        "team_names": "टीम के नाम", "team_hint": "हर टीम को एक नाम दें जिसे होस्ट पुकार सके।", "launch": "क्विज़ शुरू करें",
        "question": "प्रश्न", "of": "में से", "reveal": "उत्तर दिखाएँ", "correct": "सही उत्तर",
        "reference": "बाइबल संदर्भ", "explanation": "व्याख्या", "award": "अंक दें", "no_points": "अंक नहीं",
        "next": "अगला प्रश्न", "scoreboard": "लाइव स्कोरबोर्ड", "leader": "वर्तमान नेता", "time_up": "समय समाप्त",
        "remaining": "शेष", "final": "अंतिम परिणाम", "winner": "विजेता", "played": "प्रश्न खेले गए",
        "play_again": "फिर खेलें", "new_quiz": "नई क्विज़", "home_btn": "होम", "rank": "रैंक", "score": "अंक",
        "points_awarded": "अंक दिए गए", "missing": "अनुवाद उपलब्ध नहीं है। इस प्रश्न के लिए अंग्रेज़ी दिखाई जा रही है।",
        "bank_limit": "इस फ़िल्टर के लिए केवल {available} प्रश्न उपलब्ध हैं; क्विज़ इन सभी का उपयोग करेगी।",
        "setup_note": "अपने खेल की गति चुनें। खेल शुरू होने के बाद भी भाषा कभी भी बदली जा सकती है।",
        "team_note": "टीमें मौखिक उत्तर देंगी। होस्ट उत्तर दिखाकर मैन्युअल रूप से अंक देगा।", "start_over": "फिर से शुरू करें",
        "validation": "प्रश्न बैंक जाँच", "available": "उपलब्ध", "same_answer": "सही उत्तर", "question_number": "प्रश्न संख्या", "settings": "खेल सेटिंग्स",
        "theme": "थीम", "light": "लाइट", "dark": "डार्क", "manga_background": "बाइबल मंगा बैकग्राउंड",
        "matching": "चयनित फ़िल्टर से {count} प्रश्न मेल खाते हैं।",
    },
    "ne": {
        "home": "बाइबल क्विज लाइभ", "tagline": "टोलीहरूका लागि रमाइलो, प्रोजेक्टर-मैत्री बाइबल चुनौती।", "host": "होस्ट कन्सोल",
        "start": "नयाँ क्विज सुरु गर्नुहोस्", "setup": "क्विज सेटअप", "teams": "टोली सेटअप", "continue": "अगाडि",
        "back": "पछाडि", "language": "भाषा", "projector": "प्रोजेक्टर मोड", "questions": "प्रश्न",
        "difficulty": "कठिनाइ", "category": "वर्ग", "points": "प्रति प्रश्न अंक", "timer": "टाइमर",
        "seconds": "सेकेन्ड", "disabled": "बन्द", "custom": "कस्टम", "team_count": "टोली संख्या",
        "team_names": "टोलीका नाम", "team_hint": "होस्टले बोलाउन सक्ने गरी प्रत्येक टोलीको नाम राख्नुहोस्।", "launch": "क्विज सुरु गर्नुहोस्",
        "question": "प्रश्न", "of": "मध्ये", "reveal": "उत्तर देखाउनुहोस्", "correct": "सही उत्तर",
        "reference": "बाइबल सन्दर्भ", "explanation": "व्याख्या", "award": "अंक दिनुहोस्", "no_points": "अंक छैन",
        "next": "अर्को प्रश्न", "scoreboard": "लाइभ स्कोरबोर्ड", "leader": "अहिले अगाडि", "time_up": "समय सकियो",
        "remaining": "बाँकी", "final": "अन्तिम नतिजा", "winner": "विजेता", "played": "प्रश्न खेलिए",
        "play_again": "फेरि खेल्नुहोस्", "new_quiz": "नयाँ क्विज", "home_btn": "होम", "rank": "स्थान", "score": "अंक",
        "points_awarded": "अंक दिइयो", "missing": "अनुवाद उपलब्ध छैन। यस प्रश्नका लागि अंग्रेजी देखाइएको छ।",
        "bank_limit": "यो फिल्टरका लागि {available} प्रश्न मात्र उपलब्ध छन्; क्विजले सबै प्रयोग गर्नेछ।",
        "setup_note": "खेलको गति छान्नुहोस्। खेल सुरु भएपछि पनि भाषा जुनसुकै बेला बदल्न सकिन्छ।",
        "team_note": "टोलीहरूले मौखिक उत्तर दिनेछन्। होस्टले उत्तर देखाएर हातैले अंक दिनेछ।", "start_over": "फेरि सुरु गर्नुहोस्",
        "validation": "प्रश्न बैंक जाँच", "available": "उपलब्ध", "same_answer": "सही उत्तर", "question_number": "प्रश्न नम्बर", "settings": "खेल सेटिङहरू",
        "theme": "थीम", "light": "लाइट", "dark": "डार्क", "manga_background": "बाइबल मंगा पृष्ठभूमि",
        "matching": "चयन गरिएका फिल्टरसँग {count} प्रश्न मिल्छन्।",
    },
}


def t(key: str, lang: str | None = None, **kwargs: Any) -> str:
    lang = lang or st.session_state.get("selected_language", "en")
    value = COPY.get(lang, COPY["en"]).get(key, COPY["en"].get(key, key))
    return value.format(**kwargs)


def inject_css(projector: bool = False, theme: str = "light", manga_background: bool = True) -> None:
    scale = "1.16" if projector else "1"
    manga_uri = ""
    manga_path = ROOT / "assets" / "bible_manga_background.svg"
    if manga_background and manga_path.exists():
        manga_uri = base64.b64encode(manga_path.read_bytes()).decode("ascii")
    if theme == "dark":
        palette = "--ink:#eef6f3; --muted:#aebfbb; --cream:#0c1417; --paper:#172328; --soft:#203237; --leader:#3a3020; --warning-bg:#4a3a16; --warning-fg:#fff3b0; --warning-border:#a8842f; --question-bg:#172328; --question-fg:#eef6f3; --teal:#62d1c1; --teal2:#173d3b; --gold:#f0bb55; --coral:#f17a66; --line:#304449;"
        overlay = "linear-gradient(rgba(12,20,23,.77),rgba(12,20,23,.77))"
    else:
        palette = "--ink:#17212b; --muted:#66727d; --cream:#fbfaf7; --paper:#ffffff; --soft:#fffaf0; --leader:#fffaf0; --warning-bg:#fff3b0; --warning-fg:#4b3900; --warning-border:#d6ae28; --question-bg:#17212b; --question-fg:#ffffff; --teal:#0f766e; --teal2:#d9f3ee; --gold:#d99b27; --coral:#c9553f; --line:#e6e7e5;"
        overlay = "linear-gradient(rgba(251,250,247,.86),rgba(251,250,247,.86))"
    background = f", url(data:image/svg+xml;base64,{manga_uri})" if manga_uri else ""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    :root {{ {palette} }}
    .stApp {{ background-color:var(--cream); background-image:{overlay}{background}; background-size:cover; background-attachment:fixed; color:var(--ink); font-family:'DM Sans',sans-serif; }}
    .block-container {{ max-width: 1380px; padding: 2.1rem 3.5rem 3rem; }}
    h1,h2,h3 {{ color:var(--ink); letter-spacing:0; }} h1 {{ font-family:'Playfair Display',serif; font-size:clamp(2.4rem,5vw,5rem); line-height:1.02; }} h2 {{ font-size:2rem; }}
    .eyebrow {{ color:var(--teal); font-size:.76rem; font-weight:700; letter-spacing:.15em; text-transform:uppercase; }}
    .hero {{ border-bottom:1px solid var(--line); padding:1rem 0 2.4rem; margin-bottom:2.2rem; }}
    .hero p {{ color:var(--muted); font-size:1.12rem; max-width:660px; margin-top:-.6rem; }}
    .panel {{ background:var(--paper); color:var(--ink); border:1px solid var(--line); border-radius:12px; padding:1.3rem 1.45rem; box-shadow:0 10px 34px rgba(23,33,43,.055); margin-bottom:1.1rem; }}
    .panel-title {{ font-weight:700; font-size:1.03rem; margin-bottom:.7rem; }}
    .question-card {{ background:var(--question-bg) !important; color:var(--question-fg) !important; border-radius:16px; padding:2.2rem 2.4rem; min-height:220px; display:flex; flex-direction:column; justify-content:center; box-shadow:0 14px 34px rgba(23,33,43,.16); }}
    .question-card .eyebrow {{ color:#8de0d2 !important; }} .question-card .question-text {{ color:var(--question-fg) !important; font-family:'Playfair Display',serif; font-size:clamp(1.75rem,3.3vw,3.35rem); line-height:1.14; margin-top:.7rem; }}
    .option-letter {{ color:var(--gold); font-weight:700; margin-right:.65rem; }}
    .score-card {{ border:1px solid var(--line); background:var(--paper); color:var(--ink); border-radius:10px; padding:.9rem 1rem; margin-bottom:.6rem; display:flex; align-items:center; justify-content:space-between; }}
    .score-card.leader {{ border:2px solid var(--gold); background:var(--leader); }} .score-name {{ font-weight:700; }} .score-value {{ font-weight:700; font-size:1.45rem; color:var(--teal); }}
    .winner {{ background:linear-gradient(110deg,#124a45,#0f766e); color:white; border-radius:16px; padding:2rem; text-align:center; }} .winner h2 {{ color:white; font-family:'Playfair Display',serif; margin:.25rem 0; }}
    .answer-box {{ border-left:5px solid var(--gold); background:var(--soft); color:var(--ink); padding:1.15rem 1.3rem; border-radius:8px; margin:1rem 0; }} .answer-main {{ font-size:1.6rem; font-weight:700; }}
    .translation-warning {{ background:var(--warning-bg); color:var(--warning-fg) !important; border:1px solid var(--warning-border); border-left:5px solid var(--gold); border-radius:8px; padding:.85rem 1rem; margin:1rem 0; font-weight:700; }}
    .timer {{ color:var(--coral); font-size:2rem; font-weight:700; text-align:right; }} .timer.safe {{ color:var(--teal); }}
    .stButton > button {{ border-radius:8px; border:1px solid var(--line); min-height:3rem; font-size:1rem; font-weight:700; color:var(--ink); background:var(--paper); transition:all .18s ease; }}
    .stButton > button:hover {{ border-color:var(--teal); color:var(--teal); transform:translateY(-1px); }} .stButton > button[kind='primary'] {{ background:var(--teal); color:white; border-color:var(--teal); }}
    [data-testid='stWidgetLabel'] p, [data-testid='stCaptionContainer'], .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label, .stCheckbox label, .stRadio label {{ color:var(--ink); }}
    [data-testid='stSidebar'] {{ background:var(--cream); }} [data-testid='stSidebar'] * {{ color:var(--ink); }}
    [data-testid='stMetricValue'] {{ color:var(--teal); }} .stProgress > div > div > div > div {{ background:var(--gold); }}
    .projector-mode .question-text {{ font-size:clamp(2.2rem,4.4vw,4.4rem); }}
    @media (max-width: 800px) {{ .block-container {{ padding:1.1rem 1rem 2rem; }} .question-card {{ padding:1.6rem; }} .timer {{ text-align:left; margin-top:.5rem; }} }}
    </style>
    <div class='{'projector-mode' if projector else ''}'></div>
    """, unsafe_allow_html=True)


def load_banks() -> tuple[dict[str, dict[str, dict[str, Any]]], list[str]]:
    banks: dict[str, dict[str, dict[str, Any]]] = {}
    errors: list[str] = []
    for lang in LANGUAGES:
        path = ROOT / "data" / f"questions_{lang}.json"
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
            banks[lang] = {}
            continue
        records = raw if isinstance(raw, list) else raw.get("questions", [])
        lang_bank: dict[str, dict[str, Any]] = {}
        for index, item in enumerate(records):
            missing = REQUIRED_FIELDS - set(item)
            options = item.get("options", [])
            if missing or len(options) != 4 or len(set(options)) != 4 or item.get("correct_answer") not in options:
                errors.append(f"{lang} question {index + 1} ({item.get('id', 'unknown')}): invalid fields/options")
                continue
            if item["id"] in lang_bank:
                errors.append(f"{lang}: duplicate ID {item['id']}")
                continue
            lang_bank[item["id"]] = item
        banks[lang] = lang_bank
    common = sorted(set.intersection(*(set(banks.get(lang, {})) for lang in LANGUAGES))) if banks else []
    return banks, errors + [f"Missing translation IDs: {lang}" for lang in LANGUAGES for lang in sorted(set(banks.get("en", {})) - set(banks.get(lang, {})))]


def bank_signature() -> tuple[int, ...]:
    return tuple((ROOT / "data" / f"questions_{lang}.json").stat().st_mtime_ns for lang in LANGUAGES)


def init_state() -> None:
    defaults = {
        "screen": "home", "selected_language": "en", "projector_mode": False, "team_count": 4,
        "theme": "light", "manga_background": True,
        "team_names": [], "scores": {}, "settings": {}, "question_ids": [], "used_question_ids": [],
        "current_question_id": None, "question_number": 0, "answer_revealed": False, "timer_expired": False,
        "question_started_at": None, "timer_stopped_at": None, "awarded_team": None, "awarded_points": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    if st.session_state.selected_language not in LANGUAGES:
        st.session_state.selected_language = "en"
        st.session_state.pop("language_selector", None)
    # Reload the small local JSON banks on every rerun so manual edits are
    # visible immediately, including during an active quiz with the same ID.
    signature = bank_signature()
    st.session_state.banks, st.session_state.bank_errors = load_banks()
    st.session_state.bank_signature = signature


def filtered_ids() -> list[str]:
    settings = st.session_state.settings
    source = st.session_state.banks.get("en", {})
    ids = [qid for qid, item in source.items() if (settings["difficulty"] == "Mixed" or item["difficulty"] == settings["difficulty"]) and (settings["category"] == "Mixed" or item["category"] == settings["category"])]
    random.shuffle(ids)
    return ids


def matching_count() -> int:
    settings = st.session_state.settings
    source = st.session_state.banks.get("en", {})
    return sum(1 for item in source.values() if (settings["difficulty"] == "Mixed" or item["difficulty"] == settings["difficulty"]) and (settings["category"] == "Mixed" or item["category"] == settings["category"]))


def start_quiz() -> None:
    ids = filtered_ids()
    if not ids:
        st.session_state.screen = "teams"
        st.session_state.question_ids = []
        st.session_state.current_question_id = None
        return
    count = min(st.session_state.settings["question_count"], len(ids))
    st.session_state.question_ids = ids[:count]
    st.session_state.used_question_ids = [st.session_state.question_ids[0]] if count else []
    st.session_state.current_question_id = st.session_state.question_ids[0] if count else None
    st.session_state.question_number = 1 if count else 0
    st.session_state.answer_revealed = False
    st.session_state.timer_expired = False
    st.session_state.question_started_at = time.time()
    st.session_state.timer_stopped_at = None
    st.session_state.awarded_team = None
    st.session_state.awarded_points = 0
    st.session_state.screen = "quiz"


def question_record(qid: str, lang: str) -> tuple[dict[str, Any], bool]:
    selected = st.session_state.banks.get(lang, {}).get(qid)
    english = st.session_state.banks.get("en", {}).get(qid, {})
    if not selected:
        return english, True
    if lang != "en" and all(selected.get(field) == english.get(field) for field in ("question", "options", "correct_answer", "bible_reference", "explanation")):
        return selected, True
    return selected, False


def score_order() -> list[tuple[str, int]]:
    return sorted(st.session_state.scores.items(), key=lambda pair: (-pair[1], st.session_state.team_names.index(pair[0])))


def render_scoreboard(compact: bool = False) -> None:
    st.markdown(f"<div class='panel-title'>{html.escape(t('scoreboard'))}</div>", unsafe_allow_html=True)
    ordered = score_order()
    top_score = ordered[0][1] if ordered else 0
    for rank, (name, score) in enumerate(ordered, 1):
        leader = score == top_score and top_score > 0
        medal = "★" if leader else str(rank)
        st.markdown(f"<div class='score-card {'leader' if leader else ''}'><span><b>{medal}</b>&nbsp; <span class='score-name'>{html.escape(name)}</span></span><span class='score-value'>{score}</span></div>", unsafe_allow_html=True)
    if ordered and top_score > 0:
        st.caption(f"{t('leader')}: {ordered[0][0]}")


def render_home() -> None:
    st.markdown(f"<div class='hero'><div class='eyebrow'>{t('host')}</div><h1>{t('home')}</h1><p>{t('tagline')}</p></div>", unsafe_allow_html=True)
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("<div class='panel'><div class='panel-title'>A ready-to-run host console</div><p style='color:var(--muted)'>Set your teams, tune the challenge, and keep the whole room moving from one screen. Answers stay hidden until the host reveals them.</p></div>", unsafe_allow_html=True)
        if st.button(t("start"), type="primary", use_container_width=True):
            st.session_state.screen = "setup"; st.rerun()
    with right:
        if st.session_state.scores:
            render_scoreboard()
        else:
            st.markdown("<div class='panel'><div class='panel-title'>Built for the room</div><p style='color:var(--muted)'>Large type, high contrast, live rankings, manual scoring, timer support, and English and नेपाली at your fingertips.</p></div>", unsafe_allow_html=True)


def render_setup() -> None:
    lang = st.session_state.selected_language
    st.markdown(f"<div class='hero'><div class='eyebrow'>{t('setup')}</div><h2>{t('home')}</h2><p>{t('setup_note')}</p></div>", unsafe_allow_html=True)
    if st.button(t("back")): st.session_state.screen = "home"; st.rerun()
    with st.form("quiz_settings"):
        st.markdown(f"<div class='panel-title'>{t('settings')}</div>", unsafe_allow_html=True)
        a, b = st.columns(2)
        with a:
            count_choice = st.selectbox(t("questions"), [10, 20, 30, 50, "Custom"], index=0)
            count = st.number_input(t("questions"), min_value=1, max_value=500, value=10, step=1, disabled=count_choice != "Custom")
            difficulty = st.selectbox(t("difficulty"), DIFFICULTIES, format_func=lambda x: LABELS[lang].get(x, x))
            category = st.selectbox(t("category"), CATEGORIES, index=CATEGORIES.index("Mixed"), format_func=lambda x: LABELS[lang].get(x, x))
        with b:
            points = st.number_input(t("points"), min_value=1, max_value=10000, value=100, step=25)
            timer_choice = st.selectbox(t("timer"), [15, 30, 45, 60, t("disabled"), t("custom")])
            timer_value = st.number_input(t("timer"), min_value=5, max_value=3600, value=30, step=5, disabled=timer_choice not in [t("custom")])
            projector = st.checkbox(t("projector"), value=st.session_state.projector_mode)
        st.caption(f"{len(st.session_state.banks.get('en', {}))} {t('available')} · {t('validation')}: {'OK' if not st.session_state.bank_errors else 'review warnings below'}")
        submitted = st.form_submit_button(t("continue"), type="primary", use_container_width=True)
    if submitted:
        st.session_state.settings = {"question_count": int(count if count_choice == "Custom" else count_choice), "difficulty": difficulty, "category": category, "points": int(points), "timer_seconds": 0 if timer_choice == t("disabled") else int(timer_value if timer_choice == t("custom") else timer_choice)}
        st.session_state.projector_mode = projector
        st.session_state.screen = "teams"
        st.rerun()
    if st.session_state.bank_errors:
        with st.expander(t("validation")):
            for error in st.session_state.bank_errors[:20]: st.warning(error)


def render_teams() -> None:
    st.markdown(f"<div class='hero'><div class='eyebrow'>{t('teams')}</div><h2>{t('team_names')}</h2><p>{t('team_note')}</p></div>", unsafe_allow_html=True)
    match_count = matching_count()
    st.info(t("matching", count=match_count))
    requested = st.session_state.settings.get("question_count", match_count)
    if match_count < requested:
        st.warning(t("bank_limit", available=match_count))
    count = st.number_input(t("team_count"), min_value=2, max_value=10, value=st.session_state.team_count, step=1)
    if int(count) != st.session_state.team_count:
        st.session_state.team_count = int(count)
        st.rerun()
    with st.form("teams_form"):
        names: list[str] = []
        for start in range(0, int(count), 2):
            cols = st.columns(min(2, int(count) - start))
            for offset, col in enumerate(cols):
                index = start + offset
                existing = st.session_state.team_names[index] if index < len(st.session_state.team_names) else f"Team {index + 1}"
                with col: names.append(st.text_input(f"{t('team_names')} {index + 1}", value=existing, key=f"team_name_{index}"))
        submitted = st.form_submit_button(t("launch"), type="primary", use_container_width=True)
    if submitted:
        cleaned = [name.strip() or f"Team {i + 1}" for i, name in enumerate(names)]
        if len(set(name.casefold() for name in cleaned)) != len(cleaned): st.error("Team names must be unique.")
        else:
            available = filtered_ids()
            if not available:
                st.error("No questions match these filters. Go back and choose Mixed or another filter.")
            else:
                st.session_state.team_count = int(count); st.session_state.team_names = cleaned; st.session_state.scores = {name: 0 for name in cleaned}; start_quiz(); st.rerun()
    if st.button(t("back")): st.session_state.screen = "setup"; st.rerun()


def seconds_left() -> int | None:
    limit = st.session_state.settings.get("timer_seconds", 0)
    if not limit or not st.session_state.question_started_at: return None
    end = st.session_state.timer_stopped_at or time.time()
    return max(0, int(limit - (end - st.session_state.question_started_at)))


def reveal() -> None:
    st.session_state.answer_revealed = True
    st.session_state.timer_stopped_at = time.time()
    st.session_state.timer_expired = False


def advance() -> None:
    next_number = st.session_state.question_number + 1
    if next_number > len(st.session_state.question_ids):
        st.session_state.screen = "results"; return
    qid = st.session_state.question_ids[next_number - 1]
    st.session_state.current_question_id = qid; st.session_state.question_number = next_number; st.session_state.used_question_ids.append(qid)
    st.session_state.answer_revealed = False; st.session_state.timer_expired = False; st.session_state.question_started_at = time.time(); st.session_state.timer_stopped_at = None; st.session_state.awarded_team = None; st.session_state.awarded_points = 0


def render_quiz() -> None:
    lang = st.session_state.selected_language
    qid = st.session_state.current_question_id
    if not qid:
        st.error("No questions are available for the selected filters.")
        if st.button(t("new_quiz")): st.session_state.screen = "setup"; st.rerun()
        return
    record, fallback = question_record(qid, lang)
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown(f"<div class='eyebrow'>{t('question')} {st.session_state.question_number} {t('of')} {len(st.session_state.question_ids)} · ID {html.escape(qid)}</div>", unsafe_allow_html=True)
    with right:
        chosen = st.selectbox(t("language"), LANGUAGES, index=LANGUAGES.index(lang), format_func=lambda x: LANGUAGE_NAMES[x], key="language_selector")
        if chosen != lang: st.session_state.selected_language = chosen; st.rerun()
    if fallback: st.markdown(f"<div class='translation-warning'>{html.escape(t('missing', lang))}</div>", unsafe_allow_html=True)
    total = len(st.session_state.question_ids); st.progress(st.session_state.question_number / total if total else 0)
    remaining = seconds_left()
    if remaining is not None and not st.session_state.answer_revealed:
        if st_autorefresh: st_autorefresh(interval=1000, key=f"timer_{qid}")
        if remaining <= 0: st.session_state.timer_expired = True
    meta_left, meta_right = st.columns([2, 1])
    with meta_right:
        if remaining is not None and not st.session_state.answer_revealed:
            st.markdown(f"<div class='timer {'safe' if remaining > 10 else ''}'>{remaining}s<br><small>{t('remaining')}</small></div>", unsafe_allow_html=True)
        elif st.session_state.timer_expired: st.markdown(f"<div class='timer'>{t('time_up')}</div>", unsafe_allow_html=True)
    category_label = LABELS.get(lang, LABELS["en"]).get(record.get("category", ""), record.get("category", ""))
    difficulty_label = LABELS.get(lang, LABELS["en"]).get(record.get("difficulty", ""), record.get("difficulty", ""))
    st.markdown(f"<div class='question-card'><div class='eyebrow'>{html.escape(category_label)} · {html.escape(difficulty_label)}</div><div class='question-text'>{html.escape(record.get('question',''))}</div></div>", unsafe_allow_html=True)
    option_cols = st.columns(2)
    for index, option in enumerate(record.get("options", [])):
        with option_cols[index % 2]: st.markdown(f"<div class='panel' style='font-size:1.2rem; min-height:3.8rem;'><span class='option-letter'>{chr(65 + index)}</span>{html.escape(option)}</div>", unsafe_allow_html=True)
    if not st.session_state.answer_revealed:
        if st.button(t("reveal"), type="primary", use_container_width=True): reveal(); st.rerun()
    else:
        st.markdown(f"<div class='answer-box'><div class='eyebrow'>{t('correct')}</div><div class='answer-main'>{html.escape(record.get('correct_answer',''))}</div><p><b>{t('reference')}:</b> {html.escape(record.get('bible_reference',''))}</p><p>{html.escape(record.get('explanation',''))}</p></div>", unsafe_allow_html=True)
        if st.session_state.awarded_team is None:
            st.markdown(f"<div class='panel-title'>{t('award')} · +{st.session_state.settings['points']} {t('points_awarded')}</div>", unsafe_allow_html=True)
            award_cols = st.columns(min(3, len(st.session_state.team_names)))
            for i, name in enumerate(st.session_state.team_names):
                with award_cols[i % len(award_cols)]:
                    if st.button(f"{name}  +{st.session_state.settings['points']}", key=f"award_{qid}_{i}", use_container_width=True): st.session_state.scores[name] += st.session_state.settings["points"]; st.session_state.awarded_team = name; st.session_state.awarded_points = st.session_state.settings["points"]; st.rerun()
            if st.button(t("no_points"), use_container_width=True): st.session_state.awarded_team = "__none__"; st.rerun()
        else:
            if st.session_state.awarded_team == "__none__": st.info(t("no_points"))
            else: st.success(f"{st.session_state.awarded_team}: +{st.session_state.awarded_points}")
            if st.button(t("next"), type="primary", use_container_width=True): advance(); st.rerun()
    with st.sidebar:
        st.markdown(f"### {t('scoreboard')}"); render_scoreboard()
        st.divider(); st.checkbox(t("projector"), key="projector_mode")


def render_results() -> None:
    ordered = score_order(); winner = ordered[0][0] if ordered else ""
    st.markdown(f"<div class='hero'><div class='eyebrow'>{t('final')}</div><h2>{t('final')}</h2><p>{len(st.session_state.question_ids)} {t('played')}</p></div>", unsafe_allow_html=True)
    if winner: st.markdown(f"<div class='winner'><div class='eyebrow' style='color:#8de0d2'>{t('winner')}</div><h2>{html.escape(winner)}</h2><div style='font-size:2.8rem;font-weight:700'>{ordered[0][1]}</div><div>{t('score')}</div></div>", unsafe_allow_html=True)
    st.markdown("### " + t("scoreboard"))
    for rank, (name, score) in enumerate(ordered, 1): st.markdown(f"<div class='score-card'><span><b>{rank}</b>&nbsp; {html.escape(name)}</span><span class='score-value'>{score}</span></div>", unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        if st.button(t("play_again"), type="primary", use_container_width=True):
            st.session_state.scores = {name: 0 for name in st.session_state.team_names}
            start_quiz(); st.rerun()
    with b:
        if st.button(t("new_quiz"), use_container_width=True): st.session_state.screen = "setup"; st.rerun()
    with c:
        if st.button(t("home_btn"), use_container_width=True): st.session_state.screen = "home"; st.rerun()


def main() -> None:
    st.set_page_config(page_title="Bible Quiz Live", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")
    init_state(); inject_css(st.session_state.projector_mode)
    with st.sidebar:
        st.markdown("### " + t("theme"))
        theme_choice = st.radio(t("theme"), ["light", "dark"], index=0 if st.session_state.theme == "light" else 1, format_func=lambda value: t(value), horizontal=True, key="theme_choice")
        st.session_state.theme = theme_choice
        st.checkbox(t("manga_background"), key="manga_background")
    inject_css(st.session_state.projector_mode, st.session_state.theme, st.session_state.manga_background)
    if st.session_state.screen == "home": render_home()
    elif st.session_state.screen == "setup": render_setup()
    elif st.session_state.screen == "teams": render_teams()
    elif st.session_state.screen == "quiz": render_quiz()
    else: render_results()


if __name__ == "__main__": main()
