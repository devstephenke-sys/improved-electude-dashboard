"""
================================================================================
ELECTUDE AFRICA TVET ANALYTICS DASHBOARD - PROFESSIONAL EDITION
================================================================================

A comprehensive, enterprise-grade analytics dashboard for Technical and 
Vocational Education (TVET) data across Africa.

Version: 2.0.0
Author: Electude Africa Data Science Team

Features:
- Modern, professional UI with custom CSS styling
- Interactive Plotly visualizations
- Real-time data filtering and exploration
- AI-powered insights and recommendations
- Data quality monitoring and reporting
- Multi-format data export capabilities

Usage:
    streamlit run electude_dashboard_pro.py

Requirements:
    streamlit>=1.28.0
    pandas>=2.0.0
    plotly>=5.18.0
    numpy>=1.24.0
================================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')


# =============================================================================
# CONFIGURATION & THEME
# =============================================================================

@dataclass
class ThemeColors:
    """Professional color palette for the dashboard."""
    primary: str = "#1E3A5F"
    secondary: str = "#2E86AB"
    accent: str = "#F18F01"
    success: str = "#28A745"
    warning: str = "#FFC107"
    danger: str = "#DC3545"
    info: str = "#17A2B8"
    dark: str = "#1A1A2E"
    light: str = "#F8F9FA"
    teal: str = "#20C997"
    purple: str = "#6F42C1"
    pink: str = "#E83E8C"
    indigo: str = "#6610F2"


# Initialize theme
THEME = ThemeColors()

# Chart color sequences
CHART_COLORS = [
    THEME.primary, THEME.secondary, THEME.accent,
    THEME.teal, THEME.purple, THEME.pink
]

DIVERGENT_COLORS = [
    "#0d47a1", "#1976d2", "#42a5f5", "#90caf9",
    "#ffcc80", "#ffa726", "#f57c00", "#e65100"
]

# Country flag mappings for African countries
COUNTRY_FLAGS = {
    "Kenya": "🇰🇪", "Uganda": "🇺🇬", "Tanzania": "🇹🇿", "Rwanda": "🇷🇼",
    "Ethiopia": "🇪🇹", "Ghana": "🇬🇭", "Nigeria": "🇳🇬", "South Africa": "🇿🇦",
    "Zambia": "🇿🇲", "Malawi": "🇲🇼", "Burundi": "🇧🇮", "DRC": "🇨🇩",
    "South Sudan": "🇸🇸", "Sudan": "🇸🇩", "Senegal": "🇸🇳", "Madagascar": "🇲🇬",
    "Mozambique": "🇲🇿", "Cameroon": "🇨🇲", "Togo": "🇹🇬", "Benin": "🇧🇯",
    "Ivory Coast": "🇨🇮", "Burkina Faso": "🇧🇫", "Mali": "🇲🇱", "Niger": "🇳🇪"
}

# Language display names
LANGUAGE_DISPLAY = {
    "ENG": "🇬🇧 English",
    "FRE": "🇫🇷 French",
    "FRA": "🇫🇷 French",
    "SWA": "🇰🇪 Swahili",
    "POR": "🇵🇹 Portuguese",
    "ARA": "🇸🇦 Arabic",
    "AMH": "🇪🇹 Amharic",
}


# =============================================================================
# CUSTOM CSS STYLES
# =============================================================================

def get_custom_css() -> str:
    """Return comprehensive custom CSS for professional dashboard styling."""
    return """
    <style>
        /* ===== ROOT VARIABLES ===== */
        :root {
            --primary-color: #1E3A5F;
            --secondary-color: #2E86AB;
            --accent-color: #F18F01;
            --success-color: #28A745;
            --warning-color: #FFC107;
            --danger-color: #DC3545;
            --info-color: #17A2B8;
            --dark-color: #1A1A2E;
            --light-color: #F8F9FA;
            --gradient-primary: linear-gradient(135deg, #1E3A5F 0%, #2E86AB 100%);
            --gradient-accent: linear-gradient(135deg, #F18F01 0%, #C73E1D 100%);
            --gradient-success: linear-gradient(135deg, #28A745 0%, #20C997 100%);
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.12);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.16);
            --border-radius: 12px;
            --transition: all 0.3s ease;
        }

        /* ===== GLOBAL STYLES ===== */
        .stApp {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* ===== HEADER STYLING ===== */
        .main-header {
            background: var(--gradient-primary);
            padding: 2.5rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            transform: rotate(30deg);
        }

        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }

        .main-header .subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin-top: 0.5rem;
            position: relative;
            z-index: 1;
        }

        .main-header .header-stats {
            display: flex;
            gap: 2rem;
            margin-top: 1.5rem;
            position: relative;
            z-index: 1;
        }

        .main-header .stat-item {
            text-align: center;
        }

        .main-header .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: white;
        }

        .main-header .stat-label {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.8);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* ===== METRIC CARDS ===== */
        .metric-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }

        @media (max-width: 1200px) {
            .metric-container {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        @media (max-width: 768px) {
            .metric-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        .metric-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }

        .metric-card.students::before { background: var(--gradient-primary); }
        .metric-card.teachers::before { background: var(--gradient-accent); }
        .metric-card.institutions::before { background: var(--gradient-success); }
        .metric-card.avg-students::before { background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%); }
        .metric-card.satisfaction::before { background: linear-gradient(135deg, #17a2b8 0%, #6610f2 100%); }

        .metric-card .icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .metric-card .label {
            font-size: 0.8rem;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
        }

        .metric-card .value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-color);
        }

        .metric-card .delta {
            font-size: 0.75rem;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .metric-card .delta.positive { color: var(--success-color); }
        .metric-card .delta.negative { color: var(--danger-color); }

        /* ===== SECTION HEADERS ===== */
        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e9ecef;
        }

        .section-header .icon {
            font-size: 1.5rem;
        }

        .section-header h2 {
            margin: 0;
            font-size: 1.35rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        /* ===== CHART CARDS ===== */
        .chart-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-sm);
            margin-bottom: 1.5rem;
            transition: var(--transition);
        }

        .chart-card:hover {
            box-shadow: var(--shadow-md);
        }

        .chart-card h3 {
            margin: 0 0 1rem 0;
            font-size: 1rem;
            font-weight: 600;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* ===== SIDEBAR STYLING ===== */
        [data-testid="stSidebar"] {
            background: var(--gradient-primary) !important;
        }

        [data-testid="stSidebar"] > div {
            padding: 1.5rem 1rem;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {
            color: white !important;
        }

        [data-testid="stSidebar"] label {
            font-weight: 500;
        }

        [data-testid="stSidebar"] .stMultiSelect > div > div {
            background: white;
            border-radius: 8px;
        }

        .sidebar-header {
            text-align: center;
            padding: 1rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 1.5rem;
        }

        .sidebar-header h2 {
            font-size: 1.5rem;
            margin: 0;
        }

        .sidebar-header p {
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
            margin: 0.25rem 0 0 0;
        }

        /* ===== BUTTONS ===== */
        .stButton button,
        .stDownloadButton button {
            background: var(--gradient-primary) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.25rem !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .stButton button:hover,
        .stDownloadButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* ===== DATA TABLE STYLING ===== */
        .stDataFrame {
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }

        .stDataFrame th {
            background: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
            padding: 1rem !important;
        }

        .stDataFrame td {
            padding: 0.75rem 1rem !important;
            border-bottom: 1px solid #e9ecef;
        }

        .stDataFrame tr:hover td {
            background: #f8f9fa;
        }

        /* ===== INSIGHT BOX ===== */
        .insight-box {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left: 4px solid var(--info-color);
            padding: 1.25rem;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            margin: 1rem 0;
        }

        .insight-box h4 {
            margin: 0 0 0.75rem 0;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .insight-box ul {
            margin: 0;
            padding-left: 1.25rem;
        }

        .insight-box li {
            margin-bottom: 0.5rem;
            color: #495057;
            line-height: 1.5;
        }

        /* ===== QUALITY INDICATOR ===== */
        .quality-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        .quality-indicator .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .quality-indicator .status-dot.good { background: var(--success-color); }
        .quality-indicator .status-dot.warning { background: var(--warning-color); }
        .quality-indicator .status-dot.danger { background: var(--danger-color); }

        /* ===== TABS STYLING ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: white;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: #6c757d;
            transition: var(--transition);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: #f8f9fa;
            color: var(--primary-color);
        }

        .stTabs [aria-selected="true"] {
            background: white !important;
            color: var(--primary-color) !important;
            border-bottom: 3px solid var(--accent-color) !important;
        }

        /* ===== FOOTER ===== */
        .dashboard-footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
        }

        .dashboard-footer .logo {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        /* ===== PASSWORD SCREEN ===== */
        .password-container {
            max-width: 400px;
            margin: 8% auto;
            background: white;
            padding: 2.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            text-align: center;
        }

        .password-container .lock-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }

        .password-container h1 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }

        .password-container p {
            color: #6c757d;
            margin-bottom: 1.5rem;
        }

        /* ===== ANIMATIONS ===== */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--secondary-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-color);
        }

        /* ===== RECOMMENDATION CARDS ===== */
        .recommendation-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            box-shadow: var(--shadow-sm);
            border-left: 4px solid var(--warning-color);
        }

        .recommendation-card h5 {
            margin: 0;
            color: var(--primary-color);
            font-size: 0.95rem;
        }

        .recommendation-card p {
            margin: 0.5rem 0 0 0;
            color: #6c757d;
            font-size: 0.85rem;
        }

        .recommendation-card .priority {
            float: right;
            background: var(--warning-color);
            color: #1A1A2E;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .recommendation-card .priority.high {
            background: var(--danger-color);
            color: white;
        }

        .recommendation-card .priority.low {
            background: var(--success-color);
            color: white;
        }
    </style>
    """


# =============================================================================
# HTML COMPONENT GENERATORS
# =============================================================================

def get_metric_card_html(icon: str, label: str, value: str, card_class: str) -> str:
    """Generate HTML for a professional metric card."""
    return f"""
    <div class="metric-card {card_class} animate-fade-in">
        <div class="icon">{icon}</div>
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """


def get_section_header_html(icon: str, title: str) -> str:
    """Generate HTML for a section header."""
    return f"""
    <div class="section-header">
        <span class="icon">{icon}</span>
        <h2>{title}</h2>
    </div>
    """


def get_insight_box_html(title: str, insights: List[str]) -> str:
    """Generate HTML for an insight box."""
    insights_html = "\n".join([f"<li>{insight}</li>" for insight in insights])
    return f"""
    <div class="insight-box">
        <h4>💡 {title}</h4>
        <ul>{insights_html}</ul>
    </div>
    """


def get_quality_indicator_html(label: str, value: int, status: str) -> str:
    """Generate HTML for a data quality indicator."""
    return f"""
    <div class="quality-indicator">
        <span class="status-dot {status}"></span>
        <span>{label}: <strong>{value}</strong></span>
    </div>
    """


# =============================================================================
# CHART UTILITIES
# =============================================================================

def apply_chart_style(fig: go.Figure, title: str = None) -> go.Figure:
    """Apply consistent professional styling to any Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, sans-serif", size=11, color="#2c3e50"),
        title=dict(
            text=title,
            font=dict(size=14, color=THEME.primary),
            x=0.5,
            xanchor="center"
        ) if title else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            gridcolor="#e9ecef",
            linecolor="#dee2e6",
            ticks="outside"
        ),
        yaxis=dict(
            gridcolor="#e9ecef",
            linecolor="#dee2e6",
            ticks="outside"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor=THEME.primary,
            font_size=12
        )
    )
    return fig


def create_bar_chart(df, x, y, title, color=None, orientation="v", 
                     color_scale=None, show_values=False):
    """Create a professionally styled bar chart."""
    if color_scale is None:
        color_scale = [THEME.primary, THEME.secondary]
    
    fig = px.bar(
        df, x=x, y=y,
        color=color if color else y,
        orientation=orientation,
        color_continuous_scale=color_scale
    )
    
    apply_chart_style(fig, title)
    
    if show_values:
        fig.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside',
            textfont=dict(size=10, color="#6c757d")
        )
    
    if not color:
        fig.update_coloraxes(showscale=False)
    
    fig.update_traces(
        marker_line_width=0,
        marker_opacity=0.9
    )
    
    return fig


def create_pie_chart(df, names, values, title, hole=0.45, colors=None):
    """Create a professionally styled donut/pie chart."""
    if colors is None:
        colors = CHART_COLORS
    
    fig = px.pie(
        df, names=names, values=values,
        hole=hole,
        color_discrete_sequence=colors
    )
    
    apply_chart_style(fig, title)
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=11, color="white"),
        marker=dict(line=dict(color="white", width=2)),
        pull=[0.02] * len(df)
    )
    
    if hole > 0:
        total = df[values].sum()
        fig.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:9px'>Total</span>",
            x=0.5, y=0.5,
            font_size=14,
            font_color=THEME.primary,
            showarrow=False
        )
    
    return fig


def create_gauge_chart(value, title, max_value=100, thresholds=(40, 70)):
    """Create a gauge chart for KPI visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=12)),
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1},
            'bar': {'color': THEME.primary},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e9ecef",
            'steps': [
                {'range': [0, thresholds[0]], 'color': "#dc3545"},
                {'range': [thresholds[0], thresholds[1]], 'color': "#ffc107"},
                {'range': [thresholds[1], max_value], 'color': "#28a745"}
            ],
            'threshold': {
                'line': {'color': "#1A1A2E", 'width': 3},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'font': {'size': 20, 'color': THEME.primary}}
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=30, r=30, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_empty_chart(message="No data available"):
    """Create a placeholder chart when no data is available."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color="#6c757d")
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)",
        height=250
    )
    return fig


# =============================================================================
# DATA PROCESSING UTILITIES
# =============================================================================

@dataclass
class DataQualityReport:
    """Container for data quality metrics."""
    total_records: int
    complete_records: int
    missing_emails: int
    missing_phones: int
    missing_students: int
    duplicate_records: int
    quality_score: float


def extract_country_from_institution(institution: str) -> str:
    """Extract country name from institution string."""
    if pd.isna(institution):
        return "Unknown"
    
    institution = str(institution)
    
    # Known country mappings from the data
    country_patterns = {
        "Kenya": "Kenya",
        "Nigeria": "Nigeria",
        "Ghana": "Ghana",
        "Ethiopia": "Ethiopia",
        "Tanzania": "Tanzania",
        "South Sudan": "South Sudan",
        "Malawi": "Malawi",
        "Senegal": "Senegal",
        "Madagascar": "Madagascar",
        "Uganda": "Uganda",
        "Zambia": "Zambia",
        "Rwanda": "Rwanda",
        "Burundi": "Burundi",
        "DRC": "DRC",
        "Congo": "DRC",
        "Cameroon": "Cameroon",
        "Togo": "Togo",
        "Benin": "Benin",
        "Ivory Coast": "Ivory Coast",
        "Côte d'Ivoire": "Ivory Coast",
        "Burkina Faso": "Burkina Faso",
        "Mali": "Mali",
        "Niger": "Niger",
        "Mozambique": "Mozambique"
    }
    
    for pattern, country in country_patterns.items():
        if pattern.lower() in institution.lower():
            return country
    
    # Try to extract from the end of institution name
    parts = institution.replace("-", " ").split()
    for part in reversed(parts):
        for pattern, country in country_patterns.items():
            if pattern.lower() == part.lower():
                return country
    
    return "Other"


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply comprehensive cleaning pipeline to the dataframe."""
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    # Clean institution names
    if "Institution" in df_clean.columns:
        df_clean["Institution"] = df_clean["Institution"].str.strip()
    
    # Clean numeric columns
    if "Number of Students" in df_clean.columns:
        df_clean["Number of Students"] = pd.to_numeric(
            df_clean["Number of Students"], errors="coerce"
        ).fillna(0).astype(int)
    
    # Clean categorical columns
    for col in ["Electude Domain", "Language"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip() if df_clean[col].dtype == object else df_clean[col]
    
    # Handle teacher names
    if "Teacher / Trainer" in df_clean.columns:
        df_clean["Teacher / Trainer"] = df_clean["Teacher / Trainer"].fillna("Unknown").str.strip()
    
    # Clean contact info
    if "EMAIL" in df_clean.columns:
        df_clean["EMAIL"] = df_clean["EMAIL"].str.lower().str.strip()
    
    if "Phone number" in df_clean.columns:
        df_clean["Phone number"] = df_clean["Phone number"].astype(str).str.strip()
        df_clean["Phone number"] = df_clean["Phone number"].replace("nan", "")
    
    # Extract country from institution name
    if "Institution" in df_clean.columns:
        df_clean["Country"] = df_clean["Institution"].apply(extract_country_from_institution)
    
    return df_clean


def generate_quality_report(df: pd.DataFrame) -> DataQualityReport:
    """Generate a comprehensive data quality report."""
    if df.empty:
        return DataQualityReport(0, 0, 0, 0, 0, 0, 0.0)
    
    total = len(df)
    missing_emails = df["EMAIL"].isna().sum() if "EMAIL" in df.columns else 0
    missing_phones = df["Phone number"].isna().sum() if "Phone number" in df.columns else 0
    missing_students = (df["Number of Students"] == 0).sum() if "Number of Students" in df.columns else 0
    duplicates = df.duplicated().sum()
    
    required = ["Institution", "Teacher / Trainer", "EMAIL"]
    available_required = [col for col in required if col in df.columns]
    complete = df[available_required].notna().all(axis=1).sum() if available_required else total
    
    # Calculate quality score
    score = (
        (complete / total) * 40 +
        ((total - missing_emails - missing_phones) / (total * 2)) * 30 +
        ((total - duplicates) / total) * 30
    )
    
    return DataQualityReport(
        total_records=total,
        complete_records=int(complete),
        missing_emails=int(missing_emails),
        missing_phones=int(missing_phones),
        missing_students=int(missing_students),
        duplicate_records=int(duplicates),
        quality_score=min(100, max(0, score))
    )


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="🌍 Electude Africa TVET Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': f"""
        **Electude Africa TVET Analytics Dashboard**
        
        Version 2.0.0 | © {datetime.now().year} Electude Africa
        
        Professional TVET Analytics Platform
        """
    }
)


# =============================================================================
# AUTHENTICATION
# =============================================================================

# Hardcoded password for deployment (can be overridden by secrets)
DASHBOARD_PASSWORD = "Steve@036"

def check_password() -> bool:
    """Secure password authentication with modern UI."""
    
    def password_entered():
        """Validate password and update session state."""
        # Check secrets first, then fallback to hardcoded password
        try:
            stored_password = st.secrets.get("passwords", {}).get("password", DASHBOARD_PASSWORD)
        except:
            stored_password = DASHBOARD_PASSWORD
        
        if st.session_state.get("password") == stored_password:
            st.session_state["password_correct"] = True
            st.session_state.pop("password", None)
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="password-container">
            <div class="lock-icon">🔐</div>
            <h1>Authentication Required</h1>
            <p>Enter your credentials to access the dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Enter your password...",
            label_visibility="collapsed"
        )
        
        if "password_correct" in st.session_state and not st.session_state.password_correct:
            st.error("⚠️ Invalid password. Please try again.")
    
    return False


# =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render_header():
    """Render the professional dashboard header."""
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Electude Africa TVET Analytics</h1>
        <p class="subtitle">
            Comprehensive analytics platform for Technical and Vocational Education across Africa
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Render the professional sidebar with filters."""
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>🌍 Electude Africa</h2>
            <p>Analytics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 📊 Data Filters")
        
        # Language filter
        languages = sorted(df["Language"].dropna().unique().tolist()) if "Language" in df.columns else []
        language_filter = st.multiselect(
            "🌐 Language",
            languages,
            default=languages,
            help="Filter institutions by teaching language"
        )
        
        # Country filter
        countries = sorted(df["Country"].dropna().unique().tolist()) if "Country" in df.columns else []
        country_filter = st.multiselect(
            "🏳️ Country",
            countries,
            default=countries,
            help="Filter by country"
        )
        
        # Domain filter
        domains = sorted(df["Electude Domain"].dropna().unique().tolist()) if "Electude Domain" in df.columns else []
        domain_filter = st.multiselect(
            "🔧 Electude Domain",
            domains,
            default=domains,
            help="Filter by Electude domain"
        )
        
        st.markdown("---")
        
        # Display settings
        st.markdown("### ⚙️ Display Settings")
        show_metrics = st.checkbox("Show Key Metrics", value=True)
        show_charts = st.checkbox("Show Visualizations", value=True)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Apply filters
        filtered = df.copy()
        
        if language_filter:
            filtered = filtered[filtered["Language"].isin(language_filter)]
        if country_filter:
            filtered = filtered[filtered["Country"].isin(country_filter)]
        if domain_filter:
            filtered = filtered[filtered["Electude Domain"].isin(domain_filter)]
        
        st.metric("Filtered Records", len(filtered))
        
        return filtered, {
            "show_metrics": show_metrics,
            "show_charts": show_charts
        }


def render_metrics(filtered: pd.DataFrame):
    """Render the key metrics section."""
    
    total_students = int(filtered["Number of Students"].sum()) if "Number of Students" in filtered.columns else 0
    total_teachers = filtered["Teacher / Trainer"].nunique() if "Teacher / Trainer" in filtered.columns else 0
    institutions = filtered["Institution"].nunique() if "Institution" in filtered.columns else 0
    countries = filtered["Country"].nunique() if "Country" in filtered.columns else 0
    avg_students = round(total_students / institutions, 1) if institutions > 0 else 0
    
    st.markdown(f"""
    <div class="metric-container">
        {get_metric_card_html("🎓", "Total Students", f"{total_students:,}", "students")}
        {get_metric_card_html("👨‍🏫", "Active Teachers", f"{total_teachers:,}", "teachers")}
        {get_metric_card_html("🏛️", "Institutions", f"{institutions:,}", "institutions")}
        {get_metric_card_html("🌍", "Countries", f"{countries:,}", "avg-students")}
        {get_metric_card_html("📊", "Avg Students/Institution", f"{avg_students:,.1f}", "satisfaction")}
    </div>
    """, unsafe_allow_html=True)


def render_charts(filtered: pd.DataFrame):
    """Render all visualization charts."""
    
    st.markdown(get_section_header_html("📊", "Students Distribution Analysis"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        students_by_inst = (
            filtered.groupby("Institution")["Number of Students"]
            .sum().reset_index()
            .sort_values("Number of Students", ascending=True)
        )
        
        if not students_by_inst.empty:
            fig = create_bar_chart(
                students_by_inst.tail(15),
                x="Number of Students", y="Institution",
                title="Students per Institution (Top 15)",
                color="Number of Students",
                orientation="h",
                color_scale=[THEME.primary, THEME.secondary]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart(), use_container_width=True)
    
    with col2:
        lang_dist = (
            filtered.groupby("Language")["Number of Students"]
            .sum().reset_index()
        )
        
        if not lang_dist.empty:
            # Map language codes to display names
            lang_dist["Language Display"] = lang_dist["Language"].map(
                lambda x: LANGUAGE_DISPLAY.get(x, x)
            )
            fig = create_pie_chart(
                lang_dist,
                names="Language Display", values="Number of Students",
                title="Language Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No language data"), use_container_width=True)
    
    # Country Distribution
    st.markdown(get_section_header_html("🌍", "Distribution by Country"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        country_dist = (
            filtered.groupby("Country").agg({
                "Number of Students": "sum",
                "Institution": "nunique",
                "Teacher / Trainer": "count"
            }).reset_index()
            .rename(columns={"Institution": "Institutions", "Teacher / Trainer": "Teachers"})
            .sort_values("Number of Students", ascending=False)
        )
        
        if not country_dist.empty:
            # Add flag emojis
            country_dist["Country Flag"] = country_dist["Country"].map(
                lambda x: f"{COUNTRY_FLAGS.get(x, '🏳️')} {x}"
            )
            
            fig = create_bar_chart(
                country_dist.head(10),
                x="Country Flag", y="Number of Students",
                title="Students by Country (Top 10)",
                color="Number of Students",
                color_scale=[THEME.accent, THEME.danger],
                show_values=True
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart(), use_container_width=True)
    
    with col2:
        teachers_by_country = (
            filtered.groupby("Country")["Teacher / Trainer"]
            .count().reset_index()
            .rename(columns={"Teacher / Trainer": "Teachers"})
            .sort_values("Teachers", ascending=False)
            .head(10)
        )
        
        if not teachers_by_country.empty:
            teachers_by_country["Country Flag"] = teachers_by_country["Country"].map(
                lambda x: f"{COUNTRY_FLAGS.get(x, '🏳️')} {x}"
            )
            
            fig = create_bar_chart(
                teachers_by_country,
                x="Country Flag", y="Teachers",
                title="Teachers by Country (Top 10)",
                color="Teachers",
                color_scale=[THEME.teal, THEME.success]
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart(), use_container_width=True)


def render_ai_insights(filtered: pd.DataFrame):
    """Generate and render AI-powered insights."""
    
    st.markdown(get_section_header_html("🤖", "AI-Powered Insights"), unsafe_allow_html=True)
    
    total_students = int(filtered["Number of Students"].sum()) if "Number of Students" in filtered.columns else 0
    institutions = filtered["Institution"].nunique() if "Institution" in filtered.columns else 0
    countries = filtered["Country"].nunique() if "Country" in filtered.columns else 0
    
    students_by_inst = filtered.groupby("Institution")["Number of Students"].sum().reset_index()
    top_school = students_by_inst.loc[students_by_inst["Number of Students"].idxmax(), "Institution"] if not students_by_inst.empty else "N/A"
    top_students = int(students_by_inst["Number of Students"].max()) if not students_by_inst.empty else 0
    
    lang_dist = filtered.groupby("Language")["Number of Students"].sum().reset_index()
    most_language = lang_dist.loc[lang_dist["Number of Students"].idxmax(), "Language"] if not lang_dist.empty else "N/A"
    most_language_display = LANGUAGE_DISPLAY.get(most_language, most_language)
    
    country_dist = filtered.groupby("Country")["Number of Students"].sum().reset_index()
    top_country = country_dist.loc[country_dist["Number of Students"].idxmax(), "Country"] if not country_dist.empty else "N/A"
    top_country_flag = COUNTRY_FLAGS.get(top_country, "🏳️")
    
    insights = [
        f"**{top_school}** leads with **{top_students:,} students** - the largest institution in the network.",
        f"**{most_language_display}** is the primary language of instruction across the platform.",
        f"The Electude Africa network spans **{institutions} active institutions** across **{countries} countries**.",
        f"**Total reach: {total_students:,} learners** engaged through the platform.",
        f"**{top_country_flag} {top_country}** has the highest student enrollment."
    ]
    
    st.markdown(get_insight_box_html("Key Data Insights", insights), unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("#### 📋 Strategic Recommendations")
    
    recommendations = [
        ("Capacity Planning", f"Focus resources on {top_country} where demand is highest.", "high"),
        ("Language Strategy", f"With {most_language_display} as the dominant language, ensure content optimization.", "medium"),
        ("Teacher Development", "Implement training programs to improve student-to-teacher ratios.", "medium"),
        ("Data Quality", "Improve data collection for student counts in institutions with missing data.", "low")
    ]
    
    for title, desc, priority in recommendations:
        priority_class = "high" if priority == "high" else "low" if priority == "low" else ""
        st.markdown(f"""
        <div class="recommendation-card">
            <span class="priority {priority_class}">{priority.upper()}</span>
            <h5>{title}</h5>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)


def render_teacher_directory(filtered: pd.DataFrame):
    """Render the searchable teacher directory."""
    
    st.markdown(get_section_header_html("👨‍🏫", "Teacher Directory"), unsafe_allow_html=True)
    
    search = st.text_input("🔍 Search teachers", placeholder="Enter name, institution, or email...", key="teacher_search")
    
    directory = filtered.copy()
    if search:
        mask = (
            directory["Teacher / Trainer"].str.contains(search, case=False, na=False) |
            directory["Institution"].str.contains(search, case=False, na=False) |
            directory["EMAIL"].str.contains(search, case=False, na=False)
        )
        directory = directory[mask]
    
    cols = ["Institution", "Teacher / Trainer", "EMAIL", "Phone number", "Number of Students", "Language", "Country"]
    available = [c for c in cols if c in directory.columns]
    
    if not directory.empty:
        st.dataframe(
            directory[available].sort_values("Number of Students", ascending=False),
            use_container_width=True,
            height=400
        )
    else:
        st.info("No teachers match your search criteria.")


def render_data_quality(df: pd.DataFrame, report: DataQualityReport):
    """Render the data quality panel."""
    
    st.markdown(get_section_header_html("🧹", "Data Quality Report"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_gauge_chart(report.quality_score, "Quality Score")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Completeness Metrics")
        st.markdown(get_quality_indicator_html(
            "Missing Emails", report.missing_emails,
            "good" if report.missing_emails == 0 else "warning" if report.missing_emails < 10 else "danger"
        ), unsafe_allow_html=True)
        st.markdown(get_quality_indicator_html(
            "Missing Phones", report.missing_phones,
            "good" if report.missing_phones == 0 else "warning" if report.missing_phones < 10 else "danger"
        ), unsafe_allow_html=True)
        st.markdown(get_quality_indicator_html(
            "No Student Count", report.missing_students,
            "good" if report.missing_students == 0 else "warning" if report.missing_students < 10 else "danger"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### Record Statistics")
        st.metric("Total Records", report.total_records)
        st.metric("Complete Records", report.complete_records)
        st.metric("Completion Rate", f"{(report.complete_records / report.total_records * 100):.1f}%" if report.total_records > 0 else "N/A")


def render_export_section(filtered: pd.DataFrame):
    """Render the data export section."""
    
    st.markdown(get_section_header_html("📥", "Export Data"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 Download CSV",
            data=filtered.to_csv(index=False),
            file_name=f"electude_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="📋 Download JSON",
            data=filtered.to_json(orient="records", indent=2),
            file_name=f"electude_export_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        st.download_button(
            label="📊 Download Summary",
            data=filtered.describe(include="all").to_string(),
            file_name=f"electude_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


def render_footer():
    """Render the dashboard footer."""
    st.markdown(f"""
    <div class="dashboard-footer">
        <div class="logo">🌍 Electude Africa</div>
        <p>Professional TVET Analytics Platform | © {datetime.now().year}</p>
        <p style="font-size: 0.75rem; color: #adb5bd;">
            Built with ❤️ for African Technical Education
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Check authentication
    if not check_password():
        st.stop()
    
    # Load CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # Load data - look for the CSV file in the workspace directory
    @st.cache_data
    def load_data():
        try:
            # Try workspace directory first
            main_df = pd.read_csv("electude_data.csv")
        except FileNotFoundError:
            try:
                # Try parent directory
                main_df = pd.read_csv("../electude_data.csv")
            except FileNotFoundError:
                st.error("❌ Data file 'electude_data.csv' not found. Please ensure it's in the workspace directory.")
                st.stop()
        
        return main_df
    
    with st.spinner("Loading data..."):
        main_df = load_data()
    
    # Clean data
    df_clean = clean_dataframe(main_df)
    quality_report = generate_quality_report(df_clean)
    
    # Render sidebar
    filtered, settings = render_sidebar(df_clean)
    
    # Main content
    if settings["show_metrics"]:
        render_metrics(filtered)
    
    st.divider()
    
    if settings["show_charts"]:
        render_charts(filtered)
    
    st.divider()
    
    # AI Insights
    render_ai_insights(filtered)
    st.divider()
    
    # Teacher directory
    render_teacher_directory(filtered)
    st.divider()
    
    # Data quality
    render_data_quality(df_clean, quality_report)
    st.divider()
    
    # Export
    render_export_section(filtered)
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()