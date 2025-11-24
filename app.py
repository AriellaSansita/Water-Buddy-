import streamlit as st
import random

AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}
HYDRATION_TIPS = [
    "Try drinking a glass of water before meals.",
    "Keep a bottle on your desk as a reminder.",
    "Start your morning with a glass of water.",
    "Set small goals: one cup every hour.",
    "Hydrate after exercise to recover faster."
]

# Session state
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Callbacks for buttons
def advance_phase():
    st.session_state.phase += 1

def toggle_tips():
    st.session_state.show_tips = not st.session_state.show_tips

def toggle_mascot():
    st.session_state.mascot_on = not st.session_state.mascot_on

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Button logic (at top)
if st.session_state.phase == 1:
    st.button("Start", on_click=advance_phase, key="start")
st.button("Toggle Tips", on_click=toggle_tips, key="tips")
st.button("Toggle Mascot", on_click=toggle_mascot, key="mascot")
st.button("Toggle Dark Mode", on_click=toggle_dark_mode, key="dark")

# UI rendering (based on updated state)
st.title("Hydration Tracker")
if st.session_state.phase == 1:
    st.write("Welcome! Click Start to begin.")
elif st.session_state.phase == 2:
    st.session_state.age_group = st.selectbox("Select Age Group", list(AGE_GROUPS.keys()))
    st.session_state.goal = AGE_GROUPS[st.session_state.age_group]
    st.button("Next", on_click=advance_phase, key="next_age")
# Add more phases as needed

if st.session_state.show_tips:
    st.subheader("Tips")
    for tip in HYDRATION_TIPS:
        st.write(tip)

if st.session_state.mascot_on:
    st.write("🐳 Mascot is on!")  # Replace with image

# Dark mode (basic example)
if st.session_state.dark_mode:
    st.markdown("<style>body { background-color: black; color: white; }</style>", unsafe_allow_html=True)
