import streamlit as st

CUP_ML = 240

AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

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


def go(page):
    st.session_state.phase = page


# ------------------- WELCOME -------------------
if st.session_state.phase == "welcome":
    st.title("Welcome to WaterBuddy 🐢")
    st.write("Your friendly daily hydration companion.")
    st.button("Start", on_click=lambda: go("age"))


# ------------------- AGE SELECT -------------------
elif st.session_state.phase == "age":
    st.header("Select your age group")
    for g, ml in AGE_GROUPS.items():
        if st.button(g):
            st.session_state.age = g
            st.session_state.standard_goal = ml
            st.session_state.goal = ml
            go("goal")


# ------------------- SET GOAL -------------------
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


# ------------------- DASHBOARD -------------------
elif st.session_state.phase == "dashboard":
    st.title("WaterBuddy Dashboard")

    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1) if goal else 0

    mascot, msg = turtle_mascot(progress)
    st.markdown(f"## {mascot}")
    st.write(msg)

    st.write(f"**Standard Goal:** {st.session_state.standard_goal} ml")
    st.write(f"**Your Goal:** {goal} ml")

    st.progress(progress)

    st.write(f"**Total intake:** {total} ml ({round(total / CUP_ML, 2)} cups)")
    st.write(f"**Remaining:** {max(goal - total, 0)} ml")

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

    st.subheader("Custom Amount (ml)")
    custom = st.number_input("Enter amount:", min_value=0, step=50)
    if st.button("Add"):
        st.session_state.total += custom

    colA, colB = st.columns(2)
    with colA:
        if st.button("View Summary"):
            go("summary")
    with colB:
        if st.button("New Day"):
            st.session_state.total = 0


# ------------------- SUMMARY PAGE -------------------
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

    st.markdown("## 🐢")

    st.write("---")

    if st.button("Start New Day"):
        st.session_state.total = 0
        go("dashboard")

    if st.button("Back to Dashboard"):
        go("dashboard")
