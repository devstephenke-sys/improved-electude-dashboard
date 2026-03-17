"""
Custom CSS Styles for Electude Africa Analytics Dashboard
Professional, colorful, and modern styling system
"""

def get_custom_css():
    return """
    <style>
        /* ===== ROOT VARIABLES & THEME ===== */
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
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.2);
            --border-radius: 12px;
            --transition: all 0.3s ease;
        }

        /* ===== GLOBAL STYLES ===== */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }

        /* ===== HEADER STYLING ===== */
        .main-header {
            background: var(--gradient-primary);
            padding: 2rem;
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

        /* ===== METRIC CARDS ===== */
        .metric-container {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }

        .metric-card {
            flex: 1;
            min-width: 180px;
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
            font-size: 0.85rem;
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
            font-size: 0.8rem;
            margin-top: 0.25rem;
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
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        /* ===== CARDS & CONTAINERS ===== */
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
            font-size: 1.1rem;
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

        [data-testid="stSidebar"] .sidebar-content {
            padding: 1rem;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white !important;
        }

        [data-testid="stSidebar"] label {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 500;
        }

        [data-testid="stSidebar"] .stMultiSelect > div {
            background: white;
            border-radius: 8px;
        }

        .sidebar-header {
            text-align: center;
            padding: 1rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 1.5rem;
        }

        .sidebar-header img {
            width: 60px;
            height: 60px;
            margin-bottom: 0.5rem;
        }

        .sidebar-header h2 {
            color: white !important;
            font-size: 1.25rem;
            margin: 0;
        }

        .sidebar-header p {
            color: rgba(255,255,255,0.8);
            font-size: 0.85rem;
            margin: 0.25rem 0 0 0;
        }

        /* ===== BUTTONS ===== */
        .stButton button {
            background: var(--gradient-primary) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }

        .stDownloadButton button {
            background: var(--gradient-success) !important;
        }

        /* ===== DATA QUALITY INDICATORS ===== */
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
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .quality-indicator .status-dot.good { background: var(--success-color); }
        .quality-indicator .status-dot.warning { background: var(--warning-color); }
        .quality-indicator .status-dot.danger { background: var(--danger-color); }

        /* ===== DATA TABLE STYLING ===== */
        .stDataFrame {
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }

        .stDataFrame table {
            border-collapse: separate;
            border-spacing: 0;
        }

        .stDataFrame th {
            background: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.8rem;
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

        /* ===== ALERTS & NOTIFICATIONS ===== */
        .stAlert {
            border-radius: var(--border-radius);
            border: none;
            box-shadow: var(--shadow-sm);
        }

        .stAlert[data-baseweb="notification"] {
            background: white;
        }

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
            padding-left: 1.5rem;
        }

        .insight-box li {
            margin-bottom: 0.5rem;
            color: #495057;
        }

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

        /* ===== ANIMATIONS ===== */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }

        /* ===== PROGRESS BAR ===== */
        .progress-bar {
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 0.5rem 0;
        }

        .progress-bar .fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
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

        /* ===== RESPONSIVE DESIGN ===== */
        @media (max-width: 768px) {
            .metric-card {
                min-width: 100%;
            }

            .main-header h1 {
                font-size: 1.75rem;
            }
        }

        /* ===== PLOTLY CHART OVERRIDES ===== */
        .js-plotly-plot .plotly .modebar {
            right: 0.5rem !important;
        }

        /* ===== SCROLLBAR STYLING ===== */
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

        /* ===== PASSWORD SCREEN ===== */
        .password-container {
            max-width: 400px;
            margin: 10% auto;
            background: white;
            padding: 2.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
        }

        .password-container h1 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .password-container .lock-icon {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .password-container input {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            transition: var(--transition);
        }

        .password-container input:focus {
            border-color: var(--secondary-color);
            outline: none;
            box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.2);
        }

        /* ===== TOOLTIP ===== */
        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip .tooltip-text {
            visibility: hidden;
            background-color: var(--dark-color);
            color: white;
            text-align: center;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.85rem;
            white-space: nowrap;
        }

        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }
    </style>
    """

def get_metric_card_html(icon, label, value, card_class, delta=None, delta_text=None):
    """Generate HTML for a professional metric card."""
    delta_html = ""
    if delta is not None:
        delta_class = "positive" if delta >= 0 else "negative"
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<div class="delta {delta_class}">{arrow} {abs(delta)}% {delta_text or ""}</div>'
    
    return f"""
    <div class="metric-card {card_class} animate-fade-in">
        <div class="icon">{icon}</div>
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        {delta_html}
    </div>
    """

def get_section_header_html(icon, title):
    """Generate HTML for a section header."""
    return f"""
    <div class="section-header">
        <span class="icon">{icon}</span>
        <h2>{title}</h2>
    </div>
    """

def get_chart_card_html(title, icon, content_id):
    """Generate HTML for a chart card container."""
    return f"""
    <div class="chart-card">
        <h3>{icon} {title}</h3>
        <div id="{content_id}"></div>
    </div>
    """

def get_insight_box_html(title, insights_list):
    """Generate HTML for an insight box."""
    insights_html = "\n".join([f"<li>{insight}</li>" for insight in insights_list])
    return f"""
    <div class="insight-box">
        <h4>💡 {title}</h4>
        <ul>
            {insights_html}
        </ul>
    </div>
    """

def get_quality_indicator_html(label, value, status):
    """Generate HTML for a data quality indicator."""
    return f"""
    <div class="quality-indicator">
        <span class="status-dot {status}"></span>
        <span>{label}: <strong>{value}</strong></span>
    </div>
    """