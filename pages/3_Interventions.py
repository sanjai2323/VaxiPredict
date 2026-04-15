import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

from utils.ui_components import apply_global_theme, render_footer

st.set_page_config(page_title="💉 VaxiPredict Interventions", layout="wide")
apply_global_theme()

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
    st.error("🔐 **Access Denied** - Please login from Dashboard")
    st.stop()

# 🧠 HERO SECTION
st.markdown("""
<div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%); 
            border-radius: 28px; padding: 4rem; margin: 2rem 0; 
            box-shadow: 0 40px 120px rgba(6, 182, 212, 0.15); text-align: center; 
            border: 2px solid rgba(6, 182, 212, 0.3);'>
    <h1 style='font-size: 4rem; font-weight: 900; color: #0f172a; text-align: center; 
                margin-bottom: 1.8rem;'>
        💉 Vaccine Hesitancy Interventions
    </h1>
    <p style='font-size: 1.8rem; color: #334155; text-align: center; 
              font-weight: 700; max-width: 950px; margin: 0 auto; line-height: 1.6;'>
        Targeted Campaigns • Real-time Impact Simulation • Data-Driven Strategies
    </p>
</div>
""", unsafe_allow_html=True)

# 📍 LEVEL SELECTOR - COMPACT BUTTONS
st.markdown("### 🎯 **Select Analysis Level**")
col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    if st.button("🌍 **National**", use_container_width=True, type="primary"):
        st.session_state.analysis_level = "national"
        st.session_state.selected_reference = None
        st.rerun()

with col2:
    if st.button("🇮🇳 **State**", use_container_width=True):
        st.session_state.analysis_level = "state"
        st.rerun()

with col3:
    if st.button("🌎 **Country**", use_container_width=True):
        st.session_state.analysis_level = "country"
        st.rerun()

with col4:
    if st.button("📍 **District**", use_container_width=True):
        st.session_state.analysis_level = "district"
        st.rerun()

st.markdown("---")

# Smart selector with mock data
reference = None
level_name = "National"
selected_state = None

# MOCK DATA
STATES = ["Tamil Nadu", "Maharashtra", "Uttar Pradesh", "Kerala", "Delhi"]
DISTRICTS = ["Coimbatore", "Chennai", "Madurai", "Salem", "Tiruppur"]
COUNTRIES = ["India", "Bangladesh", "Pakistan", "Nepal", "Sri Lanka"]

if st.session_state.get("analysis_level") == "state":
    col1, col2 = st.columns([1, 4])
    with col1: st.markdown("**🇮🇳 State:**")
    with col2: reference = st.selectbox("Select State", STATES, key="int_state_selector")
    level_name = reference or "National"

elif st.session_state.get("analysis_level") == "country":
    col1, col2 = st.columns([1, 4])
    with col1: st.markdown("**🌍 Country:**")
    with col2: reference = st.selectbox("Select Country", COUNTRIES, key="int_country_selector")
    level_name = reference or "National"

elif st.session_state.get("analysis_level") == "district":
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1: st.markdown("**🇮🇳 State:**")
    with col2: selected_state = st.selectbox("State", STATES, key="int_district_state")
    with col3: reference = st.selectbox("District", DISTRICTS, key="int_district_selector")
    level_name = reference or "National"

st.markdown("---")

# 🎯 AGE GROUP SELECTION
st.markdown("### 🎛️ **Age Group Intervention Planning**")
col1, col2 = st.columns([1, 4], gap="large")

# MOCK AGE DATA
BASE_HESITANCY_BY_AGE = {
    "0-17": 18.5, "18-29": 28.1, "30-44": 31.4, 
    "45-59": 37.7, "60+": 42.3
}

with col1:
    st.markdown("**Select Age Group:**")
    selected_age = st.selectbox("", list(BASE_HESITANCY_BY_AGE.keys()), key="int_age_selector")

with col2:
    hesitancy = BASE_HESITANCY_BY_AGE[selected_age]
    if hesitancy < 25:
        color, label = "#22c55e", "🟢 LOW PRIORITY"
    elif hesitancy < 50:
        color, label = "#eab308", "🟡 MEDIUM PRIORITY"
    else:
        color, label = "#ef4444", "🔴 HIGH PRIORITY"
    
    st.markdown(f"""
    <div class="metric-card" style='background: rgba(6,182,212,0.08); border-left: 6px solid {color};'>
        <div style='font-weight: 700; color: #0f172a; font-size: 1.1rem;'>{selected_age}</div>
        <div style='font-size: 2.8rem; font-weight: 900; color: {color}; margin: 0.5rem 0;'>{hesitancy:.1f}%</div>
        <div style='color: {color}; font-weight: 700; font-size: 1.1rem;'>{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 🚀 INTERVENTION STRATEGIES
st.markdown("### 🚀 **Choose Intervention Strategy**")
col1, col2, col3 = st.columns(3, gap="large")

strategies = [
    ("📚 Basic Education", 0.8, "#22c55e"),
    ("📢 Focused Outreach", 1.3, "#f97316"), 
    ("🚀 Multi-Channel", 1.8, "#ec4899")
]

for i, (name, effect, color) in enumerate(strategies):
    with locals()[f'col{i+1}']:
        if st.button(name, use_container_width=True, type="secondary"):
            st.session_state.selected_strategy = i
            st.rerun()

selected_strategy_idx = st.session_state.get("selected_strategy", 1)
strategy_name, effect_scale, strategy_color = strategies[selected_strategy_idx]

# INTERVENTION SIMULATION
@st.cache_data
def simulate_intervention(start_hesitancy, effect_scale, strategy_name, days=90):
    np.random.seed(42 + hash(strategy_name) % 100)
    dates = pd.date_range(start=datetime.now(), periods=days, freq="D")
    
    baseline = [start_hesitancy]
    for i in range(1, days):
        drift = 0.01 + np.random.normal(0, 0.015)
        baseline.append(max(5, min(95, baseline[-1] + drift)))
    
    intervention = [start_hesitancy]
    for i in range(1, days):
        if i < 15: change = np.random.normal(-0.05, 0.2)
        else: change = -0.15 * effect_scale + np.random.normal(0, 0.25)
        intervention.append(max(5, min(95, intervention[-1] + change)))
    
    return pd.DataFrame({"Date": dates, "No Intervention": baseline, "With Strategy": intervention})

df_sim = simulate_intervention(hesitancy, effect_scale, strategy_name)

st.markdown("---")

# 📈 IMPACT VISUALIZATION
col1, col2 = st.columns([2, 1], gap="large")
with col1:
    st.markdown("### 📈 **90-Day Intervention Impact**")
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=df_sim["Date"], y=df_sim["No Intervention"],
                                name="Without Strategy", line=dict(color="#cbd5e1", width=3, dash="dot")))
    fig_sim.add_trace(go.Scatter(x=df_sim["Date"], y=df_sim["With Strategy"],
                                name=strategy_name, line=dict(color=strategy_color, width=4),
                                fill="tonexty", fillcolor=f"rgba(236,72,153,0.15)"))
    fig_sim.update_layout(height=450, template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig_sim, use_container_width=True)

with col2:
    reduction = df_sim["No Intervention"].iloc[-1] - df_sim["With Strategy"].iloc[-1]
    reduction_pct = (reduction / df_sim["No Intervention"].iloc[-1]) * 100
    
    st.markdown(f"""
    <div class="strategy-card">
        <div style='font-size: 1rem; color: #64748b; font-weight: 700; margin-bottom: 1rem;'>Expected Impact</div>
        <div style='font-size: 3rem; font-weight: 900; color: {strategy_color};'>{reduction:.1f}%</div>
        <div style='font-size: 0.95rem; color: #64748b; margin-top: 0.5rem;'>
            Absolute reduction<br><strong>{reduction_pct:.1f}%</strong> relative
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 🌈 PRIORITY MATRIX
st.markdown("### 🌈 **Population Priority Matrix**")
df_matrix = pd.DataFrame(list(BASE_HESITANCY_BY_AGE.items()), columns=["Age Group", "Hesitancy"])

fig_matrix = px.bar(df_matrix.sort_values("Hesitancy", ascending=True), 
                   y="Age Group", x="Hesitancy", orientation="h",
                   color="Hesitancy", color_continuous_scale=["#22c55e", "#eab308", "#ef4444"])
fig_matrix.update_layout(height=450, template="plotly_white")
st.plotly_chart(fig_matrix, use_container_width=True)

st.markdown("---")

# 💡 RECOMMENDATIONS
st.markdown("### 💡 **Strategic Recommendations**")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### ✅ **Best Practices**")
    st.success("👩‍⚕️ Local health worker engagement")
    st.success("🎭 Peer testimonials & stories") 
    st.success("🌍 Multi-lingual materials")
    st.success("🏕️ Mobile vaccination camps")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 **Success Metrics**")
    st.info("📈 Weekly engagement tracking")
    st.info("📉 Bi-weekly hesitancy surveys") 
    st.info("💬 Monthly community feedback")
    st.info("⚡ Real-time strategy adjustment")
    st.markdown('</div>', unsafe_allow_html=True)

# ✨ BRIGHT FOOTER
render_footer(
    title="VaxiPredict Intervention Engine",
    subtitle="Targeted Strategies • Real-time Impact • Adaptive Insights",
    meta=f"{level_name} Level • {selected_age} Group • {strategy_name} • Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}",
    icon="💉"
)

