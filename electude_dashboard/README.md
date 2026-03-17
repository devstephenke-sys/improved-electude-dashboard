# Electude Africa TVET Analytics Dashboard

A professional, enterprise-grade analytics dashboard for Technical and Vocational Education (TVET) data across Africa.

![Dashboard Preview](https://via.placeholder.com/1200x600/1E3A5F/FFFFFF?text=Electude+Africa+Dashboard)

## 🌟 Features

### Modern UI/UX
- **Professional Design**: Clean, modern interface with custom CSS styling
- **Responsive Layout**: Works seamlessly on desktop and tablet devices
- **Interactive Charts**: Beautiful Plotly visualizations with custom themes
- **Real-time Filtering**: Dynamic sidebar filters for data exploration

### Analytics Capabilities
- **Key Metrics Dashboard**: At-a-glance KPIs with animated metric cards
- **Student Distribution Analysis**: Institution and country-level insights
- **Teacher Directory**: Searchable database with contact information
- **User Satisfaction Analysis**: Survey feedback with sentiment visualization
- **AI-Powered Insights**: Automated data insights and recommendations

### Data Quality
- **Quality Reports**: Comprehensive data validation and scoring
- **Missing Value Detection**: Identify data gaps across fields
- **Duplicate Detection**: Automatic identification of duplicate records

### Export Options
- **CSV Export**: Download filtered data in CSV format
- **JSON Export**: Structured data export for APIs
- **Summary Reports**: Statistical summaries in text format

## 📁 Project Structure

```
electude_dashboard/
├── __init__.py              # Package initialization
├── app.py                   # Main Streamlit application
├── config.py                # Configuration and theme settings
├── styles.py                # Custom CSS styling
├── data_processor.py        # Data loading and processing utilities
├── chart_utils.py           # Plotly chart creation functions
├── generate_sample_data.py  # Sample data generator
├── README.md                # Documentation
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd electude_dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data** (optional)
   ```bash
   python generate_sample_data.py
   ```

4. **Create secrets file** (for authentication)
   Create `.streamlit/secrets.toml`:
   ```toml
   [passwords]
   password = "your_secure_password"
   ```

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

## 📊 Data Requirements

### Main Data File (`electude_data.csv`)

| Column | Type | Description |
|--------|------|-------------|
| Institution | string | Name of the TVET institution |
| Teacher / Trainer | string | Name of the teacher/trainer |
| Number of Students | integer | Count of enrolled students |
| EMAIL | string | Contact email address |
| Phone number | string | Contact phone number |
| Language | string | Primary teaching language |
| Electude Domain | string | Subject area/specialization |

### Survey Data File (`survey_data.csv`) - Optional

| Column | Type | Description |
|--------|------|-------------|
| Institution | string | Name of the institution |
| Satisfaction Score | float | Score from 1.0 to 5.0 |
| Feedback | string | Textual feedback |
| Respondent Type | string | Teacher, Student, or Administrator |

## ⚙️ Configuration

### Theme Customization

Edit `config.py` to customize colors and settings:

```python
@dataclass
class ThemeColors:
    primary: str = "#1E3A5F"      # Main brand color
    secondary: str = "#2E86AB"     # Accent color
    accent: str = "#F18F01"        # Highlight color
    success: str = "#28A745"       # Success states
    warning: str = "#FFC107"       # Warning states
    danger: str = "#DC3545"        # Error states
```

### Feature Flags

Enable or disable features in `config.py`:

```python
@dataclass
class AppConfig:
    enable_ai_insights: bool = True
    enable_data_export: bool = True
    enable_survey_analysis: bool = True
```

## 🎨 Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Blue | `#1E3A5F` | Headers, primary actions |
| Secondary Blue | `#2E86AB` | Secondary elements |
| Accent Orange | `#F18F01` | Highlights, CTAs |
| Success Green | `#28A745` | Positive metrics |
| Warning Yellow | `#FFC107` | Alerts, warnings |
| Danger Red | `#DC3545` | Errors, critical |

### Typography

- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Bold, primary color
- **Body**: Regular weight, dark gray

### Component Styling

- **Cards**: White background, 12px border radius, subtle shadow
- **Buttons**: Gradient backgrounds, hover animations
- **Charts**: Clean white template, consistent colors
- **Tables**: Striped rows, sortable columns

## 📈 Chart Types

The dashboard includes various chart types:

1. **Bar Charts** - Horizontal and vertical for comparisons
2. **Pie/Donut Charts** - Distribution visualization
3. **Gauge Charts** - KPI indicators
4. **Histograms** - Distribution analysis
5. **Treemaps** - Hierarchical data

## 🔐 Authentication

The dashboard includes password protection. Configure in `.streamlit/secrets.toml`:

```toml
[passwords]
password = "your_secure_password_here"
```

## 📱 Responsive Design

The dashboard is optimized for:
- Desktop browsers (1920x1080 and above)
- Large tablets (1024x768)
- Print output (via CSS print media queries)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

© 2024 Electude Africa. All rights reserved.

## 📞 Support

For support, contact:
- Email: support@electude.africa
- Website: https://electude.africa

---

Built with ❤️ for African Technical Education