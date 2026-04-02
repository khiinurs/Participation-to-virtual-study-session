"""
Virtual Study Session Participation and Remote Focus Ability Survey
Fundamentals of Programming - 4BUIS008C (Level 4)
Project 1
"""

import streamlit as st
import json
import csv
import io
import re
from datetime import date, datetime

# ─────────────────────────────────────────────
# DATA: Survey Questions (loaded from this file)
# ─────────────────────────────────────────────

QUESTIONS: list[dict] = [
    {
        "text": "How often do you join scheduled virtual study sessions?",
        "options": [
            ("Every session, without exception", 0),
            ("Most of the time", 1),
            ("Sometimes, when I feel like it", 2),
            ("Rarely – only for exams", 3),
            ("I never join virtual study sessions", 4),
        ],
    },
    {
        "text": "How long can you stay focused during an online group study call?",
        "options": [
            ("More than 90 minutes comfortably", 0),
            ("60–90 minutes before losing focus", 1),
            ("30–60 minutes", 2),
            ("Less than 30 minutes", 3),
            ("I cannot focus at all in online calls", 4),
        ],
    },
    {
        "text": "How well do you manage distractions (social media, notifications) while in a virtual study session?",
        "options": [
            ("I put my phone away and block distracting sites entirely", 0),
            ("I mostly resist but occasionally check my phone", 1),
            ("I check notifications every 10–15 minutes", 2),
            ("I frequently browse unrelated content during sessions", 3),
            ("I cannot resist distractions at all", 4),
        ],
    },
    {
        "text": "How comfortable are you asking questions or contributing during an online group session?",
        "options": [
            ("Very comfortable – I actively participate", 0),
            ("Fairly comfortable – I contribute when I have something to say", 1),
            ("Neutral – I participate only if directly asked", 2),
            ("Uncomfortable – I stay on mute most of the time", 3),
            ("I never contribute in online sessions", 4),
        ],
    },
    {
        "text": "How do you feel about your internet connection's effect on your virtual study participation?",
        "options": [
            ("Stable – it never interrupts my sessions", 0),
            ("Usually fine with rare drops", 1),
            ("Frequent minor interruptions", 2),
            ("Constant interruptions that affect my learning", 3),
            ("My connection makes it impossible to join properly", 4),
        ],
    },
    {
        "text": "After a virtual study session, how well do you retain the material covered?",
        "options": [
            ("Very well – better than in-person classes", 0),
            ("Well – about the same as in-person", 1),
            ("Somewhat – I need to review the material afterwards", 2),
            ("Poorly – I struggle to retain much", 3),
            ("I retain almost nothing from virtual sessions", 4),
        ],
    },
    {
        "text": "How often do you feel mentally fatigued specifically because of back-to-back online sessions (Zoom fatigue)?",
        "options": [
            ("Never – I handle them without fatigue", 0),
            ("Rarely – only after very long sessions", 1),
            ("Sometimes – after 2 or more sessions in a day", 2),
            ("Often – even a single session tires me", 3),
            ("Always – online sessions exhaust me more than anything else", 4),
        ],
    },
    {
        "text": "How well does your physical study environment support remote focus?",
        "options": [
            ("Excellent – quiet, dedicated, and well-equipped", 0),
            ("Good – minor disturbances occasionally", 1),
            ("Adequate – I manage despite some noise or interruptions", 2),
            ("Poor – frequent noise or lack of proper equipment", 3),
            ("Very poor – I cannot create a suitable environment at home", 4),
        ],
    },
    {
        "text": "How often do you follow a fixed schedule when participating in remote study activities?",
        "options": [
            ("Always – I plan and stick to a timetable", 0),
            ("Usually – minor deviations only", 1),
            ("Sometimes – my schedule changes day to day", 2),
            ("Rarely – I study whenever I happen to feel like it", 3),
            ("Never – I have no structured schedule at all", 4),
        ],
    },
    {
        "text": "How do you feel about collaborating with peers through online tools (e.g., shared docs, breakout rooms)?",
        "options": [
            ("Very positive – I find it effective and engaging", 0),
            ("Positive – it works well most of the time", 1),
            ("Neutral – it is neither better nor worse than in-person", 2),
            ("Negative – I find it awkward or ineffective", 3),
            ("Very negative – I strongly prefer not to use these tools", 4),
        ],
    },
    {
        "text": "How effectively do you communicate with your study group between virtual sessions (e.g., via chat or email)?",
        "options": [
            ("Very effectively – I initiate and respond promptly", 0),
            ("Effectively – I respond within a few hours", 1),
            ("Moderately – I respond when reminded", 2),
            ("Poorly – I often miss messages", 3),
            ("Not at all – I do not communicate between sessions", 4),
        ],
    },
    {
        "text": "How well do you handle technical issues (audio, video, software) during a virtual study session?",
        "options": [
            ("Very well – I troubleshoot quickly and carry on", 0),
            ("Well – minor issues cause minimal disruption", 1),
            ("Adequately – issues slow me down but I manage", 2),
            ("Poorly – technical problems significantly disrupt my session", 3),
            ("Very poorly – I give up when technical issues occur", 4),
        ],
    },
    {
        "text": "How motivated are you to prepare material before a virtual study session?",
        "options": [
            ("Very motivated – I always prepare in advance", 0),
            ("Motivated – I usually prepare", 1),
            ("Neutral – I prepare if the topic interests me", 2),
            ("Rarely motivated – I seldom prepare beforehand", 3),
            ("Not motivated at all – I never prepare", 4),
        ],
    },
    {
        "text": "How does participating in virtual study sessions affect your overall academic confidence?",
        "options": [
            ("Very positively – they boost my confidence significantly", 0),
            ("Positively – they help somewhat", 1),
            ("No effect – they neither help nor hurt", 2),
            ("Negatively – they make me feel less confident", 3),
            ("Very negatively – they undermine my confidence", 4),
        ],
    },
    {
        "text": "How well do you balance virtual study sessions with your other daily responsibilities?",
        "options": [
            ("Very well – I integrate them seamlessly", 0),
            ("Well – minor conflicts arise occasionally", 1),
            ("Adequately – I sometimes miss sessions due to other duties", 2),
            ("Poorly – other responsibilities frequently interfere", 3),
            ("Very poorly – I cannot balance them at all", 4),
        ],
    },
    {
        "text": "How would you rate your overall ability to focus on academic tasks when working remotely?",
        "options": [
            ("Excellent – I focus as well as or better than in class", 0),
            ("Good – I maintain acceptable focus", 1),
            ("Fair – focus varies considerably day to day", 2),
            ("Poor – I struggle to focus remotely most of the time", 3),
            ("Very poor – remote work severely impairs my focus", 4),
        ],
    },
    {
        "text": "How often do you use focus-enhancing techniques (e.g., Pomodoro, ambient music, app blockers) during remote study?",
        "options": [
            ("Always – they are a core part of my study routine", 0),
            ("Often – I use them most study days", 1),
            ("Sometimes – I try them occasionally", 2),
            ("Rarely – I have tried them but do not stick to them", 3),
            ("Never – I am unaware of or opposed to such techniques", 4),
        ],
    },
    {
        "text": "How do you feel emotionally after a productive virtual study session?",
        "options": [
            ("Very fulfilled and energised", 0),
            ("Satisfied and calm", 1),
            ("Indifferent – neither positive nor negative", 2),
            ("Somewhat drained or flat", 3),
            ("Exhausted or frustrated", 4),
        ],
    },
    {
        "text": "How often do you set specific learning goals before starting a virtual study session?",
        "options": [
            ("Always – I define clear objectives every time", 0),
            ("Usually – I have a rough plan", 1),
            ("Sometimes – only for high-stakes topics", 2),
            ("Rarely – I rarely plan in advance", 3),
            ("Never – I just open my laptop and see what happens", 4),
        ],
    },
    {
        "text": "How comfortable are you with the idea of future university courses being delivered entirely online?",
        "options": [
            ("Very comfortable – I prefer it", 0),
            ("Comfortable – I am happy with it", 1),
            ("Neutral – I have no strong preference", 2),
            ("Uncomfortable – I would prefer hybrid or in-person", 3),
            ("Very uncomfortable – I strongly prefer in-person only", 4),
        ],
    },
]

PSYCHOLOGICAL_STATES: list[dict] = [
    {"range": (0, 15),  "label": "Excellent Virtual Learner",
     "description": "You show outstanding participation and remote focus ability. You thrive in virtual study environments with strong self-regulation, consistent engagement, and effective digital collaboration. No intervention needed — keep up the excellent habits!"},
    {"range": (16, 30), "label": "Strong Remote Participant",
     "description": "You have a good command of virtual study practices. Participation is consistent, and focus is mostly maintained. Minor refinements — such as improving your physical environment or scheduling — could take you to the next level."},
    {"range": (31, 45), "label": "Moderate Virtual Engagement",
     "description": "You participate and focus reasonably well online, but distractions, fatigue, or inconsistency are holding you back. Consider adopting focus techniques (e.g., Pomodoro) and creating a dedicated study space to improve your remote performance."},
    {"range": (46, 60), "label": "Below-Average Remote Focus",
     "description": "Virtual study sessions present notable challenges for you. Issues such as low motivation, poor environment, or difficulty managing distractions significantly impact your learning. Structured scheduling and peer accountability are strongly recommended."},
    {"range": (61, 75), "label": "Low Virtual Participation",
     "description": "You struggle considerably with remote study engagement. Your focus, participation, and use of online tools are limited. Consider speaking with an academic advisor or counsellor to develop a personalised remote learning strategy."},
    {"range": (76, 90), "label": "Poor Remote Learning Ability",
     "description": "Virtual study sessions are highly challenging for you across multiple dimensions. Immediate steps are needed: consult your academic support services, explore digital literacy resources, and work on building a structured daily study routine."},
]

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def validate_name(name: str) -> bool:
    """Only letters, hyphens, apostrophes, and spaces allowed."""
    return bool(re.fullmatch(r"[A-Za-z\-' ]+", name.strip()))


def validate_dob(dob_str: str) -> tuple[bool, str]:
    """Validate date of birth in DD/MM/YYYY format."""
    try:
        dob = datetime.strptime(dob_str.strip(), "%d/%m/%Y").date()
        today = date.today()
        if dob >= today:
            return False, "Date of birth must be in the past."
        if today.year - dob.year > 120:
            return False, "Date of birth seems unrealistically old."
        return True, ""
    except ValueError:
        return False, "Please use DD/MM/YYYY format (e.g., 15/04/2003)."


def validate_student_id(sid: str) -> bool:
    """Only digits allowed."""
    return sid.strip().isdigit() and len(sid.strip()) > 0


def get_psychological_state(score: int) -> dict:
    for state in PSYCHOLOGICAL_STATES:
        lo, hi = state["range"]
        if lo <= score <= hi:
            return state
    return PSYCHOLOGICAL_STATES[-1]


def build_result_dict(info: dict, answers: list[int], score: int, state: dict) -> dict:
    return {
        "surname": info["surname"],
        "given_name": info["given_name"],
        "date_of_birth": info["dob"],
        "student_id": info["student_id"],
        "survey_date": date.today().strftime("%d/%m/%Y"),
        "total_score": score,
        "max_possible_score": len(QUESTIONS) * 4,
        "psychological_state": state["label"],
        "description": state["description"],
        "answers": answers,
    }


def result_to_txt(result: dict) -> str:
    lines = [
        "=" * 60,
        "   VIRTUAL STUDY SESSION & REMOTE FOCUS ABILITY SURVEY",
        "=" * 60,
        f"Name            : {result['given_name']} {result['surname']}",
        f"Date of Birth   : {result['date_of_birth']}",
        f"Student ID      : {result['student_id']}",
        f"Survey Date     : {result['survey_date']}",
        "-" * 60,
        f"Total Score     : {result['total_score']} / {result['max_possible_score']}",
        f"Psychological State : {result['psychological_state']}",
        "",
        "Assessment:",
        result['description'],
        "=" * 60,
    ]
    return "\n".join(lines)


def result_to_csv(result: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])
    writer.writerow(["Surname", result["surname"]])
    writer.writerow(["Given Name", result["given_name"]])
    writer.writerow(["Date of Birth", result["date_of_birth"]])
    writer.writerow(["Student ID", result["student_id"]])
    writer.writerow(["Survey Date", result["survey_date"]])
    writer.writerow(["Total Score", result["total_score"]])
    writer.writerow(["Max Possible Score", result["max_possible_score"]])
    writer.writerow(["Psychological State", result["psychological_state"]])
    writer.writerow(["Description", result["description"]])
    return output.getvalue()


def result_to_json(result: dict) -> str:
    return json.dumps(result, indent=4, ensure_ascii=False)


def parse_uploaded_result(content: str, fmt: str) -> dict | None:
    try:
        if fmt == "json":
            return json.loads(content)
        elif fmt == "csv":
            reader = csv.reader(io.StringIO(content))
            rows = {row[0]: row[1] for row in reader if len(row) == 2 and row[0] != "Field"}
            return {
                "surname": rows.get("Surname", ""),
                "given_name": rows.get("Given Name", ""),
                "date_of_birth": rows.get("Date of Birth", ""),
                "student_id": rows.get("Student ID", ""),
                "survey_date": rows.get("Survey Date", ""),
                "total_score": int(rows.get("Total Score", 0)),
                "max_possible_score": int(rows.get("Max Possible Score", 0)),
                "psychological_state": rows.get("Psychological State", ""),
                "description": rows.get("Description", ""),
            }
        elif fmt == "txt":
            result = {}
            for line in content.splitlines():
                for key, field in [("Name", "given_name"), ("Date of Birth", "date_of_birth"),
                                    ("Student ID", "student_id"), ("Survey Date", "survey_date"),
                                    ("Total Score", "total_score"),
                                    ("Psychological State", "psychological_state")]:
                    if line.strip().startswith(key):
                        result[field] = line.split(":", 1)[-1].strip()
            return result if result else None
    except Exception:
        return None

# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Virtual Study Focus Survey",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ── DARK MODE ── */
[data-theme="dark"] .stApp,
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

[data-theme="dark"] .hero-box,
.hero-box {
    background: linear-gradient(135deg, rgba(167,139,250,0.15), rgba(99,102,241,0.1));
    border: 1px solid rgba(167,139,250,0.3);
}

[data-theme="dark"] .question-card,
.question-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(167,139,250,0.2);
}

[data-theme="dark"] .info-chip,
.info-chip {
    background: rgba(255,255,255,0.07);
    color: #c4b5fd;
}

[data-theme="dark"] .result-card,
.result-card {
    background: linear-gradient(135deg, rgba(167,139,250,0.2), rgba(96,165,250,0.1));
}

[data-theme="dark"] .state-desc,
.state-desc {
    color: #cbd5e1;
}

[data-theme="dark"] .error-box,
.error-box {
    color: #fca5a5;
}

/* ── LIGHT MODE OVERRIDES ── */
[data-theme="light"] .stApp {
    background: linear-gradient(135deg, #ede9fe, #e0e7ff, #f0f4ff) !important;
}

[data-theme="light"] .hero-box {
    background: linear-gradient(135deg, rgba(109,40,217,0.08), rgba(79,70,229,0.06)) !important;
    border: 1px solid rgba(109,40,217,0.25) !important;
}

[data-theme="light"] .question-card {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(109,40,217,0.2) !important;
}

[data-theme="light"] .info-chip {
    background: rgba(109,40,217,0.08) !important;
    color: #5b21b6 !important;
    border: 1px solid rgba(109,40,217,0.2) !important;
}

[data-theme="light"] .result-card {
    background: linear-gradient(135deg, rgba(109,40,217,0.1), rgba(96,165,250,0.08)) !important;
    border: 1px solid rgba(109,40,217,0.3) !important;
}

[data-theme="light"] .state-desc {
    color: #374151 !important;
}

[data-theme="light"] .error-box {
    color: #b91c1c !important;
    background: rgba(239,68,68,0.08) !important;
}

[data-theme="light"] .hero-sub {
    color: #4b5563 !important;
}

/* ── INPUT TEXT FIX — visible in both modes ── */
/* Force dark text in light mode inputs */
[data-theme="light"] input[type="text"],
[data-theme="light"] input[type="number"],
[data-theme="light"] input,
[data-theme="light"] textarea,
[data-theme="light"] .stTextInput input {
    color: #111827 !important;
    background-color: #ffffff !important;
    border: 1px solid rgba(109,40,217,0.35) !important;
}

/* Force light text in dark mode inputs */
[data-theme="dark"] input[type="text"],
[data-theme="dark"] input[type="number"],
[data-theme="dark"] input,
[data-theme="dark"] textarea,
[data-theme="dark"] .stTextInput input {
    color: #f1f5f9 !important;
    background-color: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
}

/* Fallback for when theme attr not set (default = dark) */
.stTextInput input {
    color: #f1f5f9 !important;
    background-color: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 10px !important;
}

/* Placeholder text */
[data-theme="light"] .stTextInput input::placeholder {
    color: #9ca3af !important;
}
[data-theme="dark"] .stTextInput input::placeholder {
    color: #64748b !important;
}

/* ── SHARED STYLES ── */
h1, h2, h3 {
    color: #a78bfa !important;
    font-weight: 700;
}

[data-theme="light"] h1,
[data-theme="light"] h2,
[data-theme="light"] h3 {
    color: #6d28d9 !important;
}

.hero-box {
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.hero-sub {
    color: #94a3b8;
    font-size: 1rem;
}

.question-card {
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.2s;
}

.question-card:hover {
    border-color: rgba(167,139,250,0.5) !important;
}

.q-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #a78bfa;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

[data-theme="light"] .q-number {
    color: #7c3aed;
}

.result-card {
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    text-align: center;
}

.score-big {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.state-label {
    font-size: 1.4rem;
    font-weight: 600;
    color: #a78bfa;
    margin-top: 0.5rem;
}

[data-theme="light"] .state-label {
    color: #6d28d9;
}

.state-desc {
    font-size: 0.95rem;
    margin-top: 1rem;
    line-height: 1.7;
}

.info-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 1.5rem;
}

.info-chip {
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 30px;
    padding: 0.3rem 1rem;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

.stDownloadButton > button {
    background: rgba(167,139,250,0.15) !important;
    border: 1px solid rgba(167,139,250,0.4) !important;
    color: #c4b5fd !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
}

[data-theme="light"] .stDownloadButton > button {
    color: #6d28d9 !important;
    background: rgba(109,40,217,0.08) !important;
    border: 1px solid rgba(109,40,217,0.3) !important;
}

.error-box {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.section-divider {
    border: none;
    border-top: 1px solid rgba(167,139,250,0.2);
    margin: 2rem 0;
}

.progress-bar-container {
    background: rgba(255,255,255,0.08);
    border-radius: 100px;
    height: 8px;
    margin: 1rem 0 2rem 0;
    overflow: hidden;
}

[data-theme="light"] .progress-bar-container {
    background: rgba(0,0,0,0.08);
}

.progress-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #7c3aed, #60a5fa);
    transition: width 0.4s ease;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ─────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🎓 Virtual Study Focus Survey</div>
    <div class="hero-sub">Virtual Study Session Participation &amp; Remote Focus Ability Assessment</div>
</div>
""", unsafe_allow_html=True)

# ── Session State Init ───────────────────────
for key, default in [
    ("page", "home"),
    ("user_info", {}),
    ("answers", []),
    ("result", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ════════════════════════════════════════════
# PAGE: HOME – Choose action
# ════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("### What would you like to do?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝  Start New Survey", use_container_width=True):
            st.session_state.page = "info"
            st.session_state.answers = []
            st.session_state.result = None
            st.rerun()
    with col2:
        if st.button("📂  Load Existing Result", use_container_width=True):
            st.session_state.page = "load"
            st.rerun()

# ════════════════════════════════════════════
# PAGE: INFO – Collect & validate user details
# ════════════════════════════════════════════
elif st.session_state.page == "info":
    st.markdown("### 👤 Personal Information")
    st.markdown("Please fill in your details before starting the survey.")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    surname = st.text_input("Surname *", placeholder="e.g. Smith-Jones")
    given_name = st.text_input("Given Name *", placeholder="e.g. Mary Ann")
    dob_str = st.text_input("Date of Birth * (DD/MM/YYYY)", placeholder="e.g. 15/04/2003")
    student_id = st.text_input("Student ID * (digits only)", placeholder="e.g. 123456")

    errors: list[str] = []

    if st.button("Continue to Survey →"):
        if not surname.strip():
            errors.append("Surname is required.")
        elif not validate_name(surname):
            errors.append("Surname may only contain letters, hyphens (-), apostrophes ('), and spaces.")

        if not given_name.strip():
            errors.append("Given name is required.")
        elif not validate_name(given_name):
            errors.append("Given name may only contain letters, hyphens (-), apostrophes ('), and spaces.")

        if not dob_str.strip():
            errors.append("Date of birth is required.")
        else:
            ok, msg = validate_dob(dob_str)
            if not ok:
                errors.append(msg)

        if not student_id.strip():
            errors.append("Student ID is required.")
        elif not validate_student_id(student_id):
            errors.append("Student ID must contain digits only (no letters or spaces).")

        if errors:
            for e in errors:
                st.markdown(f'<div class="error-box">⚠ {e}</div>', unsafe_allow_html=True)
        else:
            st.session_state.user_info = {
                "surname": surname.strip(),
                "given_name": given_name.strip(),
                "dob": dob_str.strip(),
                "student_id": student_id.strip(),
            }
            st.session_state.page = "survey"
            st.rerun()

    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()

# ════════════════════════════════════════════
# PAGE: SURVEY – Answer all questions
# ════════════════════════════════════════════
elif st.session_state.page == "survey":
    info = st.session_state.user_info
    st.markdown(f"### 📋 Survey – {info['given_name']} {info['surname']}")

    n = len(QUESTIONS)
    answered = len(st.session_state.answers)
    pct = int(answered / n * 100)
    st.markdown(
        f'<div class="progress-bar-container">'
        f'<div class="progress-bar-fill" style="width:{pct}%"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Progress: {answered}/{n} questions answered")

    collected: list[int] = []
    all_answered = True

    with st.form("survey_form"):
        for i, q in enumerate(QUESTIONS):
            option_labels = [opt[0] for opt in q["options"]]
            st.markdown(
                f'<div class="question-card">'
                f'<div class="q-number">Question {i + 1} of {n}</div>',
                unsafe_allow_html=True,
            )
            chosen = st.radio(
                q["text"],
                options=option_labels,
                key=f"q_{i}",
                index=None,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            if chosen is None:
                all_answered = False
                collected.append(-1)
            else:
                score_val = next(s for label, s in q["options"] if label == chosen)
                collected.append(score_val)

        submitted = st.form_submit_button("🧮  Calculate My Result")

    if submitted:
        if not all_answered:
            st.warning("⚠ Please answer all questions before submitting.")
        else:
            total = sum(collected)
            state = get_psychological_state(total)
            result = build_result_dict(info, collected, total, state)
            st.session_state.result = result
            st.session_state.answers = collected
            st.session_state.page = "result"
            st.rerun()

    if st.button("← Back to Info"):
        st.session_state.page = "info"
        st.rerun()

# ════════════════════════════════════════════
# PAGE: RESULT – Display & Save
# ════════════════════════════════════════════
elif st.session_state.page == "result":
    r = st.session_state.result
    info = st.session_state.user_info

    st.markdown("### 🏆 Your Survey Result")

    st.markdown(
        f'<div class="info-row">'
        f'<span class="info-chip">👤 {r["given_name"]} {r["surname"]}</span>'
        f'<span class="info-chip">🎓 ID: {r["student_id"]}</span>'
        f'<span class="info-chip">📅 {r["survey_date"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="result-card">'
        f'<div class="score-big">{r["total_score"]}<span style="font-size:1.5rem;color:#94a3b8"> / {r["max_possible_score"]}</span></div>'
        f'<div class="state-label">{r["psychological_state"]}</div>'
        f'<div class="state-desc">{r["description"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Score ranges legend
    st.markdown("#### 📊 Score Reference Ranges")
    cols = st.columns(2)
    for idx, s in enumerate(PSYCHOLOGICAL_STATES):
        with cols[idx % 2]:
            lo, hi = s["range"]
            st.markdown(
                f"<small style='color:#94a3b8'><b style='color:#a78bfa'>{lo}–{hi}</b> — {s['label']}</small>",
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 💾 Save Your Results")

    fmt = st.selectbox("Choose file format", ["JSON (recommended)", "CSV", "TXT"])

    if fmt.startswith("JSON"):
        file_data = result_to_json(r)
        ext, mime = "json", "application/json"
    elif fmt.startswith("CSV"):
        file_data = result_to_csv(r)
        ext, mime = "csv", "text/csv"
    else:
        file_data = result_to_txt(r)
        ext, mime = "txt", "text/plain"

    filename = f"survey_{r['student_id']}_{r['survey_date'].replace('/', '-')}.{ext}"
    st.download_button(
        f"⬇  Download as .{ext.upper()}",
        data=file_data,
        file_name=filename,
        mime=mime,
        use_container_width=True,
    )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄  Take Survey Again", use_container_width=True):
            st.session_state.page = "info"
            st.session_state.answers = []
            st.session_state.result = None
            st.rerun()
    with col2:
        if st.button("🏠  Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

# ════════════════════════════════════════════
# PAGE: LOAD – Upload & display existing result
# ════════════════════════════════════════════
elif st.session_state.page == "load":
    st.markdown("### 📂 Load an Existing Result File")
    st.caption("Upload a previously saved survey result (.json, .csv, or .txt)")

    uploaded = st.file_uploader("Choose a file", type=["json", "csv", "txt"])

    if uploaded is not None:
        raw = uploaded.read().decode("utf-8", errors="ignore")
        ext = uploaded.name.rsplit(".", 1)[-1].lower()
        parsed = parse_uploaded_result(raw, ext)

        if parsed is None:
            st.markdown('<div class="error-box">⚠ Could not parse this file. Please upload a file saved by this survey.</div>', unsafe_allow_html=True)
        else:
            score = int(parsed.get("total_score", 0))
            state_label = parsed.get("psychological_state", "")
            description = parsed.get("description", "")

            st.markdown(
                f'<div class="info-row">'
                f'<span class="info-chip">👤 {parsed.get("given_name","")} {parsed.get("surname","")}</span>'
                f'<span class="info-chip">🎓 ID: {parsed.get("student_id","")}</span>'
                f'<span class="info-chip">📅 {parsed.get("survey_date","")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="result-card">'
                f'<div class="score-big">{score}<span style="font-size:1.5rem;color:#94a3b8"> / {parsed.get("max_possible_score", 80)}</span></div>'
                f'<div class="state-label">{state_label}</div>'
                f'<div class="state-desc">{description}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
