import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import csv
import hashlib
import time
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import hashlib
import time

# Path constants for reliable file access from CWD
USERS_CSV = r"c:/Users/WINDOWS11/OneDrive/Desktop/K Project 02/ecohealth_users_new.csv"
HEALTH_CSV = r"c:/Users/WINDOWS11/OneDrive/Desktop/K Project 02/ecohealth_data.csv"
MODELS_DIR = r"c:/Users/WINDOWS11/OneDrive/Desktop/K Project 02/"

# Set page configuration
st.set_page_config(

    page_title="EcoHealth AI - Disease Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for medical theme with animations
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }

    /* Unified header style for all pages, supports dark/light mode */
    .main-header-clean {
        background-color: var(--secondary-background-color, #f0f2f6);
        color: var(--text-color, #31333F);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header-clean h1 {
        margin-top: 0;
        padding-top: 0;
        font-size: 2.2rem;
        font-weight: bold;
    }
    .main-header-clean p {
        margin-bottom: 0;
        font-size: 1.1rem;
        opacity: 0.85;
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        animation: slideIn 0.8s ease-out;
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .risk-low { background-color: #d4edda; border-left-color: #28a745; }
    .risk-medium { background-color: #fff3cd; border-left-color: #ffc107; }
    .risk-high { background-color: #f8d7da; border-left-color: #dc3545; }

    .emergency-alert {
        background: linear-gradient(45deg, #ff0000, #ff4444);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        animation: pulse 2s infinite;
        border: 3px solid #cc0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    }

    .thank-you-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        animation: fadeIn 2s ease-out;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    .diet-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-out;
    }

    .login-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Database functions
def init_db():
    """Initialize CSV files for user management and health data"""
    # Initialize users CSV
    init_user_csv()

    # Initialize health data CSV
    init_health_data_csv()

def init_user_csv():
    """Create a CSV file to store user registration data."""
    csv_file = USERS_CSV
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'email', 'created_date', 'last_login'])


def init_health_data_csv():
    """Create a CSV file to store all health assessment data."""
    csv_file = HEALTH_CSV
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id', 'username', 'date', 'time', 'age', 'gender', 'height', 'weight', 'bmi',
                'blood_sugar', 'systolic_bp', 'diastolic_bp', 'smoking', 'exercise',
                'sleep_hours', 'health_score', 'diabetes_risk', 'diabetes_probability',
                'heart_risk', 'heart_probability', 'obesity_risk', 'obesity_probability',
                'created_at'
            ])



def append_user_to_csv(username, email, created_date, last_login=None):
    """Append a registered user to the CSV file."""
    if last_login is None:
        last_login = created_date
    with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, email, created_date, last_login])


def update_user_last_login_csv(username, last_login):
    """Update the last_login value for a user in the CSV file."""
    csv_file = USERS_CSV
    if not os.path.exists(csv_file):
        return

    rows = []
    updated = False
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('username') == username:
                row['last_login'] = last_login
                updated = True
            rows.append(row)

    if updated:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'password', 'email', 'created_date', 'last_login'])
            writer.writeheader()
            writer.writerows(rows)


def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email):
    """Register a new user using CSV storage"""
    # Check if user already exists
    if check_user_exists(username):
        return False, "Username already exists!"

    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Store user in CSV
    with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, hash_password(password), email, created_date, created_date])

    return True, "Registration successful!"

def check_user_exists(username):
    """Check if a user already exists in the CSV"""
    if not os.path.exists(r'C:\Users\WINDOWS11\OneDrive\Desktop\K Project 02\K Project 02\ecohealth_users_new.csv'):
        return False

    with open(r'C:\Users\WINDOWS11\OneDrive\Desktop\K Project 02\K Project 02\ecohealth_users_new.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('username') == username:
                return True
    return False

def login_user(username, password):
    """Authenticate user login using CSV"""
    if not os.path.exists(r'C:\Users\WINDOWS11\OneDrive\Desktop\K Project 02\K Project 02\ecohealth_users_new.csv'):
        return False, "User database not found!"

    with open(r'C:\Users\WINDOWS11\OneDrive\Desktop\K Project 02\K Project 02\ecohealth_users_new.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('username') == username and row.get('password') == hash_password(password):
                # Update last login
                last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                update_user_last_login_csv(username, last_login)

                # Return user data as tuple to maintain compatibility
                user_data = (row.get('username'), row.get('password'), row.get('email'),
                           row.get('created_date'), row.get('last_login'))
                return True, user_data

    return False, "Invalid username or password!"

def generate_unique_id():
    """Generate a unique ID for health data records"""
    return str(int(time.time() * 1000000))

def save_user_health_data(username, health_data):
    """Save user's health assessment data to CSV"""
    # Generate unique ID
    record_id = generate_unique_id()

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Health Assessment data of user input
    # Prepare data row
    data_row = [
        record_id,
        username,
        health_data['date'],
        health_data['time'],
        health_data['age'],
        health_data['gender'],
        health_data['height'],
        health_data['weight'],
        health_data['bmi'],
        health_data['blood_sugar'],
        health_data['systolic_bp'],
        health_data['diastolic_bp'],
        health_data['smoking'],
        health_data['exercise'],
        health_data['sleep_hours'],
        health_data['health_score'],
        health_data['diabetes_risk'],
        health_data['diabetes_probability'],
        health_data['heart_risk'],
        health_data['heart_probability'],
        health_data['obesity_risk'],
        health_data['obesity_probability'],
        created_at
    ]

    # Append to health data CSV
    with open(HEALTH_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

    return True

def get_user_health_history(username):
    """Get user's health assessment history from CSV"""
    if not os.path.exists(HEALTH_CSV):
        return []
    
    # check history of user previous data
    health_history = []
    with open(HEALTH_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('username') == username:
                # Convert to tuple format to maintain compatibility with existing code
                health_history.append((
                    int(row.get('id', 0)),
                    row.get('username'),
                    row.get('date'),
                    row.get('time'),
                    int(row.get('age', 0)),
                    row.get('gender'),
                    float(row.get('height', 0)),
                    float(row.get('weight', 0)),
                    float(row.get('bmi', 0)),
                    float(row.get('blood_sugar', 0)),
                    int(row.get('systolic_bp', 0)),
                    int(row.get('diastolic_bp', 0)),
                    row.get('smoking'),
                    row.get('exercise'),
                    float(row.get('sleep_hours', 0)),
                    float(row.get('health_score', 0)),
                    row.get('diabetes_risk'),
                    float(row.get('diabetes_probability', 0)),
                    row.get('heart_risk'),
                    float(row.get('heart_probability', 0)),
                    row.get('obesity_risk'),
                    float(row.get('obesity_probability', 0)),
                    row.get('created_at')
                ))

    # Sort by created_at descending (most recent first)
    health_history.sort(key=lambda x: x[-1], reverse=True)
    return health_history

# Initialize database
init_db()



# Utility functions

def calculate_health_score(age, bmi, blood_sugar, systolic_bp, diastolic_bp, smoking, exercise, sleep_hours):
    """Calculate overall health risk score (higher score = higher risk)"""
    risk_score = 0

    # Age factor
    if age > 60:
        risk_score += 15
    elif age > 40:
        risk_score += 10
    elif age > 25:
        risk_score += 5

    # BMI factor
    if bmi > 30:
        risk_score += 20
    elif bmi > 25:
        risk_score += 10
    elif bmi < 18.5:
        risk_score += 5

    # Blood sugar factor
    if blood_sugar > 140:
        risk_score += 15
    elif blood_sugar > 100:
        risk_score += 10

    # Blood pressure factor
    if systolic_bp > 140 or diastolic_bp > 90:
        risk_score += 15
    elif systolic_bp > 120 or diastolic_bp > 80:
        risk_score += 10

    # Smoking factor
    if smoking == "Yes":
        risk_score += 20

    # Exercise factor
    if exercise == "Never":
        risk_score += 15
    elif exercise == "Rarely":
        risk_score += 10
    elif exercise == "Regularly":
        risk_score -= 10

    # Sleep factor
    if sleep_hours < 6:
        risk_score += 15
    elif sleep_hours < 8:
        risk_score += 5
    elif sleep_hours >= 8:
        risk_score -= 5

    return max(0, min(100, risk_score))


def safe_float(value, default=0.0):
    """Safely convert a value to float (falls back to default on failure)."""
    if value is None:
        return default

    try:
        # Remove common percent formatting
        if isinstance(value, str):
            value = value.strip().replace('%', '').strip()
        return float(value)
    except (TypeError, ValueError):
        return default


def generate_diet_plan(diabetes_risk_label, diabetes_prob,
                       obesity_risk_label, obesity_prob,
                       heart_risk_label, heart_prob):
    """Generate a diet plan based on risk labels + probabilities.

    The diet plan focuses on the most urgent risk (highest probability), but also
    combines guidance if multiple risks are high.
    """
    diet_plan = {
        "diabetes_focus": {
            "Monday": {"breakfast": "Oatmeal with chia seeds and cinnamon", "lunch": "Grilled chicken salad with olive oil dressing", "dinner": "Grilled salmon with sweet potato"},
            "Tuesday": {"breakfast": "Greek yogurt with flax seeds", "lunch": "Lentil soup with mixed vegetables", "dinner": "Stir-fried vegetables with tofu"},
            "Wednesday": {"breakfast": "Vegetable omelette with spinach and tomatoes", "lunch": "Baked fish with quinoa and broccoli", "dinner": "Baked chicken with brown rice"},
            "Thursday": {"breakfast": "Quinoa porridge with berries", "lunch": "Turkey lettuce wraps with avocado", "dinner": "Vegetable curry with chickpeas"},
            "Friday": {"breakfast": "Oatmeal with almonds and blueberries", "lunch": "Grilled chicken with mixed greens", "dinner": "Grilled salmon with asparagus"},
            "Saturday": {"breakfast": "Greek yogurt with walnuts", "lunch": "Lentil and spinach soup", "dinner": "Stir-fried tofu with mixed vegetables"},
            "Sunday": {"breakfast": "Scrambled eggs with bell peppers", "lunch": "Baked fish with roasted zucchini", "dinner": "Baked chicken with quinoa"},
            "healing_waters": [
                "Methi (fenugreek) water - 1 glass daily",
                "Cucumber water - 2 glasses daily",
                "Bitter gourd juice - 1 glass alternate days",
                "Amla water - 1 glass daily"
            ],
            "superfoods": [
                "Cinnamon - 1/2 tsp daily",
                "Turmeric - 1/2 tsp in meals",
                "Ginger - fresh in teas",
                "Fenugreek seeds - 1 tsp soaked",
                "Bitter melon - 100g daily",
                "Amla (Indian gooseberry) - 2-3 daily"
            ]
        },
        "obesity_focus": {
            "Monday": {"breakfast": "Green smoothie with kale and spinach", "lunch": "Mixed green salad with grilled chicken", "dinner": "Baked fish with steamed vegetables"},
            "Tuesday": {"breakfast": "Chia pudding with almond milk", "lunch": "Vegetable stir-fry with tofu", "dinner": "Grilled chicken with salad"},
            "Wednesday": {"breakfast": "Avocado toast on whole grain bread", "lunch": "Quinoa bowl with roasted vegetables", "dinner": "Vegetable curry with lentils"},
            "Thursday": {"breakfast": "Fruit salad with nuts", "lunch": "Turkey and vegetable soup", "dinner": "Stir-fried vegetables with lean protein"},
            "Friday": {"breakfast": "Green smoothie with celery and apple", "lunch": "Mixed green salad with boiled eggs", "dinner": "Baked fish with broccoli"},
            "Saturday": {"breakfast": "Oatmeal with berries", "lunch": "Vegetable stir-fry with chickpeas", "dinner": "Grilled chicken with roasted carrots"},
            "Sunday": {"breakfast": "Avocado toast with tomatoes", "lunch": "Quinoa bowl with black beans", "dinner": "Vegetable curry with cauliflower base"},
            "healing_waters": [
                "Lemon water - 2 glasses daily",
                "Cucumber water - 3 glasses daily",
                "Ginger water - 1 glass daily",
                "Apple cider vinegar water - 1 glass daily"
            ],
            "superfoods": [
                "Green tea - 3 cups daily",
                "Apple cider vinegar - 1 tbsp daily",
                "Cayenne pepper - in meals",
                "Ginger - fresh daily",
                "Turmeric - 1/2 tsp daily",
                "Cinnamon - 1/2 tsp daily"
            ]
        },
        "heart_focus": {
            "Monday": {"breakfast": "Oatmeal with walnuts and berries", "lunch": "Salmon salad with olive oil", "dinner": "Baked salmon with vegetables"},
            "Tuesday": {"breakfast": "Smoothie with spinach and banana", "lunch": "Grilled chicken with quinoa", "dinner": "Grilled fish with brown rice"},
            "Wednesday": {"breakfast": "Whole grain toast with avocado", "lunch": "Vegetable soup with beans", "dinner": "Chicken stir-fry with broccoli"},
            "Thursday": {"breakfast": "Greek yogurt with flax seeds", "lunch": "Turkey burger with sweet potato", "dinner": "Lentil stew with vegetables"},
            "Friday": {"breakfast": "Oatmeal with almonds and strawberries", "lunch": "Mackerel salad with olive oil", "dinner": "Baked salmon with spinach"},
            "Saturday": {"breakfast": "Smoothie with kale and apple", "lunch": "Grilled chicken with brown rice", "dinner": "Grilled fish with asparagus"},
            "Sunday": {"breakfast": "Whole grain toast with almond butter", "lunch": "Vegetable soup with lentils", "dinner": "Chicken stir-fry with bell peppers"},
            "healing_waters": [
                "Beetroot water - 1 glass daily",
                "Pomegranate juice - 1 glass daily",
                "Garlic water - 1 glass alternate days",
                "Turmeric water - 1 glass daily"
            ],
            "superfoods": [
                "Omega-3 fish (salmon, mackerel) - 2-3 times weekly",
                "Dark chocolate - 30g daily",
                "Berries - 1 cup daily",
                "Nuts (walnuts, almonds) - handful daily",
                "Olive oil - for cooking",
                "Avocado - 1/2 daily"
            ]
        }
    }

    # Normalize input to allow both numeric and string probabilities
    diabetes_prob = safe_float(diabetes_prob)
    obesity_prob = safe_float(obesity_prob)
    heart_prob = safe_float(heart_prob)

    # Determine main risk based on probability (primary) but prefer a 'High' label if present
    risks = [
        ("diabetes", diabetes_prob, diabetes_risk_label),
        ("obesity", obesity_prob, obesity_risk_label),
        ("heart", heart_prob, heart_risk_label)
    ]

    # Prefer highest probability unless a 'High' label exists
    high_risks = [r for r in risks if str(r[2]).lower() == "high"]
    if high_risks:
        primary = max(high_risks, key=lambda r: r[1])
    else:
        primary = max(risks, key=lambda r: r[1])

    primary_disease = primary[0]

    if primary_disease == "diabetes":
        return diet_plan["diabetes_focus"]
    elif primary_disease == "obesity":
        return diet_plan["obesity_focus"]
    else:
        return diet_plan["heart_focus"]

def create_pdf_report(user_data, predictions, diet_plan):
    """Create PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("EcoHealth AI - Health Assessment Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Date and User Info
    info_text = f"""
    <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    <b>Patient Name:</b> {user_data['username']}<br/>
    <b>Assessment Date:</b> {user_data['date']}<br/>
    <b>Assessment Time:</b> {user_data['time']}
    """
    story.append(Paragraph(info_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # # Health Metrics
    # story.append(Paragraph("<b>Health Metrics</b>", styles['Heading2']))
    # metrics_data = [
    #     ['Metric', 'Value'],
    #     ['Age', f"{user_data['age']} years"],
    #     ['Gender', user_data['gender']],
    #     ['Height', f"{user_data['height']} cm"],
    #     ['Weight', f"{user_data['weight']} kg"],
    #     ['BMI', f"{user_data['bmi']:.1f}"],
    #     ['Blood Sugar', f"{user_data['blood_sugar']} mg/dL"],
    #     ['Blood Pressure', f"{user_data['systolic_bp']}/{user_data['diastolic_bp']} mmHg"],
    #     ['Smoking', user_data['smoking']],
    #     ['Exercise', user_data['exercise']],
    #     ['Sleep Hours', f"{user_data['sleep_hours']} hours"],
    #     ['Health Risk Score', f"{user_data['health_score']}/100 (Higher = Higher Risk)"]
    # ]

    # metrics_table = Table(metrics_data)
    # metrics_table.setStyle(TableStyle([
    #     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #     ('FONTSIZE', (0, 0), (-1, 0), 14),
    #     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #     ('GRID', (0, 0), (-1, -1), 1, colors.black)
    # ]))
    # story.append(metrics_table)
    # story.append(Spacer(1, 12))

    # Risk Assessment
    story.append(Paragraph("<b>Risk Assessment</b>", styles['Heading2']))
    risk_data = [
        ['Disease', 'Risk Level', 'Probability'],
        ['Diabetes', predictions['diabetes']['risk'], f"{predictions['diabetes']['probability']:.1f}%"],
        ['Heart Disease', predictions['heart']['risk'], f"{predictions['heart']['probability']:.1f}%"],
        ['Obesity', predictions['obesity']['risk'], f"{predictions['obesity']['probability']:.1f}%"]
    ]

    risk_table = Table(risk_data)
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 12))

    # Diet Plan
    story.append(Paragraph("<b>Personalized Weekly Diet Plan</b>", styles['Heading2']))

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        story.append(Paragraph(f"<b>{day}</b>", styles['Heading3']))
        day_plan = diet_plan.get(day, {})
        if day_plan:
            story.append(Paragraph(f"• Breakfast: {day_plan.get('breakfast', '')}", styles['Normal']))
            story.append(Paragraph(f"• Lunch:     {day_plan.get('lunch', '')}", styles['Normal']))
            story.append(Paragraph(f"• Dinner:    {day_plan.get('dinner', '')}", styles['Normal']))
            story.append(Spacer(1, 6))

    # Healing Waters
    story.append(Paragraph("<b>Healing Waters:</b>", styles['Heading3']))
    for item in diet_plan['healing_waters']:
        story.append(Paragraph(f"• {item}", styles['Normal']))

    # Superfoods
    story.append(Paragraph("<b>Recommended Superfoods:</b>", styles['Heading3']))
    for item in diet_plan['superfoods']:
        story.append(Paragraph(f"• {item}", styles['Normal']))

    story.append(Spacer(1, 12))

    # Disclaimer
    disclaimer = """
    <b>Medical Disclaimer:</b><br/>
    This report is for informational purposes only and does not constitute medical advice.
    Please consult with qualified healthcare professionals for proper diagnosis and treatment.
    Regular medical check-ups are essential for maintaining good health.
    """
    story.append(Paragraph(disclaimer, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Main app
def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'

    # Login/Register Page
    if not st.session_state.logged_in:
        show_auth_page()
    else:
        show_main_app()

def show_auth_page():
    """Show login/register page"""
    st.markdown('''
        <div class="main-header-clean">
            <h1>🏥 Welcome to EcoHealth AI</h1>
            <p><strong>Your Personal Health Assessment Companion</strong></p>
        </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with tab1:
            st.subheader("Login to Your Account")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.form_submit_button("🚀 Login", type="primary"):
                    if username and password:
                        success, result = login_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
                    else:
                        st.error("Please fill in all fields")

        with tab2:
            st.subheader("Create New Account")

            with st.form("register_form"):
                new_username = st.text_input("Username")
                new_email = st.text_input("Email (optional)")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.form_submit_button("📝 Register", type="primary"):
                    if new_username and new_password:
                        if new_password == confirm_password:
                            success, message = register_user(new_username, new_password, new_email)
                            if success:
                                st.success("✅ Registration successful! Please login.")
                            else:
                                st.error(f"❌ {message}")
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please fill in username and password")

def show_main_app():
    """Show main application after login"""
    # Sidebar navigation
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.title(f"🏥 EcoHealth AI")
    st.sidebar.markdown(f"**Welcome, {st.session_state.username}!**")

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "📝 Health Assessment", "📊 Health Analytics",
         "🥗 Diet Plan", "📋 Reports", "📈 Health History"]
    )

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Main content
    if page == "🏠 Dashboard":
        show_dashboard()

    elif page == "📝 Health Assessment":
        show_health_assessment()

    elif page == "📊 Health Analytics":
        show_health_analytics()

    elif page == "🥗 Diet Plan":
        show_diet_plan()

    elif page == "📋 Reports":
        show_reports()

    elif page == "📈 Health History":
        show_health_history()

def show_dashboard():
    """Dashboard page"""
    st.markdown(f'''
        <div class="main-header-clean">
            <h1>🏠 Health Dashboard</h1>
            <p><strong>Welcome back, {st.session_state.username}!</strong></p>
            <p><em>Your personalized health overview</em></p>
        </div>
    ''', unsafe_allow_html=True)

    # Get user's latest health data
    health_history = get_user_health_history(st.session_state.username)

    if health_history:
        # Convert to DataFrame so we can address values by name (reduces index mismatch risk)
        df = pd.DataFrame(health_history, columns=[
            'id', 'username', 'date', 'time', 'age', 'gender', 'height', 'weight', 'bmi',
            'blood_sugar', 'systolic_bp', 'diastolic_bp', 'smoking', 'exercise', 'sleep_hours',
            'health_score', 'diabetes_risk', 'diabetes_probability', 'heart_risk',
            'heart_probability', 'obesity_risk', 'obesity_probability', 'created_at'
        ])

        latest = df.iloc[0]

        # Risk Overview
        st.subheader("🎯 Current Risk Assessment")

        col1, col2, col3 = st.columns(3)

        with col1:
            diabetes_risk = latest['diabetes_risk']
            diabetes_prob = safe_float(latest['diabetes_probability'])
            risk_class = "risk-high" if diabetes_risk == "High" else "risk-medium" if diabetes_risk == "Medium" else "risk-low"
            st.markdown(f"""
            <div class="metric-card {risk_class}">
                <h4>🩸 Diabetes Risk</h4>
                <h2>{diabetes_risk}</h2>
                <p>Probability: {diabetes_prob:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            heart_risk = latest['heart_risk']
            heart_prob = safe_float(latest['heart_probability'])
            risk_class = "risk-high" if heart_risk == "High" else "risk-medium" if heart_risk == "Medium" else "risk-low"
            st.markdown(f"""
            <div class="metric-card {risk_class}">
                <h4>❤️ Heart Disease Risk</h4>
                <h2>{heart_risk}</h2>
                <p>Probability: {heart_prob:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            obesity_risk = latest['obesity_risk']
            obesity_prob = safe_float(latest['obesity_probability'])
            risk_class = "risk-high" if obesity_risk == "High" else "risk-medium" if obesity_risk == "Medium" else "risk-low"
            st.markdown(f"""
            <div class="metric-card {risk_class}">
                <h4>⚖️ Obesity Risk</h4>
                <h2>{obesity_risk}</h2>
                <p>Probability: {obesity_prob:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

        # Emergency Alert if any high risk
        if diabetes_risk == "High" or heart_risk == "High" or obesity_risk == "High":
            st.markdown("""
            <div class="emergency-alert">
                <h2>🚨 EMERGENCY ALERT</h2>
                <p><strong>High Risk Detected!</strong></p>
                <p>Please consult a doctor immediately for proper medical evaluation and treatment.</p>
                <p>Call emergency services if you experience any symptoms.</p>
            </div>
            """, unsafe_allow_html=True)

        # Health Score and BMI gauges
        health_score = safe_float(latest['health_score'])
        bmi_value = safe_float(latest['bmi'])

        st.subheader("💯 Overall Health Risk Score & ⚖️ BMI")

        # Debug: show raw probability values from DB (for verification)
        with st.expander("🔍 Raw risk probability values (debug)", expanded=False):
            st.write({
                'diabetes_probability_raw': latest['diabetes_probability'],
                'heart_probability_raw': latest['heart_probability'],
                'obesity_probability_raw': latest['obesity_probability'],
                'diabetes_probability_safe': diabetes_prob,
                'heart_probability_safe': heart_prob,
                'obesity_probability_safe': obesity_prob
            })

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig_score = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Health Risk Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "green"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ]
                }
            ))
            st.plotly_chart(fig_score, use_container_width=True)

        with col_g2:
            fig_bmi = go.Figure(go.Indicator(
                mode="gauge+number",
                value=bmi_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "BMI"},
                gauge={
                    'axis': {'range': [10, 45]},
                    'bar': {'color': "darkorange"},
                    'steps': [
                        {'range': [0, 18.5], 'color': "lightblue"},
                        {'range': [18.5, 24.9], 'color': "lightgreen"},
                        {'range': [25, 29.9], 'color': "gold"},
                        {'range': [30, 45], 'color': "tomato"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': bmi_value
                    }
                }
            ))
            st.plotly_chart(fig_bmi, use_container_width=True)

        # Recent Health Trends
        st.subheader("📈 Health Trends")

        if len(health_history) > 1:
            # Create trend data
            dates = [entry[2] for entry in health_history[:7]]  # Last 7 entries
            diabetes_probs = [entry[16] for entry in health_history[:7]]
            heart_probs = [entry[18] for entry in health_history[:7]]
            obesity_probs = [entry[20] for entry in health_history[:7]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=dates, y=diabetes_probs, name='Diabetes Risk'))
            fig.add_trace(go.Bar(x=dates, y=heart_probs, name='Heart Risk'))
            fig.add_trace(go.Bar(x=dates, y=obesity_probs, name='Obesity Risk'))

            fig.update_layout(
                title="Risk Trends Over Time",
                xaxis_title="Date",
                yaxis_title="Risk Probability (%)",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Complete more assessments to see health trends!")

    else:
        st.info("👋 Welcome! Please complete your first health assessment to see your dashboard.")

def show_health_assessment():
    """Health assessment page"""
    st.markdown('''
        <div class="main-header-clean">
            <h1>📝 Health Assessment</h1>
            <p><strong>Complete Health Evaluation</strong></p>
        </div>
    ''', unsafe_allow_html=True)

    # Use session state to manage thank-you page rendering (so buttons can be used without form restrictions)
    if 'show_thank_you' not in st.session_state:
        st.session_state.show_thank_you = False

    st.subheader("📋 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Username", value=st.session_state.username, disabled=True)
        assessment_date = st.date_input("Assessment Date", value=date.today())
        assessment_time = st.time_input("Assessment Time", value=datetime.now().time())
        age = st.number_input("Age", value=30, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    with col2:
        height = st.number_input("Height (cm)", 140.0, 220.0, 170.0)
        weight = st.number_input("Weight (kg)", 40.0, 150.0, 70.0)
        blood_sugar = st.number_input("Blood Sugar (mg/dL)", 70.0, 300.0, 100.0)
        systolic_bp = st.number_input("Systolic BP", value=120, step=1)
        diastolic_bp = st.number_input("Diastolic BP", value=80, step=1)

    st.subheader("🏃‍♂️ Lifestyle Information")

    col3, col4 = st.columns(2)

    with col3:
        smoking = st.selectbox("Do you smoke?", ["No", "Yes", "Occasionally"])
        exercise = st.selectbox("Exercise frequency?", ["Never", "Rarely", "Sometimes", "Regularly", "Daily"])
        sleep_hours = st.number_input("Average sleep hours per night", value=8.0, step=0.5)

    # Calculate BMI
    bmi = weight / ((height/100) ** 2)

    # Calculate health risk score
    health_score = calculate_health_score(
        age, bmi, blood_sugar, systolic_bp, diastolic_bp,
        smoking, exercise, sleep_hours
    )

    st.info(f"📊 Calculated BMI: {bmi:.1f}")
    st.info(f"� Health Risk Score: {health_score}/100 (Higher score = Higher risk)")

    if st.button("🔍 Generate Health Report", type="primary"):
        with st.spinner("Analyzing your health data..."):
            # Encode categorical variables
            gender_num = 1 if gender == "Male" else 0
            smoking_num = 1 if smoking == "Yes" else 0
            
            # Default values for missing UI features to preserve original UI layout
            cholesterol = 180.0
            fam_hist_num = 0
            stress_level = 5.0
            
            # Derive exercise hours from frequency
            exercise_map = {"Never": 0.0, "Rarely": 1.0, "Sometimes": 2.0, "Regularly": 4.0, "Daily": 7.0}
            exercise_hours = exercise_map.get(exercise, 2.0)

            import os
            # 1. Diabetes Prediction
            try:
                diabetes_model = joblib.load(r'C:\Desktop\K Project main\K Project 01\K Project 02\Diabetes_Risk.pkl')
                diab_features = pd.DataFrame([[age, gender_num, height, weight, bmi, blood_sugar, systolic_bp, diastolic_bp, cholesterol, smoking_num, exercise_hours, fam_hist_num, sleep_hours, stress_level]], 
                                            columns=['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI', 'Blood_Sugar_mg_dL', 'Systolic_BP', 'Diastolic_BP', 'Cholesterol_mg_dL', 'Smoking', 'Exercise_Hours_per_Week', 'Family_History', 'Sleep_Hours', 'Stress_Level_1_to_10'])
                diabetes_risk_label = diabetes_model.predict(diab_features)[0]
                diabetes_prob_arr = diabetes_model.predict_proba(diab_features)[0]
                diabetes_prob = float(diabetes_prob_arr[0] * 100 + diabetes_prob_arr[2] * 50)
            except Exception as e:
                st.error(f"Error executing Diabetes Model: {e}")
                diabetes_risk_label = 'Low'
                diabetes_prob = 0.0

            # 2. Heart Disease Prediction
            try:
                heart_model = joblib.load(r'C:\Desktop\K Project main\K Project 01\K Project 02\Heart_Disease_Risk.pkl')
                heart_features = pd.DataFrame([[age, gender_num, cholesterol, smoking_num, exercise_hours, fam_hist_num, sleep_hours, stress_level]], 
                                            columns=['Age', 'Gender', 'Cholesterol_mg_dL', 'Smoking', 'Exercise_Hours_per_Week', 'Family_History', 'Sleep_Hours', 'Stress_Level_1_to_10'])
                heart_risk_label = heart_model.predict(heart_features)[0]
                heart_prob_arr = heart_model.predict_proba(heart_features)[0]
                heart_prob = float(heart_prob_arr[0] * 100 + heart_prob_arr[2] * 50)
            except Exception as e:
                st.error(f"Error executing Heart Disease Model: {e}")
                heart_risk_label = 'Low'
                heart_prob = 0.0

            # 3. Obesity Prediction
            try:
                obesity_model = joblib.load(r'C:\Desktop\K Project main\K Project 01\K Project 02\Obesity_model.pkl')
                obesity_features = pd.DataFrame([[age, gender_num, height, weight, bmi, blood_sugar, systolic_bp, diastolic_bp, cholesterol, smoking_num, exercise_hours, fam_hist_num, sleep_hours, stress_level]], 
                                            columns=['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI', 'Blood_Sugar_mg_dL', 'Systolic_BP', 'Diastolic_BP', 'Cholesterol_mg_dL', 'Smoking', 'Exercise_Hours_per_Week', 'Family_History', 'Sleep_Hours', 'Stress_Level_1_to_10'])
                obesity_risk_label = obesity_model.predict(obesity_features)[0]
                obesity_prob_arr = obesity_model.predict_proba(obesity_features)[0]
                obesity_prob = float(obesity_prob_arr[0] * 100 + obesity_prob_arr[2] * 50)
            except Exception as e:
                st.error(f"Error executing Obesity Model: {e}")
                obesity_risk_label = 'Low'
                obesity_prob = 0.0

            predictions = {
                'diabetes': {
                    'risk': diabetes_risk_label,
                    'probability': diabetes_prob
                },
                'heart': {
                    'risk': heart_risk_label,
                    'probability': heart_prob
                },
                'obesity': {
                    'risk': obesity_risk_label,
                    'probability': obesity_prob
                }
            }

            # Adjust health score based on high risk predictions
            if predictions['diabetes']['risk'] == 'High':
                health_score = min(100, health_score + 15)
            if predictions['heart']['risk'] == 'High':
                health_score = min(100, health_score + 15)
            if predictions['obesity']['risk'] == 'High':
                health_score = min(100, health_score + 15)

            # Save to database
            health_data = {
                'username': username,
                'date': assessment_date.strftime('%Y-%m-%d'),
                'time': assessment_time.strftime('%H:%M:%S'),
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'bmi': bmi,
                'blood_sugar': blood_sugar,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'smoking': smoking,
                'exercise': exercise,
                'sleep_hours': sleep_hours,
                'health_score': health_score,
                'diabetes_risk': predictions['diabetes']['risk'],
                'diabetes_probability': predictions['diabetes']['probability'],
                'heart_risk': predictions['heart']['risk'],
                'heart_probability': predictions['heart']['probability'],
                'obesity_risk': predictions['obesity']['risk'],
                'obesity_probability': predictions['obesity']['probability']
            }

            save_user_health_data(username, health_data)

            # Store in session state for thank you page
            st.session_state.last_assessment = {
                'health_data': health_data,
                'predictions': predictions
            }

            # Trigger thank-you page after form is submitted
            st.session_state.show_thank_you = True

    # If the assessment is completed, show thank-you page
    if st.session_state.show_thank_you and 'last_assessment' in st.session_state:
        show_thank_you_page(
            st.session_state.last_assessment['health_data'],
            st.session_state.last_assessment['predictions']
        )

def show_thank_you_page(health_data, predictions):
    """Show beautiful thank you page with animations"""
    st.markdown("""
    <div class="thank-you-card">
        <h1>🎉 Thank You!</h1>
        <h2>Your Health Assessment is Complete</h2>
        <p>Your health data has been securely saved and analyzed.</p>
        <p>Check your dashboard for detailed insights and recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    # Show summary
    st.subheader("📋 Assessment Summary")

    # Calculate overall risk percentage (average of all disease probabilities)
    overall_risk_percentage = (predictions['diabetes']['probability'] +
                              predictions['heart']['probability'] +
                              predictions['obesity']['probability']) / 3

    # Present the 3 disease risk cards
    col1, col2, col3 = st.columns(3)

    # Diabetes Risk Card
    with col1:
        diabetes_color = "#28a745" if predictions['diabetes']['risk'] == 'Low' else "#ffc107" if predictions['diabetes']['risk'] == 'Medium' else "#dc3545"
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {diabetes_color};">
            <h4 style="color: {diabetes_color};">🩸 Diabetes Risk</h4>
            <h2 style="color: {diabetes_color};">{predictions['diabetes']['risk']}</h2>
            <p><strong>Probability:</strong> {safe_float(predictions['diabetes']['probability']):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Heart Risk Card
    with col2:
        heart_color = "#28a745" if predictions['heart']['risk'] == 'Low' else "#ffc107" if predictions['heart']['risk'] == 'Medium' else "#dc3545"
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {heart_color};">
            <h4 style="color: {heart_color};">❤️ Heart Disease</h4>
            <h2 style="color: {heart_color};">{predictions['heart']['risk']}</h2>
            <p><strong>Probability:</strong> {safe_float(predictions['heart']['probability']):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Obesity Risk Card
    with col3:
        obesity_color = "#28a745" if predictions['obesity']['risk'] == 'Low' else "#ffc107" if predictions['obesity']['risk'] == 'Medium' else "#dc3545"
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {obesity_color};">
            <h4 style="color: {obesity_color};">⚖️ Obesity Risk</h4>
            <h2 style="color: {obesity_color};">{predictions['obesity']['risk']}</h2>
            <p><strong>Probability:</strong> {safe_float(predictions['obesity']['probability']):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Emergency alert if needed
    if (predictions['diabetes']['risk'] == 'High' or
        predictions['heart']['risk'] == 'High' or
        predictions['obesity']['risk'] == 'High'):
        st.markdown("""
        <div class="emergency-alert">
            <h3>🚨 Important Notice</h3>
            <p>Your assessment indicates high risk in one or more areas.</p>
            <p><strong>Please consult a healthcare professional immediately.</strong></p>
        </div>
        """, unsafe_allow_html=True)



def show_health_analytics():
    """Health analytics page"""
    st.markdown('''
        <div class="main-header-clean">
            <h1>📊 Health Analytics</h1>
            <p><strong>Your Health Trends & Insights</strong></p>
        </div>
    ''', unsafe_allow_html=True)

    health_history = get_user_health_history(st.session_state.username)

    if not health_history:
        st.info("No health data available. Please complete a health assessment first.")
        return

    # Convert to DataFrame for analysis
    df = pd.DataFrame(health_history, columns=[
        'id', 'username', 'date', 'time', 'age', 'gender', 'height', 'weight', 'bmi',
        'blood_sugar', 'systolic_bp', 'diastolic_bp', 'smoking', 'exercise', 'sleep_hours',
        'health_score', 'diabetes_risk', 'diabetes_probability', 'heart_risk',
        'heart_probability', 'obesity_risk', 'obesity_probability', 'created_at'
    ])

    latest = df.iloc[0]

    # 1. Pie chart for the 3 diseases (latest)
    st.subheader("🥧 Current Disease Risk Distribution")
    pie_data = pd.DataFrame({
        'Disease': ['Diabetes', 'Heart Disease', 'Obesity'],
        'Probability': [
            safe_float(latest['diabetes_probability']), 
            safe_float(latest['heart_probability']), 
            safe_float(latest['obesity_probability'])
        ]
    })
    
    # Filter out 0 probabilities to ensure a clean chart if they happen to be 0
    pie_data = pie_data[pie_data['Probability'] > 0]
    
    if not pie_data.empty:
        fig_pie = px.pie(pie_data, values='Probability', names='Disease', title='Current Risk Distribution')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Risk probabilities are zero.")

    # 2. Bar chart comparing current vs previous assessment
    st.subheader("📊 Current vs Previous Assessment")
    if len(df) > 1:
        prev = df.iloc[1]
        comp_df = pd.DataFrame({
            'Disease': ['Diabetes', 'Diabetes', 'Heart Disease', 'Heart Disease', 'Obesity', 'Obesity'],
            'Assessment': ['Current', 'Previous', 'Current', 'Previous', 'Current', 'Previous'],
            'Probability': [
                safe_float(latest['diabetes_probability']), safe_float(prev['diabetes_probability']),
                safe_float(latest['heart_probability']), safe_float(prev['heart_probability']),
                safe_float(latest['obesity_probability']), safe_float(prev['obesity_probability'])
            ]
        })
        fig_comp = px.bar(
            comp_df, 
            x='Disease', 
            y='Probability', 
            color='Assessment', 
            barmode='group', 
            title="Current vs Previous Risk Comparison",
            color_discrete_map={'Current': 'royalblue', 'Previous': 'lightslategray'}
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.info("Complete another assessment to compare with previous data!")

def show_diet_plan():
    """Diet plan page"""
    st.markdown('''
        <div class="main-header-clean">
            <h1>🥗 Personalized Diet Plan</h1>
            <p><em>Your tailored weekly nutrition schedule</em></p>
        </div>
    ''', unsafe_allow_html=True)

    health_history = get_user_health_history(st.session_state.username)

    if not health_history:
        st.info("Please complete a health assessment to get personalized diet recommendations.")
        return

    latest_data = health_history[0]

    # Extract labels + probabilities
    diabetes_risk_label = latest_data[16]
    diabetes_prob = latest_data[17]
    heart_risk_label = latest_data[18]
    heart_prob = latest_data[19]
    obesity_risk_label = latest_data[20]
    obesity_prob = latest_data[21]

    diet_plan = generate_diet_plan(
        diabetes_risk_label, diabetes_prob,
        obesity_risk_label, obesity_prob,
        heart_risk_label, heart_prob
    )

    # Determine primary focus (prefer 'High' label, else highest probability)
    risks = [
        ("diabetes", safe_float(diabetes_prob), diabetes_risk_label),
        ("heart", safe_float(heart_prob), heart_risk_label),
        ("obesity", safe_float(obesity_prob), obesity_risk_label)
    ]
    high_risks = [r for r in risks if str(r[2]).lower() == "high"]
    if high_risks:
        primary = max(high_risks, key=lambda r: r[1])
    else:
        primary = max(risks, key=lambda r: r[1])

    primary_risk = primary[0]

    # Explicitly show the chosen focus to the user dynamically based on their health risk
    display_focus = primary_risk.capitalize() if primary_risk != "heart" else "Heart Disease"

    st.info(f"**Based on your recent assessment, this tailored diet plan is optimized specifically for maintaining a lower {display_focus} Risk.**")

    st.subheader(f"🎯 Diet Plan Focus: {display_focus} Management")

    st.subheader("📅 Weekly Meal Plan")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        with st.expander(f"🍽️ {day}'s Menu", expanded=(day == "Monday")):
            day_plan = diet_plan.get(day, {})
            if day_plan:
                st.markdown(f"**🌅 Breakfast:** {day_plan.get('breakfast', '')}")
                st.markdown(f"**🌞 Lunch:** {day_plan.get('lunch', '')}")
                st.markdown(f"**🌙 Dinner:** {day_plan.get('dinner', '')}")

    # Healing Waters
    st.markdown('<div class="diet-card">', unsafe_allow_html=True)
    st.subheader("💧 Healing Waters")
    for item in diet_plan['healing_waters']:
        st.markdown(f"• {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Superfoods
    st.markdown('<div class="diet-card">', unsafe_allow_html=True)
    st.subheader("🌟 Recommended Superfoods")
    for item in diet_plan['superfoods']:
        st.markdown(f"• {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("💡 **Tip:** Follow this diet plan for 4-6 weeks and track your progress in the dashboard!")

def show_reports():
    """Reports page"""
    st.markdown('''
        <div class="main-header-clean">
            <h1>📋 Health Reports</h1>
            <p><strong>Generate and Download Your Health Reports</strong></p>
        </div>
    ''', unsafe_allow_html=True)

    health_history = get_user_health_history(st.session_state.username)

    if not health_history:
        st.info("No health data available. Please complete a health assessment first.")
        return

    st.subheader("📄 Generate PDF Report")

    # Select assessment to report
    assessment_dates = [entry[2] + " " + entry[3] for entry in health_history]

    selected_assessment = st.selectbox(
        "Select Assessment Date:",
        assessment_dates
    )

    if selected_assessment:
        # Find the selected assessment data
        selected_index = assessment_dates.index(selected_assessment)
        selected_data = health_history[selected_index]

        # Prepare data for PDF (convert numeric values safely)
        user_data = {
            'username': st.session_state.username,
            'date': selected_data[2],
            'time': selected_data[3],
            'age': selected_data[4],
            'gender': selected_data[5],
            'height': safe_float(selected_data[6]),
            'weight': safe_float(selected_data[7]),
            'bmi': safe_float(selected_data[8]),
            'blood_sugar': safe_float(selected_data[9]),
            'systolic_bp': safe_float(selected_data[10]),
            'diastolic_bp': safe_float(selected_data[11]),
            'smoking': selected_data[12],
            'exercise': selected_data[13],
            'sleep_hours': safe_float(selected_data[14]),
            'health_score': safe_float(selected_data[15])
        }

        predictions = {
            'diabetes': {
                'risk': selected_data[16],
                'probability': safe_float(selected_data[17])
            },
            'heart': {
                'risk': selected_data[18],
                'probability': safe_float(selected_data[19])
            },
            'obesity': {
                'risk': selected_data[20],
                'probability': safe_float(selected_data[21])
            }
        }

        # Generate diet plan (based on risk label + probability)
        diet_plan = generate_diet_plan(
            predictions['diabetes']['risk'],
            predictions['diabetes']['probability'],
            predictions['obesity']['risk'],
            predictions['obesity']['probability'],
            predictions['heart']['risk'],
            predictions['heart']['probability']
        )

        if st.button("📋 Generate PDF Report", type="primary"):
            pdf_buffer = create_pdf_report(user_data, predictions, diet_plan)

            st.success("✅ PDF Report generated successfully!")

            # Download button
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"health_report_{st.session_state.username}_{selected_data[2]}.pdf",
                mime="application/pdf"
            )

def show_health_history():
    """Health history page"""
    st.markdown('''
        <div class="main-header-clean">
            <h1>📈 Health History</h1>
            <p><strong>Review Your Past Health Assessments</strong></p>
        </div>
    ''', unsafe_allow_html=True)

    health_history = get_user_health_history(st.session_state.username)

    if not health_history:
        st.info("No health history available. Please complete health assessments.")
        return

    # Convert to DataFrame for display
    df = pd.DataFrame(health_history, columns=[
        'ID', 'Username', 'Date', 'Time', 'Age', 'Gender', 'Height', 'Weight', 'BMI',
        'Blood Sugar', 'Systolic BP', 'Diastolic BP', 'Smoking', 'Exercise', 'Sleep Hours',
        'Health Risk Score', 'Diabetes Risk', 'Diabetes Prob', 'Heart Risk',
        'Heart Prob', 'Obesity Risk', 'Obesity Prob', 'Created At'
    ])

    # Display history table
    st.subheader("📋 Assessment History")
    st.dataframe(df[['Date', 'Time', 'BMI', 'Blood Sugar', 'Health Risk Score',
                     'Diabetes Risk', 'Heart Risk', 'Obesity Risk']], use_container_width=True)

    # Summary statistics
    st.subheader("📊 Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_bmi = df['BMI'].mean()
        st.metric("Average BMI", f"{avg_bmi:.1f}")

    with col2:
        avg_health_score = df['Health Risk Score'].mean()
        st.metric("Average Health Risk Score", f"{avg_health_score:.1f}")

    with col3:
        total_assessments = len(df)
        st.metric("Total Assessments", total_assessments)

if __name__ == "__main__":
    main()