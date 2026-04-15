import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import sys
import os
import random


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.level_data import (
    get_all_states, get_all_countries, get_all_districts,
    get_districts_by_state, get_regions_by_country,
    BASE_HESITANCY_BY_AGE
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
    <h1 class="main-title">🌐 Social & Communication Networks</h1>
    <p style='color: #0f172a; font-size: 1.6rem; font-weight: 700; max-width: 900px;
              margin: 0 auto; line-height: 1.7;'>
        Influence Mapping • Community Engagement • Network Analysis
    </p>
</div>
""", unsafe_allow_html=True)


# LEVEL SELECTOR
st.markdown("## 🎯 Analysis Level")
col1, col2, col3, col4 = st.columns(4, gap="large")


with col1:
    if st.button("🌍 National", use_container_width=True, key="net_nat"):
        st.session_state.analysis_level = "national"
        st.session_state.selected_reference = None
        st.rerun()
       
with col2:
    if st.button("🇮🇳 State", use_container_width=True, key="net_state"):
        st.session_state.analysis_level = "state"
        st.rerun()
       
with col3:
    if st.button("🌎 Country", use_container_width=True, key="net_country"):
        st.session_state.analysis_level = "country"
        st.rerun()
       
with col4:
    if st.button("📍 District", use_container_width=True, key="net_dist"):
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
        reference = st.selectbox("State", states, key="net_state_sel")
        level_name = reference


elif st.session_state.get("analysis_level") == "country":
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**🌎 Select Country:**")
    with col2:
        countries = get_all_countries()
        reference = st.selectbox("Country", countries, key="net_country_sel")
        level_name = reference


elif st.session_state.get("analysis_level") == "district":
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.markdown("**📍 State:**")
    with col2:
        states = get_all_states()
        selected_state = st.selectbox("State", states, key="net_dist_state")
    with col3:
        districts = get_districts_by_state(selected_state)
        reference = st.selectbox("District", districts, key="net_dist_sel")
        level_name = f"{reference}, {selected_state}"


st.markdown("---")


# Generate level-specific network metrics
def get_network_metrics(level, reference=None):
    random.seed(hash(f"{level}_{reference}") % 2**32 if reference else 0)
   
    if level == "national":
        return {
            "key_influencers": 47,
            "connected_groups": 12,
            "campaign_reach": 78.5,
            "engagement_rate": 64.2,
            "total_nodes": 1247,
            "total_connections": 8456,
            "avg_connections": 6.8,
            "primary_influencers": 15,
            "secondary_nodes": 28,
            "community_members": 234,
            "passive_followers": 512
        }
    elif level == "state":
        return {
            "key_influencers": random.randint(25, 40),
            "connected_groups": random.randint(8, 15),
            "campaign_reach": random.uniform(65, 85),
            "engagement_rate": random.uniform(55, 75),
            "total_nodes": random.randint(600, 1000),
            "total_connections": random.randint(4000, 7000),
            "avg_connections": random.uniform(5.5, 7.5),
            "primary_influencers": random.randint(8, 18),
            "secondary_nodes": random.randint(15, 30),
            "community_members": random.randint(150, 250),
            "passive_followers": random.randint(300, 450)
        }
    elif level == "country":
        return {
            "key_influencers": random.randint(50, 80),
            "connected_groups": random.randint(15, 25),
            "campaign_reach": random.uniform(70, 90),
            "engagement_rate": random.uniform(60, 80),
            "total_nodes": random.randint(2000, 3000),
            "total_connections": random.randint(15000, 25000),
            "avg_connections": random.uniform(7.0, 9.0),
            "primary_influencers": random.randint(20, 35),
            "secondary_nodes": random.randint(40, 60),
            "community_members": random.randint(400, 600),
            "passive_followers": random.randint(800, 1200)
        }
    else:  # district
        return {
            "key_influencers": random.randint(15, 30),
            "connected_groups": random.randint(5, 12),
            "campaign_reach": random.uniform(60, 80),
            "engagement_rate": random.uniform(50, 70),
            "total_nodes": random.randint(300, 500),
            "total_connections": random.randint(2000, 3500),
            "avg_connections": random.uniform(5.0, 7.0),
            "primary_influencers": random.randint(5, 12),
            "secondary_nodes": random.randint(10, 20),
            "community_members": random.randint(80, 150),
            "passive_followers": random.randint(150, 250)
        }


metrics = get_network_metrics(st.session_state.get("analysis_level", "national"), reference)


st.markdown("---")


# KEY METRICS
col1, col2, col3, col4 = st.columns(4, gap="large")


with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title" style='color: #ec4899;'>👥 Key Influencers</div>
        <div class="metric-value">{metrics['key_influencers']}</div>
    </div>
    """, unsafe_allow_html=True)
   
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title" style='color: #f97316;'>🔗 Connected Groups</div>
        <div class="metric-value">{metrics['connected_groups']}</div>
    </div>
    """, unsafe_allow_html=True)
   
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title" style='color: #22c55e;'>📱 Campaign Reach</div>
        <div class="metric-value">{metrics['campaign_reach']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
   
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title" style='color: #06b6d4;'>💬 Engagement Rate</div>
        <div class="metric-value">{metrics['engagement_rate']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# NETWORK VISUALIZATION - Enhanced based on level
st.markdown("## 🔗 Network Influence Map")
col1, col2 = st.columns([2, 1], gap="large")


with col1:
    st.subheader(f"🌐 {level_name} Network Structure")

    # Dynamic network size based on level
    if st.session_state.get("analysis_level") == "national":
        size = 20
    elif st.session_state.get("analysis_level") == "country":
        size = 18
    elif st.session_state.get("analysis_level") == "state":
        size = 15
    else:  # district
        size = 12

    np.random.seed(hash(f"{level_name}") % 2**32)
    network_data = np.random.rand(size, size)
    network_data = (network_data + network_data.T) / 2  # Make symmetric
    np.fill_diagonal(network_data, 1)  # Self connections

    # Create network visualization
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=network_data,
        colorscale='Viridis',
        showscale=True,
        hovertemplate='Connection Strength: %{z:.2f}<extra></extra>',
        name='Network Connections'
    ))

    fig.update_layout(
        height=500,
        template="plotly_white",
        title="",
        xaxis_title="Network Nodes",
        yaxis_title="Network Nodes",
        plot_bgcolor='rgba(240, 249, 255, 0.5)'
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    st.subheader("📊 Node Categories")
    st.markdown("---")

    # Node categories with dynamic values
    st.markdown(f"""
    <div style='margin: 1rem 0; padding: 1rem; background: rgba(236, 72, 153, 0.1);
                border-left: 4px solid #ec4899; border-radius: 8px;'>
        <div style='font-weight: 700; color: #ec4899;'>🟢 Primary Influencers</div>
        <div style='font-size: 1.5rem; font-weight: 900;'>{metrics['primary_influencers']}</div>
        <div style='font-size: 0.8rem; color: #64748b;'>High-reach community leaders</div>
    </div>

    <div style='margin: 1rem 0; padding: 1rem; background: rgba(249, 115, 22, 0.1);
                border-left: 4px solid #f97316; border-radius: 8px;'>
        <div style='font-weight: 700; color: #f97316;'>🟡 Secondary Nodes</div>
        <div style='font-size: 1.5rem; font-weight: 900;'>{metrics['secondary_nodes']}</div>
        <div style='font-size: 0.8rem; color: #64748b;'>Active community connectors</div>
    </div>

    <div style='margin: 1rem 0; padding: 1rem; background: rgba(34, 197, 94, 0.1);
                border-left: 4px solid #22c55e; border-radius: 8px;'>
        <div style='font-weight: 700; color: #22c55e;'>🔵 Community Members</div>
        <div style='font-size: 1.5rem; font-weight: 900;'>{metrics['community_members']}</div>
        <div style='font-size: 0.8rem; color: #64748b;'>Regular engaged participants</div>
    </div>

    <div style='margin: 1rem 0; padding: 1rem; background: rgba(6, 182, 212, 0.1);
                border-left: 4px solid #06b6d4; border-radius: 8px;'>
        <div style='font-weight: 700; color: #06b6d4;'>🟣 Passive Followers</div>
        <div style='font-size: 1.5rem; font-weight: 900;'>{metrics['passive_followers']}</div>
        <div style='font-size: 0.8rem; color: #64748b;'>Information receivers</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# COMMUNICATION CHANNELS - Enhanced with level-specific data
st.markdown("## 📡 Active Communication Channels")


def get_channel_data(level):
    random.seed(hash(f"{level}_channels") % 2**32)
   
    base_channels = ["WhatsApp Groups", "Facebook Communities", "Email Lists", "SMS Networks", "Community Centers"]
   
    if level == "national":
        multipliers = [1.0, 0.9, 0.8, 0.7, 0.6]
    elif level == "country":
        multipliers = [0.9, 0.8, 0.7, 0.6, 0.5]
    elif level == "state":
        multipliers = [0.7, 0.6, 0.5, 0.4, 0.3]
    else:  # district
        multipliers = [0.5, 0.4, 0.3, 0.2, 0.1]
   
    reach = [int(450 * m) for m in multipliers]
    engagement = [int(85 * m) for m in multipliers]
   
    return pd.DataFrame({
        "Channel": base_channels,
        "Reach": reach,
        "Engagement": engagement
    })


df_ch = get_channel_data(st.session_state.get("analysis_level", "national"))


# Create side-by-side bar chart
fig_channels = go.Figure()


fig_channels.add_trace(go.Bar(
    y=df_ch["Channel"],
    x=df_ch["Reach"],
    name="Reach",
    orientation='h',
    marker=dict(color='#3b82f6'),
    text=df_ch["Reach"],
    textposition='outside'
))


fig_channels.add_trace(go.Bar(
    y=df_ch["Channel"],
    x=df_ch["Engagement"],
    name="Engagement",
    orientation='h',
    marker=dict(color='#ec4899'),
    text=df_ch["Engagement"],
    textposition='outside',
    opacity=0.7
))


fig_channels.update_layout(
    height=450,
    template="plotly_white",
    title=f"Channel Performance - {level_name}",
    barmode='group',
    plot_bgcolor='rgba(240, 249, 255, 0.5)',
    xaxis_title="Number of Users",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)


st.plotly_chart(fig_channels, use_container_width=True)


# Add network statistics with level-specific values
st.markdown("---")
col1, col2, col3 = st.columns(3, gap="large")


with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 2rem; font-weight: 900; color: #ec4899;'>{metrics['total_nodes']:,}</div>
        <div style='color: #64748b;'>Total Network Nodes</div>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 2rem; font-weight: 900; color: #f97316;'>{metrics['total_connections']:,}</div>
        <div style='color: #64748b;'>Network Connections</div>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 20px; padding: 1.5rem; border: 2px solid #06b6d4;
                text-align: center;'>
        <div style='font-size: 2rem; font-weight: 900; color: #22c55e;'>{metrics['avg_connections']:.1f}</div>
        <div style='color: #64748b;'>Avg Connections/Node</div>
    </div>
    """, unsafe_allow_html=True)


# Add network health gauge
st.markdown("---")
st.markdown("## 📊 Network Health Dashboard")


col1, col2 = st.columns(2, gap="large")


with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 24px; padding: 2rem; border: 3px solid #06b6d4;'>
    """, unsafe_allow_html=True)
   
    st.markdown("### 🎯 Network Density")
   
    # Calculate network density
    total_possible = metrics['total_nodes'] * (metrics['total_nodes'] - 1) / 2
    density = (metrics['total_connections'] / total_possible * 100) if total_possible > 0 else 0
   
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=min(density, 100),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Connection Density %"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#06b6d4"},
            'steps': [
                {'range': [0, 30], 'color': "#fee2e2"},
                {'range': [30, 60], 'color': "#fef3c7"},
                {'range': [60, 100], 'color': "#d1fae5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 65
            }
        }
    ))
   
    fig_gauge.update_layout(height=300, template="plotly_white")
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
                border-radius: 24px; padding: 2rem; border: 3px solid #06b6d4;'>
    """, unsafe_allow_html=True)
   
    st.markdown("### 📈 Network Growth")
   
    # Generate growth data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    growth_data = pd.DataFrame({
        'Month': months,
        'New Nodes': np.random.randint(20, 100, 6),
        'New Connections': np.random.randint(100, 500, 6)
    })
   
    fig_growth = px.line(growth_data, x='Month', y=['New Nodes', 'New Connections'],
                         title="", markers=True)
    fig_growth.update_layout(
        height=300,
        template="plotly_white",
        plot_bgcolor='rgba(240, 249, 255, 0.5)'
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

render_footer(
    title="VaxiPredict Network Insights",
    subtitle="Community graphs • Influence mapping • Engagement analytics",
    meta=f"{level_name} • Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    icon="🌐"
)


