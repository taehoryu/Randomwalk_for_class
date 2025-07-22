import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

student = st.text_input("Enter your name (or ID):")
step = st.number_input("Step number", min_value=0, step=1)
step_value = st.radio("Choose step", options=[1, -1], horizontal=True)

if st.button("Submit"):
    if student:
        try:
            # Read existing data from Sheet1
            df = conn.read()#worksheet="Sheet1")

            # Append new data
            df = df._append({
                "timestamp": datetime.utcnow().isoformat(),
                "student": student,
                "step_number": step,
                "step_value": step_value
            }, ignore_index=True)

            # Write back to the sheet
            conn.update(data=df)
            st.success("Submitted successfully.")
        except Exception as e:
            st.error(f"Error submitting: {e}")
    else:
        st.warning("Please enter your name or ID.")


df = conn.read()
# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
