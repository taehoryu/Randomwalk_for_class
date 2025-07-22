import streamlit as st
from datetime import datetime
#from streamlit_gsheets import GSheetsConnection
import gspread
from streamlit_gsheets import GSheetsConnection
from oauth2client.service_account import ServiceAccountCredentials

credentials_dict = st.secrets["gcp_service_account"]

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1pAuI5OXYC8zjLS4jAUFB7BCC49qiz_ZvHFQpEpyZ21U")
worksheet = sheet.sheet1  # or worksheet by name

st.title("Random Walk Input")

student = st.text_input("Enter your name (or ID):")
step = st.number_input("Step number", min_value=0, step=1)
step_value = st.radio("Choose step", options=[1, -1], horizontal=True)

if st.button("Submit"):
    if student:
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet_url = "1pAuI5OXYC8zjLS4jAUFB7BCC49qiz_ZvHFQpEpyZ21U"
        df = conn.read(spreadsheet=sheet_url, worksheet="Sheet1")
        df = df._append({
            "timestamp": datetime.utcnow().isoformat(),
            "student": student,
            "step_number": step,
            "step_value": step_value
        }, ignore_index=True)
        conn.update(worksheet="Sheet1", data=df)
        st.success("Submitted successfully.")
    else:
        st.warning("Please enter your name or ID.")
