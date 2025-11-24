import streamlit as st
import random
import time

# ---------------------------------
# REQUIRED — Using your uploaded file
# ---------------------------------
MASCOT_IMG = "/mnt/data/Screenshot 2025-11-24 at 9.17.29 AM.png"

# ---------------------------------
# CONSTANTS
# ---------------------------------
AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

CUP_ML = 240

QUICK_AMOUNTS = [250, 500, 750, 1000]

HYDRATION_TIPS = [
    "Try drinking a glass of water before meals.",
    "Keep a bottle on your desk as a reminder.",
    "Start your morning with a glass of water.",
    "Set small goals: one cup every hour.",
    "Hydrate after exercise to recover faster."
]

# ---------------------------------
# SESSION STATE INIT
# ---------------------------------
defaults = {
    "phase": "welcome",
    "age": None,
    "standard_goal": 0,
    "goal": 0,
    "total": 0,
    "unit": "ml",
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------------------------
# TURTLE MASCOT LOGIC
# ---------------------------------
def turtle_expression(progress):
    if progress >= 1:
        return "🐢✨", "Awesome job! You did it!"
    elif progress >= 0.75:
        return "🐢👏", "So close! You're amazing!"
    elif progress >= 0.50:
        return "🐢😊", "Great progress! Keep swimming!"
    elif progress > 0:
        return "🐢👋", "Nice start! Let's keep going!"
    else:
        return "🐢💙", "Hey buddy! Ready to hydrate?"

# ---------------------------------
# ASCII WATER ANIMATION
# ---------------------------------
def animate_water(progress):
    container = st.empty()
    levels = 10
    filled = int(progress * levels)

    for i in range(filled + 1):
        bottle = ["   _______  "]
        for level in range(levels, 0, -1):
            if level <= i:
                bottle.append("  | █████ |")
            else:
                bottle.append("  |       |")
        bottle.append("   ‾‾‾‾‾‾‾  ")

        container.markdown("```\n" + "\n".join(bottle) + "\n```")
        time.sleep(0.07)

# ---------------------------------
# NAVIGATION
# ---------------------------------
def go(page):
    st.session_state.phase = page

# ---------------------------------
# PAGE: WELCOME
# ---------------------------------
if st.session_state.phase == "welcome":
    st.title("Welcome to WaterBuddy 🐢")
    st.write("Your friendly daily hydration companion.")
    st.button("Start", on_click=lambda: go("age"))

# ---------------------------------
# PAGE: AGE SELECTION
# ---------------------------------
elif st.session_state.phase == "age":
    st.header("Select your age group")
    for group, ml in AGE_GROUPS.items():
        if st.button(group):
            st.session_state.age = group
            st.session_state.standard_goal = ml
            st.session_state.goal = ml
            go("goal")

# ---------------------------------
# PAGE: ADJUST GOAL
# ---------------------------------
elif st.session_state.phase == "goal":
    st.header("Daily Water Goal")
    st.write(f"Recommended for **{st.session_state.age}**: **{st.session_state.standard_goal} ml**")

    st.session_state.goal = st.number_input(
        "Set your goal",
        value=st.session_state.standard_goal,
        min_value=500,
        step=100,
    )

    st.button("Continue", on_click=lambda: go("dashboard"))

# ---------------------------------
# PAGE: DASHBOARD
# ---------------------------------
elif st.session_state.phase == "dashboard":

    st.title("WaterBuddy Dashboard")

    # Mascot image from user-uploaded file
    st.image(MASCOT_IMG, width=200)

    # Progress calculations
    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1) if goal > 0 else 0

    # Mascot reaction
    mascot, message = turtle_expression(progress)
    st.markdown(f"## {mascot}")
    st.write(message)

    # Standard vs Adjusted Goal
    st.write(f"**Standard Goal:** {st.session_state.standard_goal} ml")
    st.write(f"**Your Goal:** {goal} ml")

    st.progress(progress)
    st.write(f"**Total intake:** {total} ml ({round(total / CUP_ML, 2)} cups)")
    st.write(f"**Remaining:** {max(goal - total, 0)} ml")

    # Unit Toggle
    st.subheader("Logging Unit")
    st.session_state.unit = st.radio("Choose unit:", ["ml", "cups"], horizontal=True)

    # QUICK ADD
    st.subheader("Quick Add Water")

    labels = ["💧 250ml", "🥛 500ml", "🥤 750ml", "🍶 1L"]

    cols = st.columns(4)
    for i, (col, amt, label) in enumerate(zip(cols, QUICK_AMOUNTS, labels)):
        with col:
            display_amt = f"{round(amt / CUP_ML, 2)} cups" if st.session_state.unit == "cups" else f"{amt} ml"
            if st.button(f"{label}\n({display_amt})"):
                st.session_state.total += amt

    # CUSTOM ADD
    st.subheader("Custom Amount")

    if st.session_state.unit == "ml":
        n = st.number_input("Enter ml:", value=250, step=50)
        if st.button("Add"):
            st.session_state.total += int(n)
    else:
        c = st.number_input("Enter cups:", value=1.0, step=0.25)
        if st.button("Add"):
            st.session_state.total += int(c * CUP_ML)

    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Animate Bottle"):
            animate_water(progress)

    with col2:
        if st.button("View Summary"):
            go("summary")

    with col3:
        if st.button("New Day"):
            st.session_state.total = 0

# ---------------------------------
# PAGE: END-OF-DAY SUMMARY
# ---------------------------------
elif st.session_state.phase == "summary":
    st.title("End of Day Summary 🌙")

    total = st.session_state.total
    goal = st.session_state.goal
    pct = int((total / goal) * 100) if goal else 0

    st.subheader("Great Effort!")
    st.write("Keep up the good work tomorrow! 🌟")

    st.write(f"**Total Intake:** {total} ml ({round(total / CUP_ML, 2)} cups)")
    st.write(f"**Goal Progress:** {pct}% of {goal} ml")

    if total >= goal:
        st.success("Goal Achieved! 🌟")
    else:
        st.info("Goal Not Achieved — tomorrow will be even better!")

    st.button("Back to Dashboard", on_click=lambda: go("dashboard"))
