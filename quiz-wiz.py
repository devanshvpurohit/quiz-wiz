import streamlit as st
import pandas as pd
import gspread
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 🔹 Google OAuth Credentials
CLIENT_ID = "269670970067-4vf0m1aal2eav4po7bs7sflmp2uqgbg5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "your-refresh-token-here"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit#gid=0"

# 🔹 Authenticate with Refresh Token
def authenticate_google():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    return creds

# 🔹 Connect to Google Sheets
def connect_gsheet():
    creds = authenticate_google()
    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(SHEET_URL).sheet1
    return sheet

# 🔹 Save Score to Google Sheets
def save_score(name, score):
    sheet = connect_gsheet()
    sheet.append_row([name, score])

# 🔹 Get Leaderboard
def get_leaderboard():
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(columns=["Name", "Score"])
    df = df.sort_values(by="Score", ascending=False)
    return df

# 🔹 Streamlit UI
st.title("🏏 IPL Quiz Challenge")
st.write("Test your IPL knowledge!")

# Leaderboard
st.header("🏆 Leaderboard")
leaderboard = get_leaderboard()
st.dataframe(leaderboard)
