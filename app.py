import streamlit as st
import random

# --------------------------
# AGE GROUPS & TIPS
# --------------------------

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
    "Set small goals—like one cup each hour.",
    "Hydrate after exercise to recover faster!"
]

# --------------------------
# SESSION STATE
# --------------------------

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

# --------------------------
# GLOBAL STYLING
# --------------------------

st.markdown("""
    <style>
    .stButton>button {
        background-color: #60A5FA;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# FUNCTIONS
# --------------------------

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


# --------------------------
# SIDE BAR SETTINGS
# --------------------------

st.sidebar.header("⚙️ Settings")
st.sidebar.toggle("Show Tips", key="show_tips")
st.sidebar.toggle("Show Mascot", key="mascot_on")


# --------------------------
# APP SCREENS
# --------------------------

# ----------- PHASE 1: WELCOME SCREEN -----------
if st.session_state.phase == 1:
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    st.button("Let's begin", on_click=start_app)

# ----------- PHASE 2: SELECT AGE GROUP -----------
elif st.session_state.phase == 2:
    st.header("Select your age group")
    for group, ml in AGE_GROUPS.items():
        st.button(group, on_click=select_age, args=(group, ml))

# ----------- PHASE 3: ADJUST GOAL -----------
elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")

    st.write(f"Recommended goal for **{st.session_state.age_group}**: "
             f"**{AGE_GROUPS[st.session_state.age_group]} ml**")

    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=AGE_GROUPS[st.session_state.age_group],
        step=100
    )
    st.button("Continue", on_click=continue_to_dashboard)

# ----------- PHASE 4: DASHBOARD -----------
elif st.session_state.phase == 4:
    st.title("📊 WaterBuddy Dashboard")

    # MASCOT
    if st.session_state.mascot_on:
        st.markdown("## 🐬 Your Hydration Buddy")

    st.write(f"**Age group:** {st.session_state.age_group}")
    st.write(f"**Your adjusted goal:** {st.session_state.goal} ml")
    st.write(f"**Standard recommended goal:** {AGE_GROUPS[st.session_state.age_group]} ml")

    # --------------- LOGGING INTAKE ---------------
    col1, col2 = st.columns(2)
    with col1:
        st.button("+250 ml", on_click=add_250)
    with col2:
        with st.form("custom_water"):
            manual = st.number_input("Log custom amount (ml):", min_value=0, step=50)
            submitted = st.form_submit_button("Add")
            if submitted:
                st.session_state.total += manual

    st.button("New Day (Reset)", on_click=reset_day)

    # --------------- CALCULATIONS ---------------
    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    # --------------- MASCOT / MESSAGES ---------------
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
            st.success(f"You drank **{st.session_state.total} ml** today!")

    # --------------- DAILY TIP ---------------
    if st.session_state.show_tips:
        st.write("---")
        if st.button("💡 Show me a hydration tip"):
            st.info(random.choice(HYDRATION_TIPS))

    # --------------- UNIT CONVERTER ---------------
    st.write("---")
    with st.expander("🔄 Unit Converter (cups ↔ ml)"):
        cups = st.number_input("Enter cups:", min_value=0.0, step=0.5)
        st.write(f"{cups} cups = **{cups * 240} ml**")

