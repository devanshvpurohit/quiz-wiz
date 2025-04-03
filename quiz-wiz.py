import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def get_player_score(player_name):
    """Fetch player historical performance using Gemini."""
    prompt = f"Provide a summary performance score (out of 100) for the cricketer {player_name} based on historical IPL data."
    response = genai.generate_text(prompt)
    return extract_score(response)

# Mock function to extract score from Gemini's response
def extract_score(response):
    try:
        return int(response.split()[0])  # Assuming response starts with score
    except:
        return 50  # Default score

# Streamlit UI
st.title("IPL 2025 Team Ranking Based on Player History")

# Dynamic input for teams and players
teams = st.text_area("Enter team names (comma-separated)").split(",")
team_players = {}
for team in teams:
    team = team.strip()
    if team:
        players = st.text_area(f"Enter players for {team} (comma-separated)").split(",")
        team_players[team] = [p.strip() for p in players if p.strip()]

if st.button("Rank Teams"):
    all_players = [(team, player) for team, players in team_players.items() for player in players]
    df = pd.DataFrame(all_players, columns=["Team", "Player"])
    df["Score"] = df["Player"].apply(get_player_score)
    team_scores = df.groupby("Team")["Score"].sum().reset_index()
    team_scores = team_scores.sort_values(by="Score", ascending=False)
    
    st.write("### Ranked Teams")
    st.dataframe(team_scores)
else:
    st.write("Enter team and player details, then click Rank Teams.")
