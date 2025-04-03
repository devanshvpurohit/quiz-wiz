import streamlit as st
import random
import gspread
from google.oauth2.credentials import Credentials

# Google Sheets Authentication
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing"
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

auth_info = {
    "web": {
        "client_id": "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com",
        "project_id": "secret-willow-453305-m7",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["https://quiz321.streamlit.app"],
        "javascript_origins": ["https://quiz321.streamlit.app"]
    }
}

def authenticate_google_sheets():
    creds = Credentials.from_authorized_user_info(auth_info["web"], scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def update_leaderboard(username, score):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(SHEET_URL).worksheet("Leaderboard")
    sheet.append_row([username, score])

def display_leaderboard():
    client = authenticate_google_sheets()
    sheet = client.open_by_url(SHEET_URL).worksheet("Leaderboard")
    data = sheet.get_all_records()
    sorted_data = sorted(data, key=lambda x: x["Score"], reverse=True)
    return sorted_data

# Predefined IPL Quiz Questions
quiz_questions = [
    {"question": "Who won the first IPL season in 2008?", "options": ["Chennai Super Kings", "Rajasthan Royals", "Mumbai Indians", "Kolkata Knight Riders"], "answer": "Rajasthan Royals"},
    {"question": "Which player has scored the most runs in IPL history?", "options": ["Virat Kohli", "Suresh Raina", "Rohit Sharma", "David Warner"], "answer": "Virat Kohli"},
    {"question": "Who has taken the most wickets in IPL history?", "options": ["Lasith Malinga", "Dwayne Bravo", "Yuzvendra Chahal", "Amit Mishra"], "answer": "Yuzvendra Chahal"},
    {"question": "Which team has won the most IPL titles?", "options": ["Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders", "Royal Challengers Bangalore"], "answer": "Mumbai Indians"},
    {"question": "Who hit the fastest century in IPL history?", "options": ["Chris Gayle", "AB de Villiers", "David Warner", "Yusuf Pathan"], "answer": "Chris Gayle"},
    {"question": "Which bowler took the first hat-trick in IPL?", "options": ["Amit Mishra", "Lakshmipathy Balaji", "Sunil Narine", "Praveen Kumar"], "answer": "Lakshmipathy Balaji"},
    {"question": "Who is known as 'Mr. IPL'?", "options": ["Virat Kohli", "MS Dhoni", "Suresh Raina", "Rohit Sharma"], "answer": "Suresh Raina"},
    {"question": "Which team scored the highest total in IPL history?", "options": ["Royal Challengers Bangalore", "Chennai Super Kings", "Kolkata Knight Riders", "Mumbai Indians"], "answer": "Royal Challengers Bangalore"}
]

st.title("🏏 IPL Quiz Challenge")

username = st.text_input("Enter your name to start:")

if username:
    score = 0
    selected_questions = random.sample(quiz_questions, 5)
    for question in selected_questions:
        st.write(question["question"])
        answer = st.radio("Choose an answer:", question["options"], key=question["question"])
        if st.button("Submit", key=question["question"] + "_btn"):
            if answer == question["answer"]:
                score += 1
    
    st.write(f"### 🎉 Your Score: {score}/5")
    update_leaderboard(username, score)

    st.write("## 🏆 Leaderboard")
    leaderboard = display_leaderboard()
    for entry in leaderboard:
        st.write(f"{entry['Username']} - {entry['Score']}")
