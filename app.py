import streamlit as st
import random
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- AGE + TIPS ----------------
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

# ---------------- SESSION STATE ----------------
if "phase" not in st.session_state: st.session_state.phase = 1
if "age_group" not in st.session_state: st.session_state.age_group = None
if "goal" not in st.session_state: st.session_state.goal = 0
if "standard_goal" not in st.session_state: st.session_state.standard_goal = 0
if "total" not in st.session_state: st.session_state.total = 0
if "history" not in st.session_state: st.session_state.history = []
if "confirm_reset" not in st.session_state: st.session_state.confirm_reset = False

# ---------------- UTILITY FUNCTIONS ----------------
def calculate_progress(total, goal):
    return min(total / goal, 1.0) if goal else 0.0

def add_water(amount):
    try:
        amt = int(amount)
    except:
        amt = 0
    if amt <= 0:
        return
    st.session_state.total += amt
    now = datetime.now().strftime("%H:%M:%S")
    cumulative = st.session_state.total
    st.session_state.history.append((now, amt, cumulative))

def get_remaining(goal, total):
    return max(goal - total, 0)

def get_message(progress):
    if progress == 0:
        return "Let's start hydrating! 🙂"
    elif progress < 0.5:
        return "Good start! Keep going 😄"
    elif progress < 0.75:
        return "Nice progress! 😎"
    elif progress < 1:
        return "Almost there! 🤗"
    else:
        return "Goal achieved! 🎉"

def get_mascot(progress):
    if progress == 0:
        return "🙂"
    elif progress < 0.5:
        return "😄"
    elif progress < 0.75:
        return "😎"
    elif progress < 1:
        return "🤗"
    else:
        return "🎉"

# ---------------- NAVIGATION ----------------
def start_app(): st.session_state.phase = 2

def select_age(group, ml):
    st.session_state.age_group = group
    st.session_state.standard_goal = ml
    st.session_state.goal = ml
    st.session_state.phase = 3

def continue_to_dashboard(): st.session_state.phase = 4

def reset_day():
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.confirm_reset = False

def view_summary(): st.session_state.phase = 5

def start_new_day():
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.phase = 4

def back_to_dashboard(): st.session_state.phase = 4

# ---------------- PHASES ----------------
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
    st.write(f"Recommended (standard) goal: {AGE_GROUPS[st.session_state.age_group]} ml")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=int(st.session_state.goal),
        step=100
    )
    st.button("Continue", on_click=continue_to_dashboard)

elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")

    st.write(f"### Age group: {st.session_state.age_group}")
    st.write(f"Standard goal: **{st.session_state.standard_goal} ml**")
    st.write(f"Your goal: **{st.session_state.goal} ml**")

    # QUICK ADD
    st.write("## 💧 Quick Add")
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        if st.button("+250 ml"): add_water(250)
    with col2: 
        if st.button("+500 ml"): add_water(500)
    with col3: 
        if st.button("+750 ml"): add_water(750)
    with col4: 
        if st.button("+1000 ml"): add_water(1000)

    # CUSTOM ADD
    st.write("### ✏️ Add custom amount")
    custom = st.number_input("Enter amount (ml):", min_value=0, step=50, value=0)
    if st.button("Add"):
        add_water(custom)

    # PROGRESS + MASCOT
    st.write("### 📊 Progress")
    total = st.session_state.total
    goal = st.session_state.goal
    progress = calculate_progress(total, goal)
    remaining = get_remaining(goal, total)

    st.progress(progress)
    st.write(f"**{total} ml consumed** — Remaining: {remaining} ml")
    st.info(f"{get_mascot(progress)} {get_message(progress)}")

    # TIP
    st.write("---")
    st.write("💡 Tip of the day:")
    st.write(random.choice(HYDRATION_TIPS))

    # HISTORY / LOG
    st.write("### ⏱ Today's Log")
    if st.session_state.history:
        for t, amt, cum in st.session_state.history[-8:]:
            st.write(f"{t} — +{amt} ml — total: {cum} ml")
    else:
        st.write("No Data History / Log")

    # RESET WITH CONFIRMATION
    colA, colB = st.columns(2)
    with colA:
        if st.button("New Day"):
            st.session_state.confirm_reset = True

        if st.session_state.confirm_reset:
            if st.checkbox("Confirm reset"):
                reset_day()

    with colB:
        st.button("View Summary", on_click=view_summary)

elif st.session_state.phase == 5:
    st.title("🌙 End-of-Day Summary")

    total = st.session_state.total
    goal = st.session_state.goal
    progress = calculate_progress(total, goal)

    st.write(f"Total intake: **{total} ml**")
    st.write(f"Progress: **{progress*100:.1f}%**")

    if total >= goal:
        st.success("Goal Achieved! 🌟")
    else:
        st.info("Keep Trying! 💪")

    st.markdown("### 📈 Today's Intake Chart")

    if st.session_state.history:
        times = [h[0] for h in st.session_state.history]
        cumul = [h[2] for h in st.session_state.history]

        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(times, cumul, marker='o')
        ax.axhline(goal, linestyle='--', label='Your Goal')
        ax.set_xlabel("Time")
        ax.set_ylabel("Cumulative intake (ml)")
        ax.set_title("Today's intake progression")
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No Data Visualization (Chart / Graph)")

    col1, col2 = st.columns(2)
    with col1: st.button("Start New Day", on_click=start_new_day)
    with col2: st.button("Back to Dashboard", on_click=back_to_dashboard)
