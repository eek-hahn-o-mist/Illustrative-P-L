import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration for a professional institutional dashboard layout
st.set_page_config(
    page_title="Corporate Financial Performance Suite",
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
st.subheader("Illustrative Income Statement & Business Driver Sensitivity Model")
st.markdown("---")

# ==============================================================================
# 1. SIDEBAR OPERATIONAL DRIVERS & SENSITIVITY SLIDERS
# ==============================================================================
st.sidebar.header("🎯 Operational Performance Drivers")
st.sidebar.write("Calibrate underlying metrics to drive top-line growth:")

# RFP Pipeline Drivers to replace the lone revenue slider
rfp_count = st.sidebar.slider(
    "Annual RFPs Submitted (2026–2027)", 
    min_value=100, max_value=500, value=280, step=5
)
win_rate = st.sidebar.slider(
    "RFP Win Rate (% Won)", 
    min_value=10.0, max_value=60.0, value=29.5, step=0.5
) / 100

st.sidebar.markdown("---")
st.sidebar.subheader("Margin & Cost Efficiencies")
gm_expansion = st.sidebar.slider(
    "Gross Margin Efficiency Target (%)", 
    min_value=0.0, max_value=10.0, value=2.5, step=0.5
) / 100

ga_efficiency_pct = st.sidebar.slider(
    "G&A Cost Efficiency Savings (%)", 
    min_value=0.0, max_value=50.0, value=20.0, step=1.0
) / 100

# ==============================================================================
# 2. OPERATIONAL FORECAST ENGINE (REVENUE DRIVEN BY PIPELINE MIX)
# ==============================================================================
raw_revenue_2024 = 62500000.0
raw_revenue_2025 = 72393163.75

# Spreadsheet Business Logic: Contracts Signed = RFPs Submitted * Win Rate
# Hardcoded standard deal value structure from data model context handles the projection values
contracts_signed = rfp_count * win_rate
assumed_deal_size_2026 = 1010000.0   # Baseline proxy scaling unit
assumed_deal_size_2027 = 1100000.0

# Calculate top-line performance dynamically based on RFP inputs
rev_2026_projected = contracts_signed * assumed_deal_size_2026
rev_2027_projected = contracts_signed * assumed_deal_size_2027

# Back-calculate implied Revenue CAGR to maintain underlying model dynamics
implied_cagr = ((rev_2027_projected / raw_revenue_2025) ** (1/2)) - 1

# Define structural margins to calibrate optimization parameters
base_margin_2025 = 25724172.75 / raw_revenue_2025
projected_margin_target = min(base_margin_2025 + gm_expansion, 0.85)

# Sales & Marketing Expense scaling anchored to the operational revenue outcome
sm_base_2025 = -12124172.75
sm_2026_projected = sm_base_2025 * (1.0 + (implied_cagr * 0.40)) * 0.85
sm_2027_projected = sm_base_2025 * (1.0 + (implied_cagr * 0.40)) * 0.85

# Product engineering maintenance metrics
pe_base_2025 = -2324172.75
pe_2026_projected, pe_2027_projected = pe_base_2025 * 1.02, pe_base_2025 * 1.0404

# G&A administrative cost efficiencies applied
ga_base_2025 = -5724172.75
ga_2026_projected = (ga_base_2025 * 1.02) * (1.0 - ga_efficiency_pct)
ga_2027_projected = (ga_2026_projected * 1.02) * (1.0 - ga_efficiency_pct)

# EBITDA Margin Protection Floor Engine (Strict 15% Minimum)
target_ebitda_floor = 0.15

def calculate_pnl_column(rev, gm_pct, sm, ga, pe):
    gp = rev * gm_pct
    cogs = -(rev - gp)
    raw_opex = sm + ga + pe
    raw_ebitda = gp + raw_opex
    
    # Floor adjustment logic check
    if (raw_ebitda / rev) < target_ebitda_floor:
        ebitda = rev * target_ebitda_floor
        opex = ebitda - gp
    else:
        ebitda = raw_ebitda
        opex = raw_opex
        
    return [rev, cogs, gp, sm, ga, pe, opex, ebitda]

col_2024 = [62500000.0, -41406250.0, 21093750.0, -10546875.0, -5273437.5, -2109375.0, -17929687.5, 3164062.5]
col_2025 = [72393163.75, -46668991.0, 25724172.75, -12124172.75, -5724172.75, -2324172.75, -20172472.75, 5551700.0]

col_2026_proj = calculate_pnl_column(rev_2026_projected, projected_margin_target, sm_2026_projected, ga_2026_projected, pe_2026_projected)
col_2027_proj = calculate_pnl_column(rev_2027_projected, projected_margin_target, sm_2027_projected, ga_2027_projected, pe_2027_projected)

pnl_report_structure = {
    "Financial Line Item": [
        "Total Revenue", "  ( - ) Cost of Goods Sold", "Gross Profit",
        "  Sales & Marketing Expenses", "  General & Administrative (G&A)", "  Product & Engineering Costs",
        "Total Operating Expenses", "EBITDA"
    ],
    "2024 Historical": col_2024,
    "2025 Baseline": col_2025,
    "2026 Projected": col_2026_proj,
    "2027 Projected": col_2027_proj
}
df_pnl_report = pd.DataFrame(pnl_report_structure)

# ==============================================================================
# 3. HORIZONTAL METRICS SUMMARY CARDS (PINNED TO TOP)
# ==============================================================================
ebitda_margin_2025_base = (col_2025[7] / col_2025[0]) * 100
ebitda_margin_2027_projected = (col_2027_proj[7] / col_2027_proj[0]) * 100
margin_variance = ebitda_margin_2027_projected - ebitda_margin_2025_base

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">2027 Projected Net Revenue</div>
            <div class="card-value">${col_2027_proj[0]/1e6:.2f}M</div>
            <div class="card-subtitle" style="color: #60a5fa;">Contracts Signed: {contracts_signed:.1f}</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">2027 Projected EBITDA Margin</div>
            <div class="card-value">{ebitda_margin_2027_projected:.1f}%</div>
            <div class="card-subtitle">▲ +{margin_variance:.1f}% Expansion Over 2025 Base</div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">Implied Revenue CAGR</div>
            <div class="card-value">{implied_cagr*100:.1f}%</div>
            <div class="card-subtitle" style="color: #60a5fa;">Pipeline-to-Growth Translation Rate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# 4. VERTICAL INCOME STATEMENT PRESENTATION LEDGER
# ==============================================================================
st.write("### 📑 Income Statement Presentation Ledger ($ Millions)")

def currency_formatter(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return f"(${abs(val)/1e6:.2f}M)"
        return f"${val/1e6:.2f}M"
    return val

def apply_institutional_formatting(styler):
    columns_to_format = [col for col in styler.columns if col != "Financial Line Item"]
    styler.format(currency_formatter, subset=columns_to_format)
    
    styler.hide(axis="index")
    styler.set_properties(subset=columns_to_format, **{'text-align': 'right'})
    styler.set_properties(subset=["Financial Line Item"], **{'text-align': 'left'})
    
    # Bold primary subtotal metrics
    styler.set_properties(subset=pd.IndexSlice[[0, 2, 6, 7], :], **{
        'font-weight': 'bold',
        'color': '#ffffff'
    })
    
    # Apply background shading to summary profit milestones rows
    styler.set_properties(subset=pd.IndexSlice[[2, 7], :], **{
        'background-color': '#1f2937',
        'border-top': '1px solid #374151',
        'border-bottom': '1px solid #374151'
    })
    return styler

df_styled_pnl = df_pnl_report.style.pipe(apply_institutional_formatting)
st.dataframe(df_styled_pnl, use_container_width=True)

st.write("")
st.info(
    "**Financial Model Rationale:** Following institutional statement formatting rules, this ledger models forecast variance "
    "driven from direct operational funnel metrics. Shifting the RFP volume and win percentage updates the top-line automatically, "
    "while opex layers respect the strict **15% minimum EBITDA margin target floor**."
)

st.markdown("---")

# ==============================================================================
# 5. RUN RATE VECTOR LINE ANALYSIS (MOVED TO BOTTOM)
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
