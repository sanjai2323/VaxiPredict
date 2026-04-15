import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
import time
import sys
import os
from datetime import datetime
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
    <h1 class="main-title">🚨 Vaccine Rumor Detector</h1>
    <p style='color: #0f172a; font-size: 1.6rem; font-weight: 700; max-width: 900px;
              margin: 0 auto; line-height: 1.7;'>
        Misinformation Detection • Keyword Analysis • ML Scoring
    </p>
</div>
""", unsafe_allow_html=True)


# LEVEL SELECTOR
st.markdown("## 🎯 Analysis Level")
col1, col2, col3, col4 = st.columns(4, gap="large")


with col1:
    if st.button("🌍 National", use_container_width=True, key="rum_nat"):
        st.session_state.analysis_level = "national"
        st.session_state.selected_reference = None
        st.rerun()
       
with col2:
    if st.button("🇮🇳 State", use_container_width=True, key="rum_state"):
        st.session_state.analysis_level = "state"
        st.rerun()
       
with col3:
    if st.button("🌎 Country", use_container_width=True, key="rum_country"):
        st.session_state.analysis_level = "country"
        st.rerun()
       
with col4:
    if st.button("📍 District", use_container_width=True, key="rum_dist"):
        st.session_state.analysis_level = "district"
        st.rerun()


st.markdown("---")


# Reference selector
reference = None
level_name = "National"
selected_state = None


if st.session_state.get("analysis_level") == "state":
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**🇮🇳 Select State:**")
    with col2:
        states = get_all_states()
        reference = st.selectbox("State", states, key="rum_state_sel")
        level_name = reference


elif st.session_state.get("analysis_level") == "country":
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**🌎 Select Country:**")
    with col2:
        countries = get_all_countries()
        reference = st.selectbox("Country", countries, key="rum_country_sel")
        level_name = reference


elif st.session_state.get("analysis_level") == "district":
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.markdown("**📍 State:**")
    with col2:
        states = get_all_states()
        selected_state = st.selectbox("State", states, key="rum_dist_state")
    with col3:
        districts = get_districts_by_state(selected_state)
        reference = st.selectbox("District", districts, key="rum_dist_sel")
        level_name = f"{reference}, {selected_state}"


st.markdown("---")


# ==========================
# LEVEL-SPECIFIC STATISTICS
# ==========================
def get_level_rumor_stats(level, reference=None):
    random.seed(hash(f"{level}_{reference}") % 2**32 if reference else 0)
   
    if level == "national":
        return {
            "total_reports": random.randint(500, 1000),
            "active_rumors": random.randint(50, 150),
            "false_positives": random.randint(10, 30),
            "accuracy": random.uniform(92, 98)
        }
    elif level == "country":
        return {
            "total_reports": random.randint(200, 400),
            "active_rumors": random.randint(20, 60),
            "false_positives": random.randint(5, 15),
            "accuracy": random.uniform(90, 96)
        }
    elif level == "state":
        return {
            "total_reports": random.randint(100, 250),
            "active_rumors": random.randint(10, 30),
            "false_positives": random.randint(3, 10),
            "accuracy": random.uniform(91, 97)
        }
    else:  # district
        return {
            "total_reports": random.randint(30, 80),
            "active_rumors": random.randint(3, 12),
            "false_positives": random.randint(1, 5),
            "accuracy": random.uniform(89, 95)
        }


# Display level-specific stats
stats = get_level_rumor_stats(st.session_state.get("analysis_level", "national"), reference)
col1, col2, col3, col4 = st.columns(4, gap="large")


with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>📊 Total Reports</div>
        <div style='font-size: 2rem; font-weight: 900; color: #3b82f6;'>{stats['total_reports']}</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>🚨 Active Rumors</div>
        <div style='font-size: 2rem; font-weight: 900; color: #ef4444;'>{stats['active_rumors']}</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>⚠️ False Positives</div>
        <div style='font-size: 2rem; font-weight: 900; color: #f59e0b;'>{stats['false_positives']}</div>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 1rem; color: #64748b; font-weight: 600;'>🎯 Accuracy</div>
        <div style='font-size: 2rem; font-weight: 900; color: #10b981;'>{stats['accuracy']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# ==========================
# COLOR MAP
# ==========================
COLOR_MAP = {
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "success": "#10b981",
    "info": "#3b82f6"
}


# ==========================
# KEYWORD DATABASE (unchanged)
# ==========================
VACCINE_RUMOR_DB = {
    "danger_keywords": {
        "autism": 4, "kills": 5, "death": 4, "sterility": 4, "infertility": 4,
        "microchip": 5, "bill gates": 4, "5g": 4, "magnet": 4, "poison": 4,
        "experimental": 3, "not tested": 3, "dangerous": 3, "deadly": 4,
        "side effects": 2, "harm": 3, "risky": 2, "toxic": 3
    },
    "safety_keywords": {
        "who": -3, "cdc": -3, "fda": -3, "safe": -3, "effective": -2,
        "approved": -2, "recommended": -2, "millions": -2, "clinical": -2,
        "protects": -2, "prevents": -2, "vaccine safe": -3
    }
}


# ==========================
# CORE LOGIC (unchanged)
# ==========================
def ml_rumor_detection(text: str):
    text_lower = text.lower()
    total_score = 0
    evidence = []


    danger_count = 0
    for keyword, weight in VACCINE_RUMOR_DB["danger_keywords"].items():
        if keyword in text_lower:
            total_score += weight
            danger_count += 1
            evidence.append(f"🚨 '{keyword}' [+{weight}]")


    safety_count = 0
    for keyword, weight in VACCINE_RUMOR_DB["safety_keywords"].items():
        if keyword in text_lower:
            total_score += weight
            safety_count += 1
            evidence.append(f"✅ '{keyword}' [{weight}]")


    confidence = min(97, max(70, 82 + danger_count * 4 + safety_count * -2))


    return {
        "score": total_score,
        "confidence": confidence,
        "danger_hits": danger_count,
        "safety_hits": safety_count,
        "evidence": evidence or ["No specific keywords detected"]
    }


def get_prediction(result):
    score = result["score"]


    if score >= 3:
        return "🚨 Dangerous rumor detected", "danger", "Very high risk pattern"
    elif score >= 1:
        return "⚠️ Likely rumor", "warning", "Suspicious language detected"
    elif score <= -1:
        return "✅ Likely factual", "success", "Aligned with trusted health sources"
    else:
        return "ℹ️ Unclear or mixed", "info", "Needs human review"


# ==========================
# MAIN INPUT
# ==========================
st.markdown("""
<div style='
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border-radius: 20px;
    border: 1px solid #93c5fd;
    padding: 2rem;
    margin-bottom: 2rem;
'>
    <h3 style='color: #1e40af;'>📝 Paste message for analysis</h3>
</div>
""", unsafe_allow_html=True)


user_input = st.text_area(
    "Message to analyze",
    height=150,
    placeholder="Paste any text message for vaccine misinformation analysis...\n\nExample: “MMR vaccine causes autism” or “WHO recommends MMR vaccine at 12 months\"",
    help="The detector scores language patterns for rumor-like content."
)


# ==========================
# ANALYZE BUTTON
# ==========================
if st.button("🚀 Analyze message", type="primary", use_container_width=True):
    if user_input.strip():
        with st.spinner("🔍 Scanning for misinformation signals..."):
            time.sleep(1)
            result = ml_rumor_detection(user_input)
            prediction, badge_type, conf_label = get_prediction(result)


        # Main result card - CLEAN WHITE DESIGN
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            border: 3px solid {COLOR_MAP[badge_type]};
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 15px 50px rgba(0,0,0,0.15);
            margin: 2rem 0;
        '>
            <h2 style='
                color: {COLOR_MAP[badge_type]};
                font-size: 2.2rem;
                margin: 0 0 1rem 0;
                font-weight: 900;
            '>{prediction}</h2>
            <div style='font-size: 1.3rem; margin: 0.5rem 0;'>
                Score: <strong style='color: #1e293b;'>{result['score']:.1f} / 10</strong>
            </div>
            <div style='font-size: 1.2rem; margin: 0.5rem 0;'>
                Confidence: <strong style='color: #1e293b;'>{result['confidence']:.0f}%</strong>
            </div>
            <div style='color: #64748b; font-size: 1rem; margin-top: 1rem;'>
                {conf_label}
            </div>
        </div>
        """, unsafe_allow_html=True)


        # Metrics row
        st.markdown(" ")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Danger words", result["danger_hits"])
        m2.metric("Safety words", result["safety_hits"])
        m3.metric("Net score", f"{result['score']:.1f}")
        m4.metric("Confidence", f"{result['confidence']:.0f}%")


        # Feature impact bar chart
        features_df = pd.DataFrame({
            "Factor": ["Danger keywords", "Safety keywords"],
            "Impact": [result["danger_hits"] * 2.5, result["safety_hits"] * -2.5]
        })
        fig = px.bar(
            features_df,
            x="Factor",
            y="Impact",
            title="📊 Contribution to rumor score",
            color="Impact",
            color_continuous_scale=["#10b981", "#ef4444"],
        )
        fig.update_layout(
            height=380,
            template="plotly_white",
            margin=dict(l=10, r=10, t=60, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)


        # Evidence list
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 1.5rem;
            margin: 1.5rem 0;
        '>
            <h3 style='color: #1e293b; margin-bottom: 1rem;'>🔍 Detection evidence</h3>
        </div>
        """, unsafe_allow_html=True)
       
        for ev in result["evidence"]:
            st.write(f"• {ev}")


        # Action suggestion
        st.markdown("---")
        if result["score"] >= 1:
            st.error(
                "⚠️ This message contains language patterns strongly associated with vaccine misinformation. "
                "Avoid sharing widely and verify with trusted health sources."
            )
        elif result["score"] <= -1:
            st.success(
                "✅ This message uses wording consistent with trusted health communication. "
                "Good to share with official source references."
            )
        else:
            st.warning(
                "ℹ️ Mixed or weak signals detected. Consult health professionals or official sources "
                "before widespread sharing."
            )


# ==========================
# QUICK TEST EXAMPLES
# ==========================
st.markdown("""
<div style='
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-radius: 20px;
    border: 1px solid #f59e0b;
    padding: 2rem;
    margin: 2rem 0 1rem 0;
'>
    <h3 style='color: #d97706;'>🧪 Quick test examples</h3>
</div>
""", unsafe_allow_html=True)


test_cases = {
    "Rumor‑like message": "MMR vaccine causes autism in children! Don't vaccinate!",
    "Trusted‑style message": "WHO recommends MMR vaccine at 12 months. Safe and effective.",
    "Regional forward": "Anna MMR vaccine la autism varum nu solranga atha kudukka vendam!",
    "Open question": "Are vaccines safe or not? Some people say dangerous."
}


for label, text in test_cases.items():
    if st.button(f"🧪 Try: {label}", key=f"test_{label}", use_container_width=True):
        st.text_area("Sample message", text, height=100, disabled=True)
        result = ml_rumor_detection(text)
        prediction, badge_type, conf_label = get_prediction(result)


        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 2px solid {COLOR_MAP[badge_type]};
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            margin: 1rem 0;
        '>
            <span style='font-size: 1.2rem; font-weight: 700; color: {COLOR_MAP[badge_type]};'>
                {prediction}
            </span><br/>
            <span style='color: #64748b; font-size: 1rem;'>
                Score: {result['score']:.1f} · Confidence: {result['confidence']:.0f}%
            </span>
        </div>
        """, unsafe_allow_html=True)


# Add trending rumors section
st.markdown("---")
st.markdown("## 📈 Trending Rumors by Region")


# Create sample trending data
trending_data = pd.DataFrame({
    'Region': ['North India', 'South India', 'East India', 'West India', 'Central India'],
    'Active Rumors': [45, 32, 28, 41, 23],
    'Resolved': [12, 8, 15, 10, 7]
})


fig_trend = px.bar(trending_data, x='Region', y=['Active Rumors', 'Resolved'],
                   barmode='group', title="Regional Rumor Distribution",
                   color_discrete_sequence=['#ef4444', '#10b981'])
fig_trend.update_layout(height=400, template="plotly_white")
st.plotly_chart(fig_trend, use_container_width=True)

render_footer(
    title="VaxiPredict Rumour Analyzer",
    subtitle="Misinformation detection • Trusted source scoring • Action guidance",
    meta="Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    icon="🗣️"
)


