import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Work Schedule Auto Formatter",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📅 Work Schedule Auto Formatter")

st.write(
    "Convert raw daily work updates into a professional time-table format automatically."
)

# ---------------- TIMINGS ----------------
TIME_SLOTS = [
    "9:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 11:30",
    "11:30 - 11:45 Break",
    "11:45 - 12:45",
    "12:45 - 2:00",
    "2:00 - 2:30 Lunch",
    "2:30 - 3:30",
    "3:30 - 4:30",
    "4:30 - 5:00",
]

# ---------------- SAMPLE FORMAT ----------------
st.subheader("📌 Input Format Example")

st.code(
"""11/5/2026
WSL2 & Docker Setup
Python venv & packages
All Agent files fix
Groq API configure
Frontend setup
AI Tutor working

8/5/2026
VS Code Agent Created
Learn and Developed on Streamlit
New LLM Installed
Worked in New Agent
Meeting with Team
""",
language="text"
)

# ---------------- TEXT INPUT ----------------
user_input = st.text_area(
    "Paste Your Work Content",
    height=350,
    placeholder="Paste your work updates here..."
)

# ---------------- PARSER FUNCTION ----------------
def parse_input(text):

    data = {}

    # Default today's work
    current_date = "Today's Work"

    data[current_date] = []

    # Split paragraph into activities
    activities = re.split(r',|\.| and ', text)

    cleaned = []

    for activity in activities:

        activity = activity.strip()

        if len(activity) > 4:
            cleaned.append(activity)

    data[current_date] = cleaned

    return data

# ---------------- GENERATE BUTTON ----------------
if st.button("Generate Schedule"):

    if not user_input.strip():
        st.warning("Please enter some work content.")

    else:

        parsed = parse_input(user_input)

        final_data = {
            "Timing / Date": TIME_SLOTS
        }

        for date, activities in parsed.items():

            schedule = []
            activity_index = 0

            for slot in TIME_SLOTS:

                if "Break" in slot:
                    schedule.append("Break")

                elif "Lunch" in slot:
                    schedule.append("Lunch")

                else:
                    if activity_index < len(activities):
                        schedule.append(activities[activity_index])
                        activity_index += 1
                    else:
                        schedule.append("-")

            final_data[date] = schedule

        # Create DataFrame
        df = pd.DataFrame(final_data)

        # ---------------- DISPLAY TABLE ----------------
        st.subheader("📋 Generated Work Schedule")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ---------------- CSV DOWNLOAD ----------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="work_schedule.csv",
            mime="text/csv"
        )

        st.success("Schedule generated successfully!")

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown(
"""
### ✅ Features
- Automatic timetable creation
- Horizontal date-wise schedule format
- Auto Break & Lunch insertion
- CSV export support
- Easy work documentation
"""
)
