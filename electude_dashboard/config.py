"""
Configuration settings for Electude Africa Analytics Dashboard
Centralized configuration for easy maintenance and customization
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import plotly.express as px

@dataclass
class ThemeColors:
    """Color palette for the dashboard theme."""
    primary: str = "#1E3A5F"
    secondary: str = "#2E86AB"
    accent: str = "#F18F01"
    success: str = "#28A745"
    warning: str = "#FFC107"
    danger: str = "#DC3545"
    info: str = "#17A2B8"
    dark: str = "#1A1A2E"
    light: str = "#F8F9FA"
    
    # Extended palette
    teal: str = "#20C997"
    purple: str = "#6F42C1"
    pink: str = "#E83E8C"
    indigo: str = "#6610F2"
    
    # Chart colors
    chart_primary: List[str] = None
    chart_divergent: List[str] = None
    
    def __post_init__(self):
        self.chart_primary = [
            self.primary, self.secondary, self.accent, 
            self.teal, self.purple, self.pink
        ]
        self.chart_divergent = [
            "#0d47a1", "#1976d2", "#42a5f5", "#90caf9",
            "#ffcc80", "#ffa726", "#f57c00", "#e65100"
        ]


@dataclass
class ChartConfig:
    """Configuration for Plotly charts."""
    template: str = "plotly_white"
    font_family: str = "Segoe UI, sans-serif"
    title_font_size: int = 16
    label_font_size: int = 12
    
    # Bar chart defaults
    bar_corner_radius: int = 4
    bar_opacity: float = 0.9
    
    # Pie chart defaults
    pie_hole: float = 0.4
    
    # Layout defaults
    margin: Dict = None
    
    def __post_init__(self):
        self.margin = dict(l=20, r=20, t=40, b=20)


@dataclass
class AppConfig:
    """Main application configuration."""
    app_name: str = "Electude Africa TVET Analytics"
    app_icon: str = "🌍"
    layout: str = "wide"
    
    # Data settings
    main_data_file: str = "electude_data.csv"
    survey_data_file: str = "survey_data.csv"
    
    # Cache settings
    cache_ttl: int = 3600  # 1 hour
    
    # Pagination
    default_page_size: int = 20
    
    # Feature flags
    enable_ai_insights: bool = True
    enable_data_export: bool = True
    enable_survey_analysis: bool = True


@dataclass
class MetricConfig:
    """Configuration for dashboard metrics."""
    icon: str
    label: str
    card_class: str
    format_string: str = "{:,}"
    show_delta: bool = False
    delta_comparison_period: str = "vs last period"


class DashboardConfig:
    """
    Central configuration class for the Electude Africa Dashboard.
    Provides easy access to all settings and theme elements.
    """
    
    def __init__(self):
        self.colors = ThemeColors()
        self.charts = ChartConfig()
        self.app = AppConfig()
        
        # Define metrics configuration
        self.metrics = {
            "students": MetricConfig(
                icon="🎓",
                label="Total Students",
                card_class="students",
                format_string="{:,}"
            ),
            "teachers": MetricConfig(
                icon="👨‍🏫",
                label="Active Teachers",
                card_class="teachers",
                format_string="{:,}"
            ),
            "institutions": MetricConfig(
                icon="🏛️",
                label="Institutions",
                card_class="institutions",
                format_string="{:,}"
            ),
            "avg_students": MetricConfig(
                icon="📊",
                label="Avg Students/Institution",
                card_class="avg-students",
                format_string="{:.1f}"
            ),
            "satisfaction": MetricConfig(
                icon="⭐",
                label="Avg. Satisfaction",
                card_class="satisfaction",
                format_string="{:.2f} / 5"
            )
        }
    
    def get_plotly_template(self):
        """Create a custom Plotly template based on the theme."""
        return {
            "layout": {
                "font": {"family": self.charts.font_family},
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "title": {
                    "font": {"size": self.charts.title_font_size, "color": self.colors.dark}
                },
                "xaxis": {
                    "gridcolor": "#e9ecef",
                    "linecolor": "#dee2e6",
                    "tickfont": {"size": self.charts.label_font_size}
                },
                "yaxis": {
                    "gridcolor": "#e9ecef",
                    "linecolor": "#dee2e6",
                    "tickfont": {"size": self.charts.label_font_size}
                },
                "margin": self.charts.margin
            }
        }
    
    def get_color_scale(self, scale_type: str = "sequential") -> List[str]:
        """
        Get color scale for charts.
        
        Args:
            scale_type: 'sequential', 'divergent', or 'categorical'
        
        Returns:
            List of color hex codes
        """
        scales = {
            "sequential": [self.primary, self.secondary, self.accent],
            "divergent": self.colors.chart_divergent,
            "categorical": self.colors.chart_primary
        }
        return scales.get(scale_type, scales["categorical"])


# Singleton instance
config = DashboardConfig()


# Chart color sequences for easy import
CHART_COLORS = config.colors.chart_primary
DIVERGENT_COLORS = config.colors.chart_divergent

# Country flag mappings for African countries
COUNTRY_FLAGS = {
    "Kenya": "🇰🇪",
    "Uganda": "🇺🇬",
    "Tanzania": "🇹🇿",
    "Rwanda": "🇷🇼",
    "Ethiopia": "🇪🇹",
    "Ghana": "🇬🇭",
    "Nigeria": "🇳🇬",
    "South Africa": "🇿🇦",
    "Zambia": "🇿🇲",
    "Malawi": "🇲🇼",
    "Burundi": "🇧🇮",
    "DRC": "🇨🇩",
    "Somalia": "🇸🇴",
    "South Sudan": "🇸🇸",
    "Sudan": "🇸🇩",
}

# Language display names
LANGUAGE_DISPLAY = {
    "English": "🇬🇧 English",
    "French": "🇫🇷 French",
    "Swahili": "🇰🇪 Swahili",
    "Portuguese": "🇵🇹 Portuguese",
    "Arabic": "🇸🇦 Arabic",
    "Amharic": "🇪🇹 Amharic",
}