import streamlit as st
import pandas as pd
import os

def load_leaderboard():
    if os.path.exists("leaderboard.xlsx"):
        return pd.read_excel("leaderboard.xlsx")
    return pd.DataFrame(columns=["Name", "Score"])

def save_score(name, score):
    leaderboard = load_leaderboard()
    new_entry = pd.DataFrame([[name, score]], columns=["Name", "Score"])
    leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)
    leaderboard.to_excel("leaderboard.xlsx", index=False)

def main():
    st.title("Quiz-Wiz Leaderboard")
    
    name = st.text_input("Enter your name:")
    score = st.number_input("Enter your score:", min_value=0, step=1)
    
    if st.button("Submit Score") and name:
        save_score(name, score)
        st.success("Score submitted successfully!")
    
    st.header("Leaderboard")
    leaderboard = load_leaderboard()
    st.dataframe(leaderboard)

if __name__ == "__main__":
    main()
