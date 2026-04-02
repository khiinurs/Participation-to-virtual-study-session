import streamlit as st
import json
import csv
import io
import re
from datetime import date, datetime

# ─────────────────────────────────────────────
# PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Virtual Study Focus Survey",
    page_icon="🎓",
    layout="centered",
)

# ─────────────────────────────────────────────
# CSS FIX (INPUT VISIBILITY) ✅
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

# ─────────────────────────────────────────────
# QUESTIONS (15 ONLY) ✅
# ─────────────────────────────────────────────
QUESTIONS = [
    {"text": "How often do you join scheduled virtual study sessions?",
     "options": [("Every session", 0), ("Most of the time", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)]},

    {"text": "How long can you stay focused during online study?",
     "options": [("90+ mins", 0), ("60–90 mins", 1), ("30–60 mins", 2), ("<30 mins", 3), ("Not at all", 4)]},

    {"text": "How well do you manage distractions?",
     "options": [("Fully control", 0), ("Mostly", 1), ("Sometimes", 2), ("Often distracted", 3), ("Never control", 4)]},

    {"text": "How comfortable are you participating?",
     "options": [("Very", 0), ("Fairly", 1), ("Neutral", 2), ("Uncomfortable", 3), ("Never", 4)]},

    {"text": "Internet stability?",
     "options": [("Perfect", 0), ("Mostly fine", 1), ("Sometimes issues", 2), ("Often issues", 3), ("Very bad", 4)]},

    {"text": "Retention after sessions?",
     "options": [("Very good", 0), ("Good", 1), ("Average", 2), ("Poor", 3), ("Very poor", 4)]},

    {"text": "Mental fatigue?",
     "options": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"text": "Study environment quality?",
     "options": [("Excellent", 0), ("Good", 1), ("Okay", 2), ("Poor", 3), ("Very poor", 4)]},

    {"text": "Follow study schedule?",
     "options": [("Always", 0), ("Usually", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)]},

    {"text": "Opinion on online collaboration?",
     "options": [("Very positive", 0), ("Positive", 1), ("Neutral", 2), ("Negative", 3), ("Very negative", 4)]},

    {"text": "Communication between sessions?",
     "options": [("Excellent", 0), ("Good", 1), ("Average", 2), ("Poor", 3), ("None", 4)]},

    {"text": "Handling technical issues?",
     "options": [("Very good", 0), ("Good", 1), ("Okay", 2), ("Poor", 3), ("Very poor", 4)]},

    {"text": "Preparation before sessions?",
     "options": [("Always", 0), ("Usually", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)]},

    {"text": "Effect on confidence?",
     "options": [("Very positive", 0), ("Positive", 1), ("Neutral", 2), ("Negative", 3), ("Very negative", 4)]},

    {"text": "Balance with responsibilities?",
     "options": [("Very well", 0), ("Well", 1), ("Okay", 2), ("Poor", 3), ("Very poor", 4)]},
]

# ─────────────────────────────────────────────
# SCORE RANGES (0–60) ✅
# ─────────────────────────────────────────────
PSYCHOLOGICAL_STATES = [
    {"range": (0, 10), "label": "Excellent"},
    {"range": (11, 20), "label": "Strong"},
    {"range": (21, 30), "label": "Moderate"},
    {"range": (31, 40), "label": "Below Average"},
    {"range": (41, 50), "label": "Low"},
    {"range": (51, 60), "label": "Poor"},
]

def get_state(score):
    for s in PSYCHOLOGICAL_STATES:
        if s["range"][0] <= score <= s["range"][1]:
            return s["label"]

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.title("🎓 Virtual Study Focus Survey")

name = st.text_input("Name")
student_id = st.text_input("Student ID")

answers = []

with st.form("survey"):
    for i, q in enumerate(QUESTIONS):
        choice = st.radio(q["text"], [o[0] for o in q["options"]], key=i)
        answers.append(next(v for t, v in q["options"] if t == choice))

    submit = st.form_submit_button("Submit")

if submit:
    score = sum(answers)
    state = get_state(score)

    st.success(f"Score: {score} / 60")
    st.info(f"State: {state}")
