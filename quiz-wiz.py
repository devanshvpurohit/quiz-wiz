import streamlit as st
import gspread
from google.oauth2.credentials import Credentials
import random

def authenticate_google_sheets():
    creds_info = {
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
    creds = Credentials.from_authorized_user_info(creds_info["web"])
    client = gspread.authorize(creds)
    return client

def update_username(username, sheet_name="Untitled"):
    client = authenticate_google_sheets()
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing").worksheet(sheet_name)
    sheet.append_row([username])

def get_quiz_questions(sheet_name="QuizQuestions"):
    client = authenticate_google_sheets()
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing").worksheet(sheet_name)
    data = sheet.get_all_records()
    return data

def update_leaderboard(username, score, sheet_name="Leaderboard"):
    client = authenticate_google_sheets()
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing").worksheet(sheet_name)
    sheet.append_row([username, score])

def display_leaderboard(sheet_name="Leaderboard"):
    client = authenticate_google_sheets()
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing").worksheet(sheet_name)
    data = sheet.get_all_records()
    sorted_data = sorted(data, key=lambda x: x["Score"], reverse=True)
    return sorted_data

st.title("🏏 IPL Quiz Challenge")

username = st.text_input("Enter your name to start:")

if username:
    update_username(username)  # Store username in 'Untitled' sheet
    questions = get_quiz_questions()
    score = 0
    for question in random.sample(questions, 5):
        st.write(question["Question"])
        answer = st.radio("Choose an answer:", question["Options"].split(","))
        if answer == question["Answer"]:
            score += 1
    
    st.write(f"### 🎉 Your Score: {score}/5")
    update_leaderboard(username, score)

    st.write("## 🏆 Leaderboard")
    leaderboard = display_leaderboard()
    for entry in leaderboard:
        st.write(f"{entry['Username']} - {entry['Score']}")
