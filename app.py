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
if "total" not in st.session_state: st.session_state.total = 0
if "custom_amount" not in st.session_state: st.session_state.custom_amount = 0
if "history" not in st.session_state: st.session_state.history = []   # NEW


# ---------------- FUNCTIONS ----------------
def calculate_progress(total, goal):
    if goal == 0:
        return 0.0
    return min(total / goal, 1.0)


def add_water(amount):
    try:
        amt = int(amount)
    except:
        amt = 0
    
    if amt > 0:
        st.session_state.total += amt

        # Add to history
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.append((now, amt, st.session_state.total))


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


# ---------------- UI CSS ----------------
st.markdown("""
    <style>
    .bottle {
        width: 120px;
        height: 220px;
        border-radius: 15px;
        border: 4px solid rgba(255,255,255,0.4);
        overflow: hidden;
        position: relative;
        background: rgba(255,255,255,0.15);
    }
    .bottle-inner {
        width: 100%;
        position: absolute;
        bottom: 0;
        background: linear-gradient(180deg, #60A5FA, #4FD1C5);
        transition: height 0.6s ease;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------
def start_app(): st.session_state.phase = 2
def select_age(group, ml):
    st.session_state.age_group = group
    st.session_state.goal = ml
    st.session_state.phase = 3
def continue_to_dashboard(): st.session_state.phase = 4
def reset_day(): 
    st.session_state.total = 0
    st.session_state.history = []
def view_summary(): st.session_state.phase = 5
def start_new_day():
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.phase = 4
def back_to_dashboard(): st.session_state.phase = 4


# ---------------- SCREENS ----------------

# PHASE 1
if st.session_state.phase == 1:
    st.title("Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    st.button("Let's begin", on_click=start_app)


# PHASE 2 — SELECT AGE
elif st.session_state.phase == 2:
    st.header("Select your age group")
    for group, ml in AGE_GROUPS.items():
        st.button(group, on_click=select_age, args=(group, ml))


# PHASE 3 — ADJUST GOAL
elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")
    st.write(f"Recommended goal: {AGE_GROUPS[st.session_state.age_group]} ml")

    st.session_state.goal = st.number_input(
        "Daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=int(st.session_state.goal),
        step=100
    )

    st.button("Continue", on_click=continue_to_dashboard)


# PHASE 4 — DASHBOARD
elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")
    st.write(f"### Age group: {st.session_state.age_group}")
    st.write(f"### Daily goal: **{st.session_state.goal} ml**")

    # QUICK ADD
    st.write("## 💧 Quick Add")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("+250 ml"): add_water(250)
    if col2.button("+500 ml"): add_water(500)
    if col3.button("+750 ml"): add_water(750)
    if col4.button("+1000 ml"): add_water(1000)

    # CUSTOM ADD
    st.write("### ✏️ Add custom amount")
    custom = st.number_input("Enter amount (ml):", min_value=0, step=50, value=0)
    if st.button("Add"):
        add_water(custom)

    # PROGRESS + BOTTLE
    st.write("### 📊 Progress")
    total = st.session_state.total
    goal = st.session_state.goal
    progress = calculate_progress(total, goal)
    fill = int(progress * 100)

    bottle_html = f"""
    <div style="display:flex; align-items:center; gap:20px;">
        <div class="bottle">
            <div class="bottle-inner" style="height:{fill}%"></div>
        </div>
        <div style="font-size:20px; font-weight:600;">
            {progress*100:.1f}% complete<br>
            {total} ml consumed
        </div>
    </div>
    """
    st.markdown(bottle_html, unsafe_allow_html=True)

    # Remaining
    st.write(f"Remaining: **{goal - total if goal > total else 0} ml**")

    # MESSAGES
    msg = get_message(progress)
    if progress >= 1:
        st.balloons()
    st.info(msg)

    # MASCOT — IMPROVED UI
    st.write("### 🐢 Mascot Reaction")
    mascot = get_mascot(progress)
    st.markdown(
        f"<div style='font-size:80px; text-align:center; margin-top:-20px;'>{mascot}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:18px; text-align:center; margin-top:-10px;'>{msg}</div>",
        unsafe_allow_html=True
    )

    # TIP
    st.write("---")
    st.write("💡 Tip of the day:")
    st.write(random.choice(HYDRATION_TIPS))

    # HISTORY (NEW)
    st.write("### 📜 Today's Log")
    if st.session_state.history:
        for t, amt, cum in st.session_state.history[-10:]:
            st.write(f"{t} — +{amt} ml (total: {cum} ml)")
    else:
        st.write("No entries yet.")

    # BUTTONS
    colA, colB = st.columns(2)
    colA.button("New Day", on_click=reset_day)
    colB.button("View Summary", on_click=view_summary)


# PHASE 5 — SUMMARY PAGE
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

    # CHART (NEW)
    st.write("### 📈 Intake Progress Chart")

    if st.session_state.history:
        times = [t for (t, amt, cum) in st.session_state.history]
        cumul = [cum for (t, amt, cum) in st.session_state.history]

        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(times, cumul, marker='o')
        ax.set_xlabel("Time")
        ax.set_ylabel("Total (ml)")
        ax.set_title("Today's Water Intake")
        plt.xticks(rotation=30)
        st.pyplot(fig)
    else:
        st.write("No data to show.")

    st.button("Start New Day", on_click=start_new_day)
    st.button("Back to Dashboard", on_click=back_to_dashboard)
