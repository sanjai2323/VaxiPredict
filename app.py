import streamlit as st
import hashlib
import runpy
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta


# 🔥 FIXED: FIRST STREAMLIT COMMAND - NO ERRORS
st.set_page_config(
    page_title="VaxiPredict",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 🔥 PERFECT DESIGN - SINGLE LINE + COMPACT FORMS
st.markdown("""
<style>
/* HIDE DEFAULT NAV */
#MainMenu, footer { visibility: hidden !important; }
section[data-testid="stStatusWidget"] > div > div { display: none !important; }
button[kind="header"] { display: none !important; }
div[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] nav,
[aria-label="Pages"],
section[data-testid="stSidebar"] > div > div > div:first-child > div > div > nav { display: none !important; }

/* MAIN CONTAINER */
section[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 40%, #f1f5f9 70%, #e0f2fe 100%) !important;
    padding: 2.2rem !important;
    min-height: 100vh !important;
    transition: margin-left 0.3s ease, width 0.3s ease !important;
}

/* FULL PAGE WHEN SIDEBAR MINIMIZED */
section[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stAppViewContainer"],
section[data-testid="stSidebar"].collapsed ~ section[data-testid="stAppViewContainer"] {
    margin-left: 60px !important;
    width: calc(100% - 60px) !important;
    padding: 2.2rem 3rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* SINGLE CUSTOM ARROW */
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stRadio > div > div > label,
section[data-testid="stSidebar"] .nav-box .stRadio label,
section[data-testid="stSidebar"] .nav-box .stRadio > div > div > label {
    position: relative;
    padding-left: 2.4rem !important;
}

/* CUSTOM ARROW → ONLY */
section[data-testid="stSidebar"] .stRadio label::before,
section[data-testid="stSidebar"] .stRadio > div > div > label::before,
section[data-testid="stSidebar"] .nav-box .stRadio label::before,
section[data-testid="stSidebar"] .nav-box .stRadio > div > div > label::before {
    content: "→";
    position: absolute;
    left: 0.4rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.1rem;
    color: #10b981;
    margin-right: 0.5rem;
}

/* HIDE ALL DEFAULT KEYBOARD / LEFT‑RIGHT SYMBOLS */
section[data-testid="stSidebar"] .stRadio label::after,
section[data-testid="stSidebar"] .stRadio > div > div > label::after,
section[data-testid="stSidebar"] .stRadio label svg,
section[data-testid="stSidebar"] .stRadio label i,
section[data-testid="stSidebar"] .stRadio label span::before,
section[data-testid="stSidebar"] .stRadio label span::after,
section[data-testid="stSidebar"] .nav-box .stRadio label::after,
section[data-testid="stSidebar"] .nav-box .stRadio > div > div > label::after,
section[data-testid="stSidebar"] .nav-box .stRadio label svg,
section[data-testid="stSidebar"] .nav-box .stRadio label i,
section[data-testid="stSidebar"] .nav-box .stRadio label span::before,
section[data-testid="stSidebar"] .nav-box .stRadio label span::after {
    display: none !important;
}

/* TITLES */
.main-title {
    font-size: 3.6rem !important;
    background: linear-gradient(135deg, #1e293b, #10b981, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900 !important;
    text-align: center !important;
    letter-spacing: -0.02em !important;
}

/* METRIC CARDS */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
    border-radius: 22px;
    padding: 2rem 1.6rem;
    text-align: center;
    border: 2px solid #e2e8f0;
    box-shadow: 0 25px 70px rgba(0,0,0,0.12);
    height: 150px;
    transition: all 0.3s ease !important;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #10b981, #06b6d4);
}
.metric-title {
    font-size: 1rem !important;
    font-weight: 800 !important;
    margin: 0 0 0.6rem 0 !important;
    line-height: 1.3 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.metric-value {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    margin: 0 !important;
    line-height: 1 !important;
}

/* WELCOME CARDS */
.welcome-card, .thank-you-card {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 40%, #fcd34d 100%);
    border-radius: 32px;
    padding: 6.5rem 4.5rem;
    text-align: center;
    box-shadow: 0 50px 120px rgba(245,158,11,0.35);
    border: 4px solid #f59e0b;
    position: relative;
}
.welcome-card::before, .thank-you-card::before {
    content: '✨';
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 3rem;
    opacity: 0.3;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(226,232,240,0.5) !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    width: 300px !important;
    min-width: 300px !important;
    padding: 1.5rem !important;
    border-radius: 20px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(59,130,246,0.05), rgba(147,197,253,0.03)) !important;
    pointer-events: none;
}

section[data-testid="stSidebar"][aria-expanded="false"],
section[data-testid="stSidebar"].collapsed {
    width: 80px !important;
    min-width: 80px !important;
    padding: 1.5rem 1rem !important;
    border-radius: 20px !important;
    overflow: hidden !important;
}

/* SIDEBAR HEADER */
.sidebar-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
}

.logo-container {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(59,130,246,0.3);
    font-size: 1.5rem;
    color: white;
    position: relative;
}

.logo-container::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 18px;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    opacity: 0.3;
    filter: blur(8px);
}

.sidebar-brand {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1f2937;
    line-height: 1.2;
}

.sidebar-subtitle {
    font-size: 0.85rem;
    color: #6b7280;
    font-weight: 500;
}

/* NAVIGATION MENU */
.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    position: relative;
    z-index: 1;
}

.sidebar-nav .stButton > button {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
    padding: 0.875rem 1rem !important;
    border-radius: 12px !important;
    background: transparent !important;
    border: none !important;
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    width: 100% !important;
    margin: 0.25rem 0 !important;
    text-align: left !important;
    justify-content: flex-start !important;
}

.sidebar-nav .stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(147,197,253,0.05)) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
    border-radius: 12px !important;
}

.sidebar-nav .stButton > button:hover::before {
    opacity: 1 !important;
}

.sidebar-nav .stButton > button:hover {
    transform: translateX(4px) !important;
    box-shadow: 0 8px 25px rgba(59,130,246,0.15) !important;
}

.sidebar-nav .stButton > button:focus {
    outline: none !important;
}

/* COLLAPSED STATE */
section[data-testid="stSidebar"][aria-expanded="false"] .nav-label,
section[data-testid="stSidebar"].collapsed .nav-label,
section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-subtitle,
section[data-testid="stSidebar"].collapsed .sidebar-subtitle {
    display: none;
}

section[data-testid="stSidebar"][aria-expanded="false"] .nav-item,
section[data-testid="stSidebar"].collapsed .nav-item {
    justify-content: center;
    padding: 0.875rem;
    position: relative;
}

section[data-testid="stSidebar"][aria-expanded="false"] .nav-item::after,
section[data-testid="stSidebar"].collapsed .nav-item::after {
    content: attr(data-tooltip);
    position: absolute;
    left: 100%;
    top: 50%;
    transform: translateY(-50%);
    background: #1f2937;
    color: white;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    font-size: 0.8rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    margin-left: 0.75rem;
    z-index: 10;
}

section[data-testid="stSidebar"][aria-expanded="false"] .nav-item:hover::after,
section[data-testid="stSidebar"].collapsed .nav-item:hover::after {
    opacity: 1;
}

/* TOGGLE BUTTON */
.sidebar-toggle {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    border: 1px solid rgba(226,232,240,0.5);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    z-index: 2;
}

.sidebar-toggle:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.toggle-icon {
    font-size: 1.2rem;
    color: #374151;
    transition: transform 0.3s ease;
}

section[data-testid="stSidebar"][aria-expanded="false"] .toggle-icon,
section[data-testid="stSidebar"].collapsed .toggle-icon {
    transform: rotate(180deg);
}


/* LOGOUT BUTTON */
.logout-btn {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    border-radius: 20px !important;
    font-weight: 900 !important;
    font-size: 1.1rem !important;
    box-shadow: 0 15px 40px rgba(239,68,68,0.3) !important;
    height: 52px !important;
    border: 2px solid rgba(239,68,68,0.3) !important;
    color: white !important;
    margin: 0 1rem 1.5rem 1rem !important;
    width: calc(100% - 2rem) !important;
}
.logout-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 50px rgba(239,68,68,0.4) !important;
}

/* LOGIN STYLES */
.login-title {
    font-size: 3.2rem !important;
    color: #1e293b !important;
    text-align: center !important;
    margin-bottom: 2.2rem !important;
    font-weight: 900 !important;
}
.login-main-text {
    font-size: 2.4rem !important;
    color: #475569 !important;
    font-weight: 800 !important;
    line-height: 1.4 !important;
}
.quote-text {
    font-size: 1.8rem !important;
    color: #059669 !important;
    font-weight: 800 !important;
}
.quote-author {
    font-size: 1.4rem !important;
    color: #166534 !important;
    font-style: italic !important;
}

/* INPUTS + BUTTONS */
.stTextInput > div > div > input {
    height: 45px !important;
    padding: 0.8rem 1rem !important;
    font-size: 1.1rem !important;
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
}
.stButton > button {
    height: 45px !important;
    padding: 0.6rem 1.5rem !important;
    font-size: 1.1rem !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    border: 2px solid !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
}

/* ALERTS */
.stAlert, .stInfo, .stSuccess {
    font-size: 1.1rem !important;
    padding: 1rem 1.2rem !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# 🚀 UNIVERSAL AUTH
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


if 'users' not in st.session_state:
    st.session_state.users = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'logout_view' not in st.session_state:
    st.session_state.logout_view = False
if 'page_selector' not in st.session_state:
    st.session_state.page_selector = "Dashboard"
if 'current_page' not in st.session_state:
    st.session_state.current_page = None
if 'sidebar_collapsed' not in st.session_state:
    st.session_state.sidebar_collapsed = False
if 'sidebar_hidden' not in st.session_state:
    st.session_state.sidebar_hidden = False


# PAGES MAP
pages_map = {
    "Dashboard": None,
    "Predictions": os.path.join("pages", "2_Predictions.py"),
    "Interventions": os.path.join("pages", "3_Interventions.py"),
    "Networks": os.path.join("pages", "4_Networks.py"),
    "Reminders": os.path.join("pages", "5_Reminders.py"),
    "Rumours": os.path.join("pages", "6_Rumours.py"),
    "Settings": os.path.join("pages", "7_Settings.py"),
    "Reports": os.path.join("pages", "reports.py"),
    "Vaccines": os.path.join("pages", "Vaccines.py"),
}


# 🔥 LOGOUT SCREEN
if st.session_state.logout_view:
    st.markdown('<style>section[data-testid="stSidebar"] {display: none !important;}</style>', unsafe_allow_html=True)
    st.markdown("""
    <div class="welcome-card thank-you-card" style="margin: 5rem auto; max-width: 950px;">
        <div style='font-size: 6.5rem; margin-bottom: 2.2rem;'>👋</div>
        <h1 style='font-size: 4.2rem; font-weight: 900; color: #92400e; margin-bottom: 1.8rem;'>Thank You!</h1>
        <p style='color: #92400e; font-size: 2.2rem; font-weight: 800;'>Have a wonderful day! 🌟</p>
        <p style='color: #b45309; font-size: 1.4rem;'>Session securely logged out</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🔐 Login Again", type="primary", use_container_width=True):
            for key in ['logout_view', 'logged_in', 'username']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            for key in ['logout_view', 'logged_in', 'username']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    st.stop()


# 🔥 PERFECT LOGIN SCREEN - COMPACT FORMS + BIG TEXT
if not st.session_state.logged_in:
    st.markdown('<style>section[data-testid="stSidebar"] {display: none !important;}</style>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                border-radius: 32px; border: 4px solid #e2e8f0; padding: 7rem 5rem;
                text-align: center; box-shadow: 0 50px 120px rgba(0,0,0,0.18);
                margin: 5rem auto; max-width: 1050px; position: relative;'>
        <h1 class="main-title">🧠 VaxiPredict</h1>
        <div class="login-main-text">
            Vaccine Hesitancy Intelligence Platform
        </div>
        <div style='background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                    padding: 3rem; border-radius: 28px; border: 4px solid #10b981;
                    margin: 2.5rem 0; box-shadow: 0 25px 60px rgba(16,185,129,0.25);'>
            <div class="quote-text">
                💡 "Together, we can build vaccine confidence for every community"
            </div>
            <div class="quote-author">
                — VaxiPredict Mission
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("👤 Login", use_container_width=True, type="primary"):
            st.session_state.view = "login"
            st.rerun()
    with col2:
        if st.button("➕ New Account", use_container_width=True):
            st.session_state.view = "signup"
            st.rerun()

    # 🔥 PERFECT LOGIN FORM - COMPACT
    if st.session_state.get('view') == "login":
        st.markdown('<h2 class="login-title">🔐 Welcome Back</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            username = st.text_input(
                "👤 Username", placeholder="Your name/username",
                label_visibility="collapsed", key="login_user"
            )
            password = st.text_input(
                "🔒 Password", type="password",
                placeholder="Your password", label_visibility="collapsed", key="login_pass"
            )
            if st.button("🚀 Enter Platform", type="primary", key="login_btn"):
                if username and password:
                    users = st.session_state.get('users', {})
                    if username in users and users[username] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        if 'view' in st.session_state:
                            del st.session_state['view']
                        st.success(f"✅ Welcome back, {username.title()}! 🎉")
                        st.balloons()
                        st.rerun()
                    else:
                        st.warning("👤 User not found? Try ➕ New Account!")
                else:
                    st.warning("⚠️ Please fill both fields!")
        with col2:
            st.info("💡 Existing users work!")
        if st.button("← Back to Home", key="back_login"):
            if 'view' in st.session_state:
                del st.session_state['view']
            st.rerun()
        st.stop()

    # 🔥 PERFECT SIGNUP FORM - COMPACT
    elif st.session_state.get('view') == "signup":
        st.markdown('<h2 class="login-title">➕ Join Us</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    padding: 2rem; border-radius: 20px; border: 3px solid #f59e0b;
                    margin-bottom: 2.5rem; text-align: center;'>
            <div style='color: #92400e; font-weight: 700; font-size: 1.8rem;'>🌟 "Every health worker makes a difference"</div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            username = st.text_input(
                "👤 Choose Username", placeholder="Your name or any username",
                label_visibility="collapsed", key="signup_user"
            )
            password = st.text_input(
                "🔒 Choose Password", type="password",
                placeholder="Any secure password", label_visibility="collapsed", key="signup_pass"
            )
            if st.button("✅ Create & Login", type="primary", key="signup_btn"):
                if username and password:
                    users = st.session_state.get('users', {})
                    if username in users:
                        st.error("❌ Username taken! Choose another.")
                    else:
                        users[username] = hash_password(password)
                        st.session_state.users = users
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        if 'view' in st.session_state:
                            del st.session_state['view']
                        st.success(f"✅ Welcome aboard, {username.title()}! 🎉")
                        st.balloons()
                        st.rerun()
                else:
                    st.warning("⚠️ Both fields required!")
        with col2:
            st.success("✅ Instant access!")
        if st.button("← Back to Home", key="back_signup"):
            if 'view' in st.session_state:
                del st.session_state['view']
            st.rerun()
        st.stop()


# 🔥 PERFECT CLEAN SIDEBAR
if st.session_state.sidebar_hidden:
    st.markdown("""
    <style>
    section[data-testid='stSidebar'] {
        width: 50px !important;
        min-width: 50px !important;
        padding: 0.8rem 0.4rem !important;
        overflow: visible !important;
    }
    section[data-testid='stSidebar'] .stMarkdown,
    section[data-testid='stSidebar'] .stRadio,
    section[data-testid='stSidebar'] .stTextInput,
    section[data-testid='stSidebar'] .stAlert,
    section[data-testid='stSidebar'] .stInfo,
    section[data-testid='stSidebar'] .stSuccess {
        display: none !important;
    }
    section[data-testid='stSidebar'] .stButton {
        width: 100% !important;
        margin: 0.2rem 0 !important;
    }
    section[data-testid='stAppViewContainer'] {
        margin-left: 50px !important;
        width: calc(100% - 50px) !important;
        padding: 2.2rem 3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    # Add collapsed class if needed
    if st.session_state.get('sidebar_collapsed', False):
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            width: 80px !important;
            min-width: 80px !important;
            padding: 1.5rem 1rem !important;
        }
        section[data-testid="stSidebar"] .sidebar-subtitle {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)

    # Dynamic style for active button
    active_page = st.session_state.page_selector
    st.markdown(f"""
    <style>
    .sidebar-nav .stButton > button[title*="{active_page}"] {{
        background: linear-gradient(135deg, #dbeafe, #bfdbfe) !important;
        color: #1d4ed8 !important;
        box-shadow: 0 8px 32px rgba(59,130,246,0.2), inset 0 1px 0 rgba(255,255,255,0.3) !important;
    }}
    .stButton > button[title="Logout"] {{
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 15px 40px rgba(239,68,68,0.3) !important;
        height: 52px !important;
        border: 2px solid rgba(239,68,68,0.3) !important;
        color: white !important;
        margin: 0 1rem 1.5rem 1rem !important;
        width: calc(100% - 2rem) !important;
    }}
    .stButton > button[title="Logout"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 20px 50px rgba(239,68,68,0.4) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Header with logo and toggle
    st.markdown("""
    <div class="sidebar-header">
        <div class="logo-container">🧠</div>
        <div>
            <div class="sidebar-brand">VaxiPredict</div>
            <div class="sidebar-subtitle">Intelligence Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle button
    toggle_icon = "▶" if st.session_state.get('sidebar_collapsed', False) else "◀"
    if st.button(toggle_icon, key="toggle_sidebar", help="Toggle sidebar"):
        st.session_state.sidebar_collapsed = not st.session_state.get('sidebar_collapsed', False)
        st.rerun()

    # Navigation Menu
    menu_items = [
        ("🏠", "Dashboard"),
        ("📊", "Predictions"),
        ("💉", "Interventions"),
        ("🌐", "Networks"),
        ("⏰", "Reminders"),
        ("🗣️", "Rumours"),
        ("⚙️", "Settings"),
        ("📋", "Reports"),
        ("🩺", "Vaccines"),
    ]

    for icon, label in menu_items:
        if st.button(f"{icon} {label}", key=f"nav_{label}", use_container_width=True, help=label):
            st.session_state.page_selector = label
            st.session_state.current_page = pages_map.get(label)
            st.rerun()

    # Logout Button
    st.markdown('<div style="margin-top: auto;">', unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True, help="Logout"):
        st.session_state.logout_view = True
        st.session_state.logged_in = False
        st.session_state.username = ""
        if 'current_page' in st.session_state:
            del st.session_state['current_page']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # JavaScript for interactions
    st.markdown("""
    <script>
    function toggleSidebar() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.classList.toggle('collapsed');
            const toggleIcon = document.querySelector('.toggle-icon');
            if (toggleIcon) {
                toggleIcon.textContent = sidebar.classList.contains('collapsed') ? '▶' : '◀';
            }
        }
    }

    function selectPage(page) {
        // Use Streamlit's setComponentValue to update session state
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            data: {page: page}
        }, '*');
    }

    function logout() {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            data: {action: 'logout'}
        }, '*');
    }

    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:setComponentValue') {
            const data = event.data.data;
            if (data.page) {
                // Update page selector
                window.location.href = window.location.href; // Trigger rerun
            } else if (data.action === 'logout') {
                // Trigger logout
                window.location.href = window.location.href; // Trigger rerun
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)


# 🔥 LOAD PAGES OR DASHBOARD
if st.session_state.get('current_page'):
    page_path = st.session_state.current_page
    if page_path and os.path.exists(page_path):
        runpy.run_path(page_path, run_name="__main__")
        st.stop()


# MAIN DASHBOARD
st.markdown("""
<div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 50%, #fcd34d 100%);
          border-radius: 32px; padding: 5rem; margin: 2.5rem 0;
          box-shadow: 0 50px 120px rgba(245,158,11,0.35); text-align: center;
          border: 5px solid #f59e0b; position: relative; overflow: hidden;'>
    <div style='position: absolute; top: 20px; right: 30px; font-size: 3rem; opacity: 0.3;'>🚀</div>
    <h1 class="main-title">🏠 VaxiPredict Control Center</h1>
    <p style='color: #92400e; font-size: 2rem; font-weight: 800; max-width: 950px;
              margin: 0 auto 5rem auto; line-height: 1.8;'>
        Real-time System Status • Active Campaigns • ML Model Performance
    </p>
</div>
""", unsafe_allow_html=True)


# METRICS
col1, col2, col3 = st.columns(3, gap="large", vertical_alignment="top")
with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title" style='color: #10b981;'>Active Users</div>
        <div class="metric-value" style='color: #059669;'>1,847</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title" style='color: #8b5cf6;'>Predictions Today</div>
        <div class="metric-value" style='color: #7c3aed;'>1,392</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title" style='color: #f59e0b;'>Model Accuracy</div>
        <div class="metric-value" style='color: #d97706;'>96.8%</div>
    </div>
    """, unsafe_allow_html=True)


# MODULE STATUS
st.markdown("### 🧩 System Modules", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4, gap="large", vertical_alignment="top")
with col1:
    st.success("🤖 GNN Model ✅ Online")
with col2:
    st.info("📱 SMS Gateway ✅ 4,127 queued")
with col3:
    st.success("🗣️ Rumour Monitor ✅ 18 active")
with col4:
    st.success("📈 Analytics Engine ✅ Live")


# HEALTH CARDS
st.markdown("### 🚀 Campaigns & Data", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large", vertical_alignment="top")
with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                border-radius: 28px; padding: 3.5rem; text-align: center;
                border: 4px solid #10b981; box-shadow: 0 40px 100px rgba(16,185,129,0.25);'>
        <h3 style='color: #059669; font-size: 2.2rem;'>🚀 Live Campaigns</h3>
        <div style='font-size: 4rem; font-weight: 900; color: #10b981;'>24</div>
        <p style='color: #166534; font-size: 1.3rem;'>Active interventions</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                border-radius: 28px; padding: 3.5rem; text-align: center;
                border: 4px solid #6b7280; box-shadow: 0 40px 100px rgba(107,114,128,0.25);'>
        <h3 style='color: #374151; font-size: 2.2rem;'>📊 Data Processed</h3>
        <div style='font-size: 4rem; font-weight: 900; color: #4b5563;'>3.7M</div>
        <p style='color: #6b7280; font-size: 1.3rem;'>Records analyzed</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
          border-radius: 28px; padding: 5rem; text-align: center; margin-top: 5rem;
          color: white; box-shadow: 0 50px 120px rgba(30,41,59,0.45); position: relative;'>
    <div style='position: absolute; top: 20px; left: 30px; font-size: 3rem; opacity: 0.3;'>⚡</div>
    <h3 style='font-size: 2.5rem; margin-bottom: 1.2rem;'>VaxiPredict Core Engine</h3>
    <div style='font-size: 1.5rem; opacity: 0.98;'>GNN + LSTM Intelligence • Real-time Processing • 24/7 Monitoring</div>
</div>
""", unsafe_allow_html=True)