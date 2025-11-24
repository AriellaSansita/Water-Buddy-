
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
if "custom_amount" not in st.session_state:
    st.session_state.custom_amount = 0

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

def start_app():
    st.session_state.phase = 2

def select_age(group, ml):
    st.session_state.age_group = group
    st.session_state.goal = ml
    st.session_state.phase = 3

def continue_to_dashboard():
    st.session_state.phase = 4

def reset_day():
    st.session_state.total = 0

def view_summary():
    st.session_state.phase = 5

def start_new_day():
    st.session_state.total = 0
    st.session_state.phase = 4

def back_to_dashboard():
    st.session_state.phase = 4

# ------------------------------------------------------
#                  SCREENS / PHASES
# ------------------------------------------------------

if st.session_state.phase == 1:
    st.title("Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    st.button("Let's begin", on_click=start_app)

elif st.session_state.phase == 2:
    st.header("Select your age group")
    for group, ml in AGE_GROUPS.items():
        st.button(group, on_click=select_age, args=(group, ml))

elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")
    st.write(f"Recommended goal for {st.session_state.age_group}: {AGE_GROUPS[st.session_state.age_group]} ml")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=st.session_state.goal if st.session_state.goal > 0 else AGE_GROUPS[st.session_state.age_group],
        step=100
    )
    st.button("Continue", on_click=continue_to_dashboard)

elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")

    st.markdown(f"### Age group: {st.session_state.age_group}")
    st.markdown(f"### Daily goal: **{st.session_state.goal} ml**")

    st.write("")

    # ------------------------------------------------------
    #   1) QUICK ADD BUTTONS
    # ------------------------------------------------------
    st.markdown("## 💧 Quick Add Water")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💧 250 ml"):
            st.session_state.total += 250
    with col2:
        if st.button("🥛 500 ml"):
            st.session_state.total += 500
    with col3:
        if st.button("🥤 750 ml"):
            st.session_state.total += 750
    with col4:
        if st.button("🍶 1 L"):
            st.session_state.total += 1000

    st.write("")

    # ------------------------------------------------------
    #   2) CUSTOM ADD
    # ------------------------------------------------------
    st.markdown("### ✏️ Add a custom amount")

    custom = st.number_input("Enter amount (ml):", min_value=0, step=50, value=st.session_state.custom_amount)
    if st.button("Add"):
        st.session_state.total += custom
        st.session_state.custom_amount = 0  # Reset after adding

    st.write("")

    # ------------------------------------------------------
    #   3) PROGRESS BAR & STATS
    # ------------------------------------------------------
    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1.0) if goal > 0 else 0

    st.markdown("### 📊 Progress")
    st.progress(progress)

    remaining = max(goal - total, 0)

    st.write(f"**Total intake so far:** {total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    st.write("")

    # ------------------------------------------------------
    #   4) MASCOT
    # ------------------------------------------------------
    if st.session_state.mascot_on:
        if progress == 0:
            st.info("Let's start hydrating! 🙂")
        elif progress < 0.5:
            st.info("Good start! Keep sipping 😃")
        elif progress < 0.75:
            st.success("Nice! You're halfway there 😎")
        elif progress < 1.0:
            st.success("Almost at your goal! 🤗")
        else:
            st.balloons()
            st.success("🎉 Congratulations! You hit your hydration goal! 🥳")

    st.write("")

    # ------------------------------------------------------
    #   5) RESET + SUMMARY
    # ------------------------------------------------------
    colA, colB = st.columns(2)
    with colA:
        st.button("New Day", on_click=reset_day)
    with colB:
        st.button("View Summary", on_click=view_summary)

    st.write("")

    # ------------------------------------------------------
    #   6) TIP OF THE DAY
    # ------------------------------------------------------
    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))

# ------------------------------------------------------
#                  END-OF-DAY SUMMARY PAGE
# ------------------------------------------------------

elif st.session_state.phase == 5:
    st.title("🌙 End-of-Day Summary")

    total = st.session_state.total
    cups = round(total / 240, 2) if total > 0 else 0
    goal = st.session_state.goal
    progress = min(total / goal, 1.0) if goal > 0 else 0

    st.subheader("Total Intake")
    st.write(f"💧 {total} ml  ({cups} cups)")

    st.subheader("Progress Percentage")
    st.write(f"{progress * 100:.1f}% of {goal} ml")

    st.subheader("Status")
    if total >= goal:
        st.success("Goal Achieved! 🌟")
    else:
        st.info("Keep Trying! 💪")

    st.markdown("## 🐢 Great effort today!")

    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Start New Day", on_click=start_new_day)
    with col2:
        st.button("Back to Dashboard", on_click=back_to_dashboard)
