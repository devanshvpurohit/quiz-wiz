import streamlit as st
import gspread
import random
import requests
from google.oauth2.credentials import Credentials

# Google Sheets API credentials
CLIENT_ID = "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "your-refresh-token-here"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing"

# Function to refresh Google OAuth token
def get_google_creds():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    response_json = response.json()
    return Credentials(token=response_json["access_token"])

# Connect to Google Sheet
def connect_gsheet():
    creds = get_google_creds()
    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(SHEET_URL).sheet1  # Connect to first sheet
    return sheet

# Fetch random IPL questions
def get_ipl_questions():
    questions = [
        {"question": "Who won the IPL 2023?", "options": ["CSK", "MI", "RCB", "KKR"], "answer": "CSK"},
        {"question": "Who has the most IPL titles?", "options": ["MI", "CSK", "KKR", "SRH"], "answer": "MI"},
        {"question": "Who scored the first IPL century?", "options": ["Brendon McCullum", "Virat Kohli", "Sachin Tendulkar", "Chris Gayle"], "answer": "Brendon McCullum"},
        {"question": "Which team has never won an IPL title?", "options": ["RCB", "RR", "DC", "SRH"], "answer": "RCB"}
    ]
    return random.sample(questions, 3)  # Pick 3 random questions

# Main quiz function
def quiz_app():
    st.title("🏏 IPL Quiz")
    username = st.text_input("Enter your name:")
    ip_address = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    
    if username:
        score = 0
        questions = get_ipl_questions()
        
        for q in questions:
            answer = st.radio(q["question"], q["options"], index=None)
            if answer and answer == q["answer"]:
                score += 1
        
        if st.button("Submit Quiz"):
            sheet = connect_gsheet()
            sheet.append_row([username, ip_address, score])
            st.success(f"✅ {username}, your score: {score}/3")
            
            # Show leaderboard
            st.subheader("🏆 Leaderboard")
            records = sheet.get_all_values()
            st.table(records)

# Run the quiz
quiz_app()
