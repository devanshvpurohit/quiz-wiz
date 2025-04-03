import streamlit as st
import gspread
from google.oauth2.credentials import Credentials
import pandas as pd

# 🚨 WARNING: Do NOT expose these credentials in production!
CLIENT_ID = "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "your-new-refresh-token-here"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit#gid=0"

# ✅ Authenticate with Google Sheets API
def authenticate_google():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    return creds

# ✅ Connect to Google Sheets
def connect_gsheet():
    creds = authenticate_google()
    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(SHEET_URL).sheet1
    return sheet

# ✅ Fetch Questions from Google Sheets
def get_questions():
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df.sample(20)  # Select 20 random IPL questions

# ✅ Save User Score to Google Sheets
def save_score(name, score):
    sheet = connect_gsheet()
    sheet.append_row([name, score])

# ✅ Fetch Leaderboard Data
def get_leaderboard():
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["Name", "Score"])
    return df.sort_values(by="Score", ascending=False)

# 🎮 Streamlit UI
st.title("🏏 IPL Quiz Game")
st.write("Answer 20 random IPL questions and see your score!")

# Leaderboard Section
st.header("🏆 Leaderboard")
leaderboard = get_leaderboard()
st.dataframe(leaderboard)

# Start Quiz
if st.button("Start Quiz"):
    questions = get_questions()
    score = 0
    for index, row in questions.iterrows():
        answer = st.radio(row["Question"], options=[row["Option1"], row["Option2"], row["Option3"], row["Option4"]])
        if answer == row["Correct Answer"]:
            score += 1

    name = st.text_input("Enter your name:")
    if st.button("Submit Score"):
        save_score(name, score)
        st.success(f"✅ {name}, your final score is: {score}/20")

