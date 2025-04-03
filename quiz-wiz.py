import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Configuration
SPREADSHEET_KEY = "1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU"

# Connect to Google Sheets
def get_gsheet():
    gc = gspread.service_account()  # Ensure correct auth method
    return gc.open_by_key(SPREADSHEET_KEY).sheet1

def get_leaderboard():
    sheet = get_gsheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_leaderboard(name, score):
    sheet = get_gsheet()
    sheet.append_row([name, score])

# Quiz Questions
QUESTIONS = [
    {"question": "What is 2+2?", "options": ["1", "3", "4", "5"], "answer": "4"},
    {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"}
]

def quiz_app():
    st.title("Quiz App with Leaderboard")
    name = st.text_input("Enter your name:")
    
    if name:
        score = 0
        for q in QUESTIONS:
            answer = st.radio(q["question"], q["options"], key=q["question"])
            if answer == q["answer"]:
                score += 1
        
        if st.button("Submit Quiz"):
            update_leaderboard(name, score)
            st.success(f"{name}, your score is {score}/3")

    # Display Leaderboard
    st.subheader("Leaderboard")
    leaderboard = get_leaderboard()
    st.dataframe(leaderboard)

if __name__ == "__main__":
    quiz_app()
