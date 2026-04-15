import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import uuid
import sys
import os
import random


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.level_data import (
    get_all_states, get_all_countries, get_all_districts,
    get_districts_by_state
)
from utils.ui_components import apply_global_theme, init_session_state, render_footer


apply_global_theme()
init_session_state()

# Add arrow styling for sidebar navigation
st.markdown("""
<style>
/* ARROW STYLING FOR SIDEBAR */
.stRadio label::before,
.stRadio > div > div > label::before,
.stRadio > div > div > label > span::before,
.nav-box .stRadio label::before,
.nav-box .stRadio > div > div > label::before,
.nav-box .stRadio > div > div > label > span::before,
section[data-testid="stSidebar"] .stRadio label::before,
section[data-testid="stSidebar"] .stRadio > div > div > label::before,
section[data-testid="stSidebar"] .stRadio > div > div > label > span::before {
    content: "→" !important;
    font-size: 1.2rem !important;
    margin-right: 0.5rem !important;
    color: #10b981 !important;
    display: inline !important;
}

/* Hide keyboard symbols */
.stRadio label::after,
.stRadio > div > div > label::after,
.stRadio > div > div > label > span > *,
.nav-box .stRadio label::after,
.nav-box .stRadio > div > div > label::after,
.nav-box .stRadio > div > div > label > span > *,
section[data-testid="stSidebar"] .stRadio label::after,
section[data-testid="stSidebar"] .stRadio > div > div > label::after,
section[data-testid="stSidebar"] .stRadio > div > div > label > span > * {
    display: none !important;
}

/* FULL PAGE WHEN SIDEBAR MINIMIZED */
section[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stAppViewContainer"],
section[data-testid="stSidebar"].collapsed ~ section[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
    width: 100% !important;
    padding: 2.2rem 4rem !important;
    transition: margin-left 0.3s ease, width 0.3s ease !important;
}

section[data-testid="stSidebar"][aria-expanded="false"],
section[data-testid="stSidebar"].collapsed {
    width: 0 !important;
    min-width: 0 !important;
    padding: 0 !important;
    border-right: none !important;
    box-shadow: none !important;
    transition: width 0.3s ease, transform 0.3s ease !important;
}
</style>
""", unsafe_allow_html=True)

# 🔐 LOGIN CHECK
if not st.session_state.get('logged_in', False):
    st.warning("🔐 Please log in from the Home page to access this section.")
    st.stop()


# HERO SECTION
st.markdown("""
<div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
           border-radius: 28px; padding: 4rem; margin: 2rem 0;
           box-shadow: 0 40px 120px rgba(6, 182, 212, 0.2); text-align: center;
           border: 4px solid #06b6d4;'>
    <h1 style='font-size: 3rem; background: linear-gradient(135deg, #0f172a, #06b6d4);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               font-weight: 900;'>⏰ Vaccination Reminder System</h1>
    <p style='color: #0f172a; font-size: 1.6rem; font-weight: 700; max-width: 900px;
              margin: 0 auto; line-height: 1.7;'>
        Timely Notifications • Schedule Tracking • Personalized Reminders
    </p>
</div>
""", unsafe_allow_html=True)


# 📍 LEVEL SELECTOR
st.markdown("## 🎯 Analysis Level")
col1, col2, col3, col4 = st.columns(4, gap="large")


with col1:
    if st.button("🌍 National", use_container_width=True, key="rem_national"):
        st.session_state.analysis_level = "national"
        st.session_state.selected_reference = None
        st.rerun()


with col2:
    if st.button("🇮🇳 State", use_container_width=True, key="rem_state"):
        st.session_state.analysis_level = "state"
        st.rerun()


with col3:
    if st.button("🌎 Country", use_container_width=True, key="rem_country"):
        st.session_state.analysis_level = "country"
        st.rerun()


with col4:
    if st.button("📍 District", use_container_width=True, key="rem_district"):
        st.session_state.analysis_level = "district"
        st.rerun()


st.markdown("---")


reference = None
level_name = "National"
selected_state = None


if st.session_state.get("analysis_level") == "state":
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**🇮🇳 Select State:**")
    with col2:
        states = get_all_states()
        reference = st.selectbox("State", states, key="rem_state_sel")
        level_name = reference


elif st.session_state.get("analysis_level") == "country":
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**🌎 Select Country:**")
    with col2:
        countries = get_all_countries()
        reference = st.selectbox("Country", countries, key="rem_country_sel")
        level_name = reference


elif st.session_state.get("analysis_level") == "district":
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.markdown("**📍 State:**")
    with col2:
        states = get_all_states()
        selected_state = st.selectbox("State", states, key="rem_dist_state")
    with col3:
        districts = get_districts_by_state(selected_state)
        reference = st.selectbox("District", districts, key="rem_dist_sel")
        level_name = f"{reference}, {selected_state}"


st.markdown("---")


# ==========================
# UTILITIES
# ==========================
def get_dob_years():
    return list(range(1900, 2027))[::-1]


def format_time_remaining(days_left):
    if days_left <= 0:
        return "📅 Today"
    elif days_left < 1:
        hours = int(days_left * 24)
        minutes = int((days_left * 24 - hours) * 60)
        return f"⏰ {hours}h {minutes}m"
    elif days_left <= 30:
        return f"📅 {int(days_left)} days"
    elif days_left <= 365:
        return f"📅 {round(days_left / 30.44)} months"
    else:
        return f"📅 {round(days_left / 365.25, 1)} years"


# ==========================
# VACCINE SCHEDULE (unchanged)
# ==========================
VACCINE_SCHEDULE = {
    "🍼 Birth (0 days)": {"days": 0, "vaccines": {
        "BCG": "TB meningitis and severe TB protection",
        "Hepatitis B #1": "Chronic liver infection prevention",
        "OPV #0": "Initial polio protection"
    }},
    "👶 6 weeks": {"days": 42, "vaccines": {
        "Pentavalent #1": "DTP+HepB+Hib 5-in-1 protection",
        "Rotavirus #1": "Severe diarrhea prevention",
        "PCV #1": "Pneumonia protection",
        "fIPV #1": "Injectable polio dose 1"
    }},
    "👶 10 weeks": {"days": 70, "vaccines": {
        "Pentavalent #2": "Second 5-in-1 dose",
        "Rotavirus #2": "Second diarrhea protection",
        "PCV #2": "Second pneumonia dose"
    }},
    "👶 14 weeks": {"days": 98, "vaccines": {
        "Pentavalent #3": "Final infant 5-in-1",
        "Rotavirus #3": "Complete diarrhea protection",
        "PCV #3": "Final infant pneumonia",
        "fIPV #2": "Final IPV dose"
    }},
    "🍼 6 months": {"days": 182, "vaccines": {
        "Hepatitis A #1": "Foodborne liver protection",
        "Influenza #1": "First annual flu shot"
    }},
    "🍼 9 months": {"days": 274, "vaccines": {
        "Measles #1": "Measles complications prevention",
        "JE #1": "Japanese encephalitis protection"
    }},
    "🍼 12 months": {"days": 365, "vaccines": {
        "MR #1": "Measles-rubella protection",
        "Vitamin A #1": "Immunity support",
        "PCV booster": "Pneumococcal booster"
    }},
    "🧒 16–18 months": {"days": 510, "vaccines": {
        "DTP booster #1": "Toddler tetanus booster",
        "OPV booster #1": "Polio booster",
        "MMR #1": "Mumps added",
        "Chickenpox": "Varicella prevention",
        "Hepatitis A #2": "Final hepatitis A"
    }},
    "🏫 4–6 years": {"days": 1825, "vaccines": {
        "DTP booster #2": "School entry booster",
        "OPV booster #2": "Final polio booster",
        "MMR #2": "School measles booster"
    }},
    "🏫 7–9 years": {"days": 2922, "vaccines": {
        "Td booster": "School tetanus-diphtheria",
        "Typhoid conjugate #1": "Typhoid prevention"
    }},
    "🎓 10–12 years": {"days": 4015, "vaccines": {
        "HPV #1": "Cancer prevention",
        "Tdap #1": "Pre-teen pertussis coverage",
        "Typhoid #2": "Typhoid booster",
        "MenACWY #1": "Meningitis protection"
    }},
    "🎓 13–14 years": {"days": 5110, "vaccines": {
        "HPV #2": "HPV series completion",
        "MenACWY booster": "Meningitis booster"
    }},
    "🧒 16–18 years": {"days": 6570, "vaccines": {
        "Tdap booster": "Teen tetanus booster",
        "MenACWY booster #2": "Final meningitis dose"
    }},
    "🧑 19–26 years": {"days": 9125, "vaccines": {
        "Tdap booster": "Tetanus every 10 years",
        "HPV #3 (if needed)": "Final HPV cancer protection",
        "Annual flu": "Yearly influenza protection"
    }},
    "🧑 27–35 years": {"days": 11881, "vaccines": {
        "Tdap booster": "Adult tetanus (10‑yearly)",
        "Annual flu": "Influenza protection",
        "Hep A/B catch-up": "Missed childhood vaccines"
    }},
    "🧑 36–49 years": {"days": 16425, "vaccines": {
        "Tdap booster": "Midlife tetanus booster",
        "Annual flu": "Ongoing flu protection",
        "Pneumococcal (risk)": "High‑risk patients only"
    }},
    "👴 50 years": {"days": 18250, "vaccines": {
        "Shingles (2 doses)": "Shingles prevention",
        "PCV20": "Pneumonia protection",
        "High‑dose flu": "Enhanced flu vaccine"
    }},
    "👴 60 years": {"days": 21900, "vaccines": {
        "PPSV23": "Additional pneumonia protection",
        "Shingles booster": "Long‑term shingles immunity",
        "High‑dose flu": "Annual senior flu shot"
    }},
    "👵 65+ years": {"days": 23725, "vaccines": {
        "RSV vaccine": "Respiratory virus protection",
        "COVID booster": "Latest COVID coverage",
        "High‑dose flu": "Maximum flu protection"
    }},
    "🤰 Pregnancy": {"days": 0, "vaccines": {
        "Tdap (27–36w)": "Newborn pertussis protection",
        "Flu vaccine": "Mother and baby flu protection"
    }},
    "🧑 Every 10 years": {"days": 3652, "vaccines": {
        "Tdap booster": "Tetanus every 10 years",
        "Annual flu": "Yearly influenza vaccine"
    }}
}



# ==========================
# SESSION STATE
# ==========================
if "reminders" not in st.session_state:
    st.session_state.reminders = []


# ==========================
# LEVEL-SPECIFIC STATISTICS
# ==========================
def get_level_stats(level, reference=None):
    random.seed(hash(f"{level}_{reference}") % 2**32 if reference else 0)
   
    if level == "national":
        return {
            "total_reminders": random.randint(5000, 8000),
            "active_reminders": random.randint(2000, 3000),
            "completion_rate": random.uniform(75, 85),
            "avg_response_time": random.uniform(2, 4)
        }
    elif level == "country":
        return {
            "total_reminders": random.randint(2000, 4000),
            "active_reminders": random.randint(800, 1500),
            "completion_rate": random.uniform(70, 80),
            "avg_response_time": random.uniform(3, 5)
        }
    elif level == "state":
        return {
            "total_reminders": random.randint(800, 1500),
            "active_reminders": random.randint(300, 600),
            "completion_rate": random.uniform(72, 82),
            "avg_response_time": random.uniform(2.5, 4.5)
        }
    else:  # district
        return {
            "total_reminders": random.randint(200, 500),
            "active_reminders": random.randint(50, 150),
            "completion_rate": random.uniform(68, 78),
            "avg_response_time": random.uniform(3, 5)
        }


# ==========================
# DISPLAY LEVEL STATS
# ==========================
stats = get_level_stats(st.session_state.get("analysis_level", "national"), reference)


col1, col2, col3, col4 = st.columns(4, gap="large")


with col1:
    st.markdown(f"""
    <div class="stats-card">
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>📊 Total Reminders</div>
        <div style='font-size: 2rem; font-weight: 900; color: #3b82f6;'>{stats['total_reminders']:,}</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div class="stats-card">
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>⏰ Active Now</div>
        <div style='font-size: 2rem; font-weight: 900; color: #f97316;'>{stats['active_reminders']:,}</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div class="stats-card">
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>✅ Completion Rate</div>
        <div style='font-size: 2rem; font-weight: 900; color: #22c55e;'>{stats['completion_rate']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div class="stats-card">
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>⏱️ Avg Response</div>
        <div style='font-size: 2rem; font-weight: 900; color: #ec4899;'>{stats['avg_response_time']:.1f}d</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


def render_sidebar_countdown():
    active = [r for r in st.session_state.reminders if r.get("status") == "active"]
    if not active:
        st.sidebar.info("No active reminders")
        return


    # next upcoming reminder
    next_r = min(active, key=lambda x: x["due_date"])
    # convert date to ms timestamp for JS
    due_dt = datetime.combine(next_r["due_date"], datetime.min.time())
    due_ts = int(due_dt.timestamp() * 1000)


    header = ("<div style='padding:15px;border-radius:15px;background:linear-gradient(135deg,#fff 0%,#f8fafc 100%);border:2px solid #06b6d4;box-shadow:0 10px 25px rgba(6,182,212,0.2);'>"
              "<div style='font-size:1rem;color:#475569;margin-bottom:8px;font-weight:700;text-transform:uppercase;letter-spacing:1px;'>⏰ Next reminder</div>")


    name_line = f"<div style='font-size:1.1rem;color:#0f172a;font-weight:800;margin-bottom:6px'>{next_r['name']} — {next_r['vaccine']}</div>"
    countdown_line = f"<div id='vax_countdown' data-due='{due_ts}' style='font-size:1.5rem;color:#dc2626;font-weight:900;letter-spacing:0.5px;font-family:monospace;'>--:--:--</div>"
    due_line = f"<div style='font-size:0.9rem;color:#6b7280;margin-top:8px'>Due: {next_r['due_date'].strftime('%d/%m/%Y')}</div>"
    footer = "</div>"


    js = ("<script> (function(){ var el = document.getElementById('vax_countdown'); if(!el) return; "
          "var due = parseInt(el.getAttribute('data-due')); function update(){ var now = Date.now(); var diff = due - now; "
          "if(diff <= 0){ el.innerText = 'Due now'; return; } var s = Math.floor(diff/1000); var days = Math.floor(s/86400); s %= 86400; "
          "var hours = Math.floor(s/3600); s %= 3600; var mins = Math.floor(s/60); var secs = s%60; var out = ''; "
          "if(days>0) out += days + 'd '; out += String(hours).padStart(2,'0') + ':' + String(mins).padStart(2,'0') + ':' + String(secs).padStart(2,'0'); "
          "el.innerText = out; } update(); setInterval(update,1000); })(); </script>")


    sidebar_html = header + name_line + countdown_line + due_line + footer + js


    # render via components.html so the <script> executes (streamlit strips scripts from markdown)
    with st.sidebar:
        components.html(sidebar_html, height=180)



# render the sidebar countdown immediately
render_sidebar_countdown()


# ==========================
# GLOBAL CONTROLS
# ==========================
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("Clear form", type="secondary", use_container_width=True):
        st.rerun()
with col2:
    if st.button("Clear active", type="secondary", use_container_width=True):
        st.session_state.reminders = [r for r in st.session_state.reminders if r["status"] != "active"]
        st.rerun()
with col3:
    if st.button("Reset all", type="primary", use_container_width=True):
        st.session_state.reminders = []
        st.rerun()


# ==========================
# TABS
# ==========================
tab1, tab2, tab3 = st.tabs(["➕ Add Reminder", "⏰ Active", "✅ Completed"])


# ==========================
# TAB 1: ADD REMINDER
# ==========================
with tab1:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-radius: 20px;
        border: 1px solid #93c5fd;
        padding: 2rem;
        margin-bottom: 2rem;
    '>
        <h3 style='color: #1e40af; font-size: 1.8rem; font-weight: 800;'>➕ Create New Reminder</h3>
    </div>
    """, unsafe_allow_html=True)


    col_a, col_b = st.columns(2)


    with col_a:
        selected_age = st.selectbox(
            "👤 Age Group",
            list(VACCINE_SCHEDULE.keys()),
            key="age_select_tab1"
        )
        age_data = VACCINE_SCHEDULE[selected_age]


        selected_vaccine = st.selectbox(
            "💉 Vaccine",
            list(age_data["vaccines"].keys()),
            key="vaccine_select_tab1"
        )


        patient_name = st.text_input(
            "📝 Patient Name",
            placeholder="Leave blank for generic label",
            key="patient_name_tab1"
        )


    with col_b:
        st.markdown("""
        <div style='padding:8px; border-radius:10px; background: linear-gradient(135deg, #f0f9ff, #ffffff); border:1px solid #06b6d4; margin-bottom:1rem;'>
            <small style='color:#0f172a; font-weight:600;'>📅 Patient DOB and Due Date</small>
        </div>
        """, unsafe_allow_html=True)


        # restrict DOB between 1900-01-01 and 2026-12-31
        patient_dob = st.date_input(
            "📅 Date of Birth",
            min_value=datetime(1900, 1, 1).date(),
            max_value=datetime(2026, 12, 31).date(),
            key="patient_dob_tab1"
        )


        # restrict due date between 2026-01-01 and 2036-12-31
        due_date_input = st.date_input(
            "📅 Due Date",
            min_value=datetime(2026, 1, 1).date(),
            max_value=datetime(2036, 12, 31).date(),
            key="due_date_tab1"
        )


        alert_days = st.slider("🔔 Alert Before (Days)", 1, 30, 7, key="alert_tab1")


    if selected_vaccine:
        benefit = age_data["vaccines"][selected_vaccine]
        time_target = format_time_remaining(age_data["days"])
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-radius: 16px;
            border-left: 6px solid #10b981;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 10px 25px rgba(16,185,129,0.2);
        '>
            <h3 style='color: #065f46; font-size: 1.5rem; font-weight: 800; margin-bottom: 0.5rem;'>{selected_vaccine}</h3>
            <p style='color: #065f46; font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 500;'>
                {benefit}
            </p>
            <p style='color: #047857; margin: 0; font-weight: 600;'>
                📍 Target: {time_target}
            </p>
        </div>
        """, unsafe_allow_html=True)


    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✅ Add Reminder", type="primary", use_container_width=True, key="add_tab1"):
            try:
                dob = patient_dob
                due_date = due_date_input
                days_left = max(0, (due_date - datetime.now().date()).days)


                reminder = {
                    "id": str(uuid.uuid4())[:8],
                    "name": patient_name.strip() or "Patient",
                    "dob": dob.strftime('%d/%m/%Y'),
                    "age_group": selected_age,
                    "vaccine": selected_vaccine,
                    "benefit": age_data["vaccines"][selected_vaccine],
                    "dob_date": dob,
                    "due_date": due_date,
                    "days_left": days_left,
                    "alert_days": alert_days,
                    "time_left": format_time_remaining(days_left),
                    "status": "active"
                }
                st.session_state.reminders.append(reminder)
                st.success(f"✅ {reminder['name']}: Reminder added successfully!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


    with col_btn2:
        if st.button("🗑️ Clear Form", type="secondary", use_container_width=True, key="clear_tab1"):
            st.rerun()


# ==========================
# TAB 2: ACTIVE REMINDERS
# ==========================
with tab2:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-radius: 20px;
        border: 1px solid #fca5a5;
        padding: 2rem;
        margin-bottom: 2rem;
    '>
        <h3 style='color: #dc2626; font-size: 1.8rem; font-weight: 800;'>⏰ Active Reminders</h3>
    </div>
    """, unsafe_allow_html=True)


    if st.button("🗑️ Clear All Active", type="secondary", use_container_width=True, key="clear_active_tab2"):
        st.session_state.reminders = [r for r in st.session_state.reminders if r["status"] != "active"]
        st.rerun()


    active = [r for r in st.session_state.reminders if r["status"] == "active"]
    if active:
        active = sorted(active, key=lambda x: x["days_left"])
        for r in active:
            priority_color = "#ef4444" if r["days_left"] <= r["alert_days"] else "#10b981"
            bg_color = "#fff5f5" if r["days_left"] <= r["alert_days"] else "#f0f9ff"
           
            st.markdown(f"""
            <div style='
                background: {bg_color};
                border-radius: 16px;
                border-left: 6px solid {priority_color};
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            '>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h4 style='color: #1e293b; margin: 0; font-size: 1.3rem; font-weight: 800;'>
                        {r['time_left']}
                    </h4>
                    <span style='background: {priority_color}; color: white; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600;'>
                        {r['vaccine']}
                    </span>
                </div>
                <p style='color: #475569; margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;'>
                    👤 {r['name']}
                </p>
                <p style='color: #6b7280; margin: 0.2rem 0; font-size: 0.95rem;'>
                    📅 Due: {r['due_date'].strftime('%d/%m/%Y')} · DOB: {r['dob']}
                </p>
            </div>
            """, unsafe_allow_html=True)


            col_x, col_y = st.columns(2)
            with col_x:
                if st.button(f"✅ Mark Completed", key=f"complete_{r['id']}", use_container_width=True):
                    r["status"] = "completed"
                    st.rerun()
            with col_y:
                if st.button(f"🗑️ Delete", key=f"delete_{r['id']}", type="secondary", use_container_width=True):
                    st.session_state.reminders.remove(r)
                    st.rerun()
    else:
        st.info("✅ No active reminders. All caught up!")


# ==========================
# TAB 3: COMPLETED
# ==========================
with tab3:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-radius: 20px;
        border: 1px solid #86efac;
        padding: 2rem;
        margin-bottom: 2rem;
    '>
        <h3 style='color: #059669; font-size: 1.8rem; font-weight: 800;'>✅ Completed Vaccines</h3>
    </div>
    """, unsafe_allow_html=True)


    if st.button("🗑️ Clear All Completed", type="secondary", use_container_width=True, key="clear_completed_tab3"):
        st.session_state.reminders = [r for r in st.session_state.reminders if r["status"] != "completed"]
        st.rerun()


    completed = [r for r in st.session_state.reminders if r["status"] == "completed"]
    if completed:
        for r in sorted(completed, key=lambda x: x["due_date"], reverse=True):
            with st.expander(f"✅ {r['name']} – {r['vaccine']} – {r['due_date'].strftime('%d/%m/%Y')}"):
                st.success(f"💉 {r['benefit']}")
                st.caption(f"📅 DOB: {r['dob']} | Age Group: {r['age_group']}")
                if st.button(f"🗑️ Delete Record", key=f"del_comp_{r['id']}", type="secondary"):
                    st.session_state.reminders.remove(r)
                    st.rerun()
    else:
        st.info("📋 No completed vaccines recorded yet.")

render_footer(
    title="VaxiPredict Reminder Center",
    subtitle="Stay on top of vaccine schedules with alerts & tracking",
    meta="Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    icon="⏰"
)


