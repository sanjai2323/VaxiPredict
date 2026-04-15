# pages/Vaccines.py - COMPLETE VACCINE LIST (25+ Vaccines)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
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

# HEADER
st.markdown("""
<div class="vaccine-hero">
    <h1 style='font-size: 4rem; background: linear-gradient(135deg, #1e293b, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>🩺 Complete Vaccine Library</h1>
    <p style='color: #059669; font-size: 2rem; font-weight: 800;'>25+ Vaccines • Age-specific • Full details • Safety data</p>
    <div style='font-size: 4rem;'>💉</div>
</div>
""", unsafe_allow_html=True)

# 🔥 DUAL INPUT: AGE + VACCINE
col1, col2 = st.columns(2)
with col1:
    age = st.slider("👶 Age (Years)", 0, 100, 30)
with col2:
    selected_vaccine = st.selectbox("💉 All Vaccines", [
        "COVID-19 (2026)", "Influenza (Annual)", "Tdap/Td", "HPV (9v)", "Pneumococcal (PCV20)", 
        "Shingles (RZV)", "Hepatitis B", "Hepatitis A", "BCG (TB)", "MMR", "Varicella (Chickenpox)",
        "Rotavirus", "Polio (IPV/OPV)", "Hib", "Meningococcal ACWY", "Meningococcal B", 
        "Dengue (if endemic)", "Typhoid (Vi)", "Japanese Encephalitis", "Rabies (PEP)",
        "RSV (Arexvy)", "Mpox (Jynneos)", "Cholera (Vaxchora)", "Yellow Fever", "Pentavalent"
    ])

# 🔥 COMPLETE VACCINE DATABASE (25+ Vaccines)
vaccine_data = {
    "COVID-19 (2026)": {"emoji": "🦠", "protection": "96% severe, 99% hospitalization", "age": "6m+", "doses": "1 annual", "benefits": ["Severe COVID prevention", "Long COVID reduction", "Pregnancy safe"], "side": "Mild soreness", "eff": [96,99,85]},
    "Influenza (Annual)": {"emoji": "🌡️", "protection": "60-80% flu", "age": "6m+", "doses": "1 yearly", "benefits": ["Flu prevention", "High-dose seniors"], "side": "Mild soreness", "eff": [70,50,80]},
    "Tdap/Td": {"emoji": "🦠", "protection": "95% pertussis", "age": "10+", "doses": "Every 10y", "benefits": ["Tetanus/diphtheria", "Pregnancy safe"], "side": "Arm soreness", "eff": [95,90,85]},
    "HPV (9v)": {"emoji": "🧬", "protection": "97% cervical cancer", "age": "9-45y", "doses": "2-3 doses", "benefits": ["9 cancer types", "Genital warts"], "side": "Mild pain", "eff": [97,92,88]},
    "Pneumococcal (PCV20)": {"emoji": "🫁", "protection": "90% pneumonia", "age": "Infants+65+", "doses": "4+1", "benefits": ["Pneumonia", "Meningitis"], "side": "Mild fever", "eff": [90,85,92]},
    "Shingles (RZV)": {"emoji": "🔥", "protection": "97% shingles", "age": "50+", "doses": "2 doses", "benefits": ["Shingles", "Neuralgia"], "side": "Fatigue 2-3d", "eff": [97,90,85]},
    "Hepatitis B": {"emoji": "🦠", "protection": "95% lifelong", "age": "Birth+", "doses": "3 doses", "benefits": ["Liver cancer", "Chronic hep"], "side": "Very safe", "eff": [95,92,98]},
    "Hepatitis A": {"emoji": "🦠", "protection": "95% HAV", "age": "12m+", "doses": "2 doses", "benefits": ["Foodborne hepatitis"], "side": "Mild soreness", "eff": [95,90,92]},
    "BCG (TB)": {"emoji": "🫁", "protection": "70-80% childhood TB", "age": "Newborns", "doses": "1 dose", "benefits": ["TB meningitis"], "side": "Local reaction", "eff": [75,70,80]},
    "MMR": {"emoji": "🤒", "protection": "97% measles", "age": "12m, 4y", "doses": "2 doses", "benefits": ["Measles/mumps/rubella"], "side": "Mild rash", "eff": [97,95,92]},
    "Varicella (Chickenpox)": {"emoji": "🤕", "protection": "90% chickenpox", "age": "12m+", "doses": "2 doses", "benefits": ["Chickenpox", "Shingles reduction"], "side": "Mild rash", "eff": [90,85,88]},
    "Rotavirus": {"emoji": "🤮", "protection": "85-98% severe", "age": "6-14w", "doses": "3 oral", "benefits": ["Diarrhea hospitalization"], "side": "Mild GI", "eff": [90,85,95]},
    "Polio (IPV/OPV)": {"emoji": "🦠", "protection": "99% paralysis", "age": "Birth+", "doses": "4-5", "benefits": ["Paralytic polio"], "side": "Very safe", "eff": [99,98,95]},
    "Hib": {"emoji": "🫁", "protection": "95% meningitis", "age": "2m+", "doses": "4 doses", "benefits": ["Meningitis, pneumonia"], "side": "Mild fever", "eff": [95,92,90]},
    "Meningococcal ACWY": {"emoji": "🧠", "protection": "90% meningitis", "age": "11y+", "doses": "1-2 boosters", "benefits": ["Meningitis A,C,W,Y"], "side": "Mild pain", "eff": [90,88,85]},
    "Meningococcal B": {"emoji": "🧠", "protection": "80-90% MenB", "age": "16-23y", "doses": "2-3 doses", "benefits": ["Meningitis B"], "side": "Fatigue", "eff": [85,82,80]},
    "Dengue (if endemic)": {"emoji": "🦟", "protection": "60-80% severe dengue", "age": "4y+ (endemic)", "doses": "3 doses", "benefits": ["Severe dengue"], "side": "Mild fever", "eff": [70,65,60]},
    "Typhoid (Vi)": {"emoji": "🍽️", "protection": "65% typhoid", "age": "2y+", "doses": "Every 3y", "benefits": ["Typhoid fever"], "side": "Mild pain", "eff": [65,60,62]},
    "Japanese Encephalitis": {"emoji": "🧠", "protection": "90% JEV", "age": "9m+ (endemic)", "doses": "2 doses", "benefits": ["Brain inflammation"], "side": "Mild fever", "eff": [90,88,85]},
    "Rabies (PEP)": {"emoji": "🐕", "protection": "100% post-exposure", "age": "All ages", "doses": "4-5 post-bite", "benefits": ["Rabies prevention"], "side": "Mild pain", "eff": [100,99,98]},
    "RSV (Arexvy)": {"emoji": "🫁", "protection": "85% severe RSV", "age": "60+", "doses": "1 dose", "benefits": ["RSV pneumonia"], "side": "Mild fatigue", "eff": [85,82,80]},
    "Mpox (Jynneos)": {"emoji": "🦠", "protection": "85% mpox", "age": "18+", "doses": "2 doses", "benefits": ["Mpox prevention"], "side": "Mild redness", "eff": [85,80,82]},
    "Cholera (Vaxchora)": {"emoji": "💧", "protection": "65% cholera", "age": "18-64y", "doses": "1 oral dose", "benefits": ["Cholera diarrhea"], "side": "Mild GI", "eff": [65,60,62]},
    "Yellow Fever": {"emoji": "🦟", "protection": "99% yellow fever", "age": "9m+ (travel)", "doses": "1 dose/10y", "benefits": ["Yellow fever"], "side": "Mild fever 10%", "eff": [99,98,97]},
    "Pentavalent": {"emoji": "🛡️", "protection": "95% 5 diseases", "age": "6,10,14w", "doses": "3 doses", "benefits": ["DTP+HepB+Hib"], "side": "Mild fever", "eff": [95,92,90]}
}

# AGE RECOMMENDATIONS
st.markdown("---")
col_age, col_vaccine = st.columns([1, 1.2])

with col_age:
    st.markdown("<h3 style='color: #1e293b;'>📅 Age-Based Vaccines</h3>", unsafe_allow_html=True)
    age_groups = {
        range(0,1): "👶 Newborn: BCG, HepB, Polio, Rotavirus, PCV, Pentavalent",
        range(1,5): "🧒 Toddler: MMR, Hib, Pneumococcal, Influenza", 
        range(5,18): "👦 Child/Teen: Tdap, HPV, MenACWY, Typhoid, JE",
        range(18,50): "👩 Adult: COVID, Flu, Tdap, HPV, HepA/B",
        range(50,101): "👴 Senior: Shingles, PCV20, RSV, High-dose Flu/COVID"
    }
    for age_range, vaccines in age_groups.items():
        if age in age_range:
            st.markdown(f"""
            <div class="age-card">
                <div style='font-size: 2.5rem;'>{list(age_range)[0]}{'+' if age_range.stop > age else '-'}</div>
                <div style='font-size: 1.2rem; line-height: 1.6;'>{vaccines}</div>
            </div>
            """, unsafe_allow_html=True)
            break

# VACCINE DETAILS
with col_vaccine:
    vaccine = vaccine_data[selected_vaccine]
    st.markdown(f"""
    <div class="vaccine-detail-card">
        <h2 style='font-size: 2.2rem; margin: 0 0 1rem 0;'>{vaccine['emoji']} {selected_vaccine}</h2>
        <div style='font-size: 1.6rem; opacity: 0.95;'>{vaccine['age']} • {vaccine['doses']}</div>
        <div style='font-size: 2rem; margin: 1.5rem 0; font-weight: 700;'>🛡️ {vaccine['protection']}</div>
    </div>
    """, unsafe_allow_html=True)

# CUSTOM HEALTH + ELIGIBILITY
st.markdown("---")
st.markdown("""
<div class="health-input">
    <h3 style='color: #1e293b; text-align: center;'>🔍 Personalized Assessment</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col2:
    health_conditions = st.multiselect(
        "🏥 Health Conditions",
        ["Pregnant", "Heart disease", "Diabetes", "Cancer", "Weak immune", "Asthma", "Hypertension", "Kidney disease", "None"],
        default=["None"]
    )
    custom_condition = st.text_input("➕ Add condition", placeholder="e.g., arthritis, epilepsy")
    if custom_condition and custom_condition not in health_conditions:
        health_conditions.append(custom_condition)
    
    recent_vax = st.radio("💉 Last COVID vaccine", ["Never", "Within 6 months", "6-12 months", "Over 1 year"])
st.markdown("</div>", unsafe_allow_html=True)

# ELIGIBILITY CHECK
if st.button("🚀 Check Eligibility", type="primary", use_container_width=True):
    eligible = "ELIGIBLE"
    if age < 6: eligible = "PEDIATRIC"
    elif any(c in health_conditions for c in ["Cancer", "Weak immune"]): eligible = "HIGH_PRIORITY"
    elif age >= 65 or "Heart disease" in health_conditions or "Diabetes" in health_conditions: eligible = "HIGH_PRIORITY"
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        status_map = {
            "ELIGIBLE": f"✅ ELIGIBLE FOR {selected_vaccine}",
            "HIGH_PRIORITY": f"🎯 HIGH PRIORITY - {selected_vaccine}", 
            "PEDIATRIC": "👶 PEDIATRIC CONSULT"
        }
        badge_class = "badge-eligible" if eligible != "PEDIATRIC" else "badge-caution"
        st.markdown(f"""
        <div class="{badge_class}" style='text-align: center; padding: 2.5rem; margin: 2rem 0; box-shadow: 0 25px 70px rgba(16,185,129,0.4);'>
            {status_map[eligible]}<br>
            <span style='font-size: 1.2rem;'>Age {age} • {len([c for c in health_conditions if c != 'None'])} conditions</span>
        </div>
        """, unsafe_allow_html=True)

# BENEFITS + CHART
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h4 style='color: #1e293b;'>✨ {selected_vaccine} Benefits</h4>", unsafe_allow_html=True)
    for benefit in vaccine['benefits']:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(16,185,129,0.1)); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; border-left: 5px solid #10b981;'>
            <span style='color: #059669; font-weight: 600;'>{benefit}</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    fig = px.bar(x=['Severe', 'Hospital', 'Mild'], y=vaccine['eff'], color=vaccine['eff'], 
                color_continuous_scale='teal', title=f"{selected_vaccine} Protection")
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# SAFETY
with st.expander(f"ℹ️ {selected_vaccine} Safety", expanded=True):
    col1, col2 = st.columns(2)
    with col1: st.markdown(f"**⚠️ Side Effects:** {vaccine['side']}")
    with col2: st.markdown(f"**✅ For:** {vaccine['age']}")

# FINAL CTA
st.markdown("""
<div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 32px; padding: 5rem; margin: 5rem 0; text-align: center; color: white; box-shadow: 0 50px 120px rgba(16,185,129,0.4);'>
    <div style='font-size: 6rem;'>🎯</div>
    <h2 style='font-size: 3rem;'>Ready to Get Protected?</h2>
    <p style='font-size: 1.8rem;'>Consult your healthcare provider to schedule</p>
    <div style='font-size: 2.5rem; background: rgba(255,255,255,0.2); padding: 2rem 4rem; border-radius: 30px; display: inline-block;'>
        📞 Contact Your Doctor Today!
    </div>
</div>
""", unsafe_allow_html=True)

render_footer(
    title="VaxiPredict Vaccine Library",
    subtitle="Comprehensive vaccine guidance • Safety & scheduling",
    meta="Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    icon="🩺"
)

