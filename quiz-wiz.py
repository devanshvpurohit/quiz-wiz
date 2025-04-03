import streamlit as st
import pandas as pd
import random
import gspread

# 🔹 Google Sheets Setup (Public Sheet Required)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit#gid=0"

def connect_gsheet():
    """ Connects to a public Google Sheet without authentication. """
    gc = gspread.open_by_url(SHEET_URL)  # No authentication needed
    sheet = gc.sheet1
    return sheet

def save_score(name, score):
    """ Saves user score to Google Sheets. """
    sheet = connect_gsheet()
    sheet.append_row([name, score])

def get_leaderboard():
    """ Fetches the leaderboard from Google Sheets. """
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["Name", "Score"])
    df = df.sort_values(by="Score", ascending=False)  # Sort by highest score
    return df

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

    # Get user name
    name = st.text_input("Enter your name to save your score:")
    
    if st.button("Save Score"):
        save_score(name, correct_answers)
        st.success("✅ Your score has been saved to Google Sheets!")

# 🔹 Leaderboard Section
st.header("🏆 Leaderboard")
leaderboard = get_leaderboard()
st.dataframe(leaderboard)
