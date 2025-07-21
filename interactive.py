import pandas as pd
import numpy as np
import sys
import streamlit as st
st.write("Running Python from:", sys.executable)
import matplotlib.pyplot as plt

st.title("Random Walk Input and Ensemble Average!")

# Use session state to hold data across reruns
if "data" not in st.session_state:
    # DataFrame indexed by step, columns = student names, values = positions
    st.session_state.data = pd.DataFrame()

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

st.write(f"### Step {st.session_state.current_step + 1}")

# Student name input (required to identify different students)
student_name = st.text_input("Enter your name:")

if student_name:
    # Get previous position for this student (last known position or 0 if new)
    if student_name in st.session_state.data.columns:
        last_position = st.session_state.data[student_name].iloc[-1]
    else:
        last_position = 0

    # Input for step: +1 or -1
    step_value = st.radio("Choose step (+1 or -1):", options=[1, -1], index=0, format_func=lambda x: f"+{x}" if x>0 else str(x))

    # Submit button to record step
    if st.button("Submit step"):

        # Increase step counter only if this student hasn't entered step for current step yet
        # Check if this step for student exists to avoid duplicate entry
        if st.session_state.current_step < len(st.session_state.data):
            if student_name in st.session_state.data.columns and not pd.isna(st.session_state.data.at[st.session_state.current_step, student_name]):
                st.warning(f"{student_name}, you already submitted step {st.session_state.current_step + 1}")
            else:
                # Update data with new step for this student
                new_pos = last_position + step_value
                st.session_state.data.at[st.session_state.current_step, student_name] = new_pos
        else:
            # New step row
            new_pos = last_position + step_value
            new_row = pd.Series({student_name: new_pos}, name=st.session_state.current_step)
            st.session_state.data = pd.concat([st.session_state.data, new_row.to_frame().T])
        
        st.success(f"Recorded step {st.session_state.current_step + 1} for {student_name} with value {step_value}")

        # After each submission, check if all students submitted current step, then increment step
        # Get all students who have ever submitted (all columns)
        all_students = st.session_state.data.columns.tolist()

        # Check if current step row is complete (no NaN for all students)
        current_row = st.session_state.data.iloc[st.session_state.current_step]
        # Fill missing students with previous positions to not block step increment
        missing_students = [s for s in all_students if pd.isna(current_row.get(s, np.nan))]
        if not missing_students:
            st.session_state.current_step += 1

# Show current data table
st.write("### Recorded Positions:")
st.dataframe(st.session_state.data.fillna(method='ffill').fillna(0).astype(int))

if not st.session_state.data.empty:
    # Fill NaN with last known positions or 0
    data_filled = st.session_state.data.fillna(method='ffill').fillna(0)

    # Plot paths for each student
    fig, ax = plt.subplots(figsize=(10,5))

    for student in data_filled.columns:
        ax.plot(data_filled.index + 1, data_filled[student], marker='o', label=student)

    # Ensemble average
    ensemble_avg = data_filled.mean(axis=1)
    ax.plot(data_filled.index + 1, ensemble_avg, 'k--', linewidth=2, label="Ensemble Average")

    ax.set_xlabel("Step")
    ax.set_ylabel("Position")
    ax.set_title("Random Walk Paths and Ensemble Average")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
