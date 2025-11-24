import streamlit as st
import random
from math import ceil

# ---------------------------
# Assets (local paths from your upload)
# ---------------------------
# Developer note: these paths come from your uploaded screenshots
ASSET_AGE_SELECT = "/mnt/data/Screenshot 2025-11-24 at 9.17.29 AM.png"
ASSET_GOAL_ADJUST = "/mnt/data/Screenshot 2025-11-24 at 9.46.47 AM.png"
ASSET_DASHBOARD = "/mnt/data/Screenshot 2025-11-24 at 9.16.55 AM.png"

# ---------------------------
# Config & constants
# ---------------------------
st.set_page_config(page_title="WaterBuddy — FA1", layout="centered", initial_sidebar_state="collapsed")

AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

CARD_COLORS = {
    "Children (4-8 years)": "#60A5FA",
    "Teens (9-13 years)": "#F472B6",
    "Adults (14-64 years)": "#2DD4BF",
    "Seniors (65+ years)": "#34D399",
}

HYDRATION_TIPS = [
    "Try drinking a glass of water before meals.",
    "Keep a bottle on your desk as a reminder.",
    "Start your morning with a glass of water.",
    "Set small goals: one cup every hour.",
    "Hydrate after exercise to recover faster."
]

# ---------------------------
# Session state defaults
# ---------------------------
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "manual_amount" not in st.session_state:
    st.session_state.manual_amount = 0
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True

# ---------------------------
# Styles to replicate screenshots
# ---------------------------
st.markdown(
    """
    <style>
    /* page background similar to your screenshots */
    .stApp {
        background: linear-gradient(180deg, #F0FBFD 0%, #F7FCFF 100%);
        min-height: 100vh;
        padding-top: 20px;
    }

    /* container card look */
    .wb-card {
        background: white;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 6px 18px rgba(12, 34, 63, 0.06);
        margin-bottom: 18px;
    }

    /* Age card style */
    .age-card {
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 18px;
        background: rgba(255,255,255,0.9);
        border: 3px solid #E6EEF9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .age-card .title { font-weight: 700; font-size: 18px; color: #0f172a; }
    .age-card .subtitle { color: #118ab2; margin-top: 10px; font-weight: 500; }

    /* Selected card */
    .age-card.selected {
        box-shadow: 0 8px 24px rgba(96,165,250,0.18);
        background: rgba(96,165,250,0.04);
    }

    /* Rounded big button (continue) */
    .big-btn {
        display: inline-block;
        background: linear-gradient(90deg,#2b9fd9,#1f6fb6);
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        text-decoration: none;
    }

    /* quick-add gradient tiles like in dashboard */
    .quick-tile {
        border-radius: 12px;
        padding: 22px;
        text-align: center;
        font-weight: 700;
        color: white;
        cursor: pointer;
        box-shadow: 0 8px 20px rgba(35,99,211,0.12);
        margin-bottom: 12px;
    }

    .tile-250 { background: linear-gradient(90deg,#2BC2D1,#3B82F6); }
    .tile-500 { background: linear-gradient(90deg,#2B9FD9,#2563EB); }
    .tile-750 { background: linear-gradient(90deg,#36D399,#06B6D4); }
    .tile-1000 { background: linear-gradient(90deg,#7C3AED,#4C1D95); }

    /* custom progress bar */
    .wb-progress {
        width: 100%;
        background: #F3F4F6;
        border-radius: 999px;
        height: 18px;
        overflow: hidden;
        margin: 16px 0;
    }
    .wb-progress > .bar {
        height: 100%;
        background: linear-gradient(90deg,#60A5FA,#2DD4BF);
        width: 0%;
        transition: width 0.5s ease;
    }

    /* footer buttons */
    .footer-row { display:flex; gap:16px; margin-top:20px; }
    .footer-left { background: white; border-radius: 12px; padding: 12px 18px; box-shadow: 0 4px 10px rgba(12,34,63,0.04); }
    .footer-right { background: linear-gradient(90deg,#2b9fd9,#1f6fb6); color: white; border-radius: 12px; padding: 12px 18px; font-weight:700; }

    /* small helpers */
    .muted { color: #475569; }
    .center { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Helper UI components
# ---------------------------
def age_card_html(name, ml, selected=False, color="#60A5FA"):
    border_style = f"border-color: {color};"
    sel_class = "selected" if selected else ""
    html = f"""
    <div class="age-card {sel_class}" style="{border_style}">
      <div>
        <div class="title">{name}</div>
        <div class="subtitle">Daily goal: {ml} ml / day</div>
      </div>
      <div style="min-width:64px">
        {'<div style="background:#2DD4BF;color:white;border-radius:999px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-weight:800;">✓</div>' if selected else ''}
      </div>
    </div>
    """
    return html

def render_progress_bar(progress_fraction):
    percent = int(progress_fraction * 100)
    html = f"""
    <div class="wb-progress">
      <div class="bar" style="width: {percent}%;"></div>
    </div>
    <div class="center"><strong>{percent}% Complete</strong></div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ---------------------------
# Phase 1: Welcome
# ---------------------------
if st.session_state.phase == 1:
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    st.image(ASSET_AGE_SELECT, width=420)  # small hero to match look
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; margin-top: 8px;'>Select Your Age Group</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<div class='center'><p style='font-size:18px; color:#0f172a'>Your friendly hydration companion</p></div>", unsafe_allow_html=True)

    start = st.button("Let's begin", key="start_btn_final")
    if start:
        st.session_state.phase = 2
        st.experimental_rerun()

# ---------------------------
# Phase 2: Age selection
# ---------------------------
elif st.session_state.phase == 2:
    st.markdown("<h2 style='margin-bottom:8px;'>Select Your Age Group</h2>", unsafe_allow_html=True)
    # render cards as HTML (keeps borders/colors)
    for group, ml in AGE_GROUPS.items():
        selected = (st.session_state.age_group == group)
        card_html = age_card_html(group, ml, selected=selected, color=CARD_COLORS[group])
        st.markdown(card_html, unsafe_allow_html=True)
        # provide hidden button overlay for click
        if st.button(f"select__{group}", key=f"select_{group}"):
            st.session_state.age_group = group
            st.session_state.goal = ml
            st.session_state.phase = 3
            st.experimental_rerun()

    st.write("")  # spacing
    st.markdown("<div class='muted'>Tip: you can customize the recommended goal next.</div>", unsafe_allow_html=True)
    if st.button("Back to welcome", key="age_back"):
        st.session_state.phase = 1
        st.experimental_rerun()

# ---------------------------
# Phase 3: Confirm / adjust goal
# ---------------------------
elif st.session_state.phase == 3:
    st.markdown("<h2>Confirm or adjust your daily goal</h2>", unsafe_allow_html=True)
    st.markdown("<div class='wb-card'>", unsafe_allow_html=True)

    # Top selected card visual
    if st.session_state.age_group:
        color = CARD_COLORS.get(st.session_state.age_group, "#60A5FA")
        st.markdown(age_card_html(st.session_state.age_group, AGE_GROUPS[st.session_state.age_group], selected=True, color=color), unsafe_allow_html=True)

    st.write("")
    # slider-like input (use number_input + custom styled progress)
    goal = st.number_input("Daily goal (ml)", min_value=500, max_value=4000, step=100,
                           value=st.session_state.goal or AGE_GROUPS[st.session_state.age_group], key="goal_confirm_input")
    st.session_state.goal = goal

    st.write("")
    st.markdown("<div style='display:flex; justify-content:space-between; align-items:center;'>", unsafe_allow_html=True)
    if st.button("← Back to Age Groups", key="back_to_age"):
        st.session_state.phase = 2
        st.experimental_rerun()
    if st.button("Continue ➡️", key="continue_to_dashboard"):
        st.session_state.phase = 4
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Phase 4: Dashboard
# ---------------------------
elif st.session_state.phase == 4:
    st.markdown("<div class='wb-card'>", unsafe_allow_html=True)
    # header area with change age group button and goal
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                f"<div><h2 style='margin:0;'>Daily Water Goal</h2><div style='color:#118ab2; font-weight:700'>{st.session_state.goal}ml</div></div>"
                f"<div><form><button class='big-btn' formaction='#' onclick='return false;'>Change Age Group</button></form></div>"
                f"</div>",
                unsafe_allow_html=True)

    # small report (intake text) and progress bar
    st.markdown("<div style='text-align:center; margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700;'>{st.session_state.total}ml / {st.session_state.goal}ml</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # custom progress rendering
    progress_fraction = min(st.session_state.total / st.session_state.goal if st.session_state.goal else 0, 1.0)
    render_progress_bar(progress_fraction)

    st.markdown("<div style='margin:18px 0; padding:18px; border-radius:12px; background:linear-gradient(90deg, rgba(45,212,191,0.12), rgba(96,165,250,0.06)); text-align:center;'>"
                "Let's start your hydration journey!"
                "</div>", unsafe_allow_html=True)

    # Quick add water tiles (two columns grid)
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("250 ml", key="tile_250"):
            st.session_state.total += 250
        # visually show tile
        st.markdown("<div class='quick-tile tile-250'>💧<div style='font-size:18px;margin-top:8px;'>250ml</div></div>", unsafe_allow_html=True)

    with c2:
        if st.button("500 ml", key="tile_500"):
            st.session_state.total += 500
        st.markdown("<div class='quick-tile tile-500'>🥛<div style='font-size:18px;margin-top:8px;'>500ml</div></div>", unsafe_allow_html=True)

    c3, c4 = st.columns([1,1])
    with c3:
        if st.button("750 ml", key="tile_750"):
            st.session_state.total += 750
        st.markdown("<div class='quick-tile tile-750'>🥤<div style='font-size:18px;margin-top:8px;'>750ml</div></div>", unsafe_allow_html=True)

    with c4:
        if st.button("1L", key="tile_1000"):
            st.session_state.total += 1000
        st.markdown("<div class='quick-tile tile-1000'>🍼<div style='font-size:18px;margin-top:8px;'>1L</div></div>", unsafe_allow_html=True)

    # custom amount input row
    st.write("")
    custom_col1, custom_col2 = st.columns([4,1])
    with custom_col1:
        amt = st.number_input("Custom amount (ml)", min_value=0, step=50, value=0, key="custom_input_amount")
    with custom_col2:
        if st.button("Add", key="add_custom_dashboard"):
            st.session_state.total += int(amt)

    # footer actions
    st.markdown("<div class='footer-row'>"
                "<div class='footer-left'><form><button type='submit' formaction='#' class='' style='background:none;border:none;font-weight:700;'>↺ Reset Day</button></form></div>"
                "<div style='flex:1'></div>"
                "<div class='footer-right'><form><button type='submit' formaction='#' style='background:transparent;border:none;color:white;font-weight:700;'>End Day Summary</button></form></div>"
                "</div>", unsafe_allow_html=True)

    # Reset and change age interactions (actual functionality)
    if st.button("Reset Day (actual)", key="reset_day_btn"):
        st.session_state.total = 0
    if st.button("Change Age Group (actual)", key="change_age_btn"):
        st.session_state.phase = 2
        st.experimental_rerun()

    # mascot & tips
    st.write("")
    if st.session_state.mascot_on:
        if progress_fraction == 0:
            st.info("Let's start hydrating! 🚰🙂")
        elif progress_fraction < 0.5:
            st.info("Good start! Keep sipping 💦😃")
        elif progress_fraction < 0.75:
            st.success("Nice! You're halfway there 😎")
        elif progress_fraction < 1.0:
            st.success("Almost at your goal! 🌊🤗")
        else:
            st.balloons()
            st.success("🎉 Congrats — hydrate champion! 🥳")

    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# End of app
# ---------------------------

