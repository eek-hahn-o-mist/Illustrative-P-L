import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration for absolute control over layout
st.set_page_config(
    page_title="Executive Pro Forma Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CUSTOM BRANDING & DARK UI GRAPHICS (CSS INJECTION)
# ==============================================================================
st.markdown("""
    <style>
        /* Base dashboard canvas dark background override */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        /* Style sidebar to match dark palette seamlessly */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #21262d;
        }
        /* Custom Key Metric Card container modules */
        .metric-card {
            background-color: #1f242d;
            border: 1px solid #2d333b;
            padding: 20px;
            border-radius: 10px;
            text-align: left;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
        }
        .metric-value {
            font-size: 1.85rem;
            color: #58a6ff;
            font-weight: 700;
            margin: 5px 0;
        }
        .metric-delta {
            font-size: 0.9rem;
            font-weight: 500;
        }
        .delta-positive { color: #3fb950; }
        .delta-negative { color: #f85149; }
    </style>
""", unsafe_allow_html=True)

# Main Title Framework
st.title("📊 Executive Financial Performance Dashboard")
st.subheader("M&A Target Pro Forma Sensitivity Engine")
st.markdown("---")

# ==============================================================================
# 1. SIDEBAR CONTROLS
# ==============================================================================
st.sidebar.header("🎯 Operational Levers")
st.sidebar.write("Calibrate post-acquisition performance assumptions:")

rev_cagr = st.sidebar.slider(
    "Pro Forma Revenue CAGR % (26-27)", 
    min_value=0.0, max_value=30.0, value=14.0, step=0.5
) / 100

gm_expansion = st.sidebar.slider(
    "Gross Margin Optimization Expansion %", 
    min_value=0.0, max_value=10.0, value=2.5, step=0.5
) / 100

ga_synergy_pct = st.sidebar.slider(
    "G&A Overlap Cost Savings %", 
    min_value=0.0, max_value=50.0, value=20.0, step=1.0
) / 100

# ==============================================================================
# 2. BASELINE DATA EXTRACTION & CALCULATIONS
# ==============================================================================
pnl_data = {
    "Financial Line Item": [
        "Total Revenue", "( - ) COGS / Delivery Costs", "Gross Profit", 
        "Sales & Marketing Expenses", "General & Administrative (G&A)", 
        "Product & Engineering Costs", "Total Operating Expenses", "EBITDA"
    ],
    "2024 Baseline": [62500000.0, -41406250.0, 21093750.0, -10546875.0, -5273437.5, -2109375.0, -17929687.5, 3164062.5],
    "2025 Baseline": [72393163.75, -46668991.0, 25724172.75, -12124172.75, -5724172.75, -2324172.75, -20172472.75, 5551700.0]
}
df_pnl = pd.DataFrame(pnl_data)

# Forecast Calculations
rev_2025 = df_pnl.loc[df_pnl["Financial Line Item"] == "Total Revenue", "2025 Baseline"].values[0]
rev_2026 = rev_2025 * (1.0 + rev_cagr)
rev_2027 = rev_2026 * (1.0 + rev_cagr)

base_margin_2025 = df_pnl.loc[df_pnl["Financial Line Item"] == "Gross Profit", "2025 Baseline"].values[0] / rev_2025
projected_margin = min(base_margin_2025 + gm_expansion, 0.85)

gp_2026, gp_2027 = rev_2026 * projected_margin, rev_2027 * projected_margin
cogs_2026, cogs_2027 = -(rev_2026 - gp_2026), -(rev_2027 - gp_2027)

# Clamped Marketing logic applied
sm_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "Sales & Marketing Expenses", "2025 Baseline"].values[0]
sm_2026 = sm_2025_base * (1.0 + (rev_cagr * 0.40)) * 0.85
sm_2027 = sm_2026 * (1.0 + (rev_cagr * 0.40)) * 0.85

pe_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "Product & Engineering Costs", "2025 Baseline"].values[0]
pe_2026, pe_2027 = pe_2025_base * 1.02, pe_2025_base * 1.0404

ga_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "General & Administrative (G&A)", "2025 Baseline"].values[0]
ga_2026 = (ga_2025_base * 1.02) * (1.0 - ga_synergy_pct)
ga_2027 = (ga_2026 * 1.02) * (1.0 - ga_synergy_pct)

# Protect Margin Floor (Min 15%)
target_ebitda_floor = 0.15
raw_opex_2026 = sm_2026 + ga_2026 + pe_2026
raw_opex_2027 = sm_2027 + ga_2027 + pe_2027
raw_ebitda_2026, raw_ebitda_2027 = gp_2026 + raw_opex_2026, gp_2027 + raw_opex_2027

ebitda_2026 = max(raw_ebitda_2026, rev_2026 * target_ebitda_floor)
opex_2026 = raw_opex_2026 if raw_ebitda_2026 >= ebitda_2026 else ebitda_2026 - gp_2026

ebitda_2027 = max(raw_ebitda_2027, rev_2027 * target_ebitda_floor)
opex_2027 = raw_opex_2027 if raw_ebitda_2027 >= ebitda_2027 else ebitda_2027 - gp_2027

df_pnl["2026 Pro Forma"] = [rev_2026, cogs_2026, gp_2026, sm_2026, ga_2026, pe_2026, opex_2026, ebitda_2026]
df_pnl["2027 Pro Forma"] = [rev_2027, cogs_2027, gp_2027, sm_2027, ga_2027, pe_2027, opex_2027, ebitda_2027]

# ==============================================================================
# 3. HORIZONTAL EXECUTIVE METRIC SUMMARY BLOCKS (MATCHES PROVIDED UI IMAGE)
# ==============================================================================
ebitda_margin_2025 = (df_pnl.loc[df_pnl["Financial Line Item"] == "EBITDA", "2025 Baseline"].values[0] / rev_2025) * 100
ebitda_margin_2027 = (ebitda_2027 / rev_2027) * 100
margin_expansion_delta = ebitda_margin_2027 - ebitda_margin_2025
total_opex_savings_2027 = abs((ga_2025_base * 1.0404) - ga_2027)

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Pro Forma 2027 Revenue Target</div>
            <div class="metric-value">${rev_2027/1e6:.1f}M</div>
            <div class="metric-delta delta-positive">▲ Across 24 Months Forecast</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">2027 EBITDA Margin Target</div>
            <div class="metric-value">{ebitda_margin_2027:.1f}%</div>
            <div class="metric-delta delta-positive">▲ +{margin_expansion_delta:.1f}% Optimization Realized</div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Annualized G&A Savings Captured</div>
            <div class="metric-value">${total_opex_savings_2027/1e3:,.1f}K</div>
            <div class="metric-delta delta-positive">▼ Corporate Overhead Reductions</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. DARK THEME CHART GENERATION & DATA TABLE STACK
# ==============================================================================
st.write("### 📈 Strategic Financial Projections & Run Rate Vectors")

df_melted = df_pnl.set_index("Financial Line Item").T.reset_index().rename(columns={"index": "Fiscal Year"})
df_melted = df_melted[df_melted["Fiscal Year"].isin(["2024 Baseline", "2025 Baseline", "2026 Pro Forma", "2027 Pro Forma"])]

fig_trends = px.line(
    df_melted, x="Fiscal Year", y=["Total Revenue", "Gross Profit", "EBITDA"],
    markers=True,
    color_discrete_sequence=["#58a6ff", "#3fb950", "#ff7b72"] # Matching theme palette accents
)

# Apply absolute dark template styling to Plotly layout
fig_trends.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0e1117",
    plot_bgcolor="#161b22",
    legend_title_text="",
    margin={"r":20,"t":20,"l":20,"b":20},
    xaxis={"gridcolor": "#21262d"},
    yaxis={"gridcolor": "#21262d"}
)
st.plotly_chart(fig_trends, use_container_width=True)

st.markdown("---")

st.write("### 📑 Pro Forma Income Statement Ledger ($ Millions)")

def format_currency_pnl(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return f"(${abs(val)/1e6:.2f}M)"
        return f"${val/1e6:.2f}M"
    return val

# Draw structured data frame matrix full width
st.dataframe(
    df_pnl.style.format({
        "2024 Baseline": format_currency_pnl,
        "2025 Baseline": format_currency_pnl,
        "2026 Pro Forma": format_currency_pnl,
        "2027 Pro Forma": format_currency_pnl
    }), 
    use_container_width=True
)
