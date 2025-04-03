import streamlit as st
import requests
import pandas as pd
import random
import gspread

# 🔥 Hardcoded API Key (Avoid using in production)
API_KEY = "AIzaSyDQnu06TUPZGkXIoZKohK9T4ut5-3Kyv5o"

# 🔹 Fetch IPL Quiz Questions (Replace with a real API if available)
def fetch_ipl_questions():
    url = f"https://api.example.com/get-ipl-questions?key={API_KEY}"  # Replace with actual API
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()["questions"]  # Assuming API returns {"questions": [...]} format
    else:
        st.warning("Failed to fetch IPL questions. Using sample data.")
        return [
            {"question": "Who won the first IPL title?", "options": ["CSK", "RR", "MI", "RCB"], "answer": "RR"},
            {"question": "Which team has won the most IPL trophies?", "options": ["MI", "CSK", "KKR", "SRH"], "answer": "MI"},
            {"question": "Who is the highest run-scorer in IPL history?", "options": ["Virat Kohli", "Rohit Sharma", "David Warner", "AB de Villiers"], "answer": "Virat Kohli"},
        ]

# 🔹 Connect to Public Google Sheet (Without Authentication)
def connect_gsheet():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit#gid=0"
    gc = gspread.service_account(filename=None)  # No credentials required for public sheets
    sheet = gc.open_by_url(SHEET_URL).sheet1
    return sheet

# 🔹 Save Quiz Results to Google Sheets
def save_results(name, score):
    sheet = connect_gsheet()
    sheet.append_row([name, score])

# 🔹 Streamlit App UI
st.title("🏏 IPL Quiz Challenge")
st.write("Test your IPL knowledge with 20 random questions!")

# Fetch and shuffle questions
questions = fetch_ipl_questions()
random.shuffle(questions)
questions = questions[:20]  # Get 20 random questions

user_answers = {}
for idx, q in enumerate(questions):
    st.subheader(f"Q{idx+1}: {q['question']}")
    user_answers[q['question']] = st.radio("Select your answer:", q['options'], key=q['question'])

# Submit Button
if st.button("Submit Answers"):
    correct_answers = sum(1 for q in questions if user_answers[q['question']] == q['answer'])
    st.success(f"🎉 You scored {correct_answers} out of 20!")

    # Get user name
    name = st.text_input("Enter your name to save your score:")
    
    if st.button("Save Score"):
        save_results(name, correct_answers)
        st.success("✅ Your score has been saved!")
