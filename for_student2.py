import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.title("Random Walk Input")

# Load Google Sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Spreadsheet ID or full URL (either works)
sheet_url = "https://docs.google.com/spreadsheets/d/1pAuI5OXYC8zjLS4jAUFB7BCC49qiz_ZvHFQpEpyZ21U"

# Student input form
student = st.text_input("Enter your name (or ID):")
step = st.number_input("Step number", min_value=0, step=1)
step_value = st.radio("Choose step", options=[1, -1], horizontal=True)

if st.button("Submit"):
    if student:
        try:
            # Read existing data from Sheet1
            df = conn.read(worksheet="Sheet1")

            # Append new data
            df = df._append({
                "timestamp": datetime.utcnow().isoformat(),
                "student": student,
                "step_number": step,
                "step_value": step_value
            }, ignore_index=True)

            # Write back to the sheet
            conn.update(worksheet="Sheet1", data=df)
            st.success("Submitted successfully.")
        except Exception as e:
            st.error(f"Error submitting: {e}")
    else:
        st.warning("Please enter your name or ID.")
