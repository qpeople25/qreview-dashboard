# qReview L&D Dashboard

Professional Learning & Development Assessment and ROI Dashboard

## 🚀 Overview

qReview is a comprehensive L&D assessment and ROI calculation tool designed to help organizations measure, analyze, and optimize their learning and development investments. Built with Streamlit, it provides a professional, user-friendly interface for 360° L&D assessments and data-driven ROI projections.

## ✨ Features

### Core Functionality
- **360° L&D Assessment Tool** - Comprehensive evaluation across 8 key elements
- **Assessment-Driven ROI Calculator** - Data-driven return on investment projections
- **Multi-Organization Support** - Scalable multi-tenant architecture
- **Role-Based Access Control** - Admin, Client, and Respondent user roles
- **Professional Analytics & Reporting** - Interactive dashboards and insights

### Assessment Elements
- Strategic Connection
- Needs Analysis
- Learning Design
- Learning Culture
- Platform and Tools
- Integration with Talent
- Learning Impact
- Future Capability

### ROI Calculator Features
- Industry-specific multipliers
- Implementation quality factors
- Assessment score integration
- Business impact projections
- Expandable element analysis

## 🏗️ Architecture

- **Frontend**: Streamlit web application
- **Backend**: Python with SQLite database
- **Authentication**: Role-based user management
- **Data Processing**: Pandas for analysis and visualization
- **Charts**: Plotly for interactive visualizations

## 🚀 Deployment

### Streamlit Cloud (Production)
This application is deployed via Streamlit Cloud for production use.

### Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/qreview-dashboard.git
cd qreview-dashboard

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run dashboard_clean.py
```

## 📊 Pilot Status

Currently piloting with **VSO (Voluntary Service Overseas)** - a not-for-profit organization committed to international development.

## 🔧 Technical Requirements

- Python 3.8+
- Streamlit 1.28+
- Pandas 2.0+
- Plotly 5.0+
- SQLite3

## 📁 Project Structure

```
qreview-dashboard/
├── dashboard_clean.py          # Main application
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules
├── database/                  # Database files
│   └── dashboard.db          # SQLite database
└── assets/                    # Static files
    └── qReview - logos.png   # Logo files
```

## 🎯 Use Cases

- **L&D Teams**: Assess current learning ecosystem maturity
- **HR Professionals**: Measure training program effectiveness
- **Business Leaders**: Calculate L&D investment ROI
- **Consultants**: Provide data-driven L&D insights
- **Organizations**: Benchmark against industry standards

## 🔐 Security Features

- Role-based access control
- Secure password hashing
- Session management
- Input validation and sanitization
- GDPR compliance considerations

## 📈 Roadmap

- [x] Core assessment functionality
- [x] ROI calculator with industry multipliers
- [x] Multi-organization support
- [x] Role-based user management
- [x] Professional UI/UX
- [ ] Production deployment
- [ ] VSO pilot completion
- [ ] Enhanced analytics
- [ ] API integration capabilities

## 🤝 Contributing

This project is currently in pilot phase. For inquiries about collaboration or deployment, please contact the development team.

## 📄 License

Proprietary software - All rights reserved.

---

**Built with ❤️ for better L&D outcomes**

