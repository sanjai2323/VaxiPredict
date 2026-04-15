import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import io

# PDF LIBRARIES
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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

# 🔐 LOGIN CHECK
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.markdown("🔐 Please login from Dashboard")
    st.stop()

# HERO SECTION
st.markdown("""
<div class="report-hero">
    <h1 style='font-size: 3.5rem; font-weight: 900;'>📄 Comprehensive Reports</h1>
    <p style='font-size: 1.3rem;'>Real-time Analysis & Export Management</p>
</div>
""", unsafe_allow_html=True)

# SAMPLE DATA
np.random.seed(42)
report_data = pd.DataFrame({
    'Region': [f'Region {i}' for i in range(1, 11)],
    'Hesitancy %': np.random.uniform(15, 75, 10),
    'Risk Level': np.random.choice(['HIGH', 'MEDIUM', 'LOW'], 10),
    'Population': np.random.randint(50000, 500000, 10),
    'Recommendation': np.random.choice(['SMS Campaign', 'Community Event', 'School Drive', 'Healthcare Partner'], 10),
    'Priority': np.random.choice(['🔴 Critical', '🟡 High', '🟢 Routine'], 10)
})

# SUMMARY
st.markdown("### 📊 Quick Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Regions", len(report_data))
col2.metric("High Risk", len(report_data[report_data['Risk Level'] == 'HIGH']))
col3.metric("Avg Hesitancy", f"{report_data['Hesitancy %'].mean():.1f}%")
col4.metric("Population", f"{report_data['Population'].sum()/1_000_000:.1f}M")

# TABLE
st.markdown("### 🗂️ Regional Breakdown")
st.dataframe(report_data, use_container_width=True)

# ACTIONS
st.markdown("### 🎯 Recommended Actions")
col1, col2 = st.columns(2)

with col1:
    st.success("""
    ✅ Immediate Actions:
    - Contact high-risk regions
    - Launch SMS campaigns
    - Conduct awareness drives
    """)

with col2:
    st.warning("""
    ⏳ Follow-up Actions:
    - Monitor trends weekly
    - Evaluate campaigns
    - Update strategies
    """)

# 📄 PDF GENERATION FUNCTION
def generate_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("VaxiPredict Report", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Regions: {len(data)}", styles['Normal']))
    elements.append(Paragraph(f"Average Hesitancy: {data['Hesitancy %'].mean():.2f}%", styles['Normal']))
    elements.append(Spacer(1, 12))

    table_data = [["Region", "Hesitancy %", "Risk", "Population"]]

    for _, row in data.iterrows():
        table_data.append([
            row["Region"],
            f"{row['Hesitancy %']:.1f}%",
            row["Risk Level"],
            str(row["Population"])
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

# EXPORT SECTION
st.markdown("### 📥 Generate & Export Reports")

col1, col2 = st.columns(2)

# CSV DOWNLOAD
with col1:
    csv = report_data.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"vaxipredict_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# PDF DOWNLOAD
with col2:
    pdf = generate_pdf(report_data)
    st.download_button(
        label="📄 Download PDF",
        data=pdf,
        file_name=f"vaxipredict_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# HISTORY
st.markdown("### 📅 Report History")

history = pd.DataFrame({
    'Date': pd.date_range(start=datetime.now() - timedelta(days=5), periods=5),
    'Type': ['Full', 'Risk', 'Campaign', 'Trend', 'Population'],
    'Status': ['Done', 'Done', 'Processing', 'Done', 'Done']
})

st.dataframe(history, use_container_width=True)

# FOOTER
render_footer(
    title="VaxiPredict Reports",
    subtitle="Exportable analytics & insights",
    meta="Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
    icon="📋"
)