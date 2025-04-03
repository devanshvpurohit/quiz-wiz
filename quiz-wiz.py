import streamlit as st
import gspread
import random
import requests
from google.oauth2.credentials import Credentials

# Google Sheets Info
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing"
CLIENT_ID = "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "your-refresh-token-here"

# Authenticate with Google Sheets
def authenticate_google():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    gc = gspread.authorize(creds)
    return gc

# Connect to Google Sheets
def connect_gsheet():
    gc = authenticate_google()
    sheet = gc.open_by_url(SHEET_URL).sheet1
    return sheet

# Get 20 random IPL questions
def get_ipl_questions():
    questions = [
        {"question": "Who has won the most IPL titles?", "options": ["CSK", "MI", "RCB", "KKR"], "answer": "MI"},
        {"question": "Who is the leading run-scorer in IPL history?", "options": ["Virat Kohli", "David Warner", "Suresh Raina", "Rohit Sharma"], "answer": "Virat Kohli"},
        {"question": "Which team won the first IPL season?", "options": ["CSK", "RR", "RCB", "KKR"], "answer": "RR"},
        {"question": "Which player has hit the most sixes in IPL history?", "options": ["MS Dhoni", "AB de Villiers", "Chris Gayle", "Rohit Sharma"], "answer": "Chris Gayle"},
        {"question": "Who is the highest wicket-taker in IPL history?", "options": ["Lasith Malinga", "Dwayne Bravo", "Amit Mishra", "Yuzvendra Chahal"], "answer": "Yuzvendra Chahal"},
        {"question": "Which team has the most final appearances?", "options": ["MI", "CSK", "KKR", "SRH"], "answer": "CSK"},
        {"question": "Who was the first Indian to score an IPL century?", "options": ["Virender Sehwag", "Sachin Tendulkar", "Manish Pandey", "Rohit Sharma"], "answer": "Manish Pandey"},
        {"question": "Which player has won the most IPL MVP awards?", "options": ["Virat Kohli", "Andre Russell", "Sunil Narine", "Chris Gayle"], "answer": "Andre Russell"},
        {"question": "Which bowler has the best bowling figures in an IPL match?", "options": ["Sohail Tanvir", "Anil Kumble", "Alzarri Joseph", "Adam Zampa"], "answer": "Alzarri Joseph"},
        {"question": "Which team was banned for two seasons due to corruption?", "options": ["CSK", "RCB", "RR", "SRH"], "answer": "CSK, RR"},
    ]
    return random.sample(questions, 5)  # Select 5 random questions

# Get user IP Address
def get_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        return response.json()["ip"]
    except:
        return "Unknown"

# Save Score to Google Sheet
def save_score(username, ip_address, score):
    sheet = connect_gsheet()
    sheet.append_row([username, ip_address, score])

# Quiz App
def quiz_app():
    st.title("🏏 IPL Quiz Challenge!")
    username = st.text_input("Enter your name:")
    
    if st.button("Start Quiz"):
        if not username:
            st.warning("Please enter your name to continue!")
            return
        
        ip_address = get_ip()
        questions = get_ipl_questions()
        score = 0

        for q in questions:
            st.subheader(q["question"])
            user_answer = st.radio("Choose an answer:", q["options"], key=q["question"])
            if st.button("Submit Answer", key=f"btn-{q['question']}"):
                if user_answer == q["answer"]:
                    score += 1
        
        st.success(f"🎉 {username}, you scored {score}/{len(questions)}!")
        save_score(username, ip_address, score)

    # Show Leaderboard
    st.subheader("🏆 Leaderboard")
    sheet = connect_gsheet()
    records = sheet.get_all_values()[1:]  # Skip header
    for record in records:
        st.write(f"{record[0]} - {record[1]} - {record[2]} points")

# Run App
if __name__ == "__main__":
    quiz_app()
