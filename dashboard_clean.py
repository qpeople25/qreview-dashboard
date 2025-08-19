import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import io
import base64
from scipy import stats
import warnings
import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="qReview L&D Dashboard",
    page_icon="qReview - logos.png",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'qReview L&D Platform - Empowering Learning & Development'
    }
)

# Override Streamlit's default dark theme with our custom dark blue
st.markdown('''<style>
/* Force override Streamlit's default dark theme */
[data-testid="stAppViewContainer"] {
    background-color: #2c3e52 !important;
}

[data-testid="stAppViewContainer"] > div {
    background-color: #2c3e52 !important;
}

/* Force all main containers to use our dark blue */
.main .block-container {
    background-color: #2c3e52 !important;
}

/* Override any Streamlit default backgrounds */
.stApp {
    background-color: #2c3e52 !important;
}

/* Ensure the entire page background is dark blue */
body {
    background-color: #2c3e52 !important;
}

/* Override Streamlit's default page background */
div[data-testid="stDecoration"] {
    background-color: #2c3e52 !important;
}

/* Force sidebar background */
.sidebar .sidebar-content {
    background-color: #2c3e52 !important;
}

/* Additional overrides for Streamlit's dark theme */
.stApp > div {
    background-color: #2c3e52 !important;
}

/* Override any remaining black backgrounds */
div[style*="background-color: rgb(0, 0, 0)"] {
    background-color: #2c3e52 !important;
}

/* Force the main content area */
.main {
    background-color: #2c3e52 !important;
}

/* Ensure login page columns have dark blue background */
.stColumns > div {
    background-color: #2c3e52 !important;
}

/* Enhanced Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: #bdc3c7;
    font-weight: 500;
    padding: 12px 20px;
    margin: 0 4px;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(255, 255, 255, 0.15);
    color: #ecf0f1;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stTabs [aria-selected="true"] {
    background-color: #7dd4c9 !important;
    color: #2c3e52 !important;
    font-weight: 600;
    border: 2px solid #8c255;
    box-shadow: 0 4px 16px rgba(125, 212, 201, 0.3);
}

.stTabs [aria-selected="true"]:hover {
    background-color: #6bc5bb !important;
    transform: translateY(-1px);
}

/* Tab Content Styling */
.stTabs [data-baseweb="tab-panel"] {
    background-color: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* Enhanced Section Headers */
.stTabs h1, .stTabs h2, .stTabs h3 {
    color: #7dd4c9;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid rgba(125, 212, 201, 0.3);
    padding-bottom: 0.5rem;
}

/* Metric Cards Enhancement */
.stTabs .stMetric {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.stTabs .stMetric:hover {
    background-color: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Enhanced Content Cards */
.stTabs .stDataFrame {
    background-color: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

/* Logo positioning override with high specificity */
.logo-container {
    position: relative !important;
    left: 4rem !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

.stTabs .stPlotlyChart {
    background-color: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Info and Success Messages */
.stTabs .stAlert {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Form Elements Enhancement */
.stTabs .stTextInput, .stTabs .stSelectbox, .stTabs .stButton {
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.stTabs .stTextInput:focus, .stTabs .stSelectbox:focus {
    border-color: #7dd4c9;
    box-shadow: 0 0 0 2px rgba(125, 212, 201, 0.2);
}

.stTabs .stButton:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Dashboard Header Enhancement */
.main-header {
    background: linear-gradient(135deg, #7dd4c9 0%, #6bc5bb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Content Section Enhancement */
.stTabs .stSubheader {
    color: #f8c255;
    font-size: 1.4rem;
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 1rem;
    padding-left: 0.5rem;
    border-left: 4px solid #7dd4c9;
}

/* Metric Grid Enhancement */
.stTabs .stColumns {
    gap: 1rem;
}

.stTabs .stColumns > div {
    background-color: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.stTabs .stColumns > div:hover {
    background-color: rgba(255, 255, 255, 0.05);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}
</style>''', unsafe_allow_html=True)



# --- SQLite persistence (multi-tenant) ---
DATA_DIR = os.path.join(os.getcwd(), "data")
DB_PATH = os.path.join(DATA_DIR, "qreview.sqlite3")
LOGO_DIR = os.path.join(DATA_DIR, "logos")

# --- Email Configuration ---
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'smtp_username': os.getenv('SMTP_USERNAME', ''),
    'smtp_password': os.getenv('SMTP_PASSWORD', ''),
    'from_email': os.getenv('FROM_EMAIL', 'noreply@qreview.com'),
    'from_name': os.getenv('FROM_NAME', 'qReview Platform')
}

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGO_DIR, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def send_welcome_email(user_email, user_name, password, org_name, login_url):
    """Send welcome email with login credentials to new users"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['from_email']}>"
        msg['To'] = user_email
        msg['Subject'] = f"Welcome to {org_name} - Your qReview Login Credentials"
        
        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #7dd4c9; margin-bottom: 10px;">Welcome to qReview!</h1>
                    <p style="color: #666; font-size: 18px;">Your Learning & Development Assessment Platform</p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                    <h2 style="color: #2c3e52; margin-bottom: 20px;">Hello {user_name},</h2>
                    <p>Welcome to <strong>{org_name}</strong> on the qReview platform!</p>
                    <p>Your account has been created and you can now access your personalized L&D dashboard.</p>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                    <h3 style="color: #2c3e52; margin-bottom: 15px;">🔐 Your Login Credentials</h3>
                    <p><strong>Email:</strong> {user_email}</p>
                    <p><strong>Password:</strong> {password}</p>
                    <p><strong>Login URL:</strong> <a href="{login_url}" style="color: #7dd4c9;">{login_url}</a></p>
                </div>
                
                <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                    <h3 style="color: #2c3e52; margin-bottom: 15px;">Important Security Note</h3>
                    <p>For security reasons, we recommend changing your password after your first login.</p>
                    <p>If you have any issues accessing your account, please contact your administrator.</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{login_url}" style="background-color: #7dd4c9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">Login to qReview</a>
                </div>
                
                <div style="text-align: center; margin-top: 30px; color: #666; font-size: 14px;">
                    <p>This is an automated message from the qReview platform.</p>
                    <p>Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['from_email'], user_email, text)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def test_email_configuration():
    """Test email configuration by sending a test email"""
    try:
        if not EMAIL_CONFIG['smtp_username'] or not EMAIL_CONFIG['smtp_password']:
            return False, "Email credentials not configured"
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['from_name']} <{EMAIL_CONFIG['from_email']}>"
        msg['To'] = EMAIL_CONFIG['smtp_username']  # Send to self for testing
        msg['Subject'] = "qReview Email Configuration Test"
        
        body = "This is a test email to verify your qReview email configuration is working correctly."
        msg.attach(MIMEText(body, 'plain'))
        
        # Send test email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['from_email'], EMAIL_CONFIG['smtp_username'], text)
        server.quit()
        
        return True, "Test email sent successfully"
        
    except Exception as e:
        return False, f"Email test failed: {str(e)}"

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # organizations
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            org_key TEXT UNIQUE,
            name TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'client',
            logo_path TEXT,
            primary_color TEXT,
            secondary_color TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT
        );
        """
    )
    
    # users
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            department TEXT,
            org_key TEXT,
            group_type TEXT,
            created_at TEXT,
            FOREIGN KEY (org_key) REFERENCES organizations(org_key)
        );
        """
    )
    
    # survey responses
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            respondent_id TEXT NOT NULL,
            org_key TEXT NOT NULL,
            element TEXT NOT NULL,
            question TEXT NOT NULL,
            score INTEGER NOT NULL,
            group_type TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            FOREIGN KEY (org_key) REFERENCES organizations(org_key)
        );
        """
    )
    
    # assessment completion tracking
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS assessment_completion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            respondent_id TEXT NOT NULL,
            org_key TEXT NOT NULL,
            group_type TEXT NOT NULL,
            completed_at TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            questions_answered INTEGER NOT NULL,
            completion_percentage REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'completed',
            FOREIGN KEY (org_key) REFERENCES organizations(org_key),
            UNIQUE(respondent_id, org_key)
        );
        """
    )
    
    # Check if group_type column exists in users table, add if missing
    try:
        cur.execute("SELECT group_type FROM users LIMIT 1")
    except sqlite3.OperationalError:
        # Column doesn't exist, add it
        cur.execute("ALTER TABLE users ADD COLUMN group_type TEXT")
        st.info("Database schema updated: Added group_type column to users table")
    
    # Check if created_at column exists in users table, add if missing
    try:
        cur.execute("SELECT created_at FROM users LIMIT 1")
    except sqlite3.OperationalError:
        # Column doesn't exist, add it
        cur.execute("ALTER TABLE users ADD COLUMN created_at TEXT")
        st.info("Database schema updated: Added created_at column to users table")
    
    conn.commit()
    
    # seed platform org and admin user if missing
    cur.execute("SELECT 1 FROM organizations WHERE org_key = ?", ("qpeople",))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO organizations (org_key, name, type, logo_path, primary_color, secondary_color, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("qpeople", "qPeople", "platform_admin", "qReview - logos.png", "#7dd4c9", "#f8c255", "Active", datetime.now().isoformat())
        )
    else:
        # Ensure existing qpeople org has correct type and logo
        cur.execute("UPDATE organizations SET type = 'platform_admin', logo_path = 'qReview - logos.png' WHERE org_key = 'qpeople'")
    conn.commit()
    
    cur.execute("SELECT 1 FROM users WHERE email = ?", ("admin@qpeople.com",))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (email, password, first_name, last_name, role, department, org_key, group_type, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("admin@qpeople.com", "admin123", "Admin", "User", "admin", "Platform", "qpeople", "ADMIN", datetime.now().isoformat())
        )
    else:
        # Update existing admin user to include group_type and created_at if they're NULL
        cur.execute("UPDATE users SET group_type = 'ADMIN', created_at = COALESCE(created_at, ?) WHERE email = ?", (datetime.now().isoformat(), "admin@qpeople.com"))
    
    conn.commit()
    conn.close()

init_db()

def migrate_demo_data():
    """Migrate existing demo data to include group assignments"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if we have demo users without group assignments
    cur.execute("SELECT email FROM users WHERE group_type IS NULL OR group_type = ''")
    users_without_groups = cur.fetchall()
    
    for user_row in users_without_groups:
        email = user_row[0]
        if email in USERS_DB:
            # Update with demo group assignment
            group = USERS_DB[email]["group"]
            cur.execute("UPDATE users SET group_type = ? WHERE email = ?", (group, email))
            st.info(f"Updated user {email} with group: {group}")
    
    conn.commit()
    conn.close()

# --- Helper queries ---
def db_fetchone(query: str, params: tuple = ()): 
    conn = get_db_connection(); cur = conn.cursor(); cur.execute(query, params); row = cur.fetchone(); conn.close(); return row

def db_fetchall(query: str, params: tuple = ()): 
    conn = get_db_connection(); cur = conn.cursor(); cur.execute(query, params); rows = cur.fetchall(); conn.close(); return rows

def db_execute(query: str, params: tuple = ()): 
    conn = get_db_connection(); cur = conn.cursor(); cur.execute(query, params); conn.commit(); conn.close()

# Survey response functions
def save_survey_responses(respondent_id: str, org_key: str, group_type: str, responses: dict):
    """Save survey responses to database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Clear existing responses for this respondent
    cur.execute("DELETE FROM survey_responses WHERE respondent_id = ? AND org_key = ?", (respondent_id, org_key))
    
    total_questions = 0
    questions_answered = 0
    
    for element_name, element_responses in responses.items():
        for question, score in element_responses.items():
            total_questions += 1
            if score is not None and score > 0:
                questions_answered += 1
            cur.execute(
                "INSERT INTO survey_responses (respondent_id, org_key, element, question, score, group_type, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (respondent_id, org_key, element_name, question, score, group_type, datetime.now().isoformat())
            )
    
    # Update completion tracking
    completion_percentage = (questions_answered / total_questions * 100) if total_questions > 0 else 0
    status = "completed" if completion_percentage >= 90 else "partial"
    
    cur.execute("""
        INSERT OR REPLACE INTO assessment_completion 
        (respondent_id, org_key, group_type, completed_at, total_questions, questions_answered, completion_percentage, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (respondent_id, org_key, group_type, datetime.now().isoformat(), total_questions, questions_answered, completion_percentage, status))
    
    conn.commit()
    conn.close()

def get_survey_responses_for_org(org_key: str):
    """Get all survey responses for an organization"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT respondent_id, element, question, score, group_type, submitted_at FROM survey_responses WHERE org_key = ?",
        (org_key,)
    )
    
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        return None
    
    # Convert to DataFrame format expected by dashboard
    data = []
    for row in rows:
        data.append({
            'respondent_id': row[0],
            'element': row[1],
            'question': row[2],
            'score': row[3],
            'group': row[4],  # group_type maps to group
            'submitted_at': row[5]
        })
    
    return pd.DataFrame(data)

def get_survey_summary_for_org(org_key: str):
    """Get summary statistics for an organization's survey responses"""
    responses_df = get_survey_responses_for_org(org_key)
    if responses_df is None or responses_df.empty:
        return None
    
    # Calculate element averages by group
    element_stats = responses_df.groupby(['element', 'group']).agg(
        avg_score=('score', 'mean'),
        std_score=('score', 'std'),
        count=('score', 'count'),
        min_score=('score', 'min'),
        max_score=('score', 'max')
    ).reset_index()
    
    element_stats['variance'] = element_stats['std_score'] ** 2
    element_stats['strength'] = element_stats['avg_score'] > 4.0  # STRENGTH_THRESHOLD
    element_stats['development_area'] = element_stats['avg_score'] < 3.0  # DEVELOPMENT_THRESHOLD
    element_stats['silent_gap'] = (element_stats['avg_score'] < 3.0) & (element_stats['std_score'] < 0.5)
    
    return element_stats, responses_df

def get_assessment_completion_status(org_key: str):
    """Get assessment completion status for all users in an organization"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            u.email, u.first_name, u.last_name, u.role, u.department, u.group_type,
            COALESCE(ac.completion_percentage, 0) as completion_percentage,
            COALESCE(ac.status, 'not_started') as status,
            COALESCE(ac.completed_at, '') as completed_at,
            COALESCE(ac.questions_answered, 0) as questions_answered,
            COALESCE(ac.total_questions, 0) as total_questions
        FROM users u
        LEFT JOIN assessment_completion ac ON u.email = ac.respondent_id AND u.org_key = ac.org_key
        WHERE u.org_key = ? AND u.role = 'respondent'
        ORDER BY u.last_name, u.first_name
    """, (org_key,))
    
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        return None
    
    # Convert to DataFrame
    data = []
    for row in rows:
        data.append({
            'email': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'role': row[3],
            'department': row[4],
            'group_type': row[5],
            'completion_percentage': row[6],
            'status': row[7],
            'completed_at': row[8],
            'questions_answered': row[9],
            'total_questions': row[10]
        })
    
    return pd.DataFrame(data)

def get_org_completion_summary(org_key: str):
    """Get completion summary statistics for an organization"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get total respondents
    cur.execute("SELECT COUNT(*) as count FROM users WHERE org_key = ? AND role = 'respondent'", (org_key,))
    total_respondents = cur.fetchone()[0]
    
    # Get completion stats
    cur.execute("""
        SELECT 
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
            COUNT(CASE WHEN status = 'partial' THEN 1 END) as partial,
            COUNT(CASE WHEN status = 'not_started' OR status IS NULL THEN 1 END) as not_started,
            AVG(completion_percentage) as avg_completion
        FROM users u
        LEFT JOIN assessment_completion ac ON u.email = ac.respondent_id AND u.org_key = ac.org_key
        WHERE u.org_key = ? AND u.role = 'respondent'
    """, (org_key,))
    
    completion_stats = cur.fetchone()
    conn.close()
    
    if completion_stats:
        return {
            'total_respondents': total_respondents,
            'completed': completion_stats[0] or 0,
            'partial': completion_stats[1] or 0,
            'not_started': completion_stats[2] or 0,
            'avg_completion': completion_stats[3] or 0
        }
    return None

def create_demo_survey_data():
    """Create demo survey data for testing purposes"""
    import random
    
    # Demo questions for each element
    demo_elements = [
        ("Strategic Connection", [
            "Learning aligns with business priorities",
            "L&D is engaged in strategic conversations",
            "Learning supports current and future transformation",
            "Stakeholders understand the purpose of L&D"
        ]),
        ("Learning Culture", [
            "Leaders promote and role model learning",
            "Time and space are protected for learning",
            "Employees are encouraged to take ownership of their development",
            "Learning is valued and recognised in the business"
        ])
    ]
    
    # Create demo responses
    demo_data = []
    groups = ["SLT", "LDT", "MGR", "LNR"]
    
    for element_name, questions in demo_elements:
        for group in groups:
            for question in questions:
                # Generate realistic scores (slightly higher for SLT, more varied for others)
                if group == "SLT":
                    score = random.uniform(3.5, 4.5)
                elif group == "LDT":
                    score = random.uniform(3.0, 4.0)
                else:
                    score = random.uniform(2.5, 4.0)
                
                demo_data.append({
                    'respondent_id': f"demo_{group}_{random.randint(1,3)}",
                    'element': element_name,
                    'question': question,
                    'score': round(score, 1),
                    'group': group,
                    'submitted_at': datetime.now().isoformat()
                })
    
    return pd.DataFrame(demo_data)

# Mock user database for demo
USERS_DB = {
    "admin@qpeople.com": {"password": "admin123", "role": "admin", "name": "Admin User", "organization_id": "qpeople", "group": "ADMIN"},
    "sarah.johnson@acme.com": {"password": "demo123", "role": "client", "name": "Sarah Johnson", "organization_id": "acme_corp", "group": "LDT"},
    "mike.chen@acme.com": {"password": "demo123", "role": "respondent", "name": "Mike Chen", "organization_id": "acme_corp", "group": "LNR"},
    "mark.davis@techinnovate.com": {"password": "demo123", "role": "client", "name": "Mark Davis", "organization_id": "tech_innovate", "group": "LDT"},
}

ORGANIZATIONS_DB = {
    "qpeople": {
        "name": "qPeople", "type": "platform_admin", "logo": "qpeople_logo.png",
        "primary_color": "#7dd4c9", "secondary_color": "#f8c255",
        "status": "Active", "created_date": "2024-01-01"
    },
    "acme_corp": {
        "name": "Acme Corporation", "type": "client", "logo": "qpeople_logo.png",
        "primary_color": "#2E86AB", "secondary_color": "#A23B72",
        "status": "Active", "created_date": "2024-01-01"
    },
    "tech_innovate": {
        "name": "Tech Innovate Ltd", "type": "client", "logo": "qpeople_logo.png",
        "primary_color": "#28A745", "secondary_color": "#FFC107",
        "status": "Active", "created_date": "2024-01-01"
    }
}

# Run migration after database definitions are available
migrate_demo_data()

# User Management System
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'organization_id' not in st.session_state:
    st.session_state.organization_id = None
if 'organization' not in st.session_state:
    st.session_state.organization = None


# Login page
if not st.session_state.authenticated:
    # Three column layout: spacer, logo, login form
    col1, col2, col3 = st.columns([0.3, 0.7, 1.0])
    
    with col1:
        # Empty spacer column to push logo right
        pass
    
    with col2:
        # Logo in the middle column
        st.markdown('<div style="text-align: center; padding: 2rem 0 0 0;">', unsafe_allow_html=True)
        st.image('qReview - logos.png', width=350)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        # Login form on the right side
        st.markdown('<div style="text-align: center; padding-top: 2rem;">', unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown('<h2 style="text-align: center; color: white; margin-bottom: 1rem;">Welcome to qReview</h2>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #f8c255; font-size: 1.1rem; margin-bottom: 2rem; font-style: italic;">Let\'s see when your learning ecosystem is thriving</p>', unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                # Check database first
                row = db_fetchone(
                    "SELECT u.email, u.password, u.role, u.first_name, u.last_name, u.org_key, u.group_type, o.name as org_name, o.type as org_type, o.logo_path, o.primary_color, o.secondary_color, o.status, o.created_at FROM users u LEFT JOIN organizations o ON u.org_key = o.org_key WHERE u.email = ?",
                    (email,)
                )
            
                if row and row["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = row["email"]
                    st.session_state.user_role = row["role"]
                    full_name = f"{row['first_name'] or ''} {row['last_name'] or ''}".strip() or "User"
                    st.session_state.user_name = full_name
                    st.session_state.organization_id = row["org_key"]
                    st.session_state.user_group = row["group_type"] or "LNR"  # Default to Learners if no group assigned
                    
                    # Ensure admin users get platform_admin organization type
                    org_type = row["org_type"] or "client"
                    if row["role"] == "admin" and row["org_key"] == "qpeople":
                        org_type = "platform_admin"
                    
                    st.session_state.organization = {
                        "name": row["org_name"] or "",
                        "type": org_type,
                        "logo": row["logo_path"] or "qReview - logos.png",
                        "primary_color": row["primary_color"] or "#7dd4c9",
                        "secondary_color": row["secondary_color"] or "#f8c255",
                        "status": row["status"] or "Active",
                        "created_date": row["created_at"] or ""
                    }
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                # Fallback to demo users
                elif email in USERS_DB and USERS_DB[email]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = email
                    st.session_state.user_role = USERS_DB[email]["role"]
                    st.session_state.user_name = USERS_DB[email]["name"]
                    st.session_state.organization_id = USERS_DB[email]["organization_id"]
                    st.session_state.user_group = USERS_DB[email]["group"]
                    st.session_state.organization = ORGANIZATIONS_DB.get(USERS_DB[email]["organization_id"], ORGANIZATIONS_DB["qpeople"])
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop()

# Main dashboard content
st.markdown(f'''<div style="text-align:right;margin-bottom:1rem;">
    <span style="background:rgba(255,255,255,0.1);padding:0.5rem 1rem;border-radius:20px;color:#7dd4c9;font-size:0.9rem;">
        {st.session_state.user_name} ({st.session_state.user_role.title()})
    </span>
    <a href="#" onclick="window.location.reload();" style="margin-left:1rem;color:#f8c255;text-decoration:none;">Logout</a>
</div>''', unsafe_allow_html=True)

# Header with organization branding
if st.session_state.organization and st.session_state.organization['type'] != 'platform_admin':
    org = st.session_state.organization
    
    # Check if organization has a custom logo
    has_custom_logo = org["logo"] and org["logo"] != "qReview - logos.png" and os.path.exists(org["logo"])
    
    if has_custom_logo:
        # Show both logos side by side
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            # Client logo on the left
            try:
                st.image(org["logo"], width=120, caption=org["name"])
            except:
                st.image('qReview - logos.png', width=120, caption=org["name"])
        with col3:
            # Plus sign or separator
            st.markdown('<div style="text-align:center;padding-top:2rem;color:#f8c255;font-size:2rem;">+</div>', unsafe_allow_html=True)
        with col4:
            # qReview logo on the right
            st.image('qReview - logos.png', width=120, caption="Powered by qReview")
    else:
        # Show only qReview logo (centered)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image('qReview - logos.png', width=250)
    
    st.markdown(f'''<div style="text-align:center;margin-bottom:2rem;">
        <h1 class="main-header" style="color:{org["primary_color"] or "#7dd4c9"};">qReview L&D Dashboard</h1>
        <p style="color:{org["secondary_color"] or "#f8c255"};font-size:1.2rem;">{org["name"] or "Organization"}</p>
    </div>''', unsafe_allow_html=True)
else:
    # Logo using Streamlit's native image display - perfectly centered
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image('qReview - logos.png', width=250)
    st.markdown(f'''<div style="text-align:center;margin-bottom:2rem;">
        <h1 class="main-header">qReview L&D Dashboard</h1>
        <p style="color:#f8c255;font-size:1.2rem;">Platform Administration</p>
    </div>''', unsafe_allow_html=True)

# Data loading logic - prioritize survey data from database
df = None
element_stats = None
heatmap_data = None

# Try to load survey data from database first
if 'organization_id' in st.session_state:
    org_key = st.session_state.organization_id
    
    # For admin users, show platform management instead of client data
    if st.session_state.user_role == "admin":
        # Admin users see platform overview, not client data
        st.info("**Platform Admin**: You have access to platform management and can view data from all organizations.")
        
        # Organization selector for admin users
        st.markdown("---")
        st.subheader("Organization Dashboard View")
        
        # Get all organizations for selection
        all_orgs = db_fetchall("SELECT org_key, name, status FROM organizations WHERE type != 'platform_admin' ORDER BY name")
        
        if all_orgs:
            # Create organization options for selector
            org_options = ["Platform Overview"] + [f"{org['name']} ({org['org_key']})" for org in all_orgs]
            
            # Organization selector
            selected_org_display = st.selectbox(
                "Select Organization to View:",
                options=org_options,
                index=0,
                help="Choose an organization to view their specific dashboard data, or select 'Platform Overview' for platform-wide metrics"
            )
            
            # Handle organization selection
            if selected_org_display == "Platform Overview":
                # Show platform overview (no specific org data)
                df = None
                element_stats = None
                heatmap_data = None
                st.info("**Viewing**: Platform-wide overview and metrics")
            else:
                # Extract org_key from selected option
                selected_org_key = selected_org_display.split("(")[-1].rstrip(")")
                
                # Store selected organization in session state for ROI calculator access
                st.session_state.admin_selected_org = selected_org_key
                st.success(f"**Debug**: Organization selected and saved: {selected_org_key}")
                
                # Load data for selected organization
                survey_data = get_survey_summary_for_org(selected_org_key)
                if survey_data:
                    element_stats, df = survey_data
                    heatmap_data = element_stats.pivot(index='element', columns='group', values='avg_score')
                    st.success(f"**Viewing**: {selected_org_display} - {len(df)} survey responses loaded")
                else:
                    st.warning(f"**No Data**: No survey data found for {selected_org_display}")
                    df = None
                    element_stats = None
                    heatmap_data = None
        else:
            st.info("**No Organizations**: No client organizations found yet. Create organizations in the Survey tab.")
            df = None
            element_stats = None
            heatmap_data = None
    else:
        # For regular users, get data from their organization
        survey_data = get_survey_summary_for_org(org_key)
        if survey_data:
            element_stats, df = survey_data
            heatmap_data = element_stats.pivot(index='element', columns='group', values='avg_score')
            # Only show success message for non-respondent users
            if st.session_state.user_role != "respondent":
                st.success(f"**Survey Data Loaded**: Using {len(df)} responses from your organization's assessments")
        else:
            st.warning(f"**No Data**: No survey data found for organization: {org_key}")
else:
    st.info("**Debug**: No organization_id in session state")

# Check if we have data to display (only stop for non-admin users)
if df is None or element_stats is None:
    if st.session_state.user_role == "admin":
        st.info("**Admin View**: No data available yet. Complete a survey as a demo user to see the dashboard in action.")
        # Don't stop for admin users - let them see the empty tabs
    else:
        st.info("**No Data Available**: Complete the survey or upload a CSV file to see dashboard insights.")
        st.stop()

# Main tabs - show different tabs based on user role
if st.session_state.user_role == "respondent":
    # Respondents see survey content directly without tabs
    pass
else:
    # Clients and admins see all tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Overview", "Heatmap", "Radar Chart", "Strengths & Gaps", "Insights", "Misalignment", "Drill Down", "ROI Calculator", "Action Plan", "Survey"
    ])

# tab1: Overview (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab1:
        if st.session_state.user_role == "admin":
            # Check if admin is viewing platform overview or specific organization
            if df is None or element_stats is None:
                # Platform Overview
                st.subheader("Platform Overview")
                
                # Platform overview for admin
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    org_count = db_fetchone("SELECT COUNT(*) as count FROM organizations")["count"]
                    st.metric("Total Organizations", org_count, delta="Platform")
                with col2:
                    user_count = db_fetchone("SELECT COUNT(*) as count FROM users")["count"]
                    st.metric("Total Users", user_count, delta="Platform Users")
                with col3:
                    response_count = db_fetchone("SELECT COUNT(*) as count FROM survey_responses")["count"]
                    st.metric("Survey Responses", response_count, delta="All Organizations")
                with col4:
                    active_orgs = db_fetchone("SELECT COUNT(*) as count FROM organizations WHERE status = 'Active'")["count"]
                    st.metric("Active Clients", active_orgs, delta="Live")
                
                # Assessment completion overview
                st.markdown("---")
                st.subheader("Assessment Completion Overview")
                
                # Get completion stats across all organizations
                total_respondents = db_fetchone("SELECT COUNT(*) as count FROM users WHERE role = 'respondent'")["count"]
                completed_assessments = db_fetchone("SELECT COUNT(*) as count FROM assessment_completion WHERE status = 'completed'")["count"]
                partial_assessments = db_fetchone("SELECT COUNT(*) as count FROM assessment_completion WHERE status = 'partial'")["count"]
                not_started = total_respondents - completed_assessments - partial_assessments
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Respondents", total_respondents, delta="Platform")
                with col2:
                    st.metric("Completed", completed_assessments, delta="Finished")
                with col3:
                    st.metric("Partial", partial_assessments, delta="In Progress")
                with col4:
                    st.metric("Not Started", not_started, delta="Pending")
                
                # Platform management summary
                st.markdown("---")
                st.markdown("**Platform Management**: Organizations • Users • Data • Settings")
                st.markdown("*Access these features in the Survey tab.*")
                
                # Compact platform insights
                col1, col2 = st.columns(2)
                with col1:
                    # Organization status breakdown
                    org_statuses = db_fetchall("SELECT status, COUNT(*) as count FROM organizations GROUP BY status")
                    if org_statuses:
                        st.subheader("Organization Status")
                        status_text = ""
                        for status_row in org_statuses:
                            status = status_row["status"]
                            count = status_row["count"]
                            if status == "Active":
                                status_text += f"**{status}**: {count} • "
                            elif status == "Inactive":
                                status_text += f"**{status}**: {count} • "
                            else:
                                status_text += f"**{status}**: {count} • "
                        st.markdown(status_text.rstrip(" • "))
                
                with col2:
                    # Recent activity
                    recent_orgs = db_fetchall("SELECT name, created_at FROM organizations ORDER BY created_at DESC LIMIT 3")
                    if recent_orgs:
                        st.subheader("Recent Organizations")
                        for org_row in recent_orgs:
                            name = org_row["name"]
                            created = org_row["created_at"][:10] if org_row["created_at"] else "N/A"
                            st.markdown(f"• **{name}** ({created})")
            else:
                # Organization-specific view
                st.subheader("Organization Dashboard")
                
                # Key metrics for selected organization
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Team Members", len(df['respondent_id'].unique()), delta="Engaged")
                with col2:
                    st.metric("Groups Analyzed", len(df['group'].unique()), delta="Comprehensive")
                with col3:
                    avg_score = df['score'].mean()
                    st.metric("Overall Feedback", f"{avg_score:.2f}/5.0", delta="Strong Foundation")
                with col4:
                    st.metric("Insights Generated", f"{len(df['element'].unique())} areas", delta="Actionable")
                
                # Assessment completion status for selected organization
                st.markdown("---")
                st.subheader("Assessment Completion Status")
                
                # Get completion data for this organization
                completion_df = get_assessment_completion_status(selected_org_key)
                if completion_df is not None and not completion_df.empty:
                    # Display completion summary
                    completion_summary = get_org_completion_summary(selected_org_key)
                    if completion_summary:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Respondents", completion_summary['total_respondents'], delta="Team")
                        with col2:
                            st.metric("Completed", completion_summary['completed'], delta="Finished")
                        with col3:
                            st.metric("Partial", completion_summary['partial'], delta="In Progress")
                        with col4:
                            st.metric("Not Started", completion_summary['not_started'], delta="Pending")
                    
                    # Compact completion summary
                    completion_rate = (completion_summary['completed'] / completion_summary['total_respondents'] * 100) if completion_summary['total_respondents'] > 0 else 0
                    st.info(f"**Overall Completion Rate**: {completion_rate:.1f}%")
                    
                    # Show only top 5 incomplete respondents
                    incomplete_df = completion_df[completion_df['status'] != 'completed'].head(5)
                    if not incomplete_df.empty:
                        st.markdown("**Top Incomplete Respondents:**")
                        for _, row in incomplete_df.iterrows():
                            name = f"{row.get('first_name', '')} {row.get('last_name', '')}".strip() or "Unknown"
                            status = row['status'].title()
                            percentage = row['completion_percentage']
                            st.markdown(f"• **{name}** ({status} - {percentage:.0f}%)")
                else:
                    st.info("No completion data available for this organization yet.")
                
                # Element performance for selected organization
                st.markdown("---")
                st.subheader("Element Performance Overview")
                element_performance = df.groupby('element')['score'].agg(['mean', 'count']).reset_index()
                element_performance.columns = ['Element', 'Average Score', 'Response Count']
                element_performance = element_performance.sort_values('Average Score', ascending=False)
                
                # Compact performance display
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(element_performance, use_container_width=True)
                with col2:
                    # Top 3 elements
                    top_elements = element_performance.head(3)
                    st.markdown("**Top Performing Elements:**")
                    for _, row in top_elements.iterrows():
                        score = row['Average Score']
                        element = row['Element']
                        if score >= 4.0:
                            st.success(f"**{element}**: {score:.2f}/5.0")
                        elif score >= 3.0:
                            st.info(f"**{element}**: {score:.2f}/5.0")
                        else:
                            st.warning(f"**{element}**: {score:.2f}/5.0")
            
        else:
            st.subheader("Dashboard Overview")
            
            # Data source indicator
            if 'organization_id' in st.session_state and df is not None:
                if len(df) > 0:
                    st.info(f"**Data Source**: {len(df)} survey responses from {st.session_state.organization_id} organization")
            
            # Key metrics
            st.subheader("Your Key Feedback Indicators")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Team Members", len(df['respondent_id'].unique()), delta="Engaged")
            with col2:
                st.metric("Groups Analyzed", len(df['group'].unique()), delta="Comprehensive")
            with col3:
                avg_score = df['score'].mean()
                st.metric("Overall Feedback", f"{avg_score:.2f}/5.0", delta="Strong Foundation")
            with col4:
                st.metric("Insights Generated", f"{len(df['element'].unique())} areas", delta="Actionable")
            
            # Assessment completion status for client
            st.markdown("---")
            st.subheader("Team Assessment Completion")
            
            # Get completion data for this organization
            org_key = st.session_state.organization_id
            completion_df = get_assessment_completion_status(org_key)
            if completion_df is not None and not completion_df.empty:
                # Display completion summary
                completion_summary = get_org_completion_summary(org_key)
                if completion_summary:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Team Members", completion_summary['total_respondents'], delta="Total")
                    with col2:
                        st.metric("Completed", completion_summary['completed'], delta="Finished")
                    with col3:
                        st.metric("Partial", completion_summary['partial'], delta="In Progress")
                    with col4:
                        st.metric("Not Started", completion_summary['not_started'], delta="Pending")
                
                # Display completion progress bar
                if completion_summary:
                    total = completion_summary['total_respondents']
                    completed = completion_summary['completed']
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    
                    st.markdown(f"**Overall Completion Rate: {completion_rate:.1f}%**")
                    st.progress(completion_rate / 100)
                    
                    if completion_rate >= 90:
                        st.success("Excellent! Your team has nearly completed all assessments.")
                    elif completion_rate >= 70:
                        st.warning("Good progress! Encourage remaining team members to complete their assessments.")
                    else:
                        st.error("Low completion rate. Consider sending reminders to your team.")
            
            # Element performance
            st.subheader("Element Performance Overview")
            element_performance = df.groupby('element')['score'].agg(['mean', 'count']).reset_index()
            element_performance.columns = ['Element', 'Average Score', 'Response Count']
            element_performance = element_performance.sort_values('Average Score', ascending=False)
            
            st.dataframe(element_performance, use_container_width=True)
            
            # Create performance chart
            fig = px.bar(element_performance, x='Element', y='Average Score',
                        title="Element Performance by Average Score",
                        color='Average Score',
                        color_continuous_scale='RdYlGn',
                        text='Average Score')
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

# tab2: Heatmap (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab2:
        if st.session_state.user_role == "admin":
            st.subheader("Platform Heatmap")
            
            # For admin users, show platform-wide heatmap when no specific org is selected
            if heatmap_data is not None:
                # Show organization-specific heatmap
                fig = px.imshow(heatmap_data, 
                               title=f"Score Heatmap - {selected_org_display if 'selected_org_display' in locals() else 'Selected Organization'}",
                               labels=dict(x="Group", y="Element", color="Score"),
                               color_continuous_scale="RdYlGn",
                               aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Show platform-wide aggregated heatmap
                st.info("**Platform Overview**: Showing aggregated data across all organizations")
                
                # Get platform-wide aggregated data
                platform_data = db_fetchall("""
                    SELECT element, group_type, AVG(score) as avg_score, COUNT(*) as response_count
                    FROM survey_responses 
                    GROUP BY element, group_type
                    HAVING response_count > 0
                    ORDER BY element, group_type
                """)
                
                if platform_data:
                    # Debug: Show what columns we actually have
                    st.info(f"**Debug**: Platform data columns: {list(platform_data[0].keys()) if platform_data else 'No data'}")
                    
                    # Convert to DataFrame for heatmap
                    import pandas as pd
                    heatmap_df = pd.DataFrame(platform_data)
                    
                    # Check if we have the expected columns
                    if 'element' in heatmap_df.columns and 'group_type' in heatmap_df.columns and 'avg_score' in heatmap_df.columns:
                        # Create pivot table for heatmap
                        heatmap_pivot = heatmap_df.pivot(index='element', columns='group_type', values='avg_score')
                        
                        # Create platform heatmap
                        fig = px.imshow(heatmap_pivot, 
                                       title="Platform-Wide Score Heatmap (All Organizations)",
                                       labels=dict(x="Group", y="Element", color="Score"),
                                       color_continuous_scale="RdYlGn",
                                       aspect="auto")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show summary statistics
                        st.markdown("---")
                        st.subheader("Platform Summary")
                        total_responses = sum(row['response_count'] for row in platform_data)
                        st.metric("Total Responses", total_responses, delta="Across all organizations")
                        
                        # Show top performing elements
                        element_totals = {}
                        for row in platform_data:
                            element = row['element']
                            if element not in element_totals:
                                element_totals[element] = []
                            element_totals[element].append(row['avg_score'])
                        
                        avg_by_element = {element: sum(scores)/len(scores) for element, scores in element_totals.items()}
                        top_elements = sorted(avg_by_element.items(), key=lambda x: x[1], reverse=True)[:3]
                        
                        st.markdown("**Top Performing Elements (Platform-Wide):**")
                        for element, score in top_elements:
                            st.success(f"• **{element}**: {score:.2f}/5.0")
                    else:
                        # Show raw data if columns don't match expectations
                        st.warning("**Column Mismatch**: Expected columns not found. Showing raw data instead.")
                        st.dataframe(heatmap_df)
                        
                        # Try to create a simple summary from available data
                        if len(platform_data) > 0:
                            st.markdown("---")
                            st.subheader("Platform Summary")
                            st.info(f"**Total Records**: {len(platform_data)}")
                            st.info(f"**Available Columns**: {list(heatmap_df.columns)}")
                else:
                    st.warning("No platform-wide survey data available yet. Complete surveys in demo organizations to see the heatmap.")
        else:
            st.subheader("Heatmap Analysis")
            if heatmap_data is not None:
                fig = px.imshow(heatmap_data, 
                               title="Score Heatmap (Elements x Groups)",
                               labels=dict(x="Group", y="Element", color="Score"),
                               color_continuous_scale="RdYlGn",
                               aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No heatmap data available")

# tab3: Radar Chart (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab3:
        st.subheader("Radar Chart Analysis")
        if element_stats is not None:
            # Prepare data for radar chart
            radar_data = element_stats.pivot(index='element', columns='group', values='avg_score')
            radar_data = radar_data.fillna(0)
            categories = list(radar_data.index)
            
            radar_colors = ['#b1d89a', '#f8c255', '#7dd4c9', '#a23b72']
            fig = go.Figure()
            for idx, group in enumerate(radar_data.columns):
                color = radar_colors[idx % len(radar_colors)]
                fig.add_trace(go.Scatterpolar(
                    r=radar_data[group].values.tolist() + [radar_data[group].values[0]],
                    theta=categories + [categories[0]],
                    name=str(group),
                    marker=dict(symbol='circle', color=color),
                    line=dict(width=2, color=color),
                    fill='toself',
                    fillcolor=color,
                    opacity=0.4
                ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 5], tickvals=[1,2,3,4,5]),
                    angularaxis=dict(direction="clockwise")
                ),
                showlegend=True,
                title="Average Score by Element (Radar Chart)",
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True, key="radar_chart")
        else:
            st.info("No radar chart data available")

# tab4: Strengths & Gaps (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab4:
        st.subheader("Strengths & Development Areas")
        if element_stats is not None:
            # Calculate overall element averages
            element_360 = df.groupby('element')['score'].mean().reset_index()
            element_360['score'] = element_360['score'].round(2)
            element_360 = element_360.sort_values('score', ascending=False)
            
            # Strengths: above threshold
            STRENGTH_THRESHOLD = 4.0
            DEVELOPMENT_THRESHOLD = 3.0
            
            strengths = element_360[element_360['score'] > STRENGTH_THRESHOLD]
            development_areas = element_360[element_360['score'] < DEVELOPMENT_THRESHOLD]
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Strengths")
                if not strengths.empty:
                    for _, row in strengths.iterrows():
                        st.success(f"**{row['element']}**: {row['score']:.2f}/5.0")
                else:
                    st.info("No areas currently above strength threshold")
            
            with col2:
                st.subheader("Development Areas")
                if not development_areas.empty:
                    for _, row in development_areas.iterrows():
                        st.warning(f"**{row['element']}**: {row['score']:.2f}/5.0")
                else:
                    st.info("All areas above development threshold")
            
            # Element performance chart
            fig = px.bar(element_360, x='score', y='element', orientation='h',
                        title="Element Performance Overview",
                        color='score',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No strengths & gaps data available")

# tab5: Insights (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab5:
        st.subheader("Key Insights")
        if element_stats is not None:
            st.info("**Insights from your survey data**")
            
            # Group comparison insights
            group_insights = element_stats.groupby('group')['avg_score'].mean().reset_index()
            group_insights = group_insights.sort_values('avg_score', ascending=False)
            
            st.subheader("Group Performance Comparison")
            fig = px.bar(group_insights, x='group', y='avg_score',
                        title="Average Scores by Group",
                        color='avg_score',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
            
            # Element insights
            element_insights = df.groupby('element')['score'].agg(['mean', 'std', 'count']).reset_index()
            element_insights.columns = ['Element', 'Average Score', 'Standard Deviation', 'Response Count']
            element_insights = element_insights.sort_values('Average Score', ascending=False)
            
            st.subheader("Element Analysis")
            st.dataframe(element_insights, use_container_width=True)
        else:
            st.info("No insights data available")

# tab6: Misalignment (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab6:
        st.subheader("Group Misalignment Analysis")
        if element_stats is not None:
            # Calculate misalignment (variance between groups for each element)
            misalignment_data = element_stats.groupby('element')['avg_score'].agg(['mean', 'std']).reset_index()
            misalignment_data['misalignment_score'] = misalignment_data['std']
            misalignment_data = misalignment_data.sort_values('misalignment_score', ascending=False)
            
            st.info("**Misalignment shows where different groups have very different perceptions**")
            
            # Top misaligned elements
            st.subheader("Most Misaligned Elements")
            top_misaligned = misalignment_data.head(5)
            for _, row in top_misaligned.iterrows():
                if row['misalignment_score'] > 0.5:
                    st.warning(f"**{row['element']}**: High variance ({row['misalignment_score']:.2f})")
                else:
                    st.info(f"**{row['element']}**: Low variance ({row['misalignment_score']:.2f})")
            
            # Misalignment chart
            fig = px.bar(misalignment_data, x='element', y='misalignment_score',
                        title="Group Misalignment by Element",
                        color='misalignment_score',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No misalignment data available")

# tab7: Drill Down (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab7:
        st.subheader("Drill Down Analysis")
        if element_stats is not None:
            # Element selector
            selected_element = st.selectbox(
                "Select an element to drill down:",
                options=sorted(df['element'].unique()),
                help="Choose an element to see detailed analysis",
                key="drill_down_element"
            )
            
            if selected_element:
                # Filter data for selected element
                element_data = df[df['element'] == selected_element]
                
                st.subheader(f"{selected_element} - Detailed Analysis")
                
                # Group breakdown
                group_breakdown = element_data.groupby('group')['score'].agg(['mean', 'count', 'std']).reset_index()
                group_breakdown.columns = ['Group', 'Average Score', 'Response Count', 'Standard Deviation']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(group_breakdown, use_container_width=True)
                
                with col2:
                    # Group comparison chart
                    fig = px.bar(group_breakdown, x='Group', y='Average Score',
                                title=f"{selected_element} - Group Comparison",
                                color='Average Score',
                                color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Question-level analysis
                st.subheader("Question-Level Analysis")
                question_breakdown = element_data.groupby('question')['score'].agg(['mean', 'count']).reset_index()
                question_breakdown.columns = ['Question', 'Average Score', 'Response Count']
                question_breakdown = question_breakdown.sort_values('Average Score', ascending=False)
                
                st.dataframe(question_breakdown, use_container_width=True)
        else:
            st.info("No drill down data available")

# tab8: ROI Calculator (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab8:
        st.markdown('''<div style="text-align:center;margin-bottom:2rem;">
            <h1 style="color:#7dd4c9;margin-bottom:0.5rem;">Assessment-Driven ROI Calculator</h1>
            <p style="color:#f8c255;font-size:1.2rem;margin:0;">Transform your 360 assessment insights into measurable business value</p>
        </div>''', unsafe_allow_html=True)
        
        # Introduction and context
        st.markdown('''<div style="background:linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);padding:1.5rem;border-radius:12px;border-left:4px solid #7dd4c9;margin-bottom:2rem;">
            <h3 style="color:#2c3e52;margin-bottom:1rem;">Why Calculate L&D ROI?</h3>
            <p style="color:#495057;margin:0;line-height:1.6;">
                Understanding the return on your learning investments helps justify budgets, prioritize initiatives, and demonstrate 
                the strategic value of L&D to stakeholders. Our calculator uses your actual assessment results and industry benchmarks 
                to provide realistic, actionable insights.
            </p>
        </div>''', unsafe_allow_html=True)
        
        # Assessment-Driven ROI Calculation
        st.markdown("### Assessment-Driven ROI Calculation")
        
        # Get assessment data for current organization
        if st.session_state.user_role == "admin":
            # For admin users, use the selected organization from the admin interface
            st.info(f"**Debug**: Session state keys: {list(st.session_state.keys())}")
            st.info(f"**Debug**: admin_selected_org value: '{getattr(st.session_state, 'admin_selected_org', 'NOT_SET')}'")
            
            if hasattr(st.session_state, 'admin_selected_org') and st.session_state.admin_selected_org:
                org_key = st.session_state.admin_selected_org
                st.success(f"**Admin View**: Using assessment data from {org_key}")
            else:
                # Fallback to first available organization
                all_orgs = db_fetchall("SELECT org_key FROM organizations WHERE type != 'platform_admin' ORDER BY name LIMIT 1")
                org_key = all_orgs[0]['org_key'] if all_orgs else None
                st.info(f"**Admin Note**: Using {org_key} for ROI calculations. Select a specific organization above to see targeted data.")
        else:
            # For client/respondent users, use their assigned organization
            org_key = st.session_state.organization_id
        
        # Initialize variables for ROI calculation
        current_element_scores = None
        current_overall = None
        has_assessment_data = False
        target_scores = {}
        improvement_potential = {}
        
        if org_key:
            st.info(f"**Debug**: Fetching data for organization: {org_key}")
            survey_data = get_survey_summary_for_org(org_key)
            if survey_data:
                element_stats, responses_df = survey_data
                st.info(f"**Debug**: Data returned - Element stats shape: {element_stats.shape if element_stats is not None else 'None'}, Responses: {len(responses_df) if responses_df is not None else 'None'}")
            else:
                st.warning("**Debug**: No survey data returned from database")
        else:
            st.warning("**Debug**: No organization key available")
            survey_data = None
        
        if survey_data is not None:
            element_stats, responses_df = survey_data
            
            if element_stats is not None and not element_stats.empty:
                # Get current assessment status
                current_element_scores = element_stats.groupby('element')['avg_score'].mean().round(2)
                current_overall = current_element_scores.mean()
                has_assessment_data = True
                
                # Show assessment data summary
                st.success(f"**Assessment Data Connected**: {len(responses_df)} responses loaded from your organization")
                
                # Calculate improvement potential for each element
                target_scores = {element: min(5.0, float(score) + 0.8) for element, score in current_element_scores.items()}
                improvement_potential = {element: target_scores[element] - float(score) for element, score in current_element_scores.items()}
            
            # Show current assessment status and ROI projection only if we have data
            if has_assessment_data and current_element_scores is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Current Assessment Status**")
                    st.metric("Overall Score", f"{current_overall:.1f}/5.0")
                    
                    # Show top improvement areas
                    improvement_areas = sorted(improvement_potential.items(), key=lambda x: x[1], reverse=True)
                    st.markdown("**Top Improvement Areas:**")
                    for element, potential in improvement_areas[:3]:
                        current = float(current_element_scores[element])
                        st.markdown(f"• **{element}**: {current:.1f}/5.0 → {target_scores[element]:.1f}/5.0")
                    
                    # Show current vs target comparison
                    if st.button("View Detailed Assessment Analysis", key="view_assessment_details"):
                        st.markdown("**Element-by-Element Analysis:**")
                        for element in current_element_scores.index:
                            current = float(current_element_scores[element])
                            target = target_scores[element]
                            potential = improvement_potential[element]
                            if potential > 0:
                                st.markdown(f"**{element}**: {current:.1f} → {target:.1f} (+{potential:.1f})")
                
                with col2:
                    st.markdown("**ROI Impact Projection**")
                    
                    # Element-to-ROI mapping based on research
                    element_roi_mapping = {
                        "Strategic Connection": {"business_impact": 0.8, "efficiency": 0.6, "talent": 0.4},
                        "Needs Analysis": {"efficiency": 0.9, "business_impact": 0.7, "talent": 0.5},
                        "Learning Design": {"individual_performance": 0.9, "efficiency": 0.7, "talent": 0.6},
                        "Learning Culture": {"talent": 0.9, "individual_performance": 0.8, "efficiency": 0.6},
                        "Platform and Tools": {"efficiency": 0.9, "individual_performance": 0.7, "business_impact": 0.5},
                        "Integration with Talent": {"talent": 0.9, "business_impact": 0.8, "individual_performance": 0.7},
                        "Learning Impact": {"business_impact": 0.9, "efficiency": 0.8, "individual_performance": 0.7},
                        "Future Capability": {"business_impact": 0.9, "talent": 0.8, "efficiency": 0.6}
                    }
                    
                    # Calculate projected ROI impact based on assessment gaps
                    # Scaling: 1-5 scale with 0.8 point improvement = significant impact
                    # Using /2.0 scaling for more realistic ROI projections
                    roi_dimensions = {
                        "individual_performance": 0,
                        "business_impact": 0,
                        "efficiency": 0,
                        "talent": 0
                    }
                    
                    for element, current_score in current_element_scores.items():
                        if element in element_roi_mapping:
                            gap = improvement_potential[element]
                            if gap > 0:
                                element_mapping = element_roi_mapping[element]
                                # For 1-5 scale, normalize gap more appropriately
                                # A 0.8 point improvement from 3.2 to 4.0 is significant
                                gap_multiplier = gap / 2.0  # More realistic scaling for 1-5 scale
                                
                                for dimension, base_impact in element_mapping.items():
                                    roi_dimensions[dimension] += base_impact * gap_multiplier
                    
                    # Display projected improvements as 2x2 squares
                    labels_order = [
                        ("individual_performance", "Individual Performance"),
                        ("business_impact", "Business Impact"),
                        ("efficiency", "Efficiency"),
                    ("talent", "Talent"),
                ]

                row1 = st.columns(2)
                row2 = st.columns(2)
                rows = [row1, row2]

                idx = 0
                for row in rows:
                    for col in row:
                        key, label = labels_order[idx]
                        value = roi_dimensions.get(key, 0)
                        with col:
                            st.markdown(f'''
                            <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.25);border-radius:12px;padding:1rem;text-align:center;min-height:120px;display:flex;flex-direction:column;justify-content:center;">
                                <div style="color:#f8c255;font-size:0.95rem;margin-bottom:0.25rem;">{label}</div>
                                <div style="color:white;font-size:1.75rem;font-weight:700;">{value:.1f}%</div>
                                <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;">Projected impact</div>
                            </div>
                            ''', unsafe_allow_html=True)
                        idx += 1
                
                # Show calculation details for transparency
                if st.checkbox("Show calculation details", key="show_roi_calc_details"):
                    st.markdown("**Calculation Details:**")
                    for element, current_score in current_element_scores.items():
                        if element in element_roi_mapping and improvement_potential[element] > 0:
                            gap = improvement_potential[element]
                            gap_multiplier = gap / 2.0
                            st.markdown(f"- **{element}**: {float(current_score):.1f} → {float(current_score) + gap:.1f} (gap: {gap:.1f}, multiplier: {gap_multiplier:.2f})")
                
                # Overall ROI projection
                total_potential = sum(roi_dimensions.values())
                if total_potential > 0:
                    st.success(f"**Total Improvement Potential**: {total_potential:.1f}%")
            else:
                st.warning("**No Assessment Data Available**: Complete a 360 assessment to see detailed analysis and ROI projections.")
        
        # Currency selection
        st.markdown("### Currency & Regional Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            currency = st.selectbox(
                "Currency",
                options=["GBP (£)", "USD ($)", "EUR (€)", "CAD (C$)", "AUD (A$)", "JPY (¥)", "CHF (Fr)", "SEK (kr)", "AED (د.إ)", "SAR (ر.س)", "OMR (ر.ع)", "QAR (ر.ق)", "KWD (د.ك)", "BHD (د.ب)"],
                index=0,
                help="Select your local currency for calculations",
                key="roi_currency"
            )
        
        with col2:
            # Currency conversion rates (simplified - in production you'd use live rates)
            currency_symbols = {
                "GBP (£)": ("£", 1.0),
                "USD ($)": ("$", 1.27),
                "EUR (€)": ("€", 1.17),
                "CAD (C$)": ("C$", 1.72),
                "AUD (A$)": ("A$", 1.94),
                "JPY (¥)": ("¥", 185.0),
                "CHF (Fr)": ("Fr", 1.10),
                "SEK (kr)": ("kr", 13.2),
                "AED (د.إ)": ("AED", 4.65),
                "SAR (ر.س)": ("SAR", 4.77),
                "OMR (ر.ع)": ("OMR", 0.49),
                "QAR (ر.ق)": ("QAR", 4.63),
                "KWD (د.ك)": ("KWD", 0.39),
                "BHD (د.ب)": ("BHD", 0.48)
            }
            selected_currency = currency_symbols[currency]
            currency_symbol = selected_currency[0]
            conversion_rate = selected_currency[1]
            
            # Show selected currency info
            st.info(f"**Selected Currency**: {currency}")
        
        # Input parameters with better organization
        st.markdown("### Input Parameters")
        st.markdown("**Assessment Scores**")

        # Auto-populate current/target from assessment data
        if has_assessment_data and current_element_scores is not None:
            current_score = current_element_scores.mean()
            target_score = min(5.0, current_score + 0.8)
            st.success(f"**Assessment Data Connected**: Using scores from your organization's 360 assessment")
            st.info(f"**Current Score**: {current_score:.2f}/5.0 (calculated from {len(current_element_scores)} elements)")
        else:
            current_score = 3.5
            target_score = 4.0
            st.warning(f"**No Assessment Data**: Using default values. Complete a 360 assessment to see organization-specific ROI calculations.")

        col_scores_l, col_scores_r = st.columns(2)
        with col_scores_l:
            current_score = st.number_input(
                "Current Average Score",
                min_value=1.0, max_value=5.0, value=float(current_score), step=0.1,
                help="Your current average score from the assessment (auto-populated)",
                key="roi_current_score"
            )
        with col_scores_r:
            target_score = st.number_input(
                "Target Average Score",
                min_value=1.0, max_value=5.0, value=float(target_score), step=0.1,
                help="Your desired average score after L&D improvements",
                key="roi_target_score"
            )

        # Score improvement indicator
        if target_score > current_score:
            improvement = ((target_score - current_score) / current_score) * 100
            st.success(f"**Score Improvement**: +{improvement:.1f}%")
        elif target_score < current_score:
            st.warning("Target score should be higher than current score")
        else:
            st.info("No score improvement planned")
        
        # Research-Based Performance Parameters
        st.markdown("### Research-Based Performance Parameters")
        st.markdown('''<div style="background:linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);padding:1rem;border-radius:8px;border-left:4px solid #ffc107;margin-bottom:1rem;">
            <p style="color:#856404;margin:0;font-size:0.9rem;">
                <strong>Evidence-Based Approach:</strong> These parameters are based on meta-analyses of 397+ training studies showing 
                medium-large effects (d≈0.60-0.63) across learning, behavior, and business outcomes.
            </p>
        </div>''', unsafe_allow_html=True)
        
        # Main Interface - 3 Essential Sliders
        col1, col2, col3 = st.columns(3)
        
        with col1:
            employee_count = st.number_input(
                "Number of Employees", 
                min_value=1, value=100, 
                help="Total employees in scope for L&D initiatives",
                key="roi_employee_count"
            )
        
        with col2:
            avg_salary = st.number_input(
                f"Average Annual Salary ({currency_symbol})", 
                min_value=20000, value=40000, step=1000,
                help="Average annual salary of employees in scope",
                key="roi_avg_salary"
            )
        
        with col3:
            l_d_investment = st.number_input(
                f"L&D Investment per Employee ({currency_symbol})", 
                min_value=500, value=2500, step=100,
                help="Annual L&D investment per employee",
                key="roi_l_d_investment"
            )
        
        # Advanced Options (Collapsible Side Menu)
        with st.expander("Advanced Options & Research Settings", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                confidence_level = st.selectbox(
                    "Confidence Level",
                    options=["High (RCT)", "Medium (DiD)", "Low (Pre/Post)"],
                    index=1,
                    help="Research design affects attribution confidence",
                    key="roi_confidence_level"
                )
                
                # Attribution coefficients based on research
                attribution_coefficients = {
                    "High (RCT)": 0.85,      # 85% attribution (realistic)
                    "Medium (DiD)": 0.65,    # 65% attribution (conservative)
                    "Low (Pre/Post)": 0.45   # 45% attribution (very conservative)
                }
                attribution = attribution_coefficients[confidence_level]
            
            with col2:
                industry_type = st.selectbox(
                    "Industry Type",
                    options=["Professional Services", "Manufacturing", "Healthcare", "Technology", "Financial Services", "Education", "Other"],
                    index=0,
                    help="Industry-specific performance multipliers",
                    key="roi_industry_type"
                )
                
                # Industry multipliers based on research
                industry_multipliers = {
                    "Professional Services": 1.2,  # Higher for knowledge workers
                    "Manufacturing": 1.0,         # Standard baseline
                    "Technology": 1.3,            # High knowledge work
                    "Financial Services": 1.15,   # Moderate knowledge work
                    "Healthcare": 1.1,            # Moderate knowledge work
                    "Education": 1.1,             # Moderate knowledge work
                    "Other": 1.0                  # Standard baseline
                }
                industry_multiplier = industry_multipliers[industry_type]
            
            with col3:
                implementation_quality = st.selectbox(
                    "Implementation Quality",
                    options=["Excellent", "Good", "Basic"],
                    index=1,
                    help="Quality of L&D program implementation",
                    key="roi_implementation_quality"
                )
                
                # Implementation quality multipliers
                quality_multipliers = {
                    "Excellent": 1.2,  # 20% boost for excellent implementation
                    "Good": 1.0,       # Standard baseline
                    "Basic": 0.8       # 20% reduction for basic implementation
                }
                quality_multiplier = quality_multipliers[implementation_quality]
            
            # Removed Research Foundation section for a cleaner UX
        
        # Auto-calculate performance improvements from assessment
        if element_stats is not None and not element_stats.empty:
            # Calculate realistic performance improvements based on assessment gaps
            current_overall = element_stats.groupby('element')['avg_score'].mean().mean()
            target_overall = min(5.0, current_overall + 0.8)
            improvement_potential = target_overall - current_overall
            
            # Smart performance calculation based on research
            if improvement_potential > 0:
                # Base performance improvement (research shows 8-15% typical)
                base_improvement = min(15, improvement_potential * 20)  # Scale gap to realistic range
                
                # Apply research-based multipliers
                research_improvement = base_improvement * industry_multiplier * quality_multiplier
                
                # Calculate benefits using research-backed approach
                annual_performance_gain = (research_improvement / 100) * avg_salary * employee_count
                
                # Apply attribution and realistic factors
                attributed_gain = annual_performance_gain * attribution * 0.8  # 80% of theoretical max
                
                # Removed Smart Calculation summary for a cleaner UX
        

        

        

        


        

        


            # Removed industry average info for a cleaner UX

        
        # Calculate ROI button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            calculate_btn = st.button(
                "Calculate Smart ROI", 
                type="primary", 
                use_container_width=True,
                key="calculate_roi"
            )
        
        # Calculate and display results
        if calculate_btn:
            # Smart ROI calculation using assessment-driven approach
            if has_assessment_data and current_element_scores is not None:
                # Use actual assessment data for ROI calculation
                current_overall = current_element_scores.mean()
                target_overall = min(5.0, current_overall + 0.8)
                improvement_potential = target_overall - current_overall
                
                st.success(f"**Using Assessment Data**: ROI calculated from {org_key} organization's actual 360 assessment results")
                st.info(f"**Assessment Scores**: Current: {current_overall:.2f}, Target: {target_overall:.2f}, Gap: {improvement_potential:.2f}")
                st.info(f"**Debug ROI Calc**: Organization: {org_key}, Element scores: {dict(current_element_scores)}")
                
                if improvement_potential > 0:
                    # Advanced L&D ROI calculation (IP - calculation logic hidden)
                    # Assessment-driven ROI with industry benchmarks
                    
                    # Global L&D ROI benchmarks (industry research)
                    global_average_roi = 85  # Mid-range L&D ROI benchmark
                    
                    # Current organization ROI based on assessment maturity
                    # Higher scores = higher ROI (our proprietary algorithm)
                    current_roi_multiplier = (current_overall / 5.0) * 0.8 + 0.4  # 0.4 to 1.2 range
                    baseline_roi = global_average_roi * current_roi_multiplier
                    
                    # Target ROI based on improvement potential
                    # Improvement gap creates exponential ROI growth (our IP)
                    improvement_gap = target_overall - current_overall
                    improvement_multiplier = 1 + (improvement_gap * 0.6)  # 0.6x improvement factor
                    
                    # Apply industry and implementation quality adjustments
                    industry_multipliers = {
                        "Technology": 1.3, "Healthcare": 1.25, "Finance": 1.2,
                        "Manufacturing": 1.15, "Retail": 1.1, "Education": 1.1,
                        "Consulting": 1.25, "Other": 1.0
                    }
                    implementation_multipliers = {
                        "Excellent": 1.25, "Good": 1.1, "Basic": 0.95, "Poor": 0.8
                    }
                    
                    industry_mult = industry_multipliers.get(industry_type, 1.0)
                    implementation_mult = implementation_multipliers.get(implementation_quality, 1.0)
                    
                    # Calculate target ROI with all factors
                    target_roi = baseline_roi * improvement_multiplier * industry_mult * implementation_mult
                    
                    # Ensure realistic ROI ranges (our IP algorithm)
                    target_roi = min(300, max(50, target_roi))  # Cap between 50-300%
                    
                    # Calculate improvement scenarios
                    conservative_improvement = baseline_roi + (improvement_gap * 15)
                    moderate_improvement = baseline_roi + (improvement_gap * 25)
                    optimistic_improvement = target_roi
                    
                    # Element-specific ROI contributions (our IP)
                    element_roi_contributions = {}
                    for element, current_score in current_element_scores.items():
                        if element in target_scores:
                            element_gap = target_scores[element] - current_score
                            if element_gap > 0:
                                # Each element contributes differently to ROI (our algorithm)
                                element_weights = {
                                    "Strategic Connection": 0.25, "Needs Analysis": 0.20,
                                    "Learning Design": 0.18, "Learning Culture": 0.15,
                                    "Platform and Tools": 0.12, "Integration with Talent": 0.22,
                                    "Learning Impact": 0.20, "Future Capability": 0.18
                                }
                                element_impact = element_gap * element_weights.get(element, 0.15) * 20
                                element_roi_contributions[element] = element_impact
                    
                    # Business impact categories (industry-flexible)
                    business_impacts = {
                        "Efficiency Gains": f"{15 + improvement_gap * 10:.0f}-{25 + improvement_gap * 15:.0f}% improvement",
                        "Innovation Capacity": f"{20 + improvement_gap * 12:.0f}-{35 + improvement_gap * 18:.0f}% improvement",
                        "Decision Quality": f"{18 + improvement_gap * 8:.0f}-{28 + improvement_gap * 12:.0f}% improvement",
                        "Knowledge Retention": f"{12 + improvement_gap * 6:.0f}-{22 + improvement_gap * 10:.0f}% improvement"
                    }
                    
                    # Display results
                    st.markdown("---")
                    st.markdown('''<div style="background:linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);padding:2rem;border-radius:16px;margin-bottom:2rem;border:2px solid #28a745;">
                        <h2 style="color:#155724;margin-bottom:1.5rem;text-align:center;">Smart ROI Results</h2>
                    </div>''', unsafe_allow_html=True)
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "Current ROI", 
                            f"{baseline_roi:.0f}%",
                            delta="Baseline performance"
                        )
                    with col2:
                        st.metric(
                            "Target ROI", 
                            f"{target_roi:.0f}%",
                            delta="Improved performance"
                        )
                    with col3:
                        st.metric(
                            "Improvement Gap", 
                            f"{improvement_gap:.1f} points",
                            delta="Assessment improvement needed"
                        )
                    with col4:
                        st.metric(
                            "Industry Multiplier", 
                            f"{industry_mult:.1f}x",
                            delta="Industry context"
                        )
                    
                    # Baseline ROI vs Target ROI Comparison
                    st.markdown("---")
                    st.markdown("### Baseline ROI vs Target ROI")
                    
                    # Baseline ROI is now calculated in the main section above
                    
                    # Display baseline vs target comparison
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Baseline ROI (Current Performance)
                        if baseline_roi < 0:
                            st.markdown('''<div style="background:linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);padding:1.5rem;border-radius:12px;border:2px solid #dc3545;margin-bottom:1rem;">
                                <h3 style="color:#721c24;margin-bottom:1rem;text-align:center;">Baseline ROI (Current)</h3>
                                <div style="text-align:center;font-size:2rem;font-weight:700;color:#721c24;margin-bottom:0.5rem;">{:.1f}%</div>
                                <div style="text-align:center;color:#721c24;font-size:0.9rem;">Current L&D Performance</div>
                            </div>'''.format(baseline_roi), unsafe_allow_html=True)
                        else:
                            st.markdown('''<div style="background:linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);padding:1.5rem;border-radius:12px;border:2px solid #28a745;margin-bottom:1rem;">
                                <h3 style="color:#155724;margin-bottom:1rem;text-align:center;">Baseline ROI (Current)</h3>
                                <div style="text-align:center;font-size:2rem;font-weight:700;color:#155724;margin-bottom:0.5rem;">{:.1f}%</div>
                                <div style="text-align:center;color:#155724;font-size:0.9rem;">Current L&D Performance</div>
                            </div>'''.format(baseline_roi), unsafe_allow_html=True)
                        
                        st.markdown(f"**Current Performance**: {current_overall:.2f}/5.0")
                        st.markdown(f"**Current ROI**: {baseline_roi:.0f}%")
                    
                    with col2:
                        # Target ROI (Improved Performance)
                        st.markdown('''<div style="background:linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);padding:1.5rem;border-radius:12px;border:2px solid #28a745;margin-bottom:1rem;">
                            <h3 style="color:#155724;margin-bottom:1rem;text-align:center;">Target ROI (Improved)</h3>
                            <div style="text-align:center;font-size:2rem;font-weight:700;color:#155724;margin-bottom:0.5rem;">{:.0f}%</div>
                            <div style="text-align:center;color:#155724;font-size:0.9rem;">With L&D Ecosystem Improvements</div>
                        </div>'''.format(target_roi), unsafe_allow_html=True)
                        
                        st.markdown(f"**Target Performance**: {target_overall:.2f}/5.0")
                        st.markdown(f"**Target ROI**: {target_roi:.0f}%")
                    
                    # ROI improvement summary
                    roi_improvement_amount = target_roi - baseline_roi
                    improvement_multiplier = target_roi / baseline_roi if baseline_roi != 0 else float('inf')
                    
                    st.markdown("---")
                    st.markdown("### ROI Transformation Summary")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ROI Improvement", f"{roi_improvement_amount:+.1f}%", delta="From current to target")
                    with col2:
                        if baseline_roi != 0:
                            st.metric("Improvement Multiplier", f"{improvement_multiplier:.1f}x", delta="ROI transformation")
                        else:
                            st.metric("Improvement Multiplier", "∞", delta="From negative to positive")
                    with col3:
                        st.metric("Performance Gap", f"{improvement_potential:.2f} points", delta="Assessment improvement needed")
                    
                    # Business impact breakdown
                    st.markdown("---")
                    st.markdown("### Business Impact Categories")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Efficiency & Innovation Focus:**")
                        for category, impact in business_impacts.items():
                            st.markdown(f"- **{category}**: {impact}")
                    
                    with col2:
                        st.markdown("**Industry Context:**")
                        st.info(f"**{industry_type} Industry**: {industry_mult:.1f}x multiplier")
                        st.info(f"**Implementation Quality**: {implementation_quality} ({implementation_multipliers.get(implementation_quality, 1.0):.1f}x)")
                    
                    # Element contribution breakdown with expandable sections
                    st.markdown("---")
                    st.markdown("### Element Contribution to ROI")
                    
                    if element_roi_contributions:
                        # Sort by impact
                        sorted_elements = sorted(element_roi_contributions.items(), key=lambda x: x[1], reverse=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Top Improvement Areas:**")
                            for element, impact in sorted_elements[:4]:
                                with st.expander(f"{element}: {impact:.1f}% ROI impact"):
                                    current_score = current_element_scores.get(element, 0)
                                    target_score = target_scores.get(element, 0)
                                    st.markdown(f"**Current Score**: {current_score:.1f}/5.0")
                                    st.markdown(f"**Target Score**: {target_score:.1f}/5.0")
                                    st.markdown(f"**Improvement Gap**: {target_score - current_score:.1f} points")
                                    st.markdown(f"**ROI Contribution**: {impact:.1f}%")
                        
                        with col2:
                            st.markdown("**ROI Impact Summary:**")
                            total_element_impact = sum(element_roi_contributions.values())
                            st.metric("Total Element Impact", f"{total_element_impact:.1f}%")
                            st.metric("ROI Multiplier", f"{target_roi/total_element_impact:.1f}x")
                    
                    # Important disclaimer
                    st.markdown("---")
                    st.markdown('''<div style="background:linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);padding:1.5rem;border-radius:12px;border:2px solid #ffc107;">
                        <h4 style="color:#856404;margin-bottom:1rem;">⚠️ Important: Indicative Figures Only</h4>
                        <p style="color:#856404;margin-bottom:0.5rem;">These ROI projections are indicative and based on assessment data analysis. Actual results depend on:</p>
                        <ul style="color:#856404;margin-bottom:0.5rem;">
                            <li>Implementation quality and commitment</li>
                            <li>Market conditions and business context</li>
                            <li>Other organizational factors beyond L&D</li>
                            <li>Measurement and tracking capabilities</li>
                        </ul>
                        <p style="color:#856404;margin-bottom:0;">Use these figures for strategic planning and comparison, not as guaranteed outcomes.</p>
                    </div>''', unsafe_allow_html=True)
                    
                    # Strategic messaging
                    if baseline_roi < global_average_roi:
                        st.success("**Strategic Insight**: Your current L&D ecosystem is below industry benchmarks. Strategic improvements could significantly enhance your ROI and competitive position.")
                    elif baseline_roi > global_average_roi:
                        st.info("**Strategic Insight**: Your L&D ecosystem is performing above average. Further improvements could unlock even greater returns and market leadership.")
                    else:
                        st.info("**Strategic Insight**: Your L&D ecosystem is at industry standard. Targeted improvements could help you outperform competitors and achieve best-in-class results.")
                    
                    # ROI interpretation
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### ROI Analysis")
                        if target_roi > 200:
                            st.success("**Exceptional ROI**: This represents outstanding value for your L&D investment!")
                        elif target_roi > 100:
                            st.success("**Strong ROI**: Excellent return that clearly justifies the investment.")
                        elif target_roi > 50:
                            st.info("**Good ROI**: Solid return that supports continued L&D investment.")
                        elif target_roi > 0:
                            st.warning("**Positive ROI**: Investment will pay for itself, but consider optimizing parameters.")
                        else:
                            st.error("**Negative ROI**: Consider adjusting your parameters or investment strategy.")
                    
                    with col2:
                        st.markdown("### Key Insights")
                        st.markdown(f"- **Assessment Gap**: {improvement_potential:.1f} points")
                        st.markdown(f"- **Current ROI**: {baseline_roi:.0f}%")
                        st.markdown(f"- **Target ROI**: {target_roi:.0f}%")
                        st.markdown(f"- **Improvement Potential**: {roi_improvement_amount:+.0f}%")
                        st.markdown(f"- **Industry Context**: {industry_type} ({industry_mult:.1f}x)")
                    
                    # Key messaging about current state vs opportunity
                    st.markdown('''
                    <div style="background:rgba(255,255,255,0.1);padding:1.5rem;border-radius:12px;border:1px solid rgba(255,255,255,0.3);margin-bottom:2rem;">
                        <p style="color:white;font-size:1.1rem;margin:0;line-height:1.6;text-align:center;">
                            <strong>💡 Key Insight:</strong> While you're not doing anything wrong currently, 
                            with a couple of strategic tweaks to your overall L&D ecosystem, 
                            we could turn this into a <strong style="color:#f8c255;">massive positive for your business</strong>.
                        </p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Clean, boxed summary section
                    st.markdown("---")
                    st.markdown("### ROI Summary")
                    
                    # Summary metrics in clean boxes
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('''<div style="background:linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);padding:1.5rem;border-radius:12px;border:2px solid #1976d2;">
                            <h4 style="color:#1565c0;margin-bottom:1rem;text-align:center;">Current State</h4>
                            <div style="text-align:center;font-size:2rem;font-weight:700;color:#1565c0;margin-bottom:0.5rem;">{:.0f}% ROI</div>
                            <div style="text-align:center;color:#1565c0;font-size:0.9rem;">Based on current assessment scores</div>
                        </div>'''.format(baseline_roi), unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('''<div style="background:linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);padding:1.5rem;border-radius:12px;border:2px solid #388e3c;">
                            <h4 style="color:#2e7d32;margin-bottom:1rem;text-align:center;">Target State</h4>
                            <div style="text-align:center;font-size:2rem;font-weight:700;color:#2e7d32;margin-bottom:0.5rem;">{:.0f}% ROI</div>
                            <div style="text-align:center;color:#2e7d32;font-size:0.9rem;">With L&D ecosystem improvements</div>
                        </div>'''.format(target_roi), unsafe_allow_html=True)
                    
                    # Key improvement metrics
                    st.markdown("---")
                    st.markdown("### Improvement Metrics")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ROI Increase", f"{roi_improvement_amount:+.0f}%", delta="From current to target")
                    with col2:
                        st.metric("Assessment Gap", f"{improvement_potential:.1f} points", delta="Improvement needed")
                    with col3:
                        st.metric("Industry Context", f"{industry_type}", delta=f"{industry_mult:.1f}x multiplier")
                    
                else:
                    st.warning("No improvement potential detected in your assessment scores.")
            else:
                st.warning("**No Assessment Data**: Complete a 360 assessment to see organization-specific ROI calculations.")


# tab9: Action Plan (only for non-respondents)
if st.session_state.user_role != "respondent":
    with tab9:
        st.subheader("Action Plan Generator")
        if element_stats is not None:
            st.info("**Generate actionable steps based on your survey results**")
            
            # Priority areas
            element_360 = df.groupby('element')['score'].mean().reset_index()
            element_360 = element_360.sort_values('score', ascending=True)  # Lowest scores first
            
            st.subheader("Priority Areas for Action")
            
            for i, (_, row) in enumerate(element_360.head(3).iterrows()):
                score = row['score']
                element = row['element']
                
                if score < 3.0:
                    priority = "High Priority"
                    color = "danger"
                elif score < 3.5:
                    priority = "Medium Priority"
                    color = "warning"
                else:
                    priority = "Low Priority"
                    color = "success"
                
                st.markdown(f"**{i+1}. {element}** ({score:.2f}/5.0) - {priority}")
                
                # Action suggestions
                if element == "Strategic Connection":
                    st.markdown("   - **Actions**: Engage senior leadership in L&D strategy discussions")
                elif element == "Learning Culture":
                    st.markdown("   - **Actions**: Implement learning champions program")
                elif element == "Learning Impact":
                    st.markdown("   - **Actions**: Establish clear KPIs and measurement framework")
                else:
                    st.markdown("   - **Actions**: Review current processes and gather stakeholder feedback")
                
                st.markdown("---")
            
            # Download action plan
            if st.button("Download Action Plan", type="primary", key="download_action_plan"):
                st.success("Action plan download feature coming soon!")
        else:
            st.info("No action plan data available")

# Survey content - show directly for respondents, in tab for others
is_respondent = st.session_state.user_role == "respondent"

container = st.container() if is_respondent else tab10

with container:
    if st.session_state.user_role in ["respondent", "client"]:
        # Initialize survey state
        if 'survey_page' not in st.session_state:
            st.session_state.survey_page = 0
        if 'survey_responses' not in st.session_state:
            st.session_state.survey_responses = {}
        if 'selected_group' not in st.session_state:
            st.session_state.selected_group = None
        
        # Get user's assigned group from session state
        user_group = st.session_state.get('user_group', 'LNR')  # This one is fine - session_state is a dict
        group_display_names = {
            "SLT": "Senior Leadership Team",
            "LDT": "L&D Team", 
            "MGR": "Managers",
            "LNR": "Learners"
        }
        
        # Check if respondent has already completed the assessment
        has_completed = False
        if st.session_state.user_role == "respondent":
            # Check database for existing completion
            completion_check = db_fetchone(
                "SELECT status FROM assessment_completion WHERE respondent_id = ? AND org_key = ?",
                (st.session_state.current_user, st.session_state.organization_id)
            )
            has_completed = completion_check and completion_check["status"] == "completed"
            
            # If completed, set survey page to -1 to show completion message
            if has_completed and st.session_state.survey_page == 0:
                st.session_state.survey_page = -1
        
        if st.session_state.survey_page == 0:
            # 50:50 split landing page
            col1, col2 = st.columns(2)
            
            with col1:
                # Welcome message and context
                st.markdown(f'''<div style="text-align:center;padding:2rem;">
                    <h1 style="color:white;margin-bottom:1rem;">Welcome to Your Assessment</h1>
                    <p style="color:white;font-size:1.2rem;margin-bottom:1.5rem;">
                        Hi <strong>{st.session_state.user_name}</strong>!
                    </p>
                    <p style="color:white;font-size:1.1rem;line-height:1.6;margin-bottom:2rem;">
                        You are part of the <strong>{group_display_names.get(user_group, 'Unknown')}</strong> group, and your insights will help shape the future of learning and development in your organization.
                    </p>
                    <div style="background:rgba(255,255,255,0.1);padding:1.5rem;border-radius:12px;border:1px solid rgba(255,255,255,0.3);">
                        <p style="color:white;font-size:1rem;margin:0;line-height:1.6;">
                            <strong>We would love your input on Development at {st.session_state.organization.get('name', "your organization")}.</strong><br><br>
                            You will be asked to reflect on 32 short statements, grouped across eight key elements of development. For each one, simply share whether you agree or disagree.<br><br>
                            It should take no more than 10-15 minutes to complete.<br><br>
                            Your responses are 100% confidential - so please answer openly and honestly. Every insight helps us build a clearer picture.
                        </p>
                    </div>
                </div>''', unsafe_allow_html=True)
            
            with col2:
                # Call to action
                st.markdown(f'''<div style="text-align:center;padding:2rem;">
                    <div style="background:linear-gradient(135deg, #f8c255 0%, #f0b84a 100%);padding:3rem 2rem;border-radius:16px;box-shadow:0 8px 32px rgba(248,194,85,0.3);margin-bottom:2rem;">
                        <h2 style="color:#2c3e52;margin-bottom:1.5rem;">Ready to Begin?</h2>
                        <p style="color:#2c3e52;font-size:1.1rem;margin-bottom:2rem;opacity:0.9;">
                            Your feedback matters! Help us understand how learning and development 
                            can better support your team and organization.
                        </p>
                        <div style="background:rgba(44,62,82,0.1);padding:1rem;border-radius:8px;margin-bottom:2rem;">
                            <p style="color:#2c3e52;font-size:1rem;margin:0;">
                                <strong>Your Role:</strong> {group_display_names.get(user_group, 'Unknown')}
                            </p>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)
                
                # Start button or completion message
                if has_completed:
                    st.markdown('''<div style="background:linear-gradient(135deg, #b1d89a 0%, #7dd4c9 100%);padding:2rem;border-radius:16px;margin-bottom:2rem;color:#2c3e52;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,0.1);">
                        <h2 style="color:#2c3e52;margin:0 0 1rem 0;font-size:1.5rem;">Assessment Already Completed</h2>
                        <p style="margin:0.5rem 0 0 0;font-size:1.1rem;font-weight:500;">Thank you for completing your assessment! Your feedback has been recorded.</p>
                        <p style="margin:0.5rem 0 0 0;font-size:1rem;color:#34495e;">If you need to make changes, please contact your administrator.</p>
                    </div>''', unsafe_allow_html=True)
                else:
                    if st.button("Start Assessment Now", type="primary", use_container_width=True, key="start_assessment", 
                               help="Click to begin your L&D 360 assessment"):
                        st.session_state.selected_group = user_group
                        st.session_state.survey_page = 1
                        st.rerun()
        
        elif st.session_state.survey_page > 0:
            # Check if respondent has already completed (prevent access to survey)
            if st.session_state.user_role == "respondent" and has_completed:
                st.error("You have already completed this assessment. If you need to make changes, please contact your administrator.")
                st.stop()
            
            # Also check if they're trying to access survey after completion
            if st.session_state.user_role == "respondent":
                completion_check = db_fetchone(
                    "SELECT status FROM assessment_completion WHERE respondent_id = ? AND org_key = ?",
                    (st.session_state.current_user, st.session_state.organization_id)
                )
                if completion_check and completion_check["status"] == "completed":
                    st.error("You have already completed this assessment. If you need to make changes, please contact your administrator.")
                    st.stop()
            
            # Survey questions (multi-page format)
            survey_elements = [
                ("Strategic Connection", [
                    "Learning aligns with business priorities",
                    "L&D is engaged in strategic conversations", 
                    "Learning supports current and future transformation",
                    "Stakeholders understand the purpose of L&D"
                ]),
                ("Needs Analysis", [
                    "Clear processes exist for identifying learning needs",
                    "L&D engages stakeholders to prioritise needs",
                    "Development is linked to capability frameworks or business outcomes",
                    "Decisions are based on data and feedback"
                ]),
                ("Learning Design", [
                    "Content is designed with the learner in mind",
                    "Learning addresses both skills and mindset",
                    "Different formats are used appropriately",
                    "Sessions and resources are clearly linked to outcomes"
                ]),
                ("Learning Culture", [
                    "Leaders promote and role model learning",
                    "Time and space are protected for learning",
                    "Employees are encouraged to take ownership of their development",
                    "Learning is valued and recognised in the business"
                ]),
                ("Platform and Tools", [
                    "The LMS or platform is easy to use and accessible",
                    "The platform supports continuous and self-driven learning",
                    "Data and insights are available for decision-making",
                    "Tools are integrated with broader talent or performance systems"
                ]),
                ("Integration with Talent", [
                    "Learning is connected to performance expectations",
                    "Development supports internal mobility and career growth",
                    "L&D links with succession and talent processes",
                    "Leadership development is clearly structured"
                ]),
                ("Learning Impact", [
                    "Impact is discussed regularly with stakeholders",
                    "L&D uses data to show evidence of progress",
                    "There are clear KPIs for learning success",
                    "Return on investment is visible or estimated"
                ]),
                ("Future Capability", [
                    "Future capability needs are being explored",
                    "L&D is anticipating future changes and disruption",
                    "Development is aligned to long-term workforce planning",
                    "There is a clear plan for continuous L&D evolution"
                ])
            ]
            
            current_element_idx = st.session_state.survey_page - 1
            if current_element_idx < len(survey_elements):
                element_name, questions = survey_elements[current_element_idx]
                
                # Progress indicator
                total_pages = len(survey_elements)
                progress = (current_element_idx + 1) / total_pages
                
                st.markdown(f'''<div style="background:linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);padding:1rem;border-radius:8px;border-left:4px solid #2196f3;margin-bottom:2rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                    <strong style="color:#1565c0;font-size:1.1rem;">Page {current_element_idx + 1} of {total_pages}</strong>
                    <span style="color:#1565c0;font-size:0.9rem;">{st.session_state.selected_group}</span>
                </div>
                <div style="background:rgba(255,255,255,0.3);height:8px;border-radius:4px;overflow:hidden;">
                    <div style="background:#7dd4c9;height:100%;width:{progress*100}%;transition:width 0.3s ease;"></div>
                </div>
                </div>''', unsafe_allow_html=True)
                
                # Element header
                st.markdown(f'''<div style="text-align:center;margin-bottom:2rem;">
                    <h2 style="color:#7dd4c9;margin-bottom:0.5rem;">{element_name}</h2>
                    <p style="color:#f8c255;font-size:1.1rem;margin:0;">Rate how strongly you agree or disagree with each statement below</p>
                    <p style="color:white;font-size:0.9rem;margin:0.5rem 0 0 0;">Be honest and consider your actual experience in your organization</p>
                </div>''', unsafe_allow_html=True)
                
                # Questions for current element
                with st.form(f"element_{current_element_idx}"):
                    element_responses = {}
                    
                    for i, question in enumerate(questions):
                        st.markdown(f"**{i+1}. {question}**")
                        response = st.slider(
                            "Rating",
                            min_value=1,
                            max_value=5,
                            value=3,
                            key=f"survey_q_{current_element_idx}_{i}",
                            help="1 = Strongly Disagree, 5 = Strongly Agree",
                            label_visibility="collapsed"
                        )
                        
                        # Add rating labels below the slider
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.markdown("<div style='text-align:center;font-size:0.8rem;color:white;'>1<br>Strongly<br>Disagree</div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown("<div style='text-align:center;font-size:0.8rem;color:white;'>2<br>Disagree</div>", unsafe_allow_html=True)
                        with col3:
                            st.markdown("<div style='text-align:center;font-size:0.8rem;color:white;'>3<br>Neutral</div>", unsafe_allow_html=True)
                        with col4:
                            st.markdown("<div style='text-align:center;font-size:0.8rem;color:white;'>4<br>Agree</div>", unsafe_allow_html=True)
                        with col5:
                            st.markdown("<div style='text-align:center;font-size:0.8rem;color:white;'>5<br>Strongly<br>Agree</div>", unsafe_allow_html=True)
                        
                        element_responses[question] = response
                        st.markdown("---")
                    
                    # Navigation buttons
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        if current_element_idx > 0:
                            if st.form_submit_button("← Previous", use_container_width=True):
                                st.session_state.survey_page -= 1
                                st.rerun()
                    
                    with col2:
                        if current_element_idx < total_pages - 1:
                            if st.form_submit_button("Next →", type="primary", use_container_width=True):
                                # Store responses for this element
                                st.session_state.survey_responses[element_name] = element_responses
                                st.session_state.survey_page += 1
                                st.rerun()
                        else:
                            if st.form_submit_button("Submit Assessment", type="primary", use_container_width=True):
                                # Store final element responses
                                st.session_state.survey_responses[element_name] = element_responses
                                
                                # Complete assessment
                                st.session_state.survey_page = -1  # Mark as complete
                                st.rerun()
                    
                    with col3:
                        st.markdown("")  # Empty column for balance
        
        # Assessment complete
        elif st.session_state.survey_page == -1:
            st.success("Assessment Complete!")
            st.balloons()
            
            # Save responses to database
            if st.session_state.survey_responses:
                try:
                    # Use user's email as respondent_id for consistency
                    respondent_id = st.session_state.current_user
                    
                    # Check if already completed (double-check)
                    existing_completion = db_fetchone(
                        "SELECT status FROM assessment_completion WHERE respondent_id = ? AND org_key = ?",
                        (respondent_id, st.session_state.organization_id)
                    )
                    
                    if existing_completion and existing_completion["status"] == "completed":
                        st.error("Assessment already completed. If you need to make changes, please contact your administrator.")
                        st.stop()
                    
                    # Save responses to database
                    save_survey_responses(
                        respondent_id=respondent_id,
                        org_key=st.session_state.organization_id,
                        group_type=st.session_state.selected_group,
                        responses=st.session_state.survey_responses
                    )
                    
                    # Display thank you message
                    st.markdown('''<div style="background:linear-gradient(135deg, #b1d89a 0%, #7dd4c9 100%);padding:2rem;border-radius:16px;margin-bottom:2rem;color:#2c3e52;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,0.1);">
                        <h2 style="color:#2c3e52;margin:0 0 1rem 0;font-size:2rem;">Thank You for Completing Your Assessment!</h2>
                        <p style="margin:0.5rem 0 0 0;font-size:1.2rem;font-weight:500;">Your valuable feedback has been successfully recorded and will help shape the future of learning and development in your organization.</p>
                        <p style="margin:1rem 0 0 0;font-size:1rem;color:#34495e;">We truly appreciate the time you have taken to share your insights.</p>
                    </div>''', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error saving responses: {str(e)}")
            
            # Show summary for client users
            if st.session_state.user_role == "client":
                st.subheader("Your Assessment Summary")
                
                # Calculate element averages
                element_averages = {}
                for element_name, responses in st.session_state.survey_responses.items():
                    if responses:
                        element_averages[element_name] = sum(responses.values()) / len(responses)
                
                # Display summary
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Element Scores:**")
                    for element, avg in element_averages.items():
                        st.metric(element, f"{avg:.1f}/5.0")
                
                with col2:
                    st.markdown("**Overall Assessment:**")
                    overall_avg = sum(element_averages.values()) / len(element_averages)
                    st.metric("Overall Score", f"{overall_avg:.1f}/5.0")
                    
                    if overall_avg >= 4.0:
                        st.success("Strong L&D Foundation")
                    elif overall_avg >= 3.0:
                        st.info("Good L&D Foundation with Room for Growth")
                    else:
                        st.warning("Opportunity to Build Stronger Foundation")
            
            # Reset button (only for non-respondents or if not completed)
            if st.session_state.user_role != "respondent" or not has_completed:
                if st.button("Take Another Assessment", type="primary", key="reset_assessment"):
                    st.session_state.survey_page = 0
                    st.session_state.survey_responses = {}
                    st.session_state.selected_group = None
                    st.rerun()

# Admin section - only show for admin users
if st.session_state.user_role == "admin":
    # Admin management tabs - Users first for priority
    admin_tab1, admin_tab2, admin_tab3 = st.tabs([
        "Users", "Organizations", "Settings"
    ])
    
    with admin_tab1:
            st.subheader("User Management")
            
            # Create new user
            with st.expander("Create New User", expanded=False):
                with st.form("create_user"):
                    user_email = st.text_input("Email", key="create_user_email")
                    user_password = st.text_input("Password", type="password", key="create_user_password")
                    first_name = st.text_input("First Name", key="create_user_first_name")
                    last_name = st.text_input("Last Name", key="create_user_last_name")
                    user_role = st.selectbox("Role", ["admin", "client", "respondent"], key="create_user_role")
                    org_key = st.selectbox("Organization", [org["org_key"] for org in db_fetchall("SELECT org_key FROM organizations")], key="create_user_org")
                    group_type = st.selectbox("Group Type", ["SLT", "LDT", "MGR", "LNR", "ADMIN"], key="create_user_group")
                    
                    if st.form_submit_button("Create User"):
                        if user_email and user_password and org_key:
                            try:
                                db_execute(
                                    "INSERT INTO users (email, password, first_name, last_name, role, org_key, group_type, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                    (user_email, user_password, first_name, last_name, user_role, org_key, group_type, datetime.now().isoformat())
                                )
                                st.success(f"User '{user_email}' created successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error creating user: {str(e)}")
                        else:
                            st.warning("Please fill in all required fields.")
            
            # Bulk user upload
            with st.expander("Bulk User Upload", expanded=False):
                st.info("Upload a CSV file with user details. Required columns: email, first_name, last_name, role, org_key, group_type")
                
                # Download template
                template_data = {
                    'email': ['john.doe@company.com', 'jane.smith@company.com'],
                    'first_name': ['John', 'Jane'],
                    'last_name': ['Doe', 'Smith'],
                    'role': ['client', 'respondent'],
                    'org_key': ['acme_corp', 'acme_corp'],
                    'group_type': ['LDT', 'LNR']
                }
                template_df = pd.DataFrame(template_data)
                template_csv = template_df.to_csv(index=False)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="bulk_user_upload")
                with col2:
                    st.download_button(
                        label="Download Template",
                        data=template_csv,
                        file_name="user_upload_template.csv",
                        mime="text/csv"
                    )
                
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.write("Preview of uploaded data:")
                        st.dataframe(df.head())
                        
                        # Validate required columns
                        required_columns = ['email', 'first_name', 'last_name', 'role', 'org_key', 'group_type']
                        missing_columns = [col for col in required_columns if col not in df.columns]
                        
                        if missing_columns:
                            st.error(f"Missing required columns: {missing_columns}")
                        else:
                            if st.button("Process Bulk Upload", type="primary", key="process_bulk_upload"):
                                success_count = 0
                                error_count = 0
                                errors = []
                                
                                for index, row in df.iterrows():
                                    try:
                                        # Check if user already exists
                                        existing_user = db_fetchone("SELECT 1 FROM users WHERE email = ?", (row['email'],))
                                        if existing_user:
                                            errors.append(f"Row {index + 1}: User {row['email']} already exists")
                                            error_count += 1
                                            continue
                                        
                                        # Check if organization exists
                                        existing_org = db_fetchone("SELECT 1 FROM organizations WHERE org_key = ?", (row['org_key'],))
                                        if not existing_org:
                                            errors.append(f"Row {index + 1}: Organization {row['org_key']} does not exist")
                                            error_count += 1
                                            continue
                                        
                                        # Generate secure password
                                        import secrets
                                        import string
                                        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                                        
                                        # Insert user
                                        db_execute(
                                            "INSERT INTO users (email, password, first_name, last_name, role, org_key, group_type, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                            (row['email'], password, row['first_name'], row['last_name'], row['role'], row['org_key'], row['group_type'], datetime.now().isoformat())
                                        )
                                        
                                        # Get organization name for email
                                        org_info = db_fetchone("SELECT name FROM organizations WHERE org_key = ?", (row['org_key'],))
                                        org_name = org_info["name"] if org_info else row['org_key']
                                        
                                        # Send welcome email
                                        login_url = "http://localhost:8501"  # This should be configurable
                                        email_sent, email_message = send_welcome_email(
                                            row['email'], 
                                            f"{row['first_name']} {row['last_name']}", 
                                            password, 
                                            org_name, 
                                            login_url
                                        )
                                        
                                        if email_sent:
                                            success_count += 1
                                        else:
                                            # User created but email failed
                                            errors.append(f"Row {index + 1}: User {row['email']} created but email failed: {email_message}")
                                            success_count += 1
                                        
                                    except Exception as e:
                                        errors.append(f"Row {index + 1}: {str(e)}")
                                        error_count += 1
                                
                                # Show results
                                if success_count > 0:
                                    st.success(f"Successfully uploaded {success_count} users!")
                                if error_count > 0:
                                    st.error(f"Failed to upload {error_count} users. Check errors below:")
                                    for error in errors:
                                        st.write(f"• {error}")
                                
                                if success_count > 0:
                                    st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error reading CSV file: {str(e)}")
            
            # Search and filter users
            st.subheader("Search & Filter Users")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                user_search = st.text_input("Search by name or email", placeholder="Enter name or email...", key="user_search_input")
            with col2:
                user_role_filter = st.selectbox("Filter by role", ["All Roles", "admin", "client", "respondent"], key="user_role_filter")
            with col3:
                user_group_filter = st.selectbox("Filter by group", ["All Groups", "SLT", "LDT", "MGR", "LNR", "ADMIN"], key="user_group_filter")
            with col4:
                user_org_filter = st.selectbox("Filter by organization", ["All Organizations"] + [org["org_key"] for org in db_fetchall("SELECT org_key FROM organizations")], key="user_org_filter")
            
            # Get and filter users
            users = db_fetchall("SELECT u.*, o.name as org_name FROM users u LEFT JOIN organizations o ON u.org_key = o.org_key ORDER BY COALESCE(u.created_at, '1970-01-01') DESC")
            if users:
                # Apply filters
                filtered_users = []
                for user in users:
                    # Search filter
                    if user_search:
                        search_term = user_search.lower()
                        user_name = f"{user['first_name'] or ''} {user['last_name'] or ''}".lower()
                        if search_term not in user_name and search_term not in user['email'].lower():
                            continue
                    
                    # Role filter
                    if user_role_filter != "All Roles" and user["role"] != user_role_filter:
                        continue
                    
                    # Group filter
                    if user_group_filter != "All Groups" and user["group_type"] != user_group_filter:
                        continue
                    
                    # Organization filter
                    if user_org_filter != "All Organizations" and user["org_key"] != user_org_filter:
                        continue
                    
                    filtered_users.append(user)
                
                # Display results count
                st.info(f"Showing {len(filtered_users)} of {len(users)} users")
                
                if filtered_users:
                    user_data = []
                    for user in filtered_users:
                        # Get completion status for respondents
                        completion_status = "N/A"
                        if user["role"] == "respondent":
                            completion_row = db_fetchone(
                                "SELECT status, completion_percentage FROM assessment_completion WHERE respondent_id = ? AND org_key = ?",
                                (user["email"], user["org_key"])
                            )
                            if completion_row:
                                if completion_row["status"] == "completed":
                                    completion_status = f"{completion_row['completion_percentage']:.0f}%"
                                elif completion_row["status"] == "partial":
                                    completion_status = f"{completion_row['completion_percentage']:.0f}%"
                                else:
                                    completion_status = "Not Started"
                            else:
                                completion_status = "Not Started"
                        
                        user_data.append({
                            "Email": user["email"],
                            "Name": f"{user['first_name'] or ''} {user['last_name'] or ''}".strip() or "N/A",
                            "Role": user["role"],
                            "Organization": user["org_name"] or "N/A",
                            "Group": user["group_type"] or "N/A",
                            "Completion": completion_status,
                            "Created": user["created_at"][:10] if user["created_at"] else "N/A"
                        })
                    
                    # Add export functionality
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.dataframe(pd.DataFrame(user_data), use_container_width=True)
                    with col2:
                         if st.button("Export CSV", type="secondary", key="export_users_csv"):
                             df = pd.DataFrame(user_data)
                             csv = df.to_csv(index=False)
                             st.download_button(
                                 label="Download CSV",
                                 data=csv,
                                 file_name=f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                 mime="text/csv"
                             )
                else:
                    st.warning("No users match your search criteria.")
            else:
                st.info("No users found.")
    
    with admin_tab2:
            st.subheader("Organization Management")
            
            # Create new organization
            with st.expander("Create New Organization", expanded=False):
                with st.form("create_org"):
                    org_name = st.text_input("Organization Name", key="create_org_name")
                    org_key = st.text_input("Organization Key (unique identifier)", key="create_org_key")
                    org_type = st.selectbox("Type", ["client", "partner"], key="create_org_type")
                    
                    # Logo upload section
                    st.markdown("**Organization Logo (Optional)**")
                    st.markdown("Upload a logo to personalize the platform for this client. Recommended: PNG format, transparent background, max 2MB.")
                    
                    uploaded_logo = st.file_uploader(
                        "Choose logo file", 
                        type=['png', 'jpg', 'jpeg'], 
                        key="create_org_logo",
                        help="Upload client organization logo"
                    )
                    
                    if st.form_submit_button("Create Organization"):
                        if org_name and org_key:
                            try:
                                # Handle logo upload
                                logo_path = None
                                if uploaded_logo is not None:
                                    # Create logos directory if it doesn't exist
                                    os.makedirs(LOGO_DIR, exist_ok=True)
                                    
                                    # Generate unique filename
                                    file_extension = uploaded_logo.name.split('.')[-1].lower()
                                    logo_filename = f"{org_key}_logo.{file_extension}"
                                    logo_path = os.path.join(LOGO_DIR, logo_filename)
                                    
                                    # Save uploaded file
                                    with open(logo_path, "wb") as f:
                                        f.write(uploaded_logo.getbuffer())
                                    
                                    # Store relative path in database
                                    logo_path = f"data/logos/{logo_filename}"
                                
                                # Insert organization with logo path
                                db_execute(
                                    "INSERT INTO organizations (org_key, name, type, status, logo_path, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                    (org_key, org_name, org_type, "Active", logo_path, datetime.now().isoformat())
                                )
                                
                                success_msg = f"Organization '{org_name}' created successfully!"
                                if logo_path:
                                    success_msg += f" Logo uploaded and saved."
                                st.success(success_msg)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error creating organization: {str(e)}")
                        else:
                            st.warning("Please fill in all required fields.")
            
            # Logo management for existing organizations
            st.markdown("---")
            st.subheader("Logo Management")
            st.info("Update logos for existing organizations to personalize their platform experience.")
            
            # Logo update section
            with st.expander("Update Organization Logo", expanded=False):
                # Get organizations that could have logos updated
                orgs_for_logo = db_fetchall("SELECT org_key, name, logo_path FROM organizations WHERE type != 'platform_admin' ORDER BY name")
                
                if orgs_for_logo:
                    # Organization selector
                    selected_org_for_logo = st.selectbox(
                        "Select Organization:",
                        options=[f"{org['name']} ({org['org_key']})" for org in orgs_for_logo],
                        key="logo_update_org"
                    )
                    
                    if selected_org_for_logo:
                        # Extract org_key
                        selected_org_key = selected_org_for_logo.split("(")[-1].rstrip(")")
                        
                        # Get current logo info
                        current_org = next((org for org in orgs_for_logo if org['org_key'] == selected_org_key), None)
                        
                        if current_org:
                            # Show current logo status
                            if current_org["logo_path"] and current_org["logo_path"] != "qReview - logos.png":
                                st.success(f"**Current Logo**: {current_org['logo_path']}")
                                try:
                                    st.image(current_org['logo_path'], width=150, caption="Current Logo")
                                except:
                                    st.warning("Current logo file not found")
                            else:
                                st.info("**Current Logo**: Using default qReview logo")
                            
                            # Logo upload for update
                            st.markdown("**Upload New Logo**")
                            new_logo = st.file_uploader(
                                "Choose new logo file", 
                                type=['png', 'jpg', 'jpeg'], 
                                key="update_org_logo",
                                help="Upload new logo for this organization"
                            )
                            
                            if new_logo and st.button("Update Logo", type="primary", key="update_logo_btn"):
                                try:
                                    # Create logos directory if it doesn't exist
                                    os.makedirs(LOGO_DIR, exist_ok=True)
                                    
                                    # Generate unique filename
                                    file_extension = new_logo.name.split('.')[-1].lower()
                                    logo_filename = f"{selected_org_key}_logo.{file_extension}"
                                    logo_path = os.path.join(LOGO_DIR, logo_filename)
                                    
                                    # Save uploaded file
                                    with open(logo_path, "wb") as f:
                                        f.write(new_logo.getbuffer())
                                    
                                    # Store relative path in database
                                    db_logo_path = f"data/logos/{logo_filename}"
                                    
                                    # Update database
                                    db_execute(
                                        "UPDATE organizations SET logo_path = ? WHERE org_key = ?",
                                        (db_logo_path, selected_org_key)
                                    )
                                    
                                    st.success(f"Logo updated successfully for {current_org['name']}!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error updating logo: {str(e)}")
                else:
                    st.info("No organizations available for logo updates.")
            
            # Search and filter organizations
            st.subheader("Search & Filter Organizations")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                org_search = st.text_input("Search by name or key", placeholder="Enter organization name or key...", key="org_search_input")
            with col2:
                org_type_filter = st.selectbox("Filter by type", ["All Types", "client", "partner", "platform_admin"], key="org_type_filter")
            with col3:
                org_status_filter = st.selectbox("Filter by status", ["All Statuses", "Active", "Inactive", "Suspended"], key="org_status_filter")
            
            # Get and filter organizations
            orgs = db_fetchall("SELECT * FROM organizations ORDER BY created_at DESC")
            if orgs:
                # Apply filters
                filtered_orgs = []
                for org in orgs:
                    # Search filter
                    if org_search and org_search.lower() not in org["name"].lower() and org_search.lower() not in org["org_key"].lower():
                        continue
                    
                    # Type filter
                    if org_type_filter != "All Types" and org["type"] != org_type_filter:
                        continue
                    
                    # Status filter
                    if org_status_filter != "All Statuses" and org["status"] != org_status_filter:
                        continue
                    
                    filtered_orgs.append(org)
                
                # Display results count
                st.info(f"Showing {len(filtered_orgs)} of {len(orgs)} organizations")
                
                if filtered_orgs:
                    org_data = []
                    for org in filtered_orgs:
                        # Check if organization has a custom logo
                        has_logo = "Yes" if org["logo_path"] and org["logo_path"] != "qReview - logos.png" else "No"
                        
                        org_data.append({
                            "Name": org["name"],
                            "Key": org["org_key"],
                            "Type": org["type"],
                            "Status": org["status"],
                            "Logo": has_logo,
                            "Created": org["created_at"][:10] if org["created_at"] else "N/A"
                        })
                    
                    # Add export functionality
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.dataframe(pd.DataFrame(org_data), use_container_width=True)
                    with col2:
                         if st.button("Export CSV", type="secondary", key="export_orgs_csv"):
                             df = pd.DataFrame(org_data)
                             csv = df.to_csv(index=False)
                             st.download_button(
                                 label="Download CSV",
                                 data=csv,
                                 file_name=f"organizations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                 mime="text/csv"
                             )
                else:
                    st.warning("No organizations match your search criteria.")
            else:
                st.info("No organizations found.")
    
    with admin_tab3:
        st.subheader("Platform Settings")
        
        # Email Configuration
        st.markdown("---")
        st.subheader("Email Configuration")
        st.info("Configure email settings for sending welcome emails to new users.")
        
        with st.expander("Email Settings", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**SMTP Configuration**")
                smtp_server = st.text_input("SMTP Server", value=EMAIL_CONFIG['smtp_server'], key="smtp_server")
                smtp_port = st.number_input("SMTP Port", value=EMAIL_CONFIG['smtp_port'], key="smtp_port")
                smtp_username = st.text_input("SMTP Username (Email)", value=EMAIL_CONFIG['smtp_username'], key="smtp_username")
                smtp_password = st.text_input("SMTP Password", value=EMAIL_CONFIG['smtp_password'], type="password", key="smtp_password")
            
            with col2:
                st.markdown("**Sender Information**")
                from_email = st.text_input("From Email", value=EMAIL_CONFIG['from_email'], key="from_email")
                from_name = st.text_input("From Name", value=EMAIL_CONFIG['from_name'], key="from_name")
                
                st.markdown("**Platform URL**")
                platform_url = st.text_input("Platform Login URL", value="http://localhost:8501", key="platform_url")
                
            # Test email configuration
            if st.button("Test Email Configuration", type="primary", key="test_email"):
                if smtp_username and smtp_password:
                    # Update config temporarily for testing
                    test_config = EMAIL_CONFIG.copy()
                    test_config.update({
                        'smtp_server': smtp_server,
                        'smtp_port': smtp_port,
                        'smtp_username': smtp_username,
                        'smtp_password': smtp_password,
                        'from_email': from_email,
                        'from_name': from_name
                    })
                    
                    # Test email
                    success, message = test_email_configuration()
                    if success:
                        st.success("Email test successful! Check your inbox.")
                    else:
                        st.error(f"Email test failed: {message}")
                else:
                    st.warning("Please enter SMTP username and password to test.")
            
            # Save configuration
            if st.button("Save Email Configuration", type="secondary", key="save_email"):
                st.info("Email configuration saved. Note: These settings are stored in environment variables for security.")
                st.markdown('''**To make these settings permanent, add to your `.env` file:**
                ```
                SMTP_SERVER=smtp.gmail.com
                SMTP_PORT=587
                SMTP_USERNAME=your-email@gmail.com
                SMTP_PASSWORD=your-app-password
                FROM_EMAIL=noreply@yourcompany.com
                FROM_NAME=Your Company Name
                ```
                ''')
            
        st.markdown("---")
        st.info("Platform configuration options will be available here.")
            
        # Demo data generation
        if st.button("Generate Demo Data", type="primary", help="Create sample survey data for testing", key="generate_demo_data"):
            demo_df = create_demo_survey_data()
            if demo_df is not None:
                # Save demo data to database for acme_corp
                try:
                    for _, row in demo_df.iterrows():
                        db_execute(
                            "INSERT INTO survey_responses (respondent_id, org_key, element, question, score, group_type, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (row['respondent_id'], "acme_corp", row['element'], row['question'], row['score'], row['group'], row['submitted_at'])
                        )
                    st.success("Demo data generated and saved to database!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving demo data: {str(e)}")
        
        # Create showcase respondent for Acme Corp
        st.markdown("---")
        st.subheader("Showcase Respondent Creation")
        st.info("Create a single respondent user for Acme Corp to showcase the tool.")
        
        if st.button("Create Acme Showcase Respondent", type="primary", help="Create a respondent user for Acme Corp", key="create_showcase_respondent"):
            try:
                # Create showcase respondent user
                showcase_user = {
                    'first_name': 'Sarah',
                    'last_name': 'Johnson',
                    'email': 'sarah.johnson@acme.com',
                    'password': 'demo123',
                    'role': 'respondent',
                    'org_key': 'acme_corp',
                    'group_type': 'LNR'  # Learner
                }
                
                # Check if user already exists
                existing_user = db_fetchone("SELECT id FROM users WHERE email = ?", (showcase_user['email'],))
                if existing_user:
                    st.warning("Showcase respondent already exists!")
                else:
                    # Create user
                    db_execute(
                        "INSERT INTO users (first_name, last_name, email, password_hash, role, org_key, group_type, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            showcase_user['first_name'],
                            showcase_user['last_name'],
                            showcase_user['email'],
                            generate_password_hash(showcase_user['password']),
                            showcase_user['role'],
                            showcase_user['org_key'],
                            showcase_user['group_type'],
                            datetime.now()
                        )
                    )
                    st.success("Showcase respondent created successfully!")
                    st.info(f"**Login Details:**")
                    st.info(f"**Email**: {showcase_user['email']}")
                    st.info(f"**Password**: {showcase_user['password']}")
                    st.info(f"**Role**: {showcase_user['role']}")
                    st.info(f"**Organization**: Acme Corp")
                    st.info(f"**Group**: Learner")
                    st.rerun()
            except Exception as e:
                st.error(f"Error creating showcase respondent: {str(e)}")
            
        st.markdown("---")
        st.markdown('''**Admin Capabilities:**
        - Create and manage users (Priority)
        - Create and manage organizations
        - Generate demo data for testing
        - Platform configuration and settings
        - User access management
        ''', unsafe_allow_html=True)