import streamlit as st
import pandas as pd
import random
import gspread
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🔹 OAuth Credentials (Directly Hardcoded - NOT SECURE)
CLIENT_ID = "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit#gid=0"

# 🔹 OAuth 2.0 Authentication
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    SCOPES,
)
creds = flow.run_local_server(port=0)
service = build("sheets", "v4", credentials=creds)

def connect_gsheet():
    """ Connects to Google Sheets API """
    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(SHEET_URL).sheet1
    return sheet

def save_score(name, score):
    """ Saves user score to Google Sheets """
    sheet = connect_gsheet()
    sheet.append_row([name, score])

def get_leaderboard():
    """ Fetches leaderboard data from Google Sheets """
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
