import streamlit as st
import pandas as pd
import random

# 🔹 Google Sheets Public CSV URL (Change "edit" to "export?format=csv")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/export?format=csv"

def get_leaderboard():
    """Fetch leaderboard from Google Sheets (Read-Only)."""
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df = df.sort_values(by="Score", ascending=False)  # Sort by highest score
        return df
    except Exception as e:
        st.error(f"⚠️ Could not fetch leaderboard: {e}")
        return pd.DataFrame(columns=["Name", "Score"])

# 🔹 IPL Quiz Questions
def get_ipl_questions():
    questions = [
        {"question": "Who won the first IPL title?", "options": ["CSK", "RR", "MI", "RCB"], "answer": "RR"},
        {"question": "Which team has won the most IPL trophies?", "options": ["MI", "CSK", "KKR", "SRH"], "answer": "MI"},
        {"question": "Who is the highest run-scorer in IPL history?", "options": ["Virat Kohli", "Rohit Sharma", "David Warner", "AB de Villiers"], "answer": "Virat Kohli"},
        {"question": "Who won the IPL 2023 title?", "options": ["CSK", "GT", "RR", "MI"], "answer": "CSK"},
        {"question": "Which IPL team has never won a trophy?", "options": ["RCB", "KKR", "SRH", "DC"], "answer": "RCB"},
    ]
    random.shuffle(questions)
    return questions[:5]  # Select 5 random questions

# 🔹 Streamlit UI
st.title("🏏 IPL Quiz Challenge")
st.write("Test your IPL knowledge with 5 random questions!")

# Fetch questions
questions = get_ipl_questions()
user_answers = {}

for idx, q in enumerate(questions):
    st.subheader(f"Q{idx+1}: {q['question']}")
    user_answers[q['question']] = st.radio("Select your answer:", q['options'], key=q['question'])

# 🔹 Submit Button
if st.button("Submit Answers"):
    correct_answers = sum(1 for q in questions if user_answers[q['question']] == q['answer'])
    st.success(f"🎉 You scored {correct_answers} out of 5!")

# 🔹 Leaderboard Section (Read-Only)
st.header("🏆 Leaderboard")
leaderboard = get_leaderboard()
st.dataframe(leaderboard)
