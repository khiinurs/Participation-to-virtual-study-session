# ONLY CHANGED PARTS ARE MARKED WITH ✅

# ─────────────────────────────────────────────
# DATA: Survey Questions (FIXED TO 15) ✅
# ─────────────────────────────────────────────

QUESTIONS: list[dict] = [
    # FIRST 15 QUESTIONS ONLY (rest removed) ✅
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
        "text": "How well do you manage distractions (social media, notifications)?",
        "options": [
            ("I fully block distractions", 0),
            ("Mostly resist", 1),
            ("Check sometimes", 2),
            ("Often distracted", 3),
            ("Cannot resist", 4),
        ],
    },
    {
        "text": "How comfortable are you contributing during online sessions?",
        "options": [
            ("Very comfortable", 0),
            ("Fairly comfortable", 1),
            ("Neutral", 2),
            ("Uncomfortable", 3),
            ("Never contribute", 4),
        ],
    },
    {
        "text": "How stable is your internet during sessions?",
        "options": [
            ("Always stable", 0),
            ("Mostly stable", 1),
            ("Sometimes issues", 2),
            ("Often interrupted", 3),
            ("Very unstable", 4),
        ],
    },
    {
        "text": "How well do you retain material after sessions?",
        "options": [
            ("Very well", 0),
            ("Well", 1),
            ("Somewhat", 2),
            ("Poorly", 3),
            ("Not at all", 4),
        ],
    },
    {
        "text": "How often do you feel fatigued after online sessions?",
        "options": [
            ("Never", 0),
            ("Rarely", 1),
            ("Sometimes", 2),
            ("Often", 3),
            ("Always", 4),
        ],
    },
    {
        "text": "How suitable is your study environment?",
        "options": [
            ("Excellent", 0),
            ("Good", 1),
            ("Adequate", 2),
            ("Poor", 3),
            ("Very poor", 4),
        ],
    },
    {
        "text": "Do you follow a fixed study schedule?",
        "options": [
            ("Always", 0),
            ("Usually", 1),
            ("Sometimes", 2),
            ("Rarely", 3),
            ("Never", 4),
        ],
    },
    {
        "text": "How do you feel about online collaboration tools?",
        "options": [
            ("Very positive", 0),
            ("Positive", 1),
            ("Neutral", 2),
            ("Negative", 3),
            ("Very negative", 4),
        ],
    },
    {
        "text": "How effectively do you communicate between sessions?",
        "options": [
            ("Very effectively", 0),
            ("Effectively", 1),
            ("Moderately", 2),
            ("Poorly", 3),
            ("Not at all", 4),
        ],
    },
    {
        "text": "How well do you handle technical issues?",
        "options": [
            ("Very well", 0),
            ("Well", 1),
            ("Adequately", 2),
            ("Poorly", 3),
            ("Very poorly", 4),
        ],
    },
    {
        "text": "How motivated are you to prepare before sessions?",
        "options": [
            ("Very motivated", 0),
            ("Motivated", 1),
            ("Neutral", 2),
            ("Rarely motivated", 3),
            ("Not motivated", 4),
        ],
    },
    {
        "text": "How do sessions affect your confidence?",
        "options": [
            ("Very positively", 0),
            ("Positively", 1),
            ("No effect", 2),
            ("Negatively", 3),
            ("Very negatively", 4),
        ],
    },
    {
        "text": "How well do you balance study with responsibilities?",
        "options": [
            ("Very well", 0),
            ("Well", 1),
            ("Adequately", 2),
            ("Poorly", 3),
            ("Very poorly", 4),
        ],
    },
]

# ─────────────────────────────────────────────
# SCORE RANGES FIXED (0–60) ✅
# ─────────────────────────────────────────────

PSYCHOLOGICAL_STATES: list[dict] = [
    {"range": (0, 10), "label": "Excellent Virtual Learner", "description": "Outstanding performance."},
    {"range": (11, 20), "label": "Strong Remote Participant", "description": "Good performance."},
    {"range": (21, 30), "label": "Moderate Virtual Engagement", "description": "Average performance."},
    {"range": (31, 40), "label": "Below-Average Remote Focus", "description": "Needs improvement."},
    {"range": (41, 50), "label": "Low Virtual Participation", "description": "Struggling."},
    {"range": (51, 60), "label": "Poor Remote Learning Ability", "description": "Serious difficulty."},
]

# ─────────────────────────────────────────────
# CSS FIX (INPUT COLOR) ✅
# ─────────────────────────────────────────────

st.markdown("""
<style>

/* Light mode */
[data-theme="light"] input,
[data-theme="light"] textarea,
[data-theme="light"] .stTextInput input {
    color: #111827 !important;
    background-color: #f9fafb !important;
    border: 1px solid #c7d2fe !important;
}

/* Dark mode */
[data-theme="dark"] input,
[data-theme="dark"] textarea,
[data-theme="dark"] .stTextInput input {
    color: #f8fafc !important;
    background-color: #1e293b !important;
    border: 1px solid #6366f1 !important;
}

/* Fallback */
input, textarea {
    color: #111827 !important;
}

input::placeholder {
    color: #9ca3af !important;
}

</style>
""", unsafe_allow_html=True)
