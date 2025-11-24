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
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Define CSS for light and dark modes
light_css = """
    <style>
    body {
        background: linear-gradient(to right, #4FD1C5, #60A5FA);
        color: #000000;
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
    .stProgress > div > div > div > div {
        background-color: #60A5FA;
    }
    .stTextInput, .stNumberInput {
        background-color: #ffffff;
        color: #000000;
    }
    </style>
"""

dark_css = """
    <style>
    body {
        background: linear-gradient(to right, #1a1a1a, #2d2d2d);
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4B5563;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #374151;
        color: white;
    }
    .stProgress > div > div > div > div {
        background-color: #60A5FA;
    }
    .stTextInput, .stNumberInput {
        background-color: #374151;
        color: #ffffff;
    }
    </style>
"""

# Apply the appropriate CSS based on dark_mode
if st.session_state.dark_mode:
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    st.markdown(light_css, unsafe_allow_html=True)

if st.session_state.phase == 1:
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    if st.button("Let's begin 💧", key="start_btn"):
        st.session_state.phase = 2

elif st.session_state.phase == 2:
    st.header("Select your age group")
    if st.button("Children (4–8 years)", key="age_children"):
        st.session_state.age_group = "Children (4-8 years)"
        st.session_state.goal = AGE_GROUPS["Children (4-8 years)"]
        st.session_state.phase = 3
    if st.button("Teens (9–13 years)", key="age_teens"):
        st.session_state.age_group = "Teens (9-13 years)"
        st.session_state.goal = AGE_GROUPS["Teens (9-13 years)"]
        st.session_state.phase = 3
    if st.button("Adults (14–64 years)", key="age_adults"):
        st.session_state.age_group = "Adults (14-64 years)"
        st.session_state.goal = AGE_GROUPS["Adults (14-64 years)"]
        st.session_state.phase = 3
    if st.button("Seniors (65+ years)", key="age_seniors"):
        st.session_state.age_group = "Seniors (65+ years)"
        st.session_state.goal = AGE_GROUPS["Seniors (65+ years)"]
        st.session_state.phase = 3

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
    if st.button("Continue ➡️", key="continue_btn"):
        st.session_state.phase = 4

elif st.session_state.phase == 4:
    st.title("📊 WaterBuddy Dashboard")
    st.write(f"Age group: {st.session_state.age_group}")
    st.write(f"Daily goal: {st.session_state.goal} ml")

    # Dark/Light mode toggle
    mode_label = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
    if st.button(mode_label, key="toggle_mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()  # Rerun to apply the new CSS

    col1, col2 = st.columns(2)
    with col1:
        if st.button("+250 ml", key="add250_btn"):
            st.session_state.total += 250
    with col2:
        manual_amount = st.number_input(
            "Log custom amount (ml):",
            min_value=0,
            step=50,
            key="manual_input"
        )
        if st.button("Add custom amount", key="add_custom"):
            st.session_state.total += manual_amount

    if st.button("🔄 New Day (Reset)", key="reset_btn"):
        st.session_state.total = 0

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
