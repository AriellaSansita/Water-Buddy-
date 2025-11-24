import streamlit as st
import random
import time

# ------------ CONSTANTS ------------
IMAGE_PATH = "/mnt/data/Screenshot 2025-11-24 at 9.17.29 AM.png"   # REQUIRED by system
CUP_ML = 240

AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

# ------------ SESSION DEFAULTS ------------
defaults = {
    "phase": "welcome",
    "age": None,
    "standard_goal": 0,
    "goal": 0,
    "total": 0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ------------ TURTLE MASCOT ------------
def turtle_mascot(progress):
    if progress >= 1:
        return "🐢✨", "Awesome job! You did it!"
    elif progress >= 0.75:
        return "🐢👏", "So close! You're amazing!"
    elif progress >= 0.5:
        return "🐢😊", "Great progress! Keep swimming!"
    elif progress > 0:
        return "🐢👋", "Nice start! Let's keep going!"
    else:
        return "🐢💙", "Hey buddy! Ready to hydrate?"


# ------------ ASCII WATER ANIMATION ------------
def animate_water(progress):
    container = st.empty()
    levels = 10
    fill = int(progress * levels)

    for i in range(fill + 1):
        bottle = ["   _______  "]
        for lvl in range(levels, 0, -1):
            if lvl <= i:
                bottle.append("  | █████ |")
            else:
                bottle.append("  |       |")
        bottle.append("   ‾‾‾‾‾‾‾  ")

        container.markdown("```\n" + "\n".join(bottle) + "\n```")
        time.sleep(0.07)


# ------------ NAVIGATION ------------
def go(page):
    st.session_state.phase = page


# ------------ PAGE: WELCOME ------------
if st.session_state.phase == "welcome":
    st.title("Welcome to WaterBuddy 🐢")
    st.write("Your friendly daily hydration companion.")
    st.button("Start", on_click=lambda: go("age"))


# ------------ PAGE: AGE SELECTION ------------
elif st.session_state.phase == "age":
    st.header("Select your age group")
    for g, ml in AGE_GROUPS.items():
        if st.button(g):
            st.session_state.age = g
            st.session_state.standard_goal = ml
            st.session_state.goal = ml
            go("goal")


# ------------ PAGE: SET GOAL ------------
elif st.session_state.phase == "goal":
    st.header("Daily Water Goal")

    st.write(f"Recommended for **{st.session_state.age}**: **{st.session_state.standard_goal} ml**")

    st.session_state.goal = st.number_input(
        "Set your goal (ml):",
        value=st.session_state.standard_goal,
        min_value=500,
        step=100
    )

    st.button("Continue", on_click=lambda: go("dashboard"))


# ------------ PAGE: DASHBOARD ------------
elif st.session_state.phase == "dashboard":
    st.title("WaterBuddy Dashboard")
    st.image(IMAGE_PATH, width=200)

    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1) if goal else 0

    # Turtle mascot
    mascot, msg = turtle_mascot(progress)
    st.markdown(f"## {mascot}")
    st.write(msg)

    # Progress summary
    st.write(f"**Standard Goal:** {st.session_state.standard_goal} ml")
    st.write(f"**Your Goal:** {goal} ml")
    st.progress(progress)
    st.write(f"**Total intake:** {total} ml ({round(total / CUP_ML, 2)} cups)")
    st.write(f"**Remaining:** {max(goal - total, 0)} ml")

    # Quick Add Buttons
    st.subheader("Quick Add Water")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💧\n250 ml"):
            st.session_state.total += 250

    with col2:
        if st.button("🥛\n500 ml"):
            st.session_state.total += 500

    with col3:
        if st.button("🥤\n750 ml"):
            st.session_state.total += 750

    with col4:
        if st.button("🍶\n1 L"):
            st.session_state.total += 1000

    # Custom Add
    st.subheader("Custom Amount (ml)")
    custom = st.number_input("Enter amount:", min_value=0, step=50)
    if st.button("Add"):
        st.session_state.total += custom

    # Controls
    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("Animate Bottle"):
            animate_water(progress)

    with colB:
        if st.button("View Summary"):
            go("summary")

    with colC:
        if st.button("New Day"):
            st.session_state.total = 0


# ------------ PAGE: END-OF-DAY SUMMARY ------------
elif st.session_state.phase == "summary":
    st.title("End-of-Day Summary 🌙")

    total = st.session_state.total
    cups = round(total / CUP_ML, 2)
    goal = st.session_state.goal
    pct = int((total / goal) * 100) if goal else 0

    st.subheader("Total Intake")
    st.write(f"{total} ml  ({cups} cups)")

    st.subheader("Progress Percentage")
    st.write(f"{pct}% of {goal} ml")

    st.subheader("Status")
    if total >= goal:
        st.success("Goal Achieved! 🌟")
    else:
        st.info("Keep Trying! 💪")

    st.subheader("Animated Water Bottle")
    st.image(IMAGE_PATH, width=200)   # Using required path

    st.write("---")

    if st.button("Start New Day"):
        st.session_state.total = 0
        go("dashboard")

    if st.button("Back to Dashboard"):
        go("dashboard")


"""
import streamlit as st
import random

AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)  ": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years) ": 1800,
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
if "log_pref" not in st.session_state:
    st.session_state.log_pref = "quick"
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True

st.markdown("""
"""
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
"""
""", unsafe_allow_html=True)

def start_app():
    st.session_state.phase = 2

def select_age(group, ml):
    st.session_state.age_group = group
    st.session_state.goal = ml
    st.session_state.phase = 3

def continue_to_dashboard():
    st.session_state.phase = 4

def add_250():
    st.session_state.total += 250

def reset_day():
    st.session_state.total = 0

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
        value=AGE_GROUPS[st.session_state.age_group],
        step=100
    )
    st.button("Continue", on_click=continue_to_dashboard)

elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")
    st.write(f"**Age group:** {st.session_state.age_group}")
    st.write(f"**Daily goal:** {st.session_state.goal} ml")

    col1, col2 = st.columns(2)
    with col1:
        st.button("+250 ml", on_click=add_250)
    with col2:
        with st.form("custom_water"):
            manual_amount = st.number_input("Log custom amount (ml):", min_value=0, step=50)
            submitted = st.form_submit_button("Add custom amount")
            if submitted:
                st.session_state.total += manual_amount

    st.button("New Day (Reset)", on_click=reset_day)

    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

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

    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))
"""
