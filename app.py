import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration for professional full-width enterprise dashboard layout
st.set_page_config(
    page_title="Corpay Corp Dev - M&A Target Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Strategic M&A Target P&L Simulator")
st.subheader("Professional Services Acquisition Analysis & Pro Forma Synergy Overlay")
st.write(
    "This interactive dashboard benchmarks the historical financial records of an illustrative "
    "Professional Services target asset against dynamic growth assumptions, cross-sell revenue "
    "acceleration parameters, and automated post-acquisition cost synergy realizations."
)

st.markdown("---")

# ==============================================================================
# 1. SIDEBAR VALUE CREATION & UNIT ECONOMIC CONTROLS
# ==============================================================================
st.sidebar.header("🎯 Value Creation Sliders")
st.sidebar.write("Adjust target performance drivers to stress-test pro forma outputs.")

st.sidebar.subheader("Top-Line Assumptions")
# Extracted Baseline CAGR from file was ~14.05%
rev_cagr = st.sidebar.slider(
    "Pro Forma Revenue Growth (2026-2027 CAGR %)", 
    min_value=0.0, 
    max_value=30.0, 
    value=14.0, 
    step=0.5
) / 100

st.sidebar.subheader("Efficiency & Margin Levers")
gm_expansion = st.sidebar.slider(
    "Gross Margin Optimization Lever (%)", 
    min_value=0.0, 
    max_value=10.0, 
    value=2.5, 
    step=0.5
) / 100

st.sidebar.subheader("Operational Synergies")
ga_synergy_pct = st.sidebar.slider(
    "G&A Overlap Cost Synergy Capture (%)", 
    min_value=0.0, 
    max_value=50.0, 
    value=20.0, 
    step=1.0
) / 100

st.sidebar.markdown("---")
st.sidebar.subheader("Corpay Portfolio Overlays")
# Standard net take rate overlay from Corpay corporate payments segment strategy
take_rate = st.sidebar.number_input(
    "Assumed Automated Payment Take Rate (%)", 
    value=0.62, 
    step=0.01
) / 100

# ==============================================================================
# 2. BASELINE FINANCIAL STRUCTURE EXTRACTION (2024 - 2025 BASE CASE)
# ==============================================================================
# Reconstructing financial line items matching the exact structural flow of your spreadsheet data
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
# 3. PRO FORMA CALCULATION FORECAST ENGINE (2026 - 2027 PROJECTIONS)
# ==============================================================================
rev_2025 = df_pnl.loc[df_pnl["Financial Line Item"] == "Total Revenue", "2025 Baseline"].values[0]

# Generate Projected Revenue Streams using dynamic CAGR parameters
rev_2026 = rev_2025 * (1.0 + rev_cagr)
rev_2027 = rev_2026 * (1.0 + rev_cagr)

# Calculate historical baseline gross margins to anchor projection scaling
base_margin_2025 = df_pnl.loc[df_pnl["Financial Line Item"] == "Gross Profit", "2025 Baseline"].values[0] / rev_2025
projected_margin = min(base_margin_2025 + gm_expansion, 0.85) # Logical efficiency ceiling anchor at 85%

gp_2026 = rev_2026 * projected_margin
gp_2027 = rev_2027 * projected_margin

cogs_2026 = -(rev_2026 - gp_2026)
cogs_2027 = -(rev_2027 - gp_2027)

# Scale variable operating cost structures proportionally with volume changes
sm_2026 = df_pnl.loc[df_pnl["Financial Line Item"] == "Sales & Marketing Expenses", "2025 Baseline"].values[0] * (rev_2026 / rev_2025) * 0.95
sm_2027 = sm_2026 * (rev_2027 / rev_2026) * 0.95

pe_2026 = df_pnl.loc[df_pnl["Financial Line Item"] == "Product & Engineering Costs", "2025 Baseline"].values[0] * 1.03
pe_2027 = pe_2026 * 1.03

# Overlay corporate overhead synergy reductions onto administrative structures
ga_2025_base = df_pnl.loc[df_pnl["Financial Line Item"] == "General & Administrative (G&A)", "2025 Baseline"].values[0]
ga_2026 = (ga_2025_base * 1.02) * (1.0 - ga_synergy_pct)
ga_2027 = (ga_2026 * 1.02) * (1.0 - ga_synergy_pct)

opex_2026 = sm_2026 + ga_2026 + pe_2026
opex_2027 = sm_2027 + ga_2027 + pe_2027

ebitda_2026 = gp_2026 + opex_2026
ebitda_2027 = gp_2027 + opex_2027

# Append newly created pro forma calculation iterations into master DataFrame
df_pnl["2026 Pro Forma"] = [rev_2026, cogs_2026, gp_2026, sm_2026, ga_2026, pe_2026, opex_2026, ebitda_2026]
df_pnl["2027 Pro Forma"] = [rev_2027, cogs_2027, gp_2027, sm_2027, ga_2027, pe_2027, opex_2027, ebitda_2027]

# ==============================================================================
# 4. DATA PRESENTATION & ACCRETION INSIGHTS VISUALS
# ==============================================================================
col_vis, col_metrics = st.columns([2, 1])

with col_vis:
    st.write("### 📈 Core Financial Trend Analysis")
    
    # Restructure dataframe orientation for line visual ingestion metrics
    df_melted = df_pnl.set_index("Financial Line Item").T.reset_index().rename(columns={"index": "Fiscal Year"})
    df_melted = df_melted[df_melted["Fiscal Year"].isin(["2024 Baseline", "2025 Baseline", "2026 Pro Forma", "2027 Pro Forma"])]
    
    # Strip negatives from cost tracking indices to keep trendlines clean and comparable
    df_melted["EBITDA"] = pd.to_numeric(df_melted["EBITDA"])
    df_melted["Gross Profit"] = pd.to_numeric(df_melted["Gross Profit"])
    df_melted["Total Revenue"] = pd.to_numeric(df_melted["Total Revenue"])
    
    fig_pnl_trends = px.line(
        df_melted, 
        x="Fiscal Year", 
        y=["Total Revenue", "Gross Profit", "EBITDA"],
        labels={"value": "Amount ($ Millions)", "variable": "Financial Statement Items"},
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_pnl_trends.update_layout(yaxis_title="USD ($)")
    st.plotly_chart(fig_pnl_trends, use_container_width=True)

with col_metrics:
    st.write("### 📊 Operational Health & Accretion KPIS")
    
    # Calculate margins to verify value expansion logic realizes target targets
    ebitda_margin_2025 = (df_pnl.loc[df_pnl["Financial Line Item"] == "EBITDA", "2025 Baseline"].values[0] / rev_2025) * 100
    ebitda_margin_2027 = (ebitda_2027 / rev_2027) * 100
    margin_expansion_delta = ebitda_margin_2027 - ebitda_margin_2025
    
    # Calculate target payment processing volumes capture potential
    addressable_interchange_rev_2027 = (abs(cogs_2027) * take_rate)
    
    # Render professional corporate reporting summary grids
    st.metric(
        label="Pro Forma 2027 EBITDA Margin", 
        value=f"{ebitda_margin_2027:.1f}%", 
        delta=f"+{margin_expansion_delta:.1f}% vs. 2025 Base"
    )
    st.metric(
        label="Estimated 2027 Automated Payment Interchange Revenue", 
        value=f"${addressable_interchange_rev_2027:,.0f}",
        help="Calculated by applying the defined take rate directly onto delivery operating costs to proxy business payment volume conversion."
    )
    st.metric(
        label="Pro Forma 2027 Projected Revenue", 
        value=f"${rev_2027:,.0f}"
    )

st.markdown("---")

# Display complete structured pro forma income ledger matrix
st.write("### 📑 Pro Forma Income Statement Ledger ($ Millions)")

def format_currency_pnl(val):
    if isinstance(val, (int, float)):
        # Retain standard bookkeeping styling rules where cost items show wrapped inside parentheses
        if val < 0:
            return f"(${abs(val)/1e6:.2f}M)"
        return f"${val/1e6:.2f}M"
    return val

# Render the stylized data frame mapping values elegantly
st.dataframe(df_pnl.style.format({
    "2024 Baseline": format_currency_pnl,
    "2025 Baseline": format_currency_pnl,
    "2026 Pro Forma": format_currency_pnl,
    "2027 Pro Forma": format_currency_pnl
}), use_container_width=True)

st.write("")

# Corp Dev Value Creation Narrative Hook Banner
st.success(
    f"**Corporate Development Strategic Rationale:** Adjusting the synergy dials highlights a clear path toward margin expansion. "
    f"Converting the target asset's standard delivery costs (${abs(cogs_2027)/1e6:.1f}M) into an automated invoice-to-pay stream "
    f"unlocks **${addressable_interchange_rev_2027/1e3:,.1f}K** in high-margin interchange fees. This core transaction framework maps "
    f"how standard target assets scale rapidly within Corpay's automated payment ecosystem."
)
