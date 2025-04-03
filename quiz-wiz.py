import streamlit as st
import gspread
import random
import requests
from google.oauth2.credentials import Credentials

# Google Sheets & OAuth Setup
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing"
CLIENT_ID = "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REDIRECT_URI = "https://quiz321.streamlit.app"

# Fetch Access Token
def get_google_creds():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(TOKEN_URL, data=payload)
    response_json = response.json()
    return Credentials(token=response_json["access_token"])

# Connect to Google Sheets
def connect_gsheet():
    creds = get_google_creds()
    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(SHEET_URL).sheet1
    return sheet

# Fetch IPL Questions
def get_ipl_questions():
    questions = [
        {"question": "Who won the first IPL season?", "options": ["CSK", "RR", "MI", "RCB"], "answer": "RR"},
        {"question": "Who has the most IPL titles?", "options": ["MI", "CSK", "KKR", "SRH"], "answer": "MI"},
        {"question": "Which player has the most IPL centuries?", "options": ["Kohli", "Warner", "Gayle", "Rohit"], "answer": "Gayle"}
    ]
    return random.sample(questions, 3)

# Save Score to Google Sheet
def save_score(username, ip, score):
    sheet = connect_gsheet()
    sheet.append_row([username, ip, score])

# Get Leaderboard
def get_leaderboard():
    sheet = connect_gsheet()
    return sheet.get_all_values()[-5:]  # Last 5 entries

# Streamlit App
def quiz_app():
    st.title("🏏 IPL Quiz Challenge")
    username = st.text_input("Enter your name:")
    ip_address = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    
    if st.button("Start Quiz"):
        questions = get_ipl_questions()
        score = 0

        for q in questions:
            answer = st.radio(q["question"], q["options"])
            if answer == q["answer"]:
                score += 1
        
        save_score(username, ip_address, score)
        st.success(f"🎉 You scored {score}/3!")
    
    st.subheader("🏆 Leaderboard")
    leaderboard = get_leaderboard()
    for row in leaderboard:
        st.write(f"{row[0]} - {row[2]} points")

if __name__ == "__main__":
    quiz_app()
