# qReview L&D Dashboard - Deployment Guide

## Overview
The qReview L&D Dashboard is a self-contained platform for conducting 360-degree learning and development assessments. All assessments are conducted within the platform itself - no external survey tools required.

## System Requirements
- Python 3.8+
- SQLite3 (included with Python)
- Web browser for Streamlit interface

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run dashboard_clean.py
```

### 3. Access the Platform
- Open your browser to the URL shown in the terminal (typically http://localhost:8501)
- Login with default admin credentials:
  - Email: admin@qpeople.com
  - Password: admin123

## Platform Features

### Built-in Assessment System
- **8 L&D Elements**: Strategic Connection, Needs Analysis, Learning Design, Learning Culture, Platform & Tools, Integration with Talent, Learning Impact, Future Capability
- **4 User Groups**: SLT (Senior Leadership), LDT (L&D Team), MGR (Managers), LNR (Learners)
- **Multi-tenant Architecture**: Support for multiple organizations

### User Roles
- **Admin**: Platform management, user creation, organization setup
- **Client**: Access to dashboard insights and reports
- **Respondent**: Complete assessments within the platform

### Dashboard Tabs
1. **Overview**: Key metrics and performance indicators
2. **Heatmap**: Visual score representation across elements and groups
3. **Radar Chart**: Multi-dimensional performance analysis
4. **Strengths & Gaps**: Identify areas of excellence and improvement
5. **Insights**: Data-driven insights and recommendations
6. **Misalignment**: Group perception differences analysis
7. **Drill Down**: Detailed element-level analysis
8. **ROI Calculator**: Learning investment return analysis
9. **Action Plan**: Prioritized improvement recommendations
10. **Survey**: Built-in assessment interface

## Data Management

### Database
- SQLite database stored in `data/qreview.sqlite3`
- Automatic schema creation and updates
- Multi-tenant data isolation

### User Management
- Create organizations and users through admin interface
- Bulk user upload via CSV
- Role-based access control

### Assessment Data
- All survey responses stored in platform database
- Real-time dashboard updates
- Export capabilities for analysis

## Deployment Options

### Local Development
```bash
streamlit run dashboard_clean.py
```

### Production Deployment
1. **Streamlit Cloud**: Upload to streamlit.io
2. **Heroku**: Deploy as Streamlit app
3. **AWS/GCP**: Container deployment
4. **Self-hosted**: Reverse proxy with nginx/apache

### Environment Variables
No external API keys required - the platform is self-contained.

## Security Features
- User authentication and session management
- Role-based access control
- Organization data isolation
- Secure password storage

## Support
- Platform admin can manage all aspects through the web interface
- No external dependencies or API integrations
- Self-contained assessment and reporting system

## Migration from Typeform
If migrating from existing Typeform data:
1. Export data to CSV format
2. Use the built-in CSV upload feature in the dashboard
3. Data will be automatically processed and integrated

## Troubleshooting
- **Database Issues**: Check `data/` directory permissions
- **Port Conflicts**: Change port with `streamlit run dashboard_clean.py --server.port 8502`
- **User Access**: Verify user roles and organization assignments in admin panel
