"""
Electude Africa TVET Analytics Dashboard
======================================
Professional analytics platform for Technical and Vocational Education

Usage:
    streamlit run electude_dashboard/app.py
"""

__version__ = "2.0.0"
__author__ = "Electude Africa Data Science Team"

from .config import config, CHART_COLORS
from .data_processor import DataLoader, DataCleaner, DataValidator, DataAggregator
from .chart_utils import (
    create_bar_chart,
    create_pie_chart,
    create_horizontal_bar_chart,
    create_gauge_chart
)
from .styles import get_custom_css, get_metric_card_html