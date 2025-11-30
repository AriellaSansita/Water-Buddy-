import streamlit as st
import random
from datetime import datetime
import math
import matplotlib.pyplot as plt

# -----------------------
# Constants / Defaults
# -----------------------
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

# -----------------------
# Session state defaults
# -----------------------
def init_state():
    defaults = {
        "phase": 1,
        "age_group": None,
        "goal": 0,
        "total": 0,
        "show_tips": True,
        "mascot_on": True,
        "custom_amount": 0,
        "history": [],  # list of (timestamp_str, added_amount, cumulative_total)
        "dark_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# -----------------------
# Styling
# -----------------------
def local_css(dark=False):
    # colors
    if dark:
        bg1 = "#0f172a"
        bg2 = "#0b1220"
        text = "#E6EEF8"
        accent = "#60A5FA"
    else:
        bg1 = "linear-gradient(to right, #4FD1C5, #60A5FA)"
        bg2 = "#ffffff"
        text = "#0f172a"
        accent = "#2563EB"

    st.markdown(f"""
    <style>
    :root {{
        --accent: {accent};
        --text: {text};
    }}
    .app-bg {{
        background: {bg1};
        padding: 18px;
        border-radius: 12px;
        color: var(--text);
    }}
    .stButton>button {{
        background-color: var(--accent);
        color: white;
        border-radius: 10px;
        font-size: 15px;
        padding: 8px 14px;
    }}
    .stButton>button:hover {{
        filter: brightness(0.9);
    }}
    /* water bottle */
    .bottle {{
        width: 120px;
        height: 220px;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        border: 4px solid rgba(255,255,255,0.25);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        margin: 10px;
    }}
    .bottle-inner {{
        position: absolute;
        bottom: 0;
        width: 100%;
        background: linear-gradient(180deg, rgba(96,165,250,0.95), rgba(79,209,197,0.95));
        transition: height 800ms ease;
    }}
    .mascot {{
        font-size: 40px;
        display: inline-block;
        margin-left: 12px;
        vertical-align: middle;
        animation: bob 2s infinite;
    }}
    @keyframes bob {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .small-muted {{ color: rgba(0,0,0,0.6); font-size: 13px; }}
    .stat-box {{ padding: 10px; border-radius: 8px; background: rgba(255,255,255,0.06); display:inline-block; margin:6px; }}
    </style>
    """, unsafe_allow_html=True)

local_css(st.session_state.dark_mode)

# -----------------------
# Helpers
# -----------------------
def start_app():
    st.session_state.phase = 2

def select_age(group):
    st.session_state.age_group = group
    st.session_state.goal = AGE_GROUPS[group]
    st.session_state.phase = 3

def continue_to_dashboard():
    st.session_state.phase = 4

def reset_day(confirm=False):
    if confirm:
        st.session_state.total = 0
        st.session_state.history = []
        st.session_state.custom_amount = 0
        # keep age & goal (teacher usually expects daily reset only, but we handle full reset separately)
        st.success("Day reset — totals cleared.")
    else:
        # show confirmation handled in UI
        pass

def full_reset(confirm=False):
    if confirm:
        st.session_state.total = 0
        st.session_state.history = []
        st.session_state.custom_amount = 0
        st.session_state.age_group = None
        st.session_state.goal = 0
        st.session_state.phase = 1
        st.success("All settings cleared. Start again!")
    else:
        pass

def view_summary():
    st.session_state.phase = 5

def start_new_day():
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.custom_amount = 0
    st.session_state.phase = 4

def back_to_dashboard():
    st.session_state.phase = 4

def add_water(amount):
    # ensure digit-by-digit correctness by using integers
    try:
        amt = int(amount)
    except Exception:
        amt = math.floor(amount)
    if amt <= 0:
        return
    st.session_state.total += amt
    now = datetime.now().strftime("%H:%M:%S")
    cumulative = st.session_state.total
    st.session_state.history.append((now, amt, cumulative))

def get_stable_daily_tip():
    # stable tip per day so refresh doesn't change it
    index = datetime.now().toordinal() % len(HYDRATION_TIPS)
    return HYDRATION_TIPS[index]

# -----------------------
# UI: PHASES
# -----------------------

if st.session_state.phase == 1:
    st.markdown("<div class='app-bg'>", unsafe_allow_html=True)
    st.title("Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion — redesigned for clarity, motivation, and privacy.")
    cols = st.columns([3,1])
    with cols[0]:
        st.write("We use age-based recommendations, quick logging buttons, and a playful mascot to keep you hydrated.")
        st.write("Start by selecting your age group.")
    with cols[1]:
        # dark mode toggle
        if st.checkbox("Dark mode", value=st.session_state.dark_mode):
            st.session_state.dark_mode = True
            local_css(True)
        else:
            st.session_state.dark_mode = False
            local_css(False)

    st.button("Let's begin", on_click=start_app)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.phase == 2:
    st.header("Select your age group")
    st.write("Choose an age group — we'll auto-suggest a daily goal you can adjust.")
    for group, ml in AGE_GROUPS.items():
        st.button(f"{group} — {ml} ml", on_click=select_age, args=(group,))

elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")
    st.write(f"Recommended goal for **{st.session_state.age_group}**: **{AGE_GROUPS[st.session_state.age_group]} ml**")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=st.session_state.goal if st.session_state.goal > 0 else AGE_GROUPS[st.session_state.age_group],
        step=100
    )
    cols = st.columns([2,1])
    with cols[0]:
        if st.button("Continue", on_click=continue_to_dashboard):
            pass
    with cols[1]:
        if st.button("Reset all and start over"):
            full_reset(confirm=True)

elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")
    st.markdown(f"**Age group:** {st.session_state.age_group}  &nbsp;&nbsp;  **Daily goal:** **{st.session_state.goal} ml**")
    st.write("")

    # QUICK ADD BUTTONS
    st.markdown("## 💧 Quick Add")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💧 +250 ml"):
            add_water(250)
    with col2:
        if st.button("🥛 +500 ml"):
            add_water(500)
    with col3:
        if st.button("🥤 +750 ml"):
            add_water(750)
    with col4:
        if st.button("🍶 +1 L"):
            add_water(1000)

    st.write("")
    # CUSTOM ADD with converter
    st.markdown("### ✏️ Add a custom amount")
    ccol1, ccol2 = st.columns([2,1])
    with ccol1:
        custom = st.number_input("Enter amount (ml):", min_value=0, step=50, value=st.session_state.custom_amount)
        st.session_state.custom_amount = custom
    with ccol2:
        if st.button("Add"):
            if custom <= 0:
                st.warning("Enter a positive amount.")
            else:
                add_water(custom)
                st.session_state.custom_amount = 0

    # Unit converter
    st.write("")
    conv_col1, conv_col2 = st.columns(2)
    with conv_col1:
        cups = st.number_input("Cups (1 cup = 240 ml):", min_value=0.0, step=0.5, value=0.0)
        if st.button("Convert cups → ml"):
            ml = int(round(cups * 240))
            st.session_state.custom_amount = ml
            st.success(f"Set custom amount to {ml} ml (from {cups} cups).")
    with conv_col2:
        ml_in = st.number_input("ml to convert:", min_value=0, step=50, value=0)
        if st.button("Convert ml → cups"):
            cups_res = round(ml_in / 240, 2) if ml_in > 0 else 0
            st.success(f"{ml_in} ml = {cups_res} cups.")

    st.write("")

    # PROGRESS CALC
    total = int(st.session_state.total)
    goal = int(st.session_state.goal) if st.session_state.goal > 0 else 0
    progress = (total / goal) if goal > 0 else 0.0
    progress = min(progress, 1.0)

    st.markdown("### 📊 Progress")
    # Animated bottle + mascot
    bottle_html = f"""
    <div style="display:flex; align-items:center;">
      <div class="bottle">
        <div class="bottle-inner" style="height: {progress*100}%"></div>
      </div>
      <div style="margin-left:18px;">
        <div style="font-size:20px; font-weight:700;">{int(progress*100)}%</div>
        <div class="small-muted">of your goal ({goal} ml)</div>
        <div style="margin-top:8px;">
    """
    # mascot selection
    if progress == 0:
        mascot = "🧊"  # chilly start
        msg = "Let's start hydrating!"
    elif progress < 0.5:
        mascot = "🙂"
        msg = "Good start! Keep sipping."
    elif progress < 0.75:
        mascot = "😄"
        msg = "Nice — you're making progress!"
    elif progress < 1.0:
        mascot = "🤗"
        msg = "Almost at your goal — finish strong!"
    else:
        mascot = "🎉"
        msg = "Goal achieved — fantastic!"
    bottle_html += f"""<span class="mascot">{mascot}</span> <div style="display:inline-block; margin-left:10px;">{msg}</div>"""
    bottle_html += "</div></div></div>"
    st.markdown(bottle_html, unsafe_allow_html=True)

    remaining = max(goal - total, 0)
    st.write("")
    st.write(f"**Total intake so far:** {total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    # Compare to standard recommended value for age group
    standard_goal = AGE_GROUPS.get(st.session_state.age_group, goal)
    percent_of_standard = min(total / standard_goal, 1.0) if standard_goal > 0 else 0.0
    st.write(f"**Compared to standard for your age ({standard_goal} ml):** {percent_of_standard*100:.1f}%")

    st.write("")
    # TIP OF THE DAY (stable)
    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(get_stable_daily_tip())

    st.write("")
    # Buttons: New Day (confirm), View Summary, Full Reset
    colA, colB, colC = st.columns([1,1,1])
    with colA:
        if st.button("New Day (clear totals)"):
            if st.confirm("Are you sure you want to clear today's totals?"):
                reset_day(confirm=True)
    with colB:
        if st.button("View Summary"):
            view_summary()
    with colC:
        if st.button("Reset All (age/goal too)"):
            if st.confirm("Reset all settings and start over?"):
                full_reset(confirm=True)

    st.write("")
    # show quick history
    st.markdown("### ⏱ Today's Log")
    if st.session_state.history:
        for t, amt, cumulative in st.session_state.history[-8:]:
            st.write(f"{t} — +{amt} ml — total: {cumulative} ml")
    else:
        st.write("No entries yet. Use the quick add buttons or custom add.")

elif st.session_state.phase == 5:
    st.title("🌙 End-of-Day Summary")
    total = int(st.session_state.total)
    goal = int(st.session_state.goal) if st.session_state.goal > 0 else 0
    progress = (total / goal) if goal > 0 else 0.0
    progress = min(progress, 1.0)
    cups = round(total / 240, 2) if total > 0 else 0

    st.subheader("Total Intake")
    st.write(f"💧 {total} ml  ({cups} cups)")

    st.subheader("Progress")
    st.write(f"{progress * 100:.1f}% of {goal} ml")

    st.subheader("Status")
    if total >= goal:
        st.success("Goal Achieved! 🌟 Great job!")
    else:
        st.info("Keep trying — you'll get there tomorrow! 💪")

    st.markdown("## 🧾 Summary Chart")
    # Build simple cumulative plot
    if st.session_state.history:
        times = [h[0] for h in st.session_state.history]
        cumul = [h[2] for h in st.session_state.history]

        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(times, cumul, marker='o')
        ax.axhline(goal, color='orange', linestyle='--', label='Your Goal')
        ax.set_xlabel("Time")
        ax.set_ylabel("Cumulative intake (ml)")
        ax.set_title("Today's intake progression")
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No logs today to chart.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start New Day"):
            start_new_day()
    with col2:
        if st.button("Back to Dashboard"):
            back_to_dashboard()
