import streamlit as st
import json
from pathlib import Path
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.level_data import (
    get_all_states, get_all_districts, get_districts_by_state,
    get_zipcodes_by_district, ZIPCODE_DATA
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

# settings file (per-user)
SETTINGS_FILE = Path(__file__).parents[1] / "settings.json"

# load existing settings (per username) if present
def load_settings():
    if SETTINGS_FILE.exists():
        try:
            return json.loads(SETTINGS_FILE.read_text())
        except Exception:
            return {}
    return {}

def save_settings(all_settings):
    try:
        SETTINGS_FILE.write_text(json.dumps(all_settings, indent=2))
        return True
    except Exception:
        return False

all_settings = load_settings()

# 🔐 LOGIN CHECK
if not st.session_state.get('logged_in', False):
    st.warning("🔐 Please log in from the Home page to access this section.")
    st.stop()

st.markdown("""
<div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%); 
           border-radius: 28px; padding: 3rem; margin: 2rem 0; 
           box-shadow: 0 40px 120px rgba(6, 182, 212, 0.2); text-align: center;
           border: 4px solid #06b6d4;'>
    <h1 class="main-header" style="margin: 0; font-size: 2.8rem;">⚙️ Settings & Profile</h1>
    <p style='color: #0f172a; font-size: 1.4rem; font-weight: 600; max-width: 800px; 
              margin: 1rem auto 0; line-height: 1.6;'>
        Personalize your VaxiPredict experience
    </p>
</div>
""", unsafe_allow_html=True)

# Profile Section - Gradient Card
with st.container():
    st.markdown("""
    <div class="profile-card">
        <h3>👤 Your Profile</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # per-user defaults
    current_user = st.session_state.get('username', 'default')
    user_settings = all_settings.get(current_user, {})

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        name = st.text_input("👤 Full Name", user_settings.get('name', "Sanjai R"), 
                           help="Your display name")
        role = st.text_input("🏥 Role", user_settings.get('role', "Student"))
    with col2:
        region = st.text_input("📍 Region", user_settings.get('region', "Nagercoil"))
        language = st.selectbox("🌐 Language", 
                              ["English", "தமிழ்", "हिंदी"], index=( ["English","தமிழ்","हिंदी"].index(user_settings.get('language')) if user_settings.get('language') in ["English","தமிழ்","हिंदी"] else 0 ))

# Analysis Settings
st.markdown('<div class="settings-card"><h4>🔬 Analysis Settings</h4></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")
with col1:
    model = st.selectbox("🤖 Prediction Model", 
                        ["GNN-LSTM (Fast)", "GNN-LSTM (High Accuracy)"], index=(0 if user_settings.get('model','GNN-LSTM (Fast)')=="GNN-LSTM (Fast)" else 1))
    live_updates = st.checkbox("🔄 Live Data Updates", value=user_settings.get('live_updates', True))
with col2:
    data_retention = st.slider("📊 Data Retention (days)", 30, 365, user_settings.get('data_retention', 90))
    auto_save = st.checkbox("💾 Auto-save preferences", value=user_settings.get('auto_save', True))

# LEVEL SELECTOR FOR SETTINGS CONTEXT
st.markdown("---")
st.markdown("## 🎯 Analysis Level Context")
col1, col2, col3 = st.columns(3, gap="large")
with col1:
    if st.button("🌍 National", use_container_width=True, key="set_nat"):
        st.session_state.analysis_level = "national"
        st.session_state.selected_reference = None
        st.rerun()
with col2:
    if st.button("📍 District", use_container_width=True, key="set_dist"):
        st.session_state.analysis_level = "district"
        st.rerun()
with col3:
    if st.button("📮 Zip Code", use_container_width=True, key="set_zip"):
        st.session_state.analysis_level = "zipcode"
        st.rerun()

st.markdown("---")

# Reference selector
reference = None
level_name = "National"
if st.session_state.get("analysis_level") == "district":
    districts = get_all_districts()
    reference = st.selectbox("District", districts, key="set_dist_sel")
    level_name = reference
elif st.session_state.get("analysis_level") == "zipcode":
    districts = get_all_districts()
    sel_dist = st.selectbox("District", districts, key="set_zip_dist")
    zipcodes = get_zipcodes_by_district(sel_dist)
    zc_opts = [f"{z} - {ZIPCODE_DATA[z]['name']}" for z in zipcodes]
    if zc_opts:
        sel_zc = st.selectbox("Zip Code", zc_opts, key="set_zip_sel")
        reference = sel_zc.split(" - ")[0]
        level_name = f"{ZIPCODE_DATA[reference]['name']}"

st.markdown("---")

# Save Button with better styling
if st.button("💾 Save Settings", type="primary", 
             help="Save all changes", use_container_width=True):
    # update settings for this user
    all_settings[current_user] = {
        'name': name,
        'role': role,
        'region': region,
        'language': language,
        'model': model,
        'live_updates': bool(live_updates),
        'data_retention': int(data_retention),
        'auto_save': bool(auto_save)
    }
    ok = save_settings(all_settings)
    if ok:
        st.success("✅ Settings saved successfully!")
        st.balloons()
        st.markdown("**Your preferences have been updated!**")
    else:
        st.error("❌ Failed to save settings to disk.")

# Status indicators - CLEAN VERSION (REMOVED NOTIFICATIONS)
st.markdown("---")
col1, col2 = st.columns(2, gap="large")
with col1:
    st.metric("👤 Profile", "Complete", "100%")
with col2:
    st.metric("🔬 Model", model.split()[0], delta="Active")

render_footer(
    title="VaxiPredict Settings",
    subtitle="Customize profiles, models & alert preferences",
    meta="Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    icon="⚙️"
)

