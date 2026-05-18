import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration for a professional institutional dashboard layout
st.set_page_config(
    page_title="Corporate Finance Performance Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS INJECTION: INSTITUTIONAL CORPORATE PALETTE & METRIC CARDS
# ==============================================================================
st.markdown("""
    <style>
        /* Main dashboard theme setting */
        .stApp {
            background-color: #0b0f19;
            color: #e4e7eb;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1f2937;
        }
        /* Corporate Summary Card Layout */
        .executive-card {
            background-color: #1f2937;
            border-top: 4px solid #3b82f6;
            padding: 18px;
            border-radius: 6px;
            text-align: left;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            margin-bottom: 15px;
        }
        .card-title {
            font-size: 0.82rem;
            color: #9ca3af;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
        }
        .card-value {
            font-size: 1.75rem;
            color: #ffffff;
            font-weight: 700;
            margin-top: 4px;
        }
        .card-subtitle {
            font-size: 0.85rem;
            color: #10b981;
            margin-top: 2px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# Main Application Headers
st.title("📊 Financial Performance Reporting Suite")
st.subheader("M&A Target Variance & Valuation Model")
st.markdown("---")

# ==============================================================================
# 1. SIDEBAR STRATEGIC OVERLAYS
# ==============================================================================
st.sidebar.header("🎯 Valuation Parameters")
st.sidebar.write("Calibrate post-merger run rate assumptions:")

rev_cagr = st.sidebar.slider(
    "Pro Forma Revenue Growth (CAGR %)", 
    min_value=0.0, max_value=30.0, value=14.0, step=0.5
) / 100

gm_expansion = st.sidebar.slider(
    "Gross Margin Optimization Expansion (%)", 
    min_value=0.0, max_value=10.0, value=2.5, step=0.5
) / 100

ga_synergy_pct = st.sidebar.slider(
    "G&A Overlap Cost Savings (%)", 
    min_value=0.0, max_value=50.0, value=20.0, step=1.0
) / 100

# ==============================================================================
# 2. DATA EXTRACTION & ENGINE FORECAST PIPELINE
# ==============================================================================
raw_revenue_2024 = 62500000.0
raw_revenue_2025 = 72393163.75

# Compound top-line targets forward across horizons
rev_2026_proforma = raw_revenue_2025 * (1.0 + rev_cagr)
rev_2027_proforma = rev_2026_proforma * (1.0 + rev_cagr)

# Standalone run rates continue along baseline historical trend paths (~14.05% CAGR)
rev_2026_standalone = raw_revenue_2025 * 1.1405
rev_2027_standalone = rev_2026_standalone * 1.1405

# Define baseline structural margins to calibrate optimization parameters
base_margin_2024 = 21093750.0 / raw_revenue_2024
base_margin_2025 = 25724172.75 / raw_revenue_2025
proforma_margin_target = min(base_margin_2025 + gm_expansion, 0.85)

# Marketing Overhead Contraction Logic
sm_base_2025 = -12124172.75
sm_2026_proforma = sm_base_2025 * (1.0 + (rev_cagr * 0.40)) * 0.85
sm_2027_proforma = sm_2026_proforma * (1.0 + (rev_cagr * 0.40)) * 0.85

sm_2026_standalone = sm_base_2025 * 1.1405
sm_2027_standalone = sm_2026_standalone * 1.1405

# General infrastructure scaling metrics
pe_base_2025 = -2324172.75
pe_2026_proforma, pe_2027_proforma = pe_base_2025 * 1.02, pe_base_2025 * 1.0404
pe_2026_standalone, pe_2027_standalone = pe_base_2025 * 1.03, pe_base_2025 * 1.0609

# G&A cost savings applied
ga_base_2025 = -5724172.75
ga_2026_proforma = (ga_base_2025 * 1.02) * (1.0 - ga_synergy_pct)
ga_2027_proforma = (ga_2026_proforma * 1.02) * (1.0 - ga_synergy_pct)

ga_2026_standalone = ga_base_2025 * 1.02
ga_2027_standalone = ga_2026_standalone * 1.0404

# EBITDA Margin Protection Engine (15% Floor)
target_ebitda_floor = 0.15

def calculate_pnl_column(rev, gm_pct, sm, ga, pe, apply_floor=False):
    gp = rev * gm_pct
    cogs = -(rev - gp)
    raw_opex = sm + ga + pe
    raw_ebitda = gp + raw_opex
    
    if apply_floor and (raw_ebitda / rev) < target_ebitda_floor:
        ebitda = rev * target_ebitda_floor
        opex = ebitda - gp
    else:
        ebitda = raw_ebitda
        opex = raw_opex
        
    return [rev, cogs, gp, sm, ga, pe, opex, ebitda]

col_2024 = [62500000.0, -41406250.0, 21093750.0, -10546875.0, -5273437.5, -2109375.0, -17929687.5, 3164062.5]
col_2025 = [72393163.75, -46668991.0, 25724172.75, -12124172.75, -5724172.75, -2324172.75, -20172472.75, 5551700.0]

col_2026_sa = calculate_pnl_column(rev_2026_standalone, base_margin_2025, sm_2026_standalone, ga_2026_standalone, pe_2026_standalone)
col_2027_sa = calculate_pnl_column(rev_2027_standalone, base_margin_2025, sm_2027_standalone, ga_2027_standalone, pe_2027_standalone)

col_2026_pf = calculate_pnl_column(rev_2026_proforma, proforma_margin_target, sm_2026_proforma, ga_2026_proforma, pe_2026_proforma, apply_floor=True)
col_2027_pf = calculate_pnl_column(rev_2027_proforma, proforma_margin_target, sm_2027_proforma, ga_2027_proforma, pe_2027_proforma, apply_floor=True)

pnl_report_structure = {
    "Financial Line Item": [
        "Total Revenue", "  ( - ) Cost of Goods Sold", "Gross Profit",
        "  Sales & Marketing Expenses", "  General & Administrative (G&A)", "  Product & Engineering Costs",
        "Total Operating Expenses", "EBITDA"
    ],
    "2024 Historical": col_2024,
    "2025 Standalone Base": col_2025,
    "2026 Standalone Projection": col_2026_sa,
    "2026 Pro Forma Synergized": col_2026_pf,
    "2027 Standalone Projection": col_2027_sa,
    "2027 Pro Forma Synergized": col_2027_pf
}
df_pnl_report = pd.DataFrame(pnl_report_structure)

# ==============================================================================
# 3. HORIZONTAL METRICS SUMMARY CARD GENERATION
# ==============================================================================
ebitda_margin_2025_base = (col_2025[7] / col_2025[0]) * 100
ebitda_margin_2027_proforma = (col_2027_pf[7] / col_2027_pf[0]) * 100
margin_variance = ebitda_margin_2027_proforma - ebitda_margin_2025_base
total_opex_savings = abs((ga_base_2025 * 1.0404) - ga_2027_proforma)

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">2027 Pro Forma Net Target Revenue</div>
            <div class="card-value">${col_2027_pf[0]/1e6:.2f}M</div>
            <div class="card-subtitle" style="color: #60a5fa;">Multi-Horizon Compounded Projections</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">2027 Target EBITDA Margin</div>
            <div class="card-value">{ebitda_margin_2027_proforma:.1f}%</div>
            <div class="card-subtitle">▲ +{margin_variance:.1f}% Expansion Over Standalone</div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">Annualized G&A Savings Captured</div>
            <div class="card-value">${total_opex_savings/1e3:,.1f}K</div>
            <div class="card-subtitle">▲ Back-Office Overlap Efficiencies</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. OPERATIONAL RUN RATE VECTOR ANALYSIS
# ==============================================================================
st.write("### 📈 Operational Run Rate Vectors")

df_melted = df_pnl_report.set_index("Financial Line Item").T.reset_index().rename(columns={"index": "Reporting Period"})
df_melted["EBITDA"] = pd.to_numeric(df_melted["EBITDA"])
df_melted["Gross Profit"] = pd.to_numeric(df_melted["Gross Profit"])
df_melted["Total Revenue"] = pd.to_numeric(df_melted["Total Revenue"])

fig_trends = px.line(
    df_melted, x="Reporting Period", y=["Total Revenue", "Gross Profit", "EBITDA"],
    markers=True, color_discrete_sequence=["#60a5fa", "#34d399", "#f87171"]
)
fig_trends.update_layout(
    template="plotly_dark", paper_bgcolor="#0b0f19", plot_bgcolor="#111827",
    legend_title_text="", margin={"r":15,"t":15,"l":15,"b":15},
    xaxis={"gridcolor": "#1f2937"}, yaxis={"gridcolor": "#1f2937"}
)
st.plotly_chart(fig_trends, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 5. HIGH
