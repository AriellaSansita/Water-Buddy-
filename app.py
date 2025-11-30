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

# ---------------- SESSION STATE ----------------
if "phase" not in st.session_state: st.session_state.phase = 1
if "age_group" not in st.session_state: st.session_state.age_group = None
if "goal" not in st.session_state: st.session_state.goal = 0
if "total" not in st.session_state: st.session_state.total = 0
if "custom_amount" not in st.session_state: st.session_state.custom_amount = 0
if "show_tips" not in st.session_state: st.session_state.show_tips = True


# ---------------- SIMPLE CSS + BOTTLE ----------------
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


# ---------------- PHASE 1 ----------------
if st.session_state.phase == 1:
    st.title("Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    st.button("Let's begin", on_click=start_app)


# ---------------- PHASE 2 — AGE ----------------
elif st.session_state.phase == 2:
    st.header("Select your age group")
    for group, ml in AGE_GROUPS.items():
        st.button(group, on_click=select_age, args=(group, ml))


# ---------------- PHASE 3 — GOAL ----------------
elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")
    st.write(f"Recommended goal: {AGE_GROUPS[st.session_state.age_group]} ml")
    
    st.session_state.goal = st.number_input(
        "Daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=st.session_state.goal,
        step=100
    )
    
    st.button("Continue", on_click=continue_to_dashboard)


# ---------------- PHASE 4 — DASHBOARD ----------------
elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")
    st.write(f"### Age group: {st.session_state.age_group}")
    st.write(f"### Daily goal: **{st.session_state.goal} ml**")

    # QUICK ADD
    st.write("## 💧 Quick Add")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("+250 ml"): st.session_state.total += 250
    with col2:
        if st.button("+500 ml"): st.session_state.total += 500
    with col3:
        if st.button("+750 ml"): st.session_state.total += 750
    with col4:
        if st.button("+1000 ml"): st.session_state.total += 1000

    # CUSTOM ADD
    st.write("### ✏️ Add custom amount")
    custom = st.number_input("Enter amount (ml):", min_value=0, step=50, value=0)
    if st.button("Add"):
        st.session_state.total += custom

    # ---------------- 📊 PROGRESS + BOTTLE (ADDED) ----------------
    st.write("### 📊 Progress")

    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1.0)

    # Bottle HTML
    bottle_html = f"""
    <div style="display:flex; align-items:center; gap:20px;">
        <div class="bottle">
            <div class="bottle-inner" style="height:{progress*100}%"></div>
        </div>
        <div style="font-size:20px; font-weight:600;">
            {progress*100:.1f}% complete<br>
            {total} ml consumed
        </div>
    </div>
    """
    st.markdown(bottle_html, unsafe_allow_html=True)

    st.write(f"Remaining: **{goal - total} ml**")

    # Mascot
    if progress == 0:
        st.info("Let's start hydrating! 🙂")
    elif progress < 0.5:
        st.info("Good start! Keep going 😄")
    elif progress < 0.75:
        st.success("Nice progress! 😎")
    elif progress < 1:
        st.success("Almost there! 🤗")
    else:
        st.balloons()
        st.success("Goal achieved! 🎉")

    # TIP OF DAY
    st.write("---")
    st.write("💡 Tip of the day:")
    st.write(random.choice(HYDRATION_TIPS))

    # Buttons
    colA, colB = st.columns(2)
    with colA: st.button("New Day", on_click=reset_day)
    with colB: st.button("View Summary", on_click=view_summary)


# ---------------- PHASE 5 — SUMMARY ----------------
elif st.session_state.phase == 5:
    st.title("🌙 End-of-Day Summary")

    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1)

    st.write(f"Total intake: **{total} ml**")
    st.write(f"Progress: **{progress*100:.1f}%**")

    if total >= goal:
        st.success("Goal Achieved! 🌟")
    else:
        st.info("Keep Trying! 💪")

    st.button("Start New Day", on_click=start_new_day)
    st.button("Back to Dashboard", on_click=back_to_dashboard)

