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
rev_2026_standalone = raw_revenue
