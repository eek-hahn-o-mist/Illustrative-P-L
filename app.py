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
st.subheader("Illustrative Income Statement & Variance Sensitivity Model")
st.markdown("---")

# ==============================================================================
# 1. SIDEBAR STRATEGIC OVERLAYS
# ==============================================================================
st.sidebar.header("🎯 Operational Parameters")
st.sidebar.write("Calibrate future performance target assumptions:")

rev_cagr = st.sidebar.slider(
    "Target Revenue Growth (CAGR %)", 
    min_value=0.0, max_value=30.0, value=14.0, step=0.5
) / 100

gm_expansion = st.sidebar.slider(
    "Gross Margin Efficiency Target (%)", 
    min_value=0.0, max_value=10.0, value=2.5, step=0.5
) / 100

ga_efficiency_pct = st.sidebar.slider(
    "G&A Cost Efficiency Savings (%)", 
    min_value=0.0, max_value=50.0, value=20.0, step=1.0
) / 100

# ==============================================================================
# 2. DATA EXTRACTION & ENGINE FORECAST PIPELINE
# ==============================================================================
raw_revenue_2024 = 62500000.0
raw_revenue_2025 = 72393163.75

# Compound top-line targets forward across horizons
rev_2026_optimized = raw_revenue_2025 * (1.0 + rev_cagr)
rev_2027_optimized = rev_2026_optimized * (1.0 + rev_cagr)

# Baseline run rates continue along baseline historical trend paths (~14.05% CAGR)
rev_2026_baseline = raw_revenue_2025 * 1.1405
rev_2027_baseline = rev_2026_baseline * 1.1405

# Define baseline structural margins to calibrate optimization parameters
base_margin_2024 = 21093750.0 / raw_revenue_2024
base_margin_2025 = 25724172.75 / raw_revenue_2025
optimized_margin_target = min(base_margin_2025 + gm_expansion, 0.85)

# Marketing Optimization Logic
sm_base_2025 = -12124172.75
sm_2026_optimized = sm_base_2025 * (1.0 + (rev_cagr * 0.40)) * 0.85
sm_2027_optimized = sm_2026_optimized * (1.0 + (rev_cagr * 0.40)) * 0.85

sm_2026_baseline = sm_base_2025 * 1.1405
sm_2027_baseline = sm_2026_baseline * 1.1405

# General infrastructure scaling metrics
pe_base_2025 = -2324172.75
pe_2026_optimized, pe_2027_optimized = pe_base_2025 * 1.02, pe_base_2025 * 1.0404
pe_2026_baseline, pe_2027_baseline = pe_base_2025 * 1.03, pe_base_2025 * 1.0609

# G&A administrative cost efficiencies applied
ga_base_2025 = -5724172.75
ga_2026_optimized = (ga_base_2025 * 1.02) * (1.0 - ga_efficiency_pct)
ga_2027_optimized = (ga_2026_optimized * 1.02) * (1.0 - ga_efficiency_pct)

ga_2026_baseline = ga_base_2025 * 1.02
ga_2027_baseline = ga_base_2025 * 1.0404

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

col_2026_bl = calculate_pnl_column(rev_2026_baseline, base_margin_2025, sm_2026_baseline, ga_2026_baseline, pe_2026_baseline)
col_2027_bl = calculate_pnl_column(rev_2027_baseline, base_margin_2025, sm_2027_baseline, ga_2027_baseline, pe_2027_baseline)

col_2026_opt = calculate_pnl_column(rev_2026_optimized, optimized_margin_target, sm_2026_optimized, ga_2026_optimized, pe_2026_optimized, apply_floor=True)
col_2027_opt = calculate_pnl_column(rev_2027_optimized, optimized_margin_target, sm_2027_optimized, ga_2027_optimized, pe_2027_optimized, apply_floor=True)

pnl_report_structure = {
    "Financial Line Item": [
        "Total Revenue", "  ( - ) Cost of Goods Sold", "Gross Profit",
        "  Sales & Marketing Expenses", "  General & Administrative (G&A)", "  Product & Engineering Costs",
        "Total Operating Expenses", "EBITDA"
    ],
    "2024 Historical": col_2024,
    "2025 Baseline Run Rate": col_2025,
    "2026 Baseline Projection": col_2026_bl,
    "2026 Optimized Case": col_2026_opt,
    "2027 Baseline Projection": col_2027_bl,
    "2027 Optimized Case": col_2027_opt
}
df_pnl_report = pd.DataFrame(pnl_report_structure)

# ==============================================================================
# 3. HORIZONTAL METRICS SUMMARY CARDS (STAYS AT TOP)
# ==============================================================================
ebitda_margin_2025_base = (col_2025[7] / col_2025[0]) * 100
ebitda_margin_2027_optimized = (col_2027_opt[7] / col_2027_opt[0]) * 100
margin_variance = ebitda_margin_2027_optimized - ebitda_margin_2025_base
total_opex_savings = abs((ga_base_2025 * 1.0404) - ga_2027_optimized)

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">2027 Optimized Revenue Target</div>
            <div class="card-value">${col_2027_opt[0]/1e6:.2f}M</div>
            <div class="card-subtitle" style="color: #60a5fa;">Multi-Horizon Compounded Projections</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">2027 Target EBITDA Margin</div>
            <div class="card-value">{ebitda_margin_2027_optimized:.1f}%</div>
            <div class="card-subtitle">▲ +{margin_variance:.1f}% Expansion Over Baseline</div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="executive-card">
            <div class="card-title">Annualized G&A Savings Captured</div>
            <div class="card-value">${total_opex_savings/1e3:,.1f}K</div>
            <div class="card-subtitle">▲ Overhead Infrastructure Optimization</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# 4. VERTICAL INCOME STATEMENT VARIANCE LEDGER (PHDATA MATRIX VIEW)
# ==============================================================================
st.write("### 📑 Income Statement Presentation & Variance Ledger ($ Millions)")

# Core accounting formatting logic (enforces parentheses on negative entries)
def currency_formatter(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return f"(${abs(val)/1e6:.2f}M)"
        return f"${val/1e6:.2f}M"
    return val

# Advanced Pandas Styler layout configuration to mimic dedicated BI interfaces
def apply_institutional_formatting(styler):
    columns_to_format = [col for col in styler.columns if col != "Financial Line Item"]
    styler.format(currency_formatter, subset=columns_to_format)
    
    styler.hide(axis="index")
    styler.set_properties(subset=columns_to_format, **{'text-align': 'right'})
    styler.set_properties(subset=["Financial Line Item"], **{'text-align': 'left'})
    
    # Bold primary subtotal metrics (Rows index 0: Revenue, 2: GP, 6: Opex, 7: EBITDA)
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
    "**Financial Model Rationale:** Following the structural formatting rules of institutional statement presentation, "
    "this ledger evaluates forecast variance tracking. Adjusting the top-line scaling parameters and administrative efficiency "
    "levers outputs an updated run rate while protecting the strict **15% minimum EBITDA margin target**."
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
