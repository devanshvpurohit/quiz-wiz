import streamlit as st
import random
import gspread
from google.oauth2.service_account import Credentials

# Google Service Account JSON credentials
service_account_info = {
    "type": "service_account",
    "project_id": "secret-willow-453305-m7",
    "private_key_id": "20d3175ecad4b2b8ad4da67fc18fcc044dedf00d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCRu8qWvmWZ9SVd\nU+h7+qBmwCG0teUZK3GYkOG4V3oMTgbacNx8gTIZpPUpmwccyhuqs0aKCAHP2q04\niBhinw/qV6dWriiUD8nW0nET3Pd811BMUJffIy6mIU2yTXum/hLOmcxc7t81wTxI\nELbAq4X3nRumnIaNrRV02QXZcry8tCzsDeAkRpjc5/tZix/a1PAam7r+vJd9FTcB\ngXDlpOQGznL2v6SkMXbNtwuFMh7sL5d1xkxtT6RO/FxuKoYsJRGQ7gxMCQha/B3M\nwJWPpYwxc11eKbXdK8KkHcusJ9cI0RRmSBaf1DCasX3E9zg5XZRqEdmLa06absg4\nUQ+m5EX3AgMBAAECggEAF3YzCoC9jQMv+u3yxt7rADpx/WID75Y/FAT4fzvUt3K/\nsgmAcv+TssLhVfY84hAm/cdzQEPuEr9NqtpniUe6rAtk3SoYTfnwEIh8UZUojNiB\nzL90K9AXXFc5PHmH7N2zkRT77IGSaC44smYVHetJ8TrBrwQ9D0WsZ3g287J/8HsX\nx7GCqOSNCxD0mR20jOELE7xh5GAXdrHp15rqzjHC5JuUMzwpddgh2Yv/SEByUwh+\nVV7bhYp9RfdazJuWvUax4OybVxcsghQebKoUDfb92QRMwP8vp44qwCZtw80ORhQV\n/CvJlXygl9NTrdz73mF7pLzaPV9VWf7ILB4veqTkvQKBgQDBw9qCwGX01uJnWH3u\nCk538UHxeaDrLYBWhIWlvgxmD/q+s4DQJz66U+KYCNZ6QRNWbTcY6ZM9lNUKodQy\nOW/dtCRzwchat3ISBiXww9Y32SqZRU4yruDsGeISNtZ96+qRNtWczO3sUOshHL91\nzIr19NkziKpr9c8ngywR25yvywKBgQDAipgbN8cNaLzheL1wxa9weKgr248t5Ss+\nsuciqIGGSBkjhwRGATCl3K3S4TUo1QSQYNqGmnNJqy4O7te1ZcZjtxpD+h11GlJ1\nUbLQHQ4XbmFykZHcaXq28PPUauKAqcUBz2v+0UXSj/RzSEBzyliMfU4fSU1DrlJY\nMMU5n7WlBQKBgQCFyzwlzr5YCsz4eWUzKhC2x3M2TzrrSVb15rn2ET20d9I3PfFz\nSbYJqQSs4GVgs3Cr2+wQmrBd9FgK6GWCbKCu4MXO3H8BDOyKP46RKljP5XeBsBZn\n7tNGlDTDSPRgrLcioE9t3x9mbxV8nsIhkCRf4zrbV8H9nBT3fp6+kfsmcwKBgDdb\n4e35dI7jbWM6juVMwWuKFXg+sYUVngBx+cjaQBt2wVuYp17lWrJlp8i5Hcq2rJBC\neLI42Cr3P8/lVjn+oDLtY2zmDfAseEbpDYuOvw13nCcPuatw3GqbDtAlRyiNJ2qk\n0705OGUZJMS8omNoa1tBb+PI9KEgDubyZtJxnA1tAoGBAJPusFX9jLnVT8Fso8IH\nyR0W4TOJf36Wple/cc8598U4wOAfBJ6IgEZypBgvaatNcu9FAW95wtgCbZUcXlS4\n6k0TwKDNm0IphWBgbSb9FsrjZaFr2UclSbf2ticKcCympkDF8Yl9/3iq0GSJ9bkN\nxKrAMsCyN2ns0Lk3ep/sH6R9\n-----END PRIVATE KEY-----\n",
    "client_email": "devanshvpurohit-118@secret-willow-453305-m7.iam.gserviceaccount.com",
    "client_id": "110282333842840776382",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/devanshvpurohit-118%40secret-willow-453305-m7.iam.gserviceaccount.com"
}

# Authenticate with Google Sheets
creds = Credentials.from_service_account_info(service_account_info)
client = gspread.authorize(creds)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1csaETbJIYJPW9amvGB9rq0uYEK7sH83Ueq8UUjpp0GU/edit?usp=sharing"

# Hardcoded IPL Quiz Questions
quiz_questions = [
    {"question": "Who won the first IPL season in 2008?", "options": ["CSK", "RCB", "RR", "MI"], "answer": "RR"},
    {"question": "Which player has the most runs in IPL history?", "options": ["Virat Kohli", "Rohit Sharma", "Suresh Raina", "David Warner"], "answer": "Virat Kohli"},
    {"question": "Who has taken the most wickets in IPL history?", "options": ["Lasith Malinga", "Dwayne Bravo", "Amit Mishra", "Yuzvendra Chahal"], "answer": "Yuzvendra Chahal"}
]

def update_leaderboard(username, score):
    sheet = client.open_by_url(SHEET_URL).worksheet("Leaderboard")
    sheet.append_row([username, score])

def display_leaderboard():
    sheet = client.open_by_url(SHEET_URL).worksheet("Leaderboard")
    data = sheet.get_all_records()
    sorted_data = sorted(data, key=lambda x: x.get("Score", 0), reverse=True)
    return sorted_data
