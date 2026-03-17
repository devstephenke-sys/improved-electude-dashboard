"""
Electude Africa TVET Analytics Dashboard
=====================================
A professional, enterprise-grade analytics dashboard for TVET institution data.
Features modern UI, comprehensive data analysis, and AI-powered insights.

Author: Electude Africa Data Science Team
Version: 2.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import custom modules
from styles import (
    get_custom_css, 
    get_metric_card_html, 
    get_section_header_html,
    get_insight_box_html,
    get_quality_indicator_html
)
from config import config, CHART_COLORS, COUNTRY_FLAGS, LANGUAGE_DISPLAY
from data_processor import (
    DataLoader, 
    DataCleaner, 
    DataValidator, 
    DataAggregator,
    process_pipeline,
    DataQualityReport
)
from chart_utils import (
    create_bar_chart,
    create_pie_chart,
    create_horizontal_bar_chart,
    create_histogram,
    create_gauge_chart,
    create_treemap,
    create_empty_chart,
    apply_chart_style
)


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title=f"{config.app.app_icon} {config.app.app_name}",
    layout=config.app.layout,
    initial_sidebar_state="expanded",
    menu_items={
        'About': f"""
        **{config.app.app_name}**
        
        Version 2.0.0 | © {datetime.now().year} Electude Africa
        
        Professional TVET Analytics Platform
        """,
        'Report a bug': 'https://electude.africa/support',
        'Get help': 'https://electude.africa/help'
    }
)


# =============================================================================
# AUTHENTICATION
# =============================================================================

def check_password() -> bool:
    """
    Secure password authentication with modern UI.
    Returns True if authentication successful.
    """
    def password_entered():
        """Validate password and update session state."""
        if st.session_state.get("password") == st.secrets.get("passwords", {}).get("password", "admin"):
            st.session_state["password_correct"] = True
            st.session_state.pop("password", None)  # Clear password from memory
        else:
            st.session_state["password_correct"] = False

    # Check if already authenticated
    if st.session_state.get("password_correct", False):
        return True

    # Render authentication UI
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="password-container">
            <div class="lock-icon">🔐</div>
            <h1>Authentication Required</h1>
            <p style="text-align: center; color: #6c757d; margin-bottom: 1.5rem;">
                Enter your credentials to access the dashboard
            </p>
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
# SIDEBAR CONFIGURATION
# =============================================================================

def render_sidebar(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Render the professional sidebar with filters and controls.
    
    Args:
        df: Full dataset
        
    Returns:
        Tuple of (filtered dataframe, filter settings)
    """
    with st.sidebar:
        # Sidebar header
        st.markdown("""
        <div class="sidebar-header">
            <h2>🌍 Electude Africa</h2>
            <p>Analytics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Filter section
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
        
        # Institution type filter (if available)
        if "Institution_Type" in df.columns:
            inst_types = sorted(df["Institution_Type"].dropna().unique().tolist())
            inst_type_filter = st.multiselect(
                "🏛️ Institution Type",
                inst_types,
                default=inst_types,
                help="Filter by institution category"
            )
        else:
            inst_type_filter = []
        
        st.markdown("---")
        
        # Display settings
        st.markdown("### ⚙️ Display Settings")
        
        show_metrics = st.checkbox("Show Key Metrics", value=True)
        show_charts = st.checkbox("Show Visualizations", value=True)
        show_data_table = st.checkbox("Show Data Table", value=True)
        
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
        if inst_type_filter and "Institution_Type" in filtered.columns:
            filtered = filtered[filtered["Institution_Type"].isin(inst_type_filter)]
        
        filter_settings = {
            "languages": language_filter,
            "countries": country_filter,
            "institution_types": inst_type_filter,
            "show_metrics": show_metrics,
            "show_charts": show_charts,
            "show_data_table": show_data_table
        }
        
        # Show filtered count
        st.metric("Filtered Records", len(filtered))
        
        return filtered, filter_settings


# =============================================================================
# HEADER COMPONENT
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


# =============================================================================
# METRICS COMPONENT
# =============================================================================

def render_metrics(filtered: pd.DataFrame, survey_df: pd.DataFrame = None):
    """
    Render the key metrics section with professional cards.
    
    Args:
        filtered: Filtered dataframe
        survey_df: Optional survey dataframe
    """
    # Calculate metrics
    total_students = int(filtered["Number of Students"].sum()) if "Number of Students" in filtered.columns else 0
    total_teachers = filtered["Teacher / Trainer"].nunique() if "Teacher / Trainer" in filtered.columns else 0
    institutions = filtered["Institution"].nunique() if "Institution" in filtered.columns else 0
    avg_students = round(total_students / institutions, 1) if institutions > 0 else 0
    
    # Calculate satisfaction if survey data available
    avg_satisfaction = "N/A"
    if survey_df is not None and not survey_df.empty and "Satisfaction Score" in survey_df.columns:
        avg_score = survey_df["Satisfaction Score"].mean()
        avg_satisfaction = f"{avg_score:.2f}"
    
    # Render metrics using HTML cards
    st.markdown("""
    <div class="metric-container">
        {}
        {}
        {}
        {}
        {}
    </div>
    """.format(
        get_metric_card_html("🎓", "Total Students", f"{total_students:,}", "students"),
        get_metric_card_html("👨‍🏫", "Active Teachers", f"{total_teachers:,}", "teachers"),
        get_metric_card_html("🏛️", "Institutions", f"{institutions:,}", "institutions"),
        get_metric_card_html("📊", "Avg Students/Institution", f"{avg_students:,.1f}", "avg-students"),
        get_metric_card_html("⭐", "Avg. Satisfaction", avg_satisfaction if avg_satisfaction == "N/A" else f"{avg_satisfaction} / 5", "satisfaction")
    ), unsafe_allow_html=True)


# =============================================================================
# CHARTS SECTION
# =============================================================================

def render_charts(filtered: pd.DataFrame):
    """
    Render all visualization charts.
    
    Args:
        filtered: Filtered dataframe
    """
    # Students per Institution Chart
    st.markdown(get_section_header_html("📊", "Students Distribution by Institution"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Aggregate by institution
        students_by_inst = (
            filtered.groupby("Institution")["Number of Students"]
            .sum()
            .reset_index()
            .sort_values("Number of Students", ascending=True)
        )
        
        if not students_by_inst.empty:
            fig = create_horizontal_bar_chart(
                students_by_inst.tail(15),
                x="Number of Students",
                y="Institution",
                title="Students per Institution (Top 15)",
                color="Number of Students",
                color_scale=[config.colors.primary, config.colors.secondary]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No institution data available"), use_container_width=True)
    
    with col2:
        # Language distribution
        lang_dist = DataAggregator.get_language_distribution(filtered)
        
        if not lang_dist.empty:
            fig = create_pie_chart(
                lang_dist,
                names="Language",
                values="Students",
                title="Language Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No language data"), use_container_width=True)
    
    # Country Distribution
    st.markdown(get_section_header_html("🌍", "Distribution by Country"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        country_dist = DataAggregator.get_country_distribution(filtered)
        
        if not country_dist.empty:
            fig = create_bar_chart(
                country_dist.head(10),
                x="Country",
                y="Students",
                title="Students by Country (Top 10)",
                color="Students",
                color_scale=[config.colors.accent, config.colors.danger],
                show_values=True
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No country data available"), use_container_width=True)
    
    with col2:
        # Teachers by institution
        teachers_by_inst = (
            filtered.groupby("Institution")["Teacher / Trainer"]
            .count()
            .reset_index()
            .rename(columns={"Teacher / Trainer": "Teachers"})
            .sort_values("Teachers", ascending=False)
            .head(10)
        )
        
        if not teachers_by_inst.empty:
            fig = create_bar_chart(
                teachers_by_inst,
                x="Institution",
                y="Teachers",
                title="Teachers per Institution (Top 10)",
                color="Teachers",
                color_scale=[config.colors.teal, config.colors.success]
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No teacher data available"), use_container_width=True)


# =============================================================================
# SURVEY ANALYSIS SECTION
# =============================================================================

def render_survey_analysis(survey_df: pd.DataFrame, filtered: pd.DataFrame):
    """
    Render the user satisfaction analysis section.
    
    Args:
        survey_df: Survey dataframe
        filtered: Main filtered dataframe
    """
    st.markdown(get_section_header_html("⭐", "User Satisfaction Analysis"), unsafe_allow_html=True)
    
    if survey_df.empty or "Satisfaction Score" not in survey_df.columns:
        st.warning("⚠️ No survey data available. Upload `survey_data.csv` to enable satisfaction analysis.")
        return
    
    # Filter survey data based on main filters
    filtered_survey = survey_df[
        survey_df["Institution"].isin(filtered["Institution"].unique())
    ] if "Institution" in survey_df.columns else survey_df
    
    if filtered_survey.empty:
        st.info("No survey data matches the current filters.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Satisfaction by institution
        satisfaction_by_inst = (
            filtered_survey.groupby("Institution")["Satisfaction Score"]
            .mean()
            .reset_index()
            .sort_values("Satisfaction Score", ascending=True)
        )
        
        fig = create_horizontal_bar_chart(
            satisfaction_by_inst,
            x="Satisfaction Score",
            y="Institution",
            title="Average Satisfaction Score by Institution",
            color="Satisfaction Score",
            color_scale=["#dc3545", "#ffc107", "#28a745"]
        )
        fig.update_xaxes(range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Score distribution
        fig = create_histogram(
            filtered_survey,
            x="Satisfaction Score",
            title="Score Distribution",
            nbins=10
        )
        fig.update_traces(marker_color=config.colors.success)
        st.plotly_chart(fig, use_container_width=True)
    
    # Feedback browser
    if "Feedback" in filtered_survey.columns:
        st.markdown("#### 💬 Qualitative Feedback Browser")
        
        # Search functionality
        search_term = st.text_input("🔍 Search feedback", placeholder="Enter keywords...")
        
        feedback_df = filtered_survey[["Institution", "Feedback", "Satisfaction Score"]].copy()
        
        if search_term:
            feedback_df = feedback_df[
                feedback_df["Feedback"].str.contains(search_term, case=False, na=False)
            ]
        
        st.dataframe(
            feedback_df.sort_values("Satisfaction Score", ascending=False),
            use_container_width=True,
            height=300
        )


# =============================================================================
# AI INSIGHTS SECTION
# =============================================================================

def render_ai_insights(filtered: pd.DataFrame, survey_df: pd.DataFrame = None):
    """
    Generate and render AI-powered insights from the data.
    
    Args:
        filtered: Filtered dataframe
        survey_df: Optional survey dataframe
    """
    st.markdown(get_section_header_html("🤖", "AI-Powered Insights"), unsafe_allow_html=True)
    
    # Calculate key metrics for insights
    total_students = int(filtered["Number of Students"].sum()) if "Number of Students" in filtered.columns else 0
    institutions = filtered["Institution"].nunique() if "Institution" in filtered.columns else 0
    
    # Top institution
    students_by_inst = DataAggregator.get_top_institutions(filtered, n=1)
    top_school = students_by_inst.iloc[0]["Institution"] if not students_by_inst.empty else "N/A"
    top_students = int(students_by_inst.iloc[0]["Total Students"]) if not students_by_inst.empty else 0
    
    # Language insights
    lang_dist = DataAggregator.get_language_distribution(filtered)
    most_language = lang_dist.iloc[0]["Language"] if not lang_dist.empty else "N/A"
    
    # Country insights
    country_dist = DataAggregator.get_country_distribution(filtered)
    top_country = country_dist.iloc[0]["Country"] if not country_dist.empty else "N/A"
    top_country_students = int(country_dist.iloc[0]["Students"]) if not country_dist.empty else 0
    
    # Generate insights
    insights = [
        f"**{top_school}** leads with **{top_students:,} students**, representing the largest institution in the network.",
        f"**{most_language}** is the primary language of instruction across the platform.",
        f"The Electude Africa network spans **{institutions} active institutions** across multiple countries.",
        f"**Total student reach: {total_students:,} learners** engaged through the platform.",
        f"**{top_country}** has the highest student enrollment with **{top_country_students:,} students**."
    ]
    
    st.markdown(get_insight_box_html("Key Data Insights", insights), unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("#### 📋 Strategic Recommendations")
    
    recommendations = [
        {
            "title": "Expansion Opportunity",
            "description": f"Consider expanding programs in {top_country} where demand is highest.",
            "priority": "High"
        },
        {
            "title": "Language Strategy",
            "description": f"With {most_language} as the dominant language, ensure all content is optimized for this market.",
            "priority": "Medium"
        },
        {
            "title": "Teacher Development",
            "description": "Implement teacher training programs to improve student-to-teacher ratios.",
            "priority": "Medium"
        }
    ]
    
    for rec in recommendations:
        priority_color = {
            "High": config.colors.danger,
            "Medium": config.colors.warning,
            "Low": config.colors.success
        }.get(rec["priority"], config.colors.info)
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid {priority_color};">
            <strong>{rec['title']}</strong>
            <span style="float: right; background: {priority_color}; color: white; padding: 2px 8px; 
                        border-radius: 12px; font-size: 0.75rem;">{rec['priority']}</span>
            <p style="margin: 0.5rem 0 0 0; color: #6c757d;">{rec['description']}</p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TEACHER DIRECTORY SECTION
# =============================================================================

def render_teacher_directory(filtered: pd.DataFrame):
    """
    Render the searchable teacher directory.
    
    Args:
        filtered: Filtered dataframe
    """
    st.markdown(get_section_header_html("👨‍🏫", "Teacher Directory"), unsafe_allow_html=True)
    
    # Search input
    search = st.text_input(
        "🔍 Search teachers",
        placeholder="Enter teacher name, institution, or email...",
        key="teacher_search"
    )
    
    # Filter based on search
    directory = filtered.copy()
    
    if search:
        mask = (
            directory["Teacher / Trainer"].str.contains(search, case=False, na=False) |
            directory["Institution"].str.contains(search, case=False, na=False) |
            directory["EMAIL"].str.contains(search, case=False, na=False)
        )
        directory = directory[mask]
    
    # Display columns
    display_cols = [
        "Institution", "Teacher / Trainer", "EMAIL", 
        "Phone number", "Number of Students", "Language"
    ]
    
    available_cols = [col for col in display_cols if col in directory.columns]
    
    if not directory.empty:
        st.dataframe(
            directory[available_cols].sort_values("Number of Students", ascending=False),
            use_container_width=True,
            height=400
        )
    else:
        st.info("No teachers match your search criteria.")


# =============================================================================
# DATA QUALITY SECTION
# =============================================================================

def render_data_quality(df: pd.DataFrame, quality_report: DataQualityReport):
    """
    Render the data quality panel.
    
    Args:
        df: Full dataframe
        quality_report: Data quality report
    """
    st.markdown(get_section_header_html("🧹", "Data Quality Report"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_gauge_chart(
            quality_report.quality_score,
            "Overall Quality Score",
            max_value=100
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Completeness Metrics")
        st.markdown(get_quality_indicator_html(
            "Missing Emails", 
            quality_report.missing_emails,
            "good" if quality_report.missing_emails == 0 else "warning" if quality_report.missing_emails < 10 else "danger"
        ), unsafe_allow_html=True)
        
        st.markdown(get_quality_indicator_html(
            "Missing Phone Numbers",
            quality_report.missing_phones,
            "good" if quality_report.missing_phones == 0 else "warning" if quality_report.missing_phones < 10 else "danger"
        ), unsafe_allow_html=True)
        
        st.markdown(get_quality_indicator_html(
            "Duplicate Records",
            quality_report.duplicate_records,
            "good" if quality_report.duplicate_records == 0 else "warning" if quality_report.duplicate_records < 5 else "danger"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### Record Statistics")
        st.metric("Total Records", quality_report.total_records)
        st.metric("Complete Records", quality_report.complete_records)
        st.metric("Completion Rate", f"{(quality_report.complete_records / quality_report.total_records * 100):.1f}%" if quality_report.total_records > 0 else "N/A")


# =============================================================================
# EXPORT SECTION
# =============================================================================

def render_export_section(filtered: pd.DataFrame):
    """
    Render the data export section.
    
    Args:
        filtered: Filtered dataframe to export
    """
    st.markdown(get_section_header_html("📥", "Export Data"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        csv_data = filtered.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"electude_data_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # JSON Export
        json_data = filtered.to_json(orient="records", indent=2)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name=f"electude_data_export_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        # Summary Report Export
        summary = filtered.describe(include="all").to_string()
        st.download_button(
            label="📊 Download Summary",
            data=summary,
            file_name=f"electude_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


# =============================================================================
# FOOTER
# =============================================================================

def render_footer():
    """Render the dashboard footer."""
    st.markdown("""
    <div class="dashboard-footer">
        <div class="logo">🌍 Electude Africa</div>
        <p>Professional TVET Analytics Platform | © {}</p>
        <p style="font-size: 0.75rem; color: #adb5bd;">
            Built with ❤️ for African Technical Education
        </p>
    </div>
    """.format(datetime.now().year), unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Check authentication
    if not check_password():
        st.stop()
    
    # Load custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # Load data
    with st.spinner("Loading data..."):
        df = DataLoader.load_main_data(config.app.main_data_file)
        survey_df = DataLoader.load_survey_data(config.app.survey_data_file)
    
    if df.empty:
        st.error("❌ Unable to load data. Please check that the data file exists.")
        st.stop()
    
    # Process data
    df_clean, quality_report = process_pipeline(df)
    
    # Render sidebar and get filters
    filtered, filter_settings = render_sidebar(df_clean)
    
    # Main content area
    if filter_settings["show_metrics"]:
        render_metrics(filtered, survey_df)
    
    st.divider()
    
    if filter_settings["show_charts"]:
        render_charts(filtered)
    
    st.divider()
    
    # Survey Analysis (if data available)
    if config.app.enable_survey_analysis and not survey_df.empty:
        render_survey_analysis(survey_df, filtered)
        st.divider()
    
    # AI Insights
    if config.app.enable_ai_insights:
        render_ai_insights(filtered, survey_df)
        st.divider()
    
    # Teacher Directory
    if filter_settings["show_data_table"]:
        render_teacher_directory(filtered)
        st.divider()
    
    # Data Quality
    render_data_quality(df_clean, quality_report)
    st.divider()
    
    # Export Section
    if config.app.enable_data_export:
        render_export_section(filtered)
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()