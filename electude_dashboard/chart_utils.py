"""
Chart Utilities for Electude Africa Analytics Dashboard
Provides standardized, professional chart creation functions
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

# Import configuration
from config import config, CHART_COLORS, DIVERGENT_COLORS


@dataclass
class ChartTheme:
    """Theme settings for consistent chart styling."""
    primary_color: str = config.colors.primary
    secondary_color: str = config.colors.secondary
    accent_color: str = config.colors.accent
    success_color: str = config.colors.success
    font_family: str = config.charts.font_family
    title_size: int = config.charts.title_font_size
    label_size: int = config.charts.label_font_size


def apply_chart_style(fig: go.Figure, title: str = None) -> go.Figure:
    """
    Apply consistent professional styling to any Plotly figure.
    
    Args:
        fig: Plotly figure object
        title: Optional chart title
        
    Returns:
        Styled Plotly figure
    """
    fig.update_layout(
        template="plotly_white",
        font=dict(
            family=ChartTheme.font_family,
            size=ChartTheme.label_size,
            color="#2c3e50"
        ),
        title=dict(
            text=title,
            font=dict(size=ChartTheme.title_size, color="#1E3A5F"),
            x=0.5,
            xanchor="center"
        ) if title else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            gridcolor="#e9ecef",
            linecolor="#dee2e6",
            ticks="outside",
            tickfont=dict(size=ChartTheme.label_size)
        ),
        yaxis=dict(
            gridcolor="#e9ecef",
            linecolor="#dee2e6",
            ticks="outside",
            tickfont=dict(size=ChartTheme.label_size)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor="#1E3A5F",
            font_size=12,
            font_family=ChartTheme.font_family
        )
    )
    
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str = None,
    orientation: str = "v",
    color_scale: List[str] = None,
    show_values: bool = False,
    horizontal_labels: bool = False
) -> go.Figure:
    """
    Create a professionally styled bar chart.
    
    Args:
        df: Input dataframe
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        color: Column for color encoding
        orientation: 'v' for vertical, 'h' for horizontal
        color_scale: List of colors for gradient
        show_values: Whether to show value labels on bars
        horizontal_labels: Rotate x-axis labels horizontally
        
    Returns:
        Styled Plotly figure
    """
    if color_scale is None:
        color_scale = [config.colors.primary, config.colors.secondary]
    
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color if color else y,
        orientation=orientation,
        color_continuous_scale=color_scale,
    )
    
    # Apply styling
    apply_chart_style(fig, title)
    
    # Add value labels if requested
    if show_values:
        fig.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside',
            textfont=dict(size=10, color="#6c757d")
        )
    
    # Handle horizontal labels
    if horizontal_labels:
        fig.update_xaxes(tickangle=45)
    
    # Remove color bar for single-color charts
    if not color:
        fig.update_coloraxes(showscale=False)
    
    # Improve bar styling
    fig.update_traces(
        marker_line_width=0,
        marker_opacity=0.9
    )
    
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    hole: float = 0.4,
    colors: List[str] = None
) -> go.Figure:
    """
    Create a professionally styled donut/pie chart.
    
    Args:
        df: Input dataframe
        names: Column for slice names
        values: Column for slice values
        title: Chart title
        hole: Size of the center hole (0 for pie, 0.4-0.6 for donut)
        colors: List of colors for slices
        
    Returns:
        Styled Plotly figure
    """
    if colors is None:
        colors = CHART_COLORS
    
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=hole,
        color_discrete_sequence=colors
    )
    
    # Apply styling
    apply_chart_style(fig, title)
    
    # Add percentage labels
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=12, color="white"),
        marker=dict(line=dict(color="white", width=2)),
        pull=[0.02] * len(df),
        rotation=45
    )
    
    # Center the title
    fig.update_layout(
        annotations=[
            dict(
                text=f"<b>{df[values].sum():,}</b><br><span style='font-size:10px'>Total</span>",
                x=0.5, y=0.5,
                font_size=16,
                font_color="#1E3A5F",
                showarrow=False
            )
        ] if hole > 0 else []
    )
    
    return fig


def create_horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str = None,
    color_scale: List[str] = None,
    show_values: bool = True
) -> go.Figure:
    """
    Create a professionally styled horizontal bar chart.
    Optimized for displaying rankings or comparisons.
    
    Args:
        df: Input dataframe
        x: Column for x-axis (values)
        y: Column for y-axis (categories)
        title: Chart title
        color: Column for color encoding
        color_scale: Color gradient
        show_values: Show value labels
        
    Returns:
        Styled Plotly figure
    """
    return create_bar_chart(
        df=df,
        x=x,
        y=y,
        title=title,
        color=color,
        orientation="h",
        color_scale=color_scale,
        show_values=show_values
    )


def create_histogram(
    df: pd.DataFrame,
    x: str,
    title: str,
    color: str = None,
    nbins: int = 20,
    show_kde: bool = False
) -> go.Figure:
    """
    Create a professionally styled histogram.
    
    Args:
        df: Input dataframe
        x: Column to plot
        title: Chart title
        color: Optional color column
        nbins: Number of bins
        show_kde: Show kernel density estimate (as line)
        
    Returns:
        Styled Plotly figure
    """
    fig = px.histogram(
        df,
        x=x,
        color=color,
        nbins=nbins,
        color_discrete_sequence=[config.colors.success] if not color else CHART_COLORS,
        opacity=0.85
    )
    
    apply_chart_style(fig, title)
    
    # Style bars
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="white"
    )
    
    return fig


def create_gauge_chart(
    value: float,
    title: str,
    max_value: float = 100,
    thresholds: Tuple[float, float] = (40, 70),
    colors: Tuple[str, str, str] = ("#dc3545", "#ffc107", "#28a745")
) -> go.Figure:
    """
    Create a gauge/bullet chart for KPI visualization.
    
    Args:
        value: Current value
        title: Chart title
        max_value: Maximum possible value
        thresholds: Yellow and green threshold values
        colors: Colors for (danger, warning, success) zones
        
    Returns:
        Styled Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=14)),
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1, 'tickcolor': "#6c757d"},
            'bar': {'color': config.colors.primary},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e9ecef",
            'steps': [
                {'range': [0, thresholds[0]], 'color': colors[0]},
                {'range': [thresholds[0], thresholds[1]], 'color': colors[1]},
                {'range': [thresholds[1], max_value], 'color': colors[2]}
            ],
            'threshold': {
                'line': {'color': "#1A1A2E", 'width': 3},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'font': {'size': 24, 'color': config.colors.primary}}
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_treemap(
    df: pd.DataFrame,
    path: List[str],
    values: str,
    title: str,
    color: str = None
) -> go.Figure:
    """
    Create a treemap visualization for hierarchical data.
    
    Args:
        df: Input dataframe
        path: List of columns defining hierarchy
        values: Column for size values
        title: Chart title
        color: Column for color encoding
        
    Returns:
        Styled Plotly figure
    """
    fig = px.treemap(
        df,
        path=path,
        values=values,
        color=color if color else values,
        color_continuous_scale=[config.colors.primary, config.colors.secondary, config.colors.accent]
    )
    
    apply_chart_style(fig, title)
    
    fig.update_traces(
        textinfo="label+value+percent root",
        textfont=dict(size=12),
        marker=dict(line=dict(color="white", width=1))
    )
    
    return fig


def create_comparison_chart(
    df: pd.DataFrame,
    x: str,
    y1: str,
    y2: str,
    title: str,
    labels: Tuple[str, str] = None
) -> go.Figure:
    """
    Create a dual-axis comparison chart.
    
    Args:
        df: Input dataframe
        x: X-axis column
        y1: First y-axis column
        y2: Second y-axis column
        title: Chart title
        labels: Tuple of (y1_label, y2_label)
        
    Returns:
        Styled Plotly figure
    """
    if labels is None:
        labels = (y1, y2)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add first trace
    fig.add_trace(
        go.Bar(
            x=df[x],
            y=df[y1],
            name=labels[0],
            marker_color=config.colors.primary,
            opacity=0.8
        ),
        secondary_y=False
    )
    
    # Add second trace as line
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y2],
            name=labels[1],
            mode="lines+markers",
            line=dict(color=config.colors.accent, width=2),
            marker=dict(size=8)
        ),
        secondary_y=True
    )
    
    apply_chart_style(fig, title)
    
    # Set axis titles
    fig.set_xaxes(title_text=x)
    fig.set_yaxes(title_text=labels[0], secondary_y=False)
    fig.set_yaxes(title_text=labels[1], secondary_y=True)
    
    return fig


def create_heatmap(
    df: pd.DataFrame,
    title: str,
    x_col: str = None,
    y_col: str = None,
    value_col: str = None,
    colorscale: str = "Blues"
) -> go.Figure:
    """
    Create a correlation heatmap or matrix visualization.
    
    Args:
        df: Input dataframe (can be correlation matrix or raw data)
        title: Chart title
        x_col: X-axis column (for raw data)
        y_col: Y-axis column (for raw data)
        value_col: Value column (for raw data)
        colorscale: Plotly colorscale name
        
    Returns:
        Styled Plotly figure
    """
    # If raw data provided, pivot it
    if x_col and y_col and value_col:
        matrix = df.pivot(index=y_col, columns=x_col, values=value_col)
    else:
        matrix = df
    
    fig = px.imshow(
        matrix,
        color_continuous_scale=colorscale,
        aspect="auto"
    )
    
    apply_chart_style(fig, title)
    
    fig.update_traces(
        hovertemplate="<b>%{y}</b> - %{x}<br>Value: %{z:.2f}<extra></extra>"
    )
    
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    size: str = None,
    color: str = None,
    hover_name: str = None,
    trendline: bool = False
) -> go.Figure:
    """
    Create a professionally styled scatter plot.
    
    Args:
        df: Input dataframe
        x: X-axis column
        y: Y-axis column
        title: Chart title
        size: Column for marker size
        color: Column for color encoding
        hover_name: Column for hover labels
        trendline: Add regression trendline
        
    Returns:
        Styled Plotly figure
    """
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=hover_name,
        trendline="ols" if trendline else None,
        color_discrete_sequence=CHART_COLORS,
        size_max=20
    )
    
    apply_chart_style(fig, title)
    
    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=1, color="white")),
        selector=dict(mode='markers')
    )
    
    return fig


def create_empty_chart(message: str = "No data available") -> go.Figure:
    """
    Create a placeholder chart when no data is available.
    
    Args:
        message: Message to display
        
    Returns:
        Placeholder Plotly figure
    """
    fig = go.Figure()
    
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#6c757d")
    )
    
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        height=300
    )
    
    return fig