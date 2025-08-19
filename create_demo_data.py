import sqlite3
import os
from datetime import datetime, timedelta
import random

# Database setup
DATA_DIR = os.path.join(os.getcwd(), "data")
DB_PATH = os.path.join(DATA_DIR, "qreview.sqlite3")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_comprehensive_demo_data():
    """Create comprehensive demo data with two organizations, varied responses, and test accounts"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Clear existing demo data
    cur.execute("DELETE FROM survey_responses WHERE org_key IN ('acme_corp', 'tech_innovate')")
    cur.execute("DELETE FROM assessment_completion WHERE org_key IN ('acme_corp', 'tech_innovate')")
    cur.execute("DELETE FROM users WHERE org_key IN ('acme_corp', 'tech_innovate')")
    cur.execute("DELETE FROM organizations WHERE org_key IN ('acme_corp', 'tech_innovate')")
    
    # Create two demo organizations
    organizations = [
        {
            'org_key': 'acme_corp',
            'name': 'Acme Corporation',
            'type': 'client',
            'logo_path': 'qpeople_logo.png',
            'primary_color': '#2E86AB',
            'secondary_color': '#A23B72',
            'status': 'Active',
            'created_at': datetime.now().isoformat()
        },
        {
            'org_key': 'tech_innovate',
            'name': 'Tech Innovate Ltd',
            'type': 'client',
            'logo_path': 'qpeople_logo.png',
            'primary_color': '#28A745',
            'secondary_color': '#FFC107',
            'status': 'Active',
            'created_at': datetime.now().isoformat()
        }
    ]
    
    # Insert organizations
    for org in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations 
            (org_key, name, type, logo_path, primary_color, secondary_color, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            org['org_key'], org['name'], org['type'], 
            org['logo_path'], org['primary_color'], org['secondary_color'],
            org['status'], org['created_at']
        ))
    
    # Create comprehensive demo users for both organizations
    demo_users = [
        # Acme Corporation - 15 users
        {
            'email': 'sarah.johnson@acme.com',
            'password': 'demo123',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'role': 'client',
            'department': 'HR',
            'org_key': 'acme_corp'
        },
        {
            'email': 'mike.chen@acme.com',
            'password': 'demo123',
            'first_name': 'Mike',
            'last_name': 'Chen',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'acme_corp',
            'group': 'LDT'
        },
        {
            'email': 'lisa.rodriguez@acme.com',
            'password': 'demo123',
            'first_name': 'Lisa',
            'last_name': 'Rodriguez',
            'role': 'respondent',
            'department': 'Sales',
            'org_key': 'acme_corp',
            'group': 'MGR'
        },
        {
            'email': 'david.kim@acme.com',
            'password': 'demo123',
            'first_name': 'David',
            'last_name': 'Kim',
            'role': 'respondent',
            'department': 'Marketing',
            'org_key': 'acme_corp',
            'group': 'MGR'
        },
        {
            'email': 'emma.wilson@acme.com',
            'password': 'demo123',
            'first_name': 'Emma',
            'last_name': 'Wilson',
            'role': 'respondent',
            'department': 'Operations',
            'org_key': 'acme_corp',
            'group': 'LNR'
        },
        {
            'email': 'james.brown@acme.com',
            'password': 'demo123',
            'first_name': 'James',
            'last_name': 'Brown',
            'role': 'respondent',
            'department': 'Finance',
            'org_key': 'acme_corp',
            'group': 'SLT'
        },
        {
            'email': 'anna.garcia@acme.com',
            'password': 'demo123',
            'first_name': 'Anna',
            'last_name': 'Garcia',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'acme_corp',
            'group': 'LDT'
        },
        {
            'email': 'robert.lee@acme.com',
            'password': 'demo123',
            'first_name': 'Robert',
            'last_name': 'Lee',
            'role': 'respondent',
            'department': 'Sales',
            'org_key': 'acme_corp',
            'group': 'MGR'
        },
        {
            'email': 'sophie.martin@acme.com',
            'password': 'demo123',
            'first_name': 'Sophie',
            'last_name': 'Martin',
            'role': 'respondent',
            'department': 'Operations',
            'org_key': 'acme_corp',
            'group': 'LNR'
        },
        {
            'email': 'thomas.anderson@acme.com',
            'password': 'demo123',
            'first_name': 'Thomas',
            'last_name': 'Anderson',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'acme_corp',
            'group': 'LDT'
        },
        {
            'email': 'maria.silva@acme.com',
            'password': 'demo123',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'role': 'respondent',
            'department': 'Marketing',
            'org_key': 'acme_corp',
            'group': 'MGR'
        },
        {
            'email': 'kevin.zhang@acme.com',
            'password': 'demo123',
            'first_name': 'Kevin',
            'last_name': 'Zhang',
            'role': 'respondent',
            'department': 'Operations',
            'org_key': 'acme_corp',
            'group': 'LNR'
        },
        {
            'email': 'jennifer.white@acme.com',
            'password': 'demo123',
            'first_name': 'Jennifer',
            'last_name': 'White',
            'role': 'respondent',
            'department': 'Finance',
            'org_key': 'acme_corp',
            'group': 'SLT'
        },
        {
            'email': 'alex.turner@acme.com',
            'password': 'demo123',
            'first_name': 'Alex',
            'last_name': 'Turner',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'acme_corp',
            'group': 'LDT'
        },
        {
            'email': 'rachel.clark@acme.com',
            'password': 'demo123',
            'first_name': 'Rachel',
            'last_name': 'Clark',
            'role': 'respondent',
            'department': 'Sales',
            'org_key': 'acme_corp',
            'group': 'MGR'
        },
        
        # Tech Innovate Ltd - 12 users
        {
            'email': 'mark.davis@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Mark',
            'last_name': 'Davis',
            'role': 'client',
            'department': 'Operations',
            'org_key': 'tech_innovate'
        },
        {
            'email': 'sarah.williams@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'tech_innovate',
            'group': 'LDT'
        },
        {
            'email': 'michael.johnson@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'role': 'respondent',
            'department': 'Product',
            'org_key': 'tech_innovate',
            'group': 'MGR'
        },
        {
            'email': 'lisa.chen@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Lisa',
            'last_name': 'Chen',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'tech_innovate',
            'group': 'LDT'
        },
        {
            'email': 'david.rodriguez@techinnovate.com',
            'password': 'demo123',
            'first_name': 'David',
            'last_name': 'Rodriguez',
            'role': 'respondent',
            'department': 'Sales',
            'org_key': 'tech_innovate',
            'group': 'MGR'
        },
        {
            'email': 'emma.kim@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Emma',
            'last_name': 'Kim',
            'role': 'respondent',
            'department': 'Operations',
            'org_key': 'tech_innovate',
            'group': 'LNR'
        },
        {
            'email': 'james.brown@techinnovate.com',
            'password': 'demo123',
            'first_name': 'James',
            'last_name': 'Brown',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'tech_innovate',
            'group': 'LDT'
        },
        {
            'email': 'anna.garcia@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Anna',
            'last_name': 'Garcia',
            'role': 'respondent',
            'department': 'Product',
            'org_key': 'tech_innovate',
            'group': 'MGR'
        },
        {
            'email': 'robert.lee@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Robert',
            'last_name': 'Lee',
            'role': 'respondent',
            'department': 'Operations',
            'org_key': 'tech_innovate',
            'group': 'LNR'
        },
        {
            'email': 'sophie.martin@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Sophie',
            'last_name': 'Martin',
            'role': 'respondent',
            'department': 'Engineering',
            'org_key': 'tech_innovate',
            'group': 'LDT'
        },
        {
            'email': 'thomas.anderson@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Thomas',
            'last_name': 'Anderson',
            'role': 'respondent',
            'department': 'Sales',
            'org_key': 'tech_innovate',
            'group': 'MGR'
        },
        {
            'email': 'maria.silva@techinnovate.com',
            'password': 'demo123',
            'first_name': 'Maria',
            'last_name': 'Silva',
            'role': 'respondent',
            'department': 'Operations',
            'org_key': 'tech_innovate',
            'group': 'LNR'
        }
    ]
    
    # Insert users
    for user in demo_users:
        cur.execute("""
            INSERT OR REPLACE INTO users 
            (email, password, first_name, last_name, role, department, org_key)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user['email'], user['password'], user['first_name'], 
            user['last_name'], user['role'], user['department'], user['org_key']
        ))
    
    # Survey structure
    survey_elements = [
        "Strategic Connection",
        "Needs Analysis", 
        "Learning Design",
        "Learning Culture",
        "Platform and Tools",
        "Integration with Talent",
        "Learning Impact",
        "Future Capability"
    ]
    
    questions_per_element = {
        "Strategic Connection": [
            "Learning aligns with business priorities",
            "L&D is engaged in strategic conversations",
            "Learning supports current and future transformation",
            "Stakeholders understand the purpose of L&D"
        ],
        "Needs Analysis": [
            "Clear processes exist for identifying learning needs",
            "L&D engages stakeholders to prioritise needs",
            "Development is linked to capability frameworks or business outcomes",
            "Decisions are based on data and feedback"
        ],
        "Learning Design": [
            "Content is designed with the learner in mind",
            "Learning addresses both skills and mindset",
            "Different formats are used appropriately",
            "Sessions and resources are clearly linked to outcomes"
        ],
        "Learning Culture": [
            "Leaders promote and role model learning",
            "Time and space are protected for learning",
            "Employees are encouraged to take ownership of their development",
            "Learning is valued and recognised in the business"
        ],
        "Platform and Tools": [
            "The LMS or platform is easy to use and accessible",
            "The platform supports continuous and self-driven learning",
            "Data and insights are available for decision-making",
            "Tools are integrated with broader talent or performance systems"
        ],
        "Integration with Talent": [
            "Learning is connected to performance expectations",
            "Development supports internal mobility and career growth",
            "L&D links with succession and talent processes",
            "Leadership development is clearly structured"
        ],
        "Learning Impact": [
            "Impact is discussed regularly with stakeholders",
            "L&D uses data to show evidence of progress",
            "There are clear KPIs for learning success",
            "Return on investment is visible or estimated"
        ],
        "Future Capability": [
            "Future capability needs are being explored",
            "L&D is anticipating future changes and disruption",
            "Development is aligned to long-term workforce planning",
            "There is a clear plan for continuous L&D evolution"
        ]
    }
    
    # Create varied response patterns for different organizations and groups
    # This will create realistic misalignment and varied scores
    
    # Organization-specific base scores (different starting points)
    org_base_scores = {
        'acme_corp': {
            "Strategic Connection": 3.8,
            "Needs Analysis": 3.2,
            "Learning Design": 4.1,
            "Learning Culture": 3.5,
            "Platform and Tools": 2.9,
            "Integration with Talent": 3.7,
            "Learning Impact": 3.3,
            "Future Capability": 3.6
        },
        'tech_innovate': {
            "Strategic Connection": 4.2,
            "Needs Analysis": 3.8,
            "Learning Design": 4.4,
            "Learning Culture": 4.0,
            "Platform and Tools": 3.5,
            "Integration with Talent": 4.1,
            "Learning Impact": 3.9,
            "Future Capability": 4.3
        }
    }
    
    # Group-specific modifiers (creates misalignment between groups)
    group_modifiers = {
        'SLT': {
            "Strategic Connection": 0.4,  # SLT sees this more positively
            "Needs Analysis": 0.2,
            "Learning Design": 0.1,
            "Learning Culture": 0.3,
            "Platform and Tools": -0.2,  # SLT less aware of technical issues
            "Integration with Talent": 0.2,
            "Learning Impact": 0.4,  # SLT sees impact more positively
            "Future Capability": 0.3
        },
        'LDT': {
            "Strategic Connection": -0.1,  # LDT more critical of strategic alignment
            "Needs Analysis": 0.3,  # LDT sees this more positively
            "Learning Design": 0.4,  # LDT sees design quality
            "Learning Culture": 0.1,
            "Platform and Tools": 0.2,  # LDT more aware of technical capabilities
            "Integration with Talent": 0.3,
            "Learning Impact": -0.1,  # LDT more critical of impact measurement
            "Future Capability": 0.2
        },
        'MGR': {
            "Strategic Connection": 0.2,
            "Needs Analysis": 0.1,
            "Learning Design": 0.2,
            "Learning Culture": 0.3,  # Managers see culture more positively
            "Platform and Tools": 0.0,
            "Integration with Talent": 0.4,  # Managers see talent integration
            "Learning Impact": 0.2,
            "Future Capability": 0.1
        },
        'LNR': {
            "Strategic Connection": -0.2,  # Non-L&D less aware of strategic connection
            "Needs Analysis": -0.1,
            "Learning Design": 0.1,
            "Learning Culture": 0.2,
            "Platform and Tools": -0.3,  # Non-L&D less satisfied with tools
            "Integration with Talent": -0.1,
            "Learning Impact": -0.2,  # Non-L&D less aware of impact
            "Future Capability": -0.1
        }
    }
    
    # Generate varied survey responses
    for user in demo_users:
        if user['role'] == 'respondent':
            org_key = user['org_key']
            group = user.get('group', 'LNR')  # Default to LNR if not specified
            
            # Each respondent completes the full survey
            for element in survey_elements:
                for question in questions_per_element[element]:
                    # Start with organization base score
                    base_score = org_base_scores[org_key][element]
                    
                    # Apply group-specific modifier
                    group_modifier = group_modifiers[group][element]
                    adjusted_score = base_score + group_modifier
                    
                    # Add individual variation (±0.6) but keep within 1-5 range
                    variation = random.uniform(-0.6, 0.6)
                    final_score = max(1, min(5, round(adjusted_score + variation, 1)))
                    
                    # Insert response
                    cur.execute("""
                        INSERT INTO survey_responses 
                        (respondent_id, org_key, element, question, score, group_type, submitted_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        user['email'], org_key, element, question, final_score, group,
                        (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
                    ))
    
    # Add completion tracking for each respondent
    for user in demo_users:
        if user['role'] == 'respondent':
            org_key = user['org_key']
            group = user.get('group', 'LNR')
            
            # Calculate completion stats
            total_questions = len(survey_elements) * 4  # 4 questions per element
            questions_answered = total_questions  # All questions answered in demo
            completion_percentage = 100.0
            status = "completed"
            
            # Insert completion record
            cur.execute("""
                INSERT OR REPLACE INTO assessment_completion 
                (respondent_id, org_key, group_type, completed_at, total_questions, questions_answered, completion_percentage, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user['email'], org_key, group, datetime.now().isoformat(), 
                total_questions, questions_answered, completion_percentage, status
            ))
    
    conn.commit()
    conn.close()
    
    print("✅ Comprehensive demo data created successfully!")
    print(f"🏢 Organizations: {len(organizations)}")
    print(f"👥 Total users: {len(demo_users)}")
    print(f"📝 Survey responses: {sum(1 for u in demo_users if u['role'] == 'respondent') * len(survey_elements) * 4} total responses")
    print(f"\n🔑 Demo login credentials:")
    print(f"   **Acme Corporation:**")
    print(f"   - Client: sarah.johnson@acme.com / demo123")
    print(f"   - Test Respondents: mike.chen@acme.com, lisa.rodriguez@acme.com, emma.wilson@acme.com / demo123")
    print(f"   **Tech Innovate Ltd:**")
    print(f"   - Client: mark.davis@techinnovate.com / demo123")
    print(f"   - Test Respondents: sarah.williams@techinnovate.com, michael.johnson@techinnovate.com / demo123")
    print(f"\n📊 Respondent Groups Coverage:")
    print(f"   - SLT (Senior Leadership): 2 users")
    print(f"   - LDT (Learning & Development Team): 6 users")
    print(f"   - MGR (Managers): 6 users")
    print(f"   - LNR (Learning & Non-Respondents): 4 users")
    print(f"\n🎯 Key Features:")
    print(f"   - Varied scores create realistic misalignment between groups")
    print(f"   - Different starting points for each organization")
    print(f"   - Group-specific perspectives on different elements")
    print(f"   - Individual variation within groups")

if __name__ == "__main__":
    create_comprehensive_demo_data()

