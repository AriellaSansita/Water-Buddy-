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

# Callback functions for button actions (added for single-click responsiveness)
def start_app():
    st.session_state.phase = 2

def select_children():
    st.session_state.age_group = "Children (4-8 years)"
    st.session_state.goal = AGE_GROUPS["Children (4-8 years)"]
    st.session_state.phase = 3

def select_teens():
    st.session_state.age_group = "Teens (9-13 years)"
    st.session_state.goal = AGE_GROUPS["Teens (9-13 years)"]
    st.session_state.phase = 3

def select_adults():
    st.session_state.age_group = "Adults (14-64 years)"
    st.session_state.goal = AGE_GROUPS["Adults (14-64 years)"]
    st.session_state.phase = 3

def select_seniors():
    st.session_state.age_group = "Seniors (65+ years)"
    st.session_state.goal = AGE_GROUPS["Seniors (65+ years)"]
    st.session_state.phase = 3

def continue_to_dashboard():
    st.session_state.phase = 4

def add_250():
    st.session_state.total += 250

def add_custom(manual_amount):
    st.session_state.total += manual_amount

def reset_day():
    st.session_state.total = 0

st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #4FD1C5, #60A5FA);
    }
    .stButton>button {
        background-color: #60A5FA;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.phase == 1:
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    if st.button("Let's begin 💧", key="start_btn", on_click=start_app):
        pass  # Action handled by callback

elif st.session_state.phase == 2:
    st.header("Select your age group")
    if st.button("Children (4–8 years)", key="age_children", on_click=select_children):
        pass  # Action handled by callback
    if st.button("Teens (9–13 years)", key="age_teens", on_click=select_teens):
        pass  # Action handled by callback
    if st.button("Adults (14–64 years)", key="age_adults", on_click=select_adults):
        pass  # Action handled by callback
    if st.button("Seniors (65+ years)", key="age_seniors", on_click=select_seniors):
        pass  # Action handled by callback

elif st.session_state.phase == 3:
    st.header("Confirm or adjust your daily goal")
    st.write(f"Recommended goal for {st.session_state.age_group}: {AGE_GROUPS[st.session_state.age_group]} ml")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=4000,
        value=AGE_GROUPS[st.session_state.age_group],
        step=100,
        key="goal_input"
    )
    if st.button("Continue ➡️", key="continue_btn", on_click=continue_to_dashboard):
        pass  # Action handled by callback

elif st.session_state.phase == 4:
    st.title("📊 WaterBuddy Dashboard")
    st.write(f"Age group: {st.session_state.age_group}")
    st.write(f"Daily goal: {st.session_state.goal} ml")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("+250 ml", key="add250_btn", on_click=add_250):
            pass  # Action handled by callback
    with col2:
        manual_amount = st.number_input(
            "Log custom amount (ml):",
            min_value=0,
            step=50,
            key="manual_input"
        )
        if st.button("Add custom amount", key="add_custom", on_click=lambda: add_custom(manual_amount)):
            pass  # Action handled by callback

    if st.button("🔄 New Day (Reset)", key="reset_btn", on_click=reset_day):
        pass  # Action handled by callback

    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"Total intake so far: {st.session_state.total} ml")
    st.write(f"Remaining to goal: {remaining} ml")
    st.write(f"Progress: {progress*100:.1f}%")

    if st.session_state.mascot_on:
        if progress == 0:
            st.info("Let's start hydrating! 🚰🙂")
        elif progress < 0.5:
            st.info("Good start! Keep sipping 💦😃")
        elif progress < 0.75:
            st.success("Nice! You're halfway there 😎")
        elif progress < 1.0:
            st.success("Almost at your goal! 🌊🤗")
        else:
            st.balloons()
            st.success("🎉 Congratulations! You hit your hydration goal! 🥳")

    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))
