# app.py - WaterBuddy (final FA-2 version)
# NOTE: developer requested this exact path be included as the mascot image.
MASCOT_IMG_PATH = "/mnt/data/Screenshot 2025-11-24 at 9.17.29 AM.png"

import streamlit as st
import time
import random

# -------------------------
# Constants
# -------------------------
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

# -------------------------
# Session state defaults
# -------------------------
defaults = {
    "page": "welcome",   # welcome, age, goal, dashboard, summary
    "age_group": None,
    "standard_goal": 0,
    "goal": 0,
    "total": 0,
    "log_unit": "ml",    # "ml" or "cups"
    "show_tips": True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------------
# Styling (simple)
# -------------------------
st.set_page_config(page_title="WaterBuddy", layout="centered")

st.markdown(
    """
    <style>
    .page-title {text-align: center; font-size:32px; font-weight:700; margin-bottom:4px;}
    .card {background: rgba(255,255,255,0.06); border-radius:12px; padding:12px; box-shadow:0 4px 12px rgba(0,0,0,0.06);}
    .small {font-size:14px; color:#DBEAFE; margin-bottom:8px;}
    .btn-grid > div {display:inline-block; margin:6px;}
    .emoji-btn {font-size:15px; padding:10px 14px; border-radius:10px; border:none;}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Helper functions
# -------------------------
def go(page):
    st.session_state.page = page

def set_age(group):
    st.session_state.age_group = group
    st.session_state.standard_goal = AGE_GROUPS[group]
    st.session_state.goal = AGE_GROUPS[group]
    go("goal")

def add_ml(amount_ml):
    st.session_state.total += int(amount_ml)

def reset_day_and_go_dashboard():
    st.session_state.total = 0
    go("dashboard")

def compute_progress():
    if st.session_state.goal <= 0:
        return 0.0
    return min(st.session_state.total / st.session_state.goal, 1.0)

# Turtle mascot mapping (from user's JS)
def turtle_mascot(progress_frac):
    # progress_frac in 0..1
    if progress_frac >= 1.0:
        return "🐢✨", "Awesome job! You did it!"
    elif progress_frac >= 0.75:
        return "🐢👏", "So close! You're amazing!"
    elif progress_frac >= 0.5:
        return "🐢😊", "Great progress! Keep swimming!"
    elif progress_frac > 0:
        return "🐢👋", "Nice start! Let's keep going!"
    else:
        return "🐢💙", "Hey buddy! Ready to hydrate?"

# Simple ASCII water bottle animation
def animate_bottle(progress_frac, speed=0.06):
    levels = 10
    filled = int(round(progress_frac * levels))
    container = st.empty()
    # animate incremental fill from 0 to filled
    for lvl in range(filled + 1):
        lines = ["   _______  "]
        for i in range(levels, 0, -1):
            if i <= lvl:
                lines.append("  | █████ |")
            else:
                lines.append("  |       |")
        lines.append("   ‾‾‾‾‾‾‾  ")
        container.markdown("```\n" + "\n".join(lines) + "\n```")
        time.sleep(speed)
    # final hold
    time.sleep(0.12)

# -------------------------
# Pages
# -------------------------

# ------- WELCOME -------
if st.session_state.page == "welcome":
    st.markdown('<div class="page-title">WaterBuddy 🐢</div>', unsafe_allow_html=True)
    st.markdown("<div class='small'>Your friendly daily hydration companion — simple, fast, friendly.</div>", unsafe_allow_html=True)
    st.image(MASCOT_IMG_PATH, width=220)  # using user-provided path as required
    st.write("")
    if st.button("Get started"):
        go("age")

# ------- AGE SELECTION -------
elif st.session_state.page == "age":
    st.header("Select your age group")
    cols = st.columns(2)
    i = 0
    for group in AGE_GROUPS.keys():
        with cols[i % 2]:
            if st.button(group):
                set_age(group)
        i += 1
    st.write("")
    if st.button("Back"):
        go("welcome")

# ------- ADJUST GOAL -------
elif st.session_state.page == "goal":
    st.header("Set your daily goal")
    st.write(f"Recommended for **{st.session_state.age_group}**: **{st.session_state.standard_goal} ml**")
    st.session_state.goal = st.number_input("Adjust your daily water goal (ml)", min_value=500, max_value=10000, step=100, value=st.session_state.standard_goal)
    st.write("")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Continue to Dashboard"):
            go("dashboard")
    with col2:
        if st.button("Back"):
            go("age")

# ------- DASHBOARD -------
elif st.session_state.page == "dashboard":
    st.title("WaterBuddy Dashboard")
    # top cards row
    card1, card2 = st.columns([1.6, 1])
    with card1:
        st.markdown("### Progress")
        progress = compute_progress()
        st.progress(progress)
        st.write(f"**Total:** {st.session_state.total} ml  ({round(st.session_state.total / CUP_ML, 2)} cups)")
        st.write(f"**Remaining:** {max(st.session_state.goal - st.session_state.total, 0)} ml")
    with card2:
        st.markdown("### Goal")
        st.write(f"**Standard:** {st.session_state.standard_goal} ml")
        st.write(f"**Your goal:** {st.session_state.goal} ml")
        st.write("")
        st.markdown("### Mascot")
        mascot_emoji, mascot_msg = turtle_mascot(progress)
        # show the uploaded image then emoji message (image may fail if path invalid on remote)
        try:
            st.image(MASCOT_IMG_PATH, width=150)
        except Exception:
            st.markdown(mascot_emoji, unsafe_allow_html=True)
        st.write(mascot_msg)

    st.write("---")

    # Two-column main area: left = quick-add, right = logging controls
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Quick Add Water")
        # show in a clean grid
        qa_cols = st.columns(4)
        for i, amt in enumerate(QUICK_AMOUNTS):
            label = {250: "💧 250 ml", 500: "🥛 500 ml", 750: "🥤 750 ml", 1000: "🍶 1 L"}[amt]
            display = f"{round(amt / CUP_ML, 2)} cups" if st.session_state.log_unit == "cups" else f"{amt} ml"
            if qa_cols[i].button(f"{label}\n({display})"):
                add_ml(amt)
        st.write("")
        st.markdown("**Tip:** Use quick-add buttons for fast logging.")
        if st.button("Animate bottle (show current fill)"):
            animate_bottle(progress)

    with right:
        st.subheader("Custom Log")
        st.write("Choose logging unit (this switch affects the custom input display only):")
        st.session_state.log_unit = st.radio("", ["ml", "cups"], index=0 if st.session_state.log_unit == "ml" else 1, horizontal=True)
        if st.session_state.log_unit == "ml":
            custom_ml = st.number_input("Enter amount (ml)", min_value=0, step=50, value=250, key="custom_ml")
            if st.button("Add custom (ml)"):
                add_ml(custom_ml)
        else:
            custom_cups = st.number_input("Enter amount (cups)", min_value=0.0, step=0.25, value=1.0, format="%.2f", key="custom_cups")
            if st.button("Add custom (cups)"):
                add_ml(int(round(custom_cups * CUP_ML)))

        st.write("---")
        st.subheader("Extras")
        if st.button("View End-of-Day Summary"):
            go("summary")
        if st.button("Start new day (reset)"):
            reset_day_and_go_dashboard()

    st.write("---")

    # small tip area
    if st.session_state.show_tips:
        if st.button("Show hydration tip"):
            st.info(random.choice(HYDRATION_TIPS))

# ------- SUMMARY -------
elif st.session_state.page == "summary":
    st.title("End-of-Day Summary")
    st.markdown("**Great Effort!** Keep up the good work tomorrow! 🌟")
    total = st.session_state.total
    cups = round(total / CUP_ML, 2)
    standard = st.session_state.standard_goal
    pct = int(round((total / st.session_state.goal) * 100)) if st.session_state.goal else 0

    st.markdown("### Total Intake")
    st.write(f"{total} ml ({cups} cups)")

    st.markdown("### Goal Progress")
    st.write(f"{pct}% of {standard} ml")

    st.markdown("### Status")
    if total >= st.session_state.goal:
        st.success("Goal Achieved! 🌟")
    else:
        st.info("Goal Not Achieved — you came close, keep going tomorrow!")

    st.write("")
    # separate animate preview for summary
    if st.button("Animate summary bottle"):
        animate_bottle(compute_progress())

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Dashboard"):
            go("dashboard")
    with col2:
        if st.button("Start New Day and Return"):
            st.session_state.total = 0
            go("dashboard")

# End of file


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
