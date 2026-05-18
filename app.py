import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration for high-end executive dark UI layout
st.set_page_config(
    page_title="Executive Financial Target Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS INJECTION: PREMIUM DARK EXECUTIVE THEME
# ==============================================================================
st.markdown("""
    <style>
        /* Base application canvas styling */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
        }
        /* Sidebar layout formatting */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        /* Header typography adjustments */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        /* Custom Key Performance Metric Card Modules */
        .metric-card {
            background-color: #1f242d;
            border: 1px solid #30363d;
            padding: 22px;
            border-radius: 8px;
            text-align: left;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            margin-bottom: 15px;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
        }
        .metric-value {
            font-size: 1.9rem;
            color: #58a6ff;
            font-weight: 700;
            margin: 6px 0;
        }
        .metric-delta {
            font-size: 0.88rem;
            font-weight: 500;
            color: #58a6ff;
        }
        /* Section Dividers */
        hr {
            border-color: #30363d !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Titles matching executive presentation slides
st.title("📊 M&A Target Pro Forma Sensitivity Model")
st.subheader("Value Creation Framework: Standalone vs. Synergized Trajectory")
st.markdown("---")

# ==============================================================================
# 1. SIDEBAR VALUE CREATION CONTROLS
# ==============================================================================
st.sidebar.header("🎯 Operational Levers")
st.sidebar.write("Calibrate the transaction thesis value drivers below:")

st.sidebar.subheader("Top-Line Revenue Drivers")
rev_cagr = st.sidebar.slider(
    "Pro Forma Revenue CAGR % (26-27)", 
    min_value=0.0, max_value=30.0, value=14.0, step=0.5
) / 100

st.sidebar.subheader("Margin & Cost Optimizations")
gm_expansion = st.sidebar.slider(
    "Gross Margin Efficiency Gain (%)", 
    min_value=0.0, max_value=10.0, value=2.5, step=0.5
) / 100

ga_synergy_pct = st.sidebar.slider(
    "G&A Overlap Cost Savings (%)", 
    min_value=0.0, max_value=50.0, value=20.0, step=1.0
) / 100

# ==============================================================================
# 2. BASELINE DATA EXTRACTION
# ==============================================================================
pnl_data = {
    "Financial Line Item": [
        "Total Revenue", 
        "( - ) COGS / Delivery Costs", 
        "Gross Profit", 
        "Sales & Marketing Expenses", 
        "General & Administrative (G&A)", 
        "Product & Engineering Costs", 
        "Total Operating Expenses", 
        "EBITDA"
    ],
    "2024 Baseline": [62500000.0, -41406250.0, 21093750.0, -10546875.0, -5273437.5, -2109375.0, -17929687.5, 3164062.5],
    "2025 Baseline": [72393163.75, -46668991.0, 25724172.75, -12124172.75, -5724172.75, -2324172.75, -20172472.75, 5551700.0]
}
df_pnl = pd.DataFrame(pnl_data)

# ==============================================================================
# 3. PRO FORMA CALCULATION PIPELINE & PROTECTION ENGINE
# ==============================================================================
rev_2025 = df_pnl.loc[df_pnl["Financial Line Item"] == "Total Revenue", "2025 Baseline"].values[0]

# Forward-compound top-line growth assumptions
rev_2026 = rev_2025 * (1.0 + rev_cagr)
rev_2027 = rev_2026 * (1.0 + rev_cagr)

# Calibrate Gross Margins based on efficiency gains
base_margin_2025 = df_pnl.loc[df_pnl["Financial Line Item"] == "Gross Profit", "2025 Baseline"].values[0] / rev_2025
projected_margin = min(base_margin_2025 + gm_expansion, 0.85)

gp_2026, gp_2027 = rev_2026 * projected_margin, rev_2027 * projected_margin
cogs_2026, cogs_2027 = -(rev_2026 - gp_2026), -(rev_2027 - gp_2027)

# Reduced Marketing Cost Logic: Scale constraints applied to mirror scale efficiencies
sm_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "Sales & Marketing Expenses", "2025 Baseline"].values[0]
sm_2026 = sm_2025_base * (1.0 + (rev_cagr * 0.40)) * 0.85
sm_2027 = sm_2026 * (1.0 + (rev_cagr * 0.40)) * 0.85

# Product maintenance projections
pe_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "Product & Engineering Costs", "2025 Baseline"].values[0]
pe_2026, pe_2027 = pe_2025_base * 1.02, pe_2025_base * 1.0404

# G&A rationalization synergies applied
ga_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "General & Administrative (G&A)", "2025 Baseline"].values[0]
ga_2026 = (ga_2025_base * 1.02) * (1.0 - ga_synergy_pct)
ga_2027 = (ga_2026 * 1.02) * (1.0 - ga_synergy_pct)

# Enforcing the Strict Minimum EBITDA Floor (15%)
target_ebitda_floor = 0.15
raw_opex_2026 = sm_2026 + ga_2026 + pe_2026
raw_opex_2027 = sm_2027 + ga_2027 + pe_2027
raw_ebitda_2026, raw_ebitda_2027 = gp_2026 + raw_opex_2026, gp_2027 + raw_opex_2027

ebitda_2026 = max(raw_ebitda_2026, rev_2026 * target_ebitda_floor)
opex_2026 = raw_opex_2026 if raw_ebitda_2026 >= ebitda_2026 else ebitda_2026 - gp_2026

ebitda_2027 = max(raw_ebitda_2027, rev_2027 * target_ebitda_floor)
opex_2027 = raw_opex_2027 if raw_ebitda_2027 >= ebitda_2027 else ebitda_2027 - gp_2027

# Adjust row balances if the floor is triggered to keep accounting integrity
if ebitda_2027 == (rev_2027 * target_ebitda_floor):
    scale_factor = opex_2027 / raw_opex_2027
    sm_2026, sm_2027 = sm_2026 * scale_factor, sm_2027 * scale_factor
    ga_2026, ga_2027 = ga_2026 * scale_factor, ga_2027 * scale_factor
    pe_2026, pe_2027 = pe_2026 * scale_factor, pe_2027 * scale_factor

df_pnl["2026 Pro Forma"] = [rev_2026, cogs_2026, gp_2026, sm_2026, ga_2026, pe_2026, opex_2026, ebitda_2026]
df_pnl["2027 Pro Forma"] = [rev_2027, cogs_2027, gp_2027, sm_2027, ga_2027, pe_2027, opex_2027, ebitda_2027]

# ==============================================================================
# 4. HORIZONTAL EXECUTIVE METRIC SUMMARY CARDS
# ==============================================================================
ebitda_margin_2025 = (df_pnl.loc[df_pnl["Financial Line Item"] == "EBITDA", "2025 Baseline"].values[0] / rev_2025) * 100
ebitda_margin_2027 = (ebitda_2027 / rev_2027) * 100
margin_expansion_delta = ebitda_margin_2027 - ebitda_margin_2025
total_opex_savings_2027 = abs((ga_2025_base * 1.0404) - ga_2027)

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Pro Forma 2027 Target Revenue</div>
            <div class="metric-value">${rev_2027/1e6:.1f}M</div>
            <div class="metric-delta">2-Year Compound Growth Matrix</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Pro Forma 2027 EBITDA Margin</div>
            <div class="metric-value">{ebitda_margin_2027:.1f}%</div>
            <div class="metric-delta" style="color: #3fb950;">▲ +{margin_expansion_delta:.1f}% vs 2025 Standalone</div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Annualized Operating Cost Synergies</div>
            <div class="metric-value">${total_opex_savings_2027/1e3:,.1f}K</div>
            <div class="metric-delta" style="color: #ff7b72;">▼ G&A Infrastructure Trimming</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. HIGH-CONTRAST PLOTLY RUN RATE CHART
# ==============================================================================
st.write("### 📈 Strategic Run Rate Vectors")

df_melted = df_pnl.set_index("Financial Line Item").T.reset_index().rename(columns={"index": "Fiscal Year"})
df_melted = df_melted[df_melted["Fiscal Year"].isin(["2024 Baseline", "2025 Baseline", "2026 Pro Forma", "2027 Pro Forma"])]

df_melted["EBITDA"] = pd.to_numeric(df_melted["EBITDA"])
df_melted["Gross Profit"] = pd.to_numeric(df_melted["Gross Profit"])
df_melted["Total Revenue"] = pd.to_numeric(df_melted["Total Revenue"])

fig_trends = px.line(
    df_melted, x="Fiscal Year", y=["Total Revenue", "Gross Profit", "EBITDA"],
    markers=True,
    color_discrete_sequence=["#58a6ff", "#3fb950", "#ff7b72"] 
)

fig_trends.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#161b22",
    legend_title_text="",
    margin={"r":20,"t":20,"l":20,"b":20},
    xaxis={"gridcolor": "#21262d"},
    yaxis={"gridcolor": "#21262d"}
)
st.plotly_chart(fig_trends, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 6. STANDALONE VS. SYNERGIZED OPERATIONAL LEDGER
# ==============================================================================
st.write("### 📑 Pro Forma Income Statement Ledger ($ Millions)")

def format_currency_pnl(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return f"(${abs(val)/1e6:.2f}M)"
        return f"${val/1e6:.2f}M"
    return val

st.dataframe(
    df_pnl.style.format({
        "2024 Baseline": format_currency_pnl,
        "2025 Baseline": format_currency_pnl,
        "2026 Pro Forma": format_currency_pnl,
        "2027 Pro Forma": format_currency_pnl
    }), 
    use_container_width=True
)
