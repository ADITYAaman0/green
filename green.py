import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
import json
from typing import Dict, List, Optional
import random
import time
from faker import Faker
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

# Initialize Faker for realistic data generation
fake = Faker()

# Page Configuration
st.set_page_config(
    page_title="GREENSTRIKAS - Climate Finance Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Climate Theme with enhanced styling
st.markdown("""
<style>
    /* Enhanced Theme Colors */
    :root {
        --primary-green: #1B5E20;
        --secondary-green: #388E3C;
        --accent-blue: #1565C0;
        --accent-teal: #00695C;
        --dark-bg: #0D47A1;
        --light-green: #E8F5E9;
        --gradient-primary: linear-gradient(135deg, #1B5E20 0%, #1565C0 100%);
        --gradient-secondary: linear-gradient(135deg, #388E3C 0%, #00695C 100%);
    }
    
    /* Enhanced Header Styling */
    .main-header {
        background: var(--gradient-primary);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        animation: float 20s linear infinite;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(-20px, -20px) rotate(360deg); }
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid var(--primary-green);
        margin-bottom: 1rem;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: var(--gradient-secondary);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: var(--gradient-primary);
    }
    
    /* Advanced Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%);
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #E8F5E9;
        border-radius: 12px;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        margin: 0;
        font-weight: 600;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: var(--primary-green);
        background: var(--light-green);
    }
    
    /* Advanced Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #81C784;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Blockchain Verification Badge */
    .blockchain-badge {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* AI Insights Container */
    .ai-insight {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 4px solid #1976D2;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    /* Risk Indicator */
    .risk-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .risk-low { background: #4CAF50; }
    .risk-medium { background: #FF9800; }
    .risk-high { background: #F44336; }
    
    /* Registration Form Styling */
    .registration-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .verification-success {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border: 2px solid #4CAF50;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State with enhanced features
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"
if 'blockchain_transactions' not in st.session_state:
    st.session_state.blockchain_transactions = []
if 'ai_insights' not in st.session_state:
    st.session_state.ai_insights = []
if 'user_accounts' not in st.session_state:
    st.session_state.user_accounts = {}
if 'verification_tokens' not in st.session_state:
    st.session_state.verification_tokens = {}
if 'reset_tokens' not in st.session_state:
    st.session_state.reset_tokens = {}
if 'show_registration' not in st.session_state:
    st.session_state.show_registration = False
if 'show_password_reset' not in st.session_state:
    st.session_state.show_password_reset = False
if 'show_verification' not in st.session_state:
    st.session_state.show_verification = False

# Email Configuration (Update these with your email service details)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',  # Change this
    'sender_password': 'your-app-password'   # Change this
}

# Enhanced Mock Data Generation
def generate_advanced_mock_projects():
    """Generate advanced mock climate finance projects with realistic data"""
    categories = ['Solar Energy', 'Wind Energy', 'Energy Efficiency', 'Green Buildings', 
                 'Sustainable Transport', 'Waste Management', 'Hydrogen', 'Carbon Capture']
    
    projects = []
    for i in range(25):
        risk_score = round(random.uniform(1, 5), 1)
        if risk_score <= 2:
            risk_category = "Low"
        elif risk_score <= 3.5:
            risk_category = "Medium"
        else:
            risk_category = "High"
            
        project = {
            'id': f'PRJ{1000+i}',
            'name': f'{random.choice(categories)} Project {fake.city()}',
            'category': random.choice(categories),
            'location': fake.city(),
            'investment_required': round(random.uniform(10, 200), 2),
            'expected_return': round(random.uniform(8, 18), 2),
            'risk_score': risk_score,
            'risk_category': risk_category,
            'carbon_offset': round(random.uniform(1000, 100000), 0),
            'status': random.choice(['Active', 'Funded', 'In Progress', 'Seeking Funds', 'Under Review']),
            'completion': random.randint(0, 100),
            'esg_score': round(random.uniform(70, 98), 1),
            'verification_status': random.choice(['Blockchain Verified', 'Pending', 'In Review', 'Government Certified']),
            'maturity': f'{random.randint(3, 12)} years',
            'min_investment': round(random.uniform(0.5, 10), 2),
            'first_loss_coverage': random.choice([10, 15, 20]),
            'currency_hedging': random.choice([True, False]),
            'government_backing': random.choice([True, False]),
            'technology_readiness': random.choice(['Early Stage', 'Proven', 'Commercial']),
            'sdg_alignment': random.sample([1, 3, 7, 8, 9, 11, 12, 13], random.randint(3, 6)),
            'blockchain_hash': hashlib.sha256(f"project{1000+i}".encode()).hexdigest()[:16]
        }
        projects.append(project)
    return projects

def generate_blockchain_transactions():
    """Generate mock blockchain transactions for transparency"""
    transactions = []
    for i in range(50):
        tx = {
            'hash': hashlib.sha256(f"tx{i}{random.randint(1000,9999)}".encode()).hexdigest(),
            'timestamp': fake.date_time_this_year(),
            'type': random.choice(['Carbon Credit', 'Green Bond', 'Verification', 'Settlement']),
            'amount': round(random.uniform(1000, 500000), 2),
            'status': random.choice(['Confirmed', 'Pending', 'Verified']),
            'block_height': random.randint(1000000, 2000000),
            'participants': [fake.company(), fake.company()]
        }
        transactions.append(tx)
    return transactions

def generate_ai_insights():
    """Generate AI-powered insights"""
    insights = [
        "📈 Solar projects in Gujarat showing 18% higher returns than national average",
        "⚠️ Currency volatility risk increasing - recommend additional hedging for Q2 2025",
        "🎯 Untapped opportunity in tier-2 cities for green building projects",
        "🔍 Carbon credit demand expected to surge 35% in next quarter",
        "💡 Wind energy storage projects achieving 94% of projected returns",
        "🌱 Bio-energy projects showing strong ESG alignment with SDG targets",
        "🔄 Portfolio diversification opportunity in waste-to-energy sector",
        "📊 Predictive model indicates 12.8% average returns for Q1 2025"
    ]
    return insights

# Password Hashing
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a stored password against one provided by user"""
    return hash_password(password) == hashed

# Token Generation
def generate_verification_token():
    """Generate a random verification token"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def generate_reset_token():
    """Generate a random password reset token"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))

# Email Simulation (For demo purposes - in production, use real email sending)
def simulate_send_verification_email(email, token):
    """Simulate sending verification email (for demo)"""
    st.session_state.verification_tokens[token] = {
        'email': email,
        'created_at': datetime.now(),
        'used': False
    }
    return True, f"Verification email sent to {email}. Use token: {token}"

def simulate_send_password_reset_email(email, token):
    """Simulate sending password reset email (for demo)"""
    st.session_state.reset_tokens[token] = {
        'email': email,
        'created_at': datetime.now(),
        'used': False
    }
    return True, f"Password reset email sent to {email}. Use token: {token}"

# Real Email Sending Functions (Uncomment and configure for production)
def send_verification_email(email, token):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = email
        msg['Subject'] = "Verify Your Email - GREENSTRIKAS"
        
        body = f'''
        Welcome to GREENSTRIKAS!
        
        Verification Code: {token}
        
        Enter this code to verify your email address.
        '''
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
        server.quit()
        
        st.session_state.verification_tokens[token] = {
            'email': email,
            'created_at': datetime.now(),
            'used': False
        }
        
        return True, "Verification email sent successfully!"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def send_password_reset_email(email, token):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = email
        msg['Subject'] = "Password Reset - GREENSTRIKAS"
        
        body = f'''
        Password Reset Request
        
        Reset Code: {token}
        
        Enter this code to reset your password.
        '''
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
        server.quit()
        
        st.session_state.reset_tokens[token] = {
            'email': email,
            'created_at': datetime.now(),
            'used': False
        }
        
        return True, "Password reset email sent successfully!"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

# Validation Functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, "Username is valid"

# Enhanced Authentication System
def register_user(username, email, password, user_type, full_name, organization):
    """Register a new user"""
    # Validate inputs
    if username in st.session_state.user_accounts:
        return False, "Username already exists"
    
    if not validate_email(email):
        return False, "Invalid email format"
    
    is_valid, message = validate_password(password)
    if not is_valid:
        return False, message
    
    is_valid, message = validate_username(username)
    if not is_valid:
        return False, message
    
    # Check if email is already registered
    for user_data in st.session_state.user_accounts.values():
        if user_data['email'] == email:
            return False, "Email already registered"
    
    # Create user account
    st.session_state.user_accounts[username] = {
        'email': email,
        'password_hash': hash_password(password),
        'user_type': user_type,
        'full_name': full_name,
        'organization': organization,
        'verified': False,
        'created_at': datetime.now(),
        'last_login': None
    }
    
    # Generate verification token and send email
    verification_token = generate_verification_token()
    success, message = simulate_send_verification_email(email, verification_token)
    # For production, use: success, message = send_verification_email(email, verification_token)
    
    if success:
        return True, message
    else:
        # Remove the user account if email sending failed
        del st.session_state.user_accounts[username]
        return False, f"Registration failed: {message}"

def verify_user_email(token):
    """Verify user email using token"""
    if token in st.session_state.verification_tokens:
        token_data = st.session_state.verification_tokens[token]
        
        if token_data['used']:
            return False, "Token has already been used"
        
        # Check if token is expired (24 hours)
        if datetime.now() - token_data['created_at'] > timedelta(hours=24):
            return False, "Verification token has expired"
        
        # Find user by email and mark as verified
        for username, user_data in st.session_state.user_accounts.items():
            if user_data['email'] == token_data['email']:
                user_data['verified'] = True
                token_data['used'] = True
                return True, "Email verified successfully! You can now log in."
        
        return False, "User not found"
    
    return False, "Invalid verification token"

def request_password_reset(email):
    """Request password reset for a user"""
    # Find user by email
    user_found = False
    for username, user_data in st.session_state.user_accounts.items():
        if user_data['email'] == email:
            user_found = True
            # Generate reset token and send email
            reset_token = generate_reset_token()
            success, message = simulate_send_password_reset_email(email, reset_token)
            # For production, use: success, message = send_password_reset_email(email, reset_token)
            
            if success:
                return True, message
            else:
                return False, f"Failed to send reset email: {message}"
    
    if not user_found:
        return False, "No account found with this email address"

def reset_password(token, new_password):
    """Reset user password using token"""
    if token in st.session_state.reset_tokens:
        token_data = st.session_state.reset_tokens[token]
        
        if token_data['used']:
            return False, "Token has already been used"
        
        # Check if token is expired (1 hour)
        if datetime.now() - token_data['created_at'] > timedelta(hours=1):
            return False, "Reset token has expired"
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return False, message
        
        # Find user by email and update password
        for username, user_data in st.session_state.user_accounts.items():
            if user_data['email'] == token_data['email']:
                user_data['password_hash'] = hash_password(new_password)
                token_data['used'] = True
                return True, "Password reset successfully! You can now log in with your new password."
        
        return False, "User not found"
    
    return False, "Invalid reset token"

def authenticate_user(username: str, password: str) -> bool:
    """Enhanced authentication system with role-based access"""
    # Check mock users first (for demo accounts)
    mock_users = {
        'investor': {'password': 'investor123', 'type': 'Investor', 'name': 'Global Investment Fund', 'email': 'investor@greenstrikas.com'},
        'developer': {'password': 'developer123', 'type': 'Developer', 'name': 'GreenTech Solutions', 'email': 'developer@greenstrikas.com'},
        'admin': {'password': 'admin123', 'type': 'Admin', 'name': 'Platform Administrator', 'email': 'admin@greenstrikas.com'},
        'government': {'password': 'gov123', 'type': 'Government', 'name': 'Climate Finance Agency', 'email': 'gov@greenstrikas.com'},
        'demo': {'password': 'demo123', 'type': 'Investor', 'name': 'Demo Investor', 'email': 'demo@greenstrikas.com'}
    }
    
    if username in mock_users and mock_users[username]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_type = mock_users[username]['type']
        st.session_state.user_display_name = mock_users[username]['name']
        
        # Initialize user-specific data
        if st.session_state.user_type == "Investor":
            st.session_state.portfolio_value = random.uniform(50000, 5000000)
            st.session_state.risk_tolerance = random.choice(['Low', 'Medium', 'High'])
        
        return True
    
    # Check registered users
    if username in st.session_state.user_accounts:
        user_data = st.session_state.user_accounts[username]
        
        if not user_data['verified']:
            st.error("Please verify your email before logging in.")
            return False
        
        if verify_password(password, user_data['password_hash']):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_type = user_data['user_type']
            st.session_state.user_display_name = user_data['full_name']
            user_data['last_login'] = datetime.now()
            
            # Initialize user-specific data
            if st.session_state.user_type == "Investor":
                st.session_state.portfolio_value = random.uniform(50000, 5000000)
                st.session_state.risk_tolerance = random.choice(['Low', 'Medium', 'High'])
            
            return True
    
    return False

# Registration Form
def render_registration_form():
    """Render user registration form"""
    st.markdown("### 👥 Create New Account")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            username = st.text_input("👤 Username", placeholder="Choose a username")
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
        
        with col2:
            organization = st.text_input("🏢 Organization", placeholder="Your company/organization")
            user_type = st.selectbox("🎯 Account Type", 
                                   ["Investor", "Developer", "Government", "Admin", "Analyst"])
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        
        # Password strength indicator
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.success("✅ " + message)
            else:
                st.error("❌ " + message)
        
        # Terms and conditions
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        if submitted:
            if not all([full_name, username, email, password, confirm_password, organization]):
                st.error("Please fill in all required fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            if not agree_terms:
                st.error("Please agree to the Terms of Service and Privacy Policy")
                return
            
            success, message = register_user(username, email, password, user_type, full_name, organization)
            
            if success:
                st.success(message)
                st.session_state.show_registration = False
                st.session_state.show_verification = True
            else:
                st.error(message)

# Password Reset Forms
def render_password_reset_request():
    """Render password reset request form"""
    st.markdown("### 🔑 Reset Your Password")
    st.info("Enter your email address and we'll send you instructions to reset your password.")
    
    with st.form("password_reset_request"):
        email = st.text_input("📧 Email Address", placeholder="Enter your registered email")
        
        submitted = st.form_submit_button("📧 Send Reset Instructions", use_container_width=True)
        
        if submitted:
            if not email:
                st.error("Please enter your email address")
                return
            
            success, message = request_password_reset(email)
            
            if success:
                st.success(message)
                st.session_state.show_password_reset = False
            else:
                st.error(message)
    
    if st.button("↩️ Back to Login", use_container_width=True):
        st.session_state.show_password_reset = False

def render_password_reset_form(token=None):
    """Render password reset form"""
    st.markdown("### 🔑 Create New Password")
    
    # If no token provided, ask for it
    if not token:
        token = st.text_input("🔑 Reset Token", placeholder="Enter the reset token from your email")
    
    with st.form("password_reset"):
        new_password = st.text_input("🔒 New Password", type="password", placeholder="Enter new password")
        confirm_password = st.text_input("🔒 Confirm New Password", type="password", placeholder="Confirm new password")
        
        submitted = st.form_submit_button("🔄 Reset Password", use_container_width=True)
        
        if submitted:
            if not token:
                st.error("Please enter the reset token")
                return
            
            if not new_password or not confirm_password:
                st.error("Please fill in all password fields")
                return
            
            if new_password != confirm_password:
                st.error("Passwords do not match")
                return
            
            success, message = reset_password(token, new_password)
            
            if success:
                st.success(message)
                st.session_state.show_password_reset = False
            else:
                st.error(message)

# Email Verification Form
def render_email_verification():
    """Render email verification form"""
    st.markdown("### 📧 Verify Your Email")
    st.info("Check your email for the verification token and enter it below.")
    
    with st.form("email_verification"):
        token = st.text_input("🔑 Verification Token", placeholder="Enter the verification token from your email")
        
        submitted = st.form_submit_button("✅ Verify Email", use_container_width=True)
        
        if submitted:
            if not token:
                st.error("Please enter the verification token")
                return
            
            success, message = verify_user_email(token)
            
            if success:
                st.success(message)
                st.session_state.show_verification = False
            else:
                st.error(message)
    
    if st.button("↩️ Back to Login", use_container_width=True):
        st.session_state.show_verification = False

# Enhanced Login Form with Registration Options
def render_advanced_login():
    """Render enhanced login page with registration options"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">🌱 Welcome to GREENSTRIKAS</h1>
        <p style="margin: 0.5rem 0 0 0;">Transforming Climate Finance Through Innovation</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            Integrated Climate Finance Ecosystem | Blockchain Secured | AI Powered
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show verification form if needed
    if st.session_state.show_verification:
        render_email_verification()
        return
    
    # Show password reset form if needed
    if st.session_state.show_password_reset:
        render_password_reset_request()
        return
    
    # Show registration form if needed
    if st.session_state.show_registration:
        render_registration_form()
        
        st.markdown("---")
        if st.button("↩️ Back to Login", use_container_width=True):
            st.session_state.show_registration = False
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Sign In to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("🚀 Sign In", use_container_width=True)
            with col_b:
                demo = st.form_submit_button("👁️ Demo Access", use_container_width=True)
            
            if submit:
                if authenticate_user(username, password):
                    st.success(f"Welcome back, {st.session_state.user_display_name}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or unverified account. Please try again.")
            
            if demo:
                if authenticate_user('demo', 'demo123'):
                    st.success("Logged in with demo account!")
                    st.rerun()
        
        st.markdown("---")
        
        # Additional options
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("👤 Create Account", use_container_width=True):
                st.session_state.show_registration = True
                st.rerun()
        with col_y:
            if st.button("🔑 Forgot Password", use_container_width=True):
                st.session_state.show_password_reset = True
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### 🎯 Demo Credentials")
        st.info("""
        **Username:** demo  
        **Password:** demo123  
        **Type:** Investor
        
        *Explore all platform features with demo access*
        """)

# Enhanced Dashboard Components
def render_advanced_header():
    """Render enhanced main header"""
    st.markdown(f"""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">🌱 GREENSTRIKAS</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: 300;">India's Premier Climate Finance Platform</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Bridging the $126 Billion Annual Climate Finance Gap</p>
        <div style="margin-top: 1rem; font-size: 0.9rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0 0.3rem;">
                🔐 Blockchain Secured
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0 0.3rem;">
                🤖 AI Powered
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0 0.3rem;">
                🌍 UN SDG Aligned
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_advanced_metrics():
    """Display enhanced key platform metrics"""
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics = [
        ("💰 Total Capital Mobilized", "$2.8B", "+15.2%", "normal"),
        ("🌱 Active Projects", "189", "+12", "normal"),
        ("🏭 CO₂ Offset (MT)", "56.3M", "+3.1M", "normal"),
        ("👥 Registered Investors", f"{len(st.session_state.user_accounts) + 3847}", f"+{len(st.session_state.user_accounts)}", "normal"),
        ("📈 Avg. Returns", "12.1%", "+1.2%", "normal"),
        ("🔒 Risk Coverage", "18%", "+2%", "normal")
    ]
    
    for i, (label, value, delta, color) in enumerate(metrics):
        with [col1, col2, col3, col4, col5, col6][i]:
            st.metric(label=label, value=value, delta=delta, delta_color=color)

def render_government_derisking():
    """Render Government De-risking Dashboard"""
    st.subheader("🏛️ Government De-risking Ecosystem")
    
    st.info("""
    **Official Government Partnership**: First-loss guarantees, policy stability, and currency hedging facilities 
    to make climate investments as secure as developed markets.
    """)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Risk Mitigation", "📜 Policy Framework", "💰 Financial Instruments", "📊 Impact Dashboard"])
    
    with tab1:
        st.markdown("### Risk Mitigation Mechanisms")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>First-Loss Guarantee</h4>
                <h2>15-20%</h2>
                <p>Government/MDB absorption of initial losses</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>Policy Stability</h4>
                <h2>15 Years</h2>
                <p>Guaranteed policy framework under Climate Investment Protection Act</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>Currency Hedging</h4>
                <h2>Subsidized</h2>
                <p>Centralized facility for forex risk management</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk reduction visualization
        st.markdown("### Risk Reduction Impact")
        
        fig = go.Figure()
        
        # Before de-risking
        fig.add_trace(go.Bar(
            name='Before De-risking',
            x=['Political Risk', 'Currency Risk', 'Regulatory Risk', 'Technology Risk'],
            y=[8, 7, 9, 6],
            marker_color='#FF6B6B'
        ))
        
        # After de-risking
        fig.add_trace(go.Bar(
            name='After De-risking',
            x=['Political Risk', 'Currency Risk', 'Regulatory Risk', 'Technology Risk'],
            y=[2, 3, 2, 4],
            marker_color='#4ECDC4'
        ))
        
        fig.update_layout(
            title="Risk Score Reduction Through Government Mechanisms (1-10 Scale)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Policy Framework & Compliance")
        
        policies = [
            {"policy": "Climate Investment Protection Act", "status": "🟢 Active", "coverage": "15 years"},
            {"policy": "Single Window Clearance", "status": "🟢 Active", "coverage": "All projects >$50M"},
            {"policy": "Green Bond Taxonomy", "status": "🟢 Active", "coverage": "SEBI compliant"},
            {"policy": "Carbon Credit Regulation", "status": "🟡 Pending", "coverage": "Article 6 alignment"},
            {"policy": "ESG Disclosure Standards", "status": "🟢 Active", "coverage": "BRSR compliance"}
        ]
        
        for policy in policies:
            with st.expander(f"{policy['policy']} - {policy['status']}"):
                st.write(f"**Coverage:** {policy['coverage']}")
                st.write("**Benefits:** Reduced regulatory uncertainty, streamlined approvals, enhanced investor confidence")
                if st.button("View Compliance Requirements", key=f"compliance_{policy['policy']}"):
                    st.info(f"Compliance details for {policy['policy']}")
    
    with tab3:
        st.markdown("### Financial De-risking Instruments")
        
        instruments = [
            {
                "name": "First-Loss Capital Facility",
                "provider": "National Climate Finance Corporation",
                "coverage": "20% first loss",
                "eligibility": "Projects >$25M with >70% climate alignment",
                "status": "🟢 Available"
            },
            {
                "name": "Currency Hedging Facility",
                "provider": "RBI Partnership",
                "coverage": "Subsidized forex hedging",
                "eligibility": "All foreign investments",
                "status": "🟢 Available"
            },
            {
                "name": "Political Risk Insurance",
                "provider": "MIGA/ECGC",
                "coverage": "Full political risk coverage",
                "eligibility": "International investors",
                "status": "🟢 Available"
            }
        ]
        
        for instrument in instruments:
            st.markdown(f"""
            <div class="info-box">
                <h4>{instrument['name']} {instrument['status']}</h4>
                <p><strong>Provider:</strong> {instrument['provider']}</p>
                <p><strong>Coverage:</strong> {instrument['coverage']}</p>
                <p><strong>Eligibility:</strong> {instrument['eligibility']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### De-risking Impact Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Capital Mobilized", "$2.8B", "+$450M")
        with col2:
            st.metric("Cost of Capital Reduction", "250 bps", "-50 bps")
        with col3:
            st.metric("Project Approval Time", "45 days", "-60%")
        
        # Impact visualization
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = 2800,
            delta = {'reference': 2350, 'increasing': {'color': "#2E7D32"}},
            gauge = {
                'axis': {'range': [None, 5000], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#2E7D32"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 1000], 'color': '#C8E6C9'},
                    {'range': [1000, 3000], 'color': '#81C784'},
                    {'range': [3000, 5000], 'color': '#4CAF50'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4900}}))
        
        fig.update_layout(title = "Capital Mobilization Progress ($B)")
        st.plotly_chart(fig, use_container_width=True)

def render_blockchain_verification():
    """Render Blockchain Verification System"""
    st.subheader("⛓️ Blockchain Verification & Transparency")
    
    st.info("""
    **Immutable Transparency**: Every transaction, carbon credit, and project verification is recorded on our 
    distributed ledger for complete transparency and auditability.
    """)
    
    tab1, tab2, tab3 = st.tabs(["📜 Transaction Ledger", "🌍 Carbon Credit Tracking", "🔍 Audit Trail"])
    
    with tab1:
        st.markdown("### Live Transaction Ledger")
        
        if not st.session_state.blockchain_transactions:
            st.session_state.blockchain_transactions = generate_blockchain_transactions()
        
        # Live transaction feed
        st.markdown("#### 🔴 Live Transactions")
        
        # Simulate live updates
        if st.button("🔄 Refresh Transactions"):
            new_tx = {
                'hash': hashlib.sha256(f"tx{len(st.session_state.blockchain_transactions)}".encode()).hexdigest(),
                'timestamp': datetime.now(),
                'type': random.choice(['Carbon Credit', 'Green Bond', 'Verification']),
                'amount': round(random.uniform(1000, 100000), 2),
                'status': 'Confirmed',
                'block_height': random.randint(2000000, 3000000),
                'participants': [fake.company(), fake.company()]
            }
            st.session_state.blockchain_transactions.insert(0, new_tx)
            st.rerun()
        
        # Display recent transactions
        for tx in st.session_state.blockchain_transactions[:10]:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.code(f"Hash: {tx['hash'][:16]}...", language=None)
            with col2:
                st.write(f"**{tx['type']}**")
                st.write(f"${tx['amount']:,.2f}")
            with col3:
                st.write(tx['timestamp'].strftime("%Y-%m-%d %H:%M"))
                st.write(f"Block: {tx['block_height']}")
            with col4:
                status_color = "🟢" if tx['status'] == 'Confirmed' else "🟡"
                st.write(f"{status_color} {tx['status']}")
            
            st.markdown("---")
    
    with tab2:
        st.markdown("### Carbon Credit Lifecycle Tracking")
        
        # Generate carbon credit lifecycle
        credit_id = f"CC-{fake.random_int(10000, 99999)}"
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Credit ID", credit_id)
        with col2:
            st.metric("Project", "Solar Farm Gujarat")
        with col3:
            st.metric("Verification", "Gold Standard")
        with col4:
            st.metric("Status", "🔗 Blockchain Verified")
        
        # Lifecycle visualization
        st.markdown("### Credit Lifecycle")
        
        stages = [
            {"stage": "Project Registration", "status": "✅ Complete", "timestamp": "2024-01-15", "block": "1,234,567"},
            {"stage": "Verification Audit", "status": "✅ Complete", "timestamp": "2024-02-20", "block": "1,245,678"},
            {"stage": "Credit Issuance", "status": "✅ Complete", "timestamp": "2024-03-10", "block": "1,256,789"},
            {"stage": "Market Listing", "status": "✅ Complete", "timestamp": "2024-03-15", "block": "1,267,890"},
            {"stage": "Purchase", "status": "⏳ Pending", "timestamp": "-", "block": "-"},
            {"stage": "Retirement", "status": "⏳ Pending", "timestamp": "-", "block": "-"}
        ]
        
        for stage in stages:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"**{stage['stage']}**")
            with col2:
                st.write(stage['status'])
            with col3:
                st.write(stage['timestamp'])
            with col4:
                st.write(stage['block'])
            
            st.markdown("---")
    
    with tab3:
        st.markdown("### Comprehensive Audit Trail")
        
        st.markdown("""
        <div class="info-box">
            <h4>🔒 Immutable Record Keeping</h4>
            <ul>
                <li>Every transaction cryptographically signed and timestamped</li>
                <li>Smart contracts for automated compliance</li>
                <li>Real-time audit capabilities for regulators</li>
                <li>Transparent project funding flows</li>
                <li>Carbon credit double-spending prevention</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Audit statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Transactions", "45,678", "+1,234")
        with col2:
            st.metric("Blocks Mined", "2.3M", "+45,672")
        with col3:
            st.metric("Network Uptime", "99.98%", "+0.02%")
        
        if st.button("📄 Generate Audit Report"):
            with st.spinner("Generating comprehensive audit report..."):
                time.sleep(2)
                st.success("Audit report generated successfully!")
                st.info("Report includes: Transaction history, verification logs, compliance checks, and blockchain proofs")

def render_ai_advisory():
    """Render AI-Powered Advisory System"""
    st.subheader("🤖 AI-Powered Climate Finance Advisory")
    
    st.info("""
    **Intelligent Insights**: Our AI system analyzes market trends, project data, and risk factors to provide 
    data-driven investment recommendations and risk assessments.
    """)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Investment Recommendations", "⚠️ Risk Intelligence", "📈 Market Predictions", "🔍 Due Diligence AI"])
    
    with tab1:
        st.markdown("### Personalized Investment Recommendations")
        
        if st.session_state.user_type == "Investor":
            st.markdown(f"""
            <div class="ai-insight">
                <h4>👤 Investor Profile Analysis</h4>
                <p><strong>Risk Tolerance:</strong> {st.session_state.get('risk_tolerance', 'Medium')}</p>
                <p><strong>Portfolio Value:</strong> ${st.session_state.get('portfolio_value', 0):,.2f}</p>
                <p><strong>Preferred Sectors:</strong> Renewable Energy, Green Infrastructure</p>
            </div>
            """, unsafe_allow_html=True)
        
        # AI Recommendations
        st.markdown("### 🤖 AI Investment Recommendations")
        
        recommendations = [
            {
                "project": "Gujarat Solar Park Expansion",
                "sector": "Solar Energy",
                "expected_return": "14.2%",
                "risk_score": "2.1/5.0",
                "ai_confidence": "92%",
                "reason": "Strong government backing, proven technology, high ESG alignment"
            },
            {
                "project": "Bangalore Green Building Portfolio",
                "sector": "Green Buildings",
                "expected_return": "11.8%",
                "risk_score": "1.8/5.0",
                "ai_confidence": "88%",
                "reason": "Urban demand growth, energy efficiency savings, premium rental yields"
            },
            {
                "project": "Tamil Nadu Offshore Wind",
                "sector": "Wind Energy",
                "expected_return": "16.5%",
                "risk_score": "3.8/5.0",
                "ai_confidence": "76%",
                "reason": "High return potential, emerging technology, coastal location advantages"
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"🏆 {rec['project']} - {rec['expected_return']} Expected Return"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sector", rec['sector'])
                    st.metric("AI Confidence", rec['ai_confidence'])
                with col2:
                    st.metric("Expected Return", rec['expected_return'])
                    st.metric("Risk Score", rec['risk_score'])
                with col3:
                    if st.button("📊 Detailed Analysis", key=f"analysis_{rec['project']}"):
                        st.info(f"Detailed AI analysis for {rec['project']}")
                
                st.markdown(f"**🤖 AI Insight:** {rec['reason']}")
                
                if st.button("💰 Express Interest", key=f"interest_{rec['project']}"):
                    st.success(f"Interest registered for {rec['project']}! Our team will contact you.")
    
    with tab2:
        st.markdown("### Real-time Risk Intelligence")
        
        # Risk dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Portfolio VaR", "$2.1M", "-$0.3M", delta_color="inverse")
        with col2:
            st.metric("Climate Physical Risk", "Medium", "-1 Level")
        with col3:
            st.metric("Regulatory Risk Index", "2.8/10", "-0.4")
        with col4:
            st.metric("Currency Risk Exposure", "12%", "-3%")
        
        # Risk heat map
        st.markdown("### Risk Heat Map by Sector")
        
        sectors = ["Solar", "Wind", "Green Buildings", "EV Infrastructure", "Waste Management"]
        risk_factors = ["Technology", "Regulatory", "Market", "Execution", "Climate"]
        
        risk_matrix = np.random.uniform(1, 5, (5, 5))
        
        fig = px.imshow(risk_matrix,
                       labels=dict(x="Risk Factors", y="Sectors", color="Risk Level"),
                       x=risk_factors, y=sectors,
                       color_continuous_scale="RdYlGn_r",
                       aspect="auto")
        
        fig.update_layout(title="Sector-wise Risk Assessment Heat Map")
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Risk Alerts
        st.markdown("### ⚠️ AI Risk Alerts")
        
        alerts = [
            "🔴 High currency volatility detected in INR-USD pair - recommend immediate hedging",
            "🟡 Regulatory changes expected in carbon credit trading - monitor policy updates",
            "🟢 Solar panel supply chain issues resolved - favorable buying conditions",
            "🔴 Project delays reported in Maharashtra due to monsoon - review timelines"
        ]
        
        for alert in alerts:
            st.warning(alert)
    
    with tab3:
        st.markdown("### Market Predictions & Trends")
        
        # Carbon price prediction
        st.markdown("#### Carbon Credit Price Forecast")
        
        dates = pd.date_range(start='2024-01-01', periods=24, freq='M')
        actual_prices = 25 + np.cumsum(np.random.randn(24) * 0.8)
        predicted_prices = actual_prices[-12:].tolist() + [30, 32, 35, 38, 40, 42, 45, 47, 49, 52, 54, 56]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates[:12], y=actual_prices[:12],
            mode='lines', name='Historical',
            line=dict(color='#2E7D32', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=dates[12:], y=predicted_prices[12:],
            mode='lines', name='AI Prediction',
            line=dict(color='#FF6B6B', width=3, dash='dash')
        ))
        
        fig.update_layout(
            title="Carbon Credit Price Forecast ($/ton)",
            xaxis_title="Date",
            yaxis_title="Price ($/ton)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market insights
        st.markdown("### 📊 AI Market Insights")
        
        if not st.session_state.ai_insights:
            st.session_state.ai_insights = generate_ai_insights()
        
        for insight in st.session_state.ai_insights:
            st.markdown(f"""
            <div class="ai-insight">
                {insight}
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### AI-Powered Due Diligence")
        
        st.markdown("""
        Our AI system automates and enhances due diligence processes with:
        - **Document Analysis**: Automated review of project documents and contracts
        - **Risk Scoring**: Comprehensive risk assessment across multiple dimensions
        - **Compliance Checking**: Real-time regulatory compliance verification
        - **Financial Modeling**: Advanced projections and scenario analysis
        """)
        
        # Due diligence interface
        project_url = st.text_input("Enter Project URL or Upload Documents for AI Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_files = st.file_uploader("Upload Project Documents", 
                                            type=['pdf', 'docx', 'xlsx'],
                                            accept_multiple_files=True)
        with col2:
            analysis_type = st.selectbox("Analysis Type", 
                                       ["Comprehensive Due Diligence", 
                                        "Financial Viability", 
                                        "ESG Compliance",
                                        "Risk Assessment"])
        
        if st.button("🚀 Start AI Due Diligence"):
            with st.spinner("AI is analyzing the project... This may take 2-3 minutes."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)
                
                st.success("AI Due Diligence Complete!")
                
                # Mock results
                st.markdown("### 📋 Due Diligence Report")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Score", "87/100", "Good")
                    st.metric("Financial Viability", "92/100", "Excellent")
                with col2:
                    st.metric("Risk Assessment", "2.3/5.0", "Low")
                    st.metric("ESG Compliance", "89/100", "Good")
                with col3:
                    st.metric("Regulatory Alignment", "94/100", "Excellent")
                    st.metric("Technology Readiness", "85/100", "Good")
                
                st.markdown("#### 🤖 AI Recommendations")
                st.info("""
                - **Strengths**: Strong financial projections, excellent regulatory compliance, proven technology
                - **Concerns**: Moderate currency exposure, dependency on single technology provider
                - **Recommendations**: Implement additional currency hedging, diversify technology suppliers
                - **Confidence Level**: 88%
                """)

def render_sdg_tracker():
    """Render UN Sustainable Development Goals Tracker"""
    st.subheader("🌍 UN SDG Alignment Tracker")
    
    st.info("""
    **Sustainable Development Impact**: Track how investments contribute to United Nations Sustainable Development Goals.
    Real-time impact measurement and reporting for ESG compliance and impact investing.
    """)
    
    # SDG Dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("SDGs Addressed", "9/17", "+2")
    with col2:
        st.metric("Projects Aligned", "156", "+18")
    with col3:
        st.metric("Impact Score", "87/100", "+5")
    with col4:
        st.metric("ESG Compliance", "94%", "+3%")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🎯 SDG Progress", "📊 Impact Analytics", "📑 Compliance Reporting"])
    
    with tab1:
        st.markdown("### SDG Contribution Dashboard")
        
        # SDG icons and progress
        sdgs = [
            {"goal": "SDG 7", "name": "Affordable & Clean Energy", "progress": 92, "projects": 45},
            {"goal": "SDG 8", "name": "Decent Work & Economic Growth", "progress": 78, "projects": 23},
            {"goal": "SDG 9", "name": "Industry, Innovation & Infrastructure", "progress": 85, "projects": 34},
            {"goal": "SDG 11", "name": "Sustainable Cities & Communities", "progress": 76, "projects": 28},
            {"goal": "SDG 12", "name": "Responsible Consumption & Production", "progress": 82, "projects": 19},
            {"goal": "SDG 13", "name": "Climate Action", "progress": 95, "projects": 67}
        ]
        
        for sdg in sdgs:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                st.markdown(f"**{sdg['goal']}**")
            with col2:
                st.write(sdg['name'])
                st.progress(sdg['progress'] / 100)
            with col3:
                st.write(f"{sdg['progress']}% Alignment")
            with col4:
                st.write(f"{sdg['projects']} Projects")
            
            st.markdown("---")
    
    with tab2:
        st.markdown("### Impact Measurement Analytics")
        
        # Impact metrics visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Environmental impact
            categories = ["CO₂ Reduction", "Renewable Energy", "Water Saved", "Waste Reduced"]
            values = [45.6, 12.8, 8.3, 4.2]
            
            fig = go.Figure(data=[go.Bar(x=categories, y=values, marker_color=['#2E7D32', '#1976D2', '#00838F', '#6A1B9A'])])
            fig.update_layout(title="Environmental Impact (Annual)", yaxis_title="Million Units")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Social impact
            social_metrics = ["Green Jobs", "Community Benefits", "Health Improvements", "Education"]
            social_values = [125, 89, 67, 45]
            
            fig = px.pie(values=social_values, names=social_metrics, 
                        title="Social Impact Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Real-time impact tracker
        st.markdown("### 📈 Real-time Impact Tracker")
        
        impact_data = {
            "Metric": ["CO₂ Reduced (tons)", "Renewable Energy (MWh)", "Green Jobs Created", "Water Saved (ML)"],
            "Today": [12500, 45000, 340, 8500],
            "This Week": [78500, 285000, 2150, 53200],
            "This Month": [325000, 1180000, 8900, 221000]
        }
        
        st.dataframe(pd.DataFrame(impact_data), use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Automated Compliance Reporting")
        
        st.markdown("""
        Generate comprehensive reports for:
        - **ESG Compliance** (SEBI BRSR, Global Reporting Initiative)
        - **Climate Disclosure** (TCFD, IFRS S2)
        - **Impact Reporting** (UN PRI, Impact Management Project)
        - **Regulatory Filings** (RBI, SEBI, Ministry of Environment)
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Standard Reports")
            report_type = st.selectbox("Select Report Type", 
                                     ["ESG Performance Report", 
                                      "Climate Impact Assessment",
                                      "SDG Contribution Report",
                                      "Regulatory Compliance Filing"])
            
            period = st.selectbox("Reporting Period",
                                ["Q4 2024", "FY 2024", "H2 2024", "Custom Range"])
            
            if st.button("📄 Generate Standard Report", use_container_width=True):
                with st.spinner(f"Generating {report_type}..."):
                    time.sleep(2)
                    st.success(f"{report_type} generated successfully!")
        
        with col2:
            st.markdown("#### Custom Report Builder")
            
            frameworks = st.multiselect("Reporting Frameworks",
                                      ["GRI Standards", "TCFD", "SASB", "UN SDGs", 
                                       "SEBI BRSR", "IFRS Sustainability"])
            
            metrics = st.multiselect("Include Metrics",
                                   ["Carbon Emissions", "Energy Consumption", "Water Usage",
                                    "Waste Management", "Community Investment", "Employee Diversity"])
            
            if st.button("🔨 Build Custom Report", use_container_width=True):
                if frameworks and metrics:
                    st.success("Custom report configuration saved!")
                else:
                    st.warning("Please select frameworks and metrics")

def render_dashboard():
    """Render main dashboard"""
    render_advanced_header()
    render_advanced_metrics()
    
    st.markdown("---")
    
    # Market Overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Platform Performance")
        
        # Generate sample time series data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        capital_mobilized = 2.8 + np.cumsum(np.random.randn(100) * 0.1)
        projects_funded = 189 + np.cumsum(np.random.randn(100) * 2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=capital_mobilized, name='Capital Mobilized ($B)',
            line=dict(color='#2E7D32', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=projects_funded/100, name='Projects Funded (scaled)',
            line=dict(color='#1976D2', width=3)
        ))
        
        fig.update_layout(
            title="Platform Growth Trajectory",
            xaxis_title="Date",
            yaxis_title="Value",
            height=400,
            showlegend=True,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        st.markdown("""
        <div class="info-box">
            <h4>Available Actions</h4>
            <ul>
                <li>Browse Climate Projects</li>
                <li>Trade Carbon Credits</li>
                <li>Access Blended Finance</li>
                <li>View Portfolio Performance</li>
                <li>Generate ESG Reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Browse Projects", use_container_width=True):
                st.session_state.page = "Projects"
        with col_b:
            if st.button("🌍 Carbon Trading", use_container_width=True):
                st.session_state.page = "Carbon Trading"
        
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = "Analytics"
        if st.button("🛡️ De-risking", use_container_width=True):
            st.session_state.page = "De-risking"
    
    # Recent Activity Feed
    st.markdown("---")
    st.subheader("📰 Recent Platform Activity")
    
    activities = [
        {"time": "2 hours ago", "action": "New Solar Project Listed", "value": "$45M", "location": "Gujarat"},
        {"time": "4 hours ago", "action": "Carbon Credits Traded", "value": "5,000 tons", "location": "Maharashtra"},
        {"time": "6 hours ago", "action": "Project Funded", "value": "$23M", "location": "Tamil Nadu"},
        {"time": "1 day ago", "action": "Green Bond Issued", "value": "$100M", "location": "Karnataka"},
        {"time": "2 days ago", "action": "ESG Verification Complete", "value": "Score: 92", "location": "Rajasthan"}
    ]
    
    for activity in activities[:5]:
        st.markdown(f"""
        <div style="background: #F5F5F5; padding: 0.5rem 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #2E7D32;">
            <strong>{activity['action']}</strong> - {activity['value']} | {activity['location']} <span style="color: #666; float: right;">{activity['time']}</span>
        </div>
        """, unsafe_allow_html=True)

def render_projects():
    """Render Projects Marketplace"""
    st.subheader("🌱 Climate Projects Marketplace")
    
    if not st.session_state.projects:
        st.session_state.projects = generate_advanced_mock_projects()
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        category_filter = st.selectbox("Category", ["All", "Solar Energy", "Wind Energy", "Energy Efficiency", "Green Buildings"])
    with col2:
        risk_filter = st.selectbox("Risk Level", ["All", "Low", "Medium", "High"])
    with col3:
        min_investment = st.number_input("Min Investment ($M)", min_value=0, max_value=100, value=0)
    with col4:
        location_filter = st.text_input("Location", placeholder="Filter by location")
    
    # Apply filters
    filtered_projects = st.session_state.projects
    if category_filter != "All":
        filtered_projects = [p for p in filtered_projects if p['category'] == category_filter]
    if risk_filter != "All":
        filtered_projects = [p for p in filtered_projects if p['risk_category'] == risk_filter]
    if min_investment > 0:
        filtered_projects = [p for p in filtered_projects if p['min_investment'] >= min_investment]
    if location_filter:
        filtered_projects = [p for p in filtered_projects if location_filter.lower() in p['location'].lower()]
    
    # Display projects
    st.markdown(f"### 📋 Available Projects ({len(filtered_projects)})")
    
    for project in filtered_projects:
        with st.expander(f"🌱 {project['name']} - ${project['investment_required']}M Required"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Project ID:** {project['id']}")
                st.markdown(f"**Category:** {project['category']}")
                st.markdown(f"**Location:** {project['location']}")
                st.markdown(f"**Status:** {project['status']}")
                st.markdown(f"**Verification:** {project['verification_status']}")
            
            with col2:
                st.markdown(f"**Expected Return:** {project['expected_return']}%")
                st.markdown(f"**Risk Score:** {project['risk_score']}/5.0")
                st.markdown(f"**ESG Score:** {project['esg_score']}/100")
                st.markdown(f"**Maturity:** {project['maturity']}")
                st.markdown(f"**Min Investment:** ${project['min_investment']}M")
            
            with col3:
                st.markdown(f"**Carbon Offset:** {project['carbon_offset']:,.0f} MT/year")
                st.markdown(f"**First-Loss Coverage:** {project['first_loss_coverage']}%")
                st.markdown(f"**Govt Backing:** {'Yes' if project['government_backing'] else 'No'}")
                st.markdown(f"**Currency Hedging:** {'Yes' if project['currency_hedging'] else 'No'}")
                
                progress = project['completion'] / 100
                st.progress(progress)
                st.caption(f"Funding Progress: {project['completion']}%")
            
            # SDG Alignment
            st.markdown("**SDG Alignment:**")
            sdg_icons = " ".join([f"🎯 {sdg}" for sdg in project['sdg_alignment']])
            st.markdown(sdg_icons)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button(f"📄 View Details", key=f"detail_{project['id']}"):
                    st.info(f"Detailed analysis for {project['name']} would be shown here")
            with col_b:
                if st.button(f"💰 Invest Now", key=f"invest_{project['id']}"):
                    st.success(f"Investment process initiated for {project['name']}")
            with col_c:
                if st.button(f"📊 Download Report", key=f"report_{project['id']}"):
                    st.info("Report download initiated")

def render_carbon_trading():
    """Render Carbon Credit Trading Hub"""
    st.subheader("🌍 Carbon Credit Trading Hub")
    
    # Market Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Carbon Price Index", "$32.45", "+2.3%")
    with col2:
        st.metric("Daily Volume", "45,230 tons", "+12%")
    with col3:
        st.metric("Active Listings", "234", "+8")
    with col4:
        st.metric("Verified Credits", "2.3M tons", "+15%")
    
    st.markdown("---")
    
    # Trading Interface
    tab1, tab2, tab3 = st.tabs(["🛒 Buy Credits", "💰 Sell Credits", "📊 Market Analysis"])
    
    with tab1:
        st.markdown("### Available Carbon Credits")
        
        credits = [
            {"type": "Solar RECs", "volume": 5000, "price": 28.50, "verification": "Gold Standard", "location": "Gujarat"},
            {"type": "Wind RECs", "volume": 3200, "price": 26.75, "verification": "VCS", "location": "Tamil Nadu"},
            {"type": "Forest Conservation", "volume": 15000, "price": 35.20, "verification": "CAR", "location": "Karnataka"},
            {"type": "Energy Efficiency", "volume": 8700, "price": 22.80, "verification": "CDM", "location": "Maharashtra"},
        ]
        
        for credit in credits:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    st.markdown(f"**{credit['type']}**")
                    st.caption(f"Verification: {credit['verification']} | Location: {credit['location']}")
                with col2:
                    st.metric("Price", f"${credit['price']}/ton")
                with col3:
                    st.metric("Available", f"{credit['volume']:,} tons")
                with col4:
                    quantity = st.number_input("Quantity", min_value=1, max_value=credit['volume'], 
                                              value=100, key=f"buy_{credit['type']}")
                with col5:
                    if st.button("Buy", key=f"purchase_{credit['type']}"):
                        total_cost = quantity * credit['price']
                        st.success(f"Purchase order placed: {quantity} tons for ${total_cost:,.2f}")
                st.markdown("---")
    
    with tab2:
        st.markdown("### List Your Carbon Credits")
        
        with st.form("sell_credits_form"):
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input("Project Name")
                credit_type = st.selectbox("Credit Type", ["Solar RECs", "Wind RECs", "Forest Conservation", "Energy Efficiency"])
                verification = st.selectbox("Verification Standard", ["Gold Standard", "VCS", "CDM", "CAR"])
            with col2:
                quantity = st.number_input("Quantity (tons)", min_value=1, value=1000)
                price = st.number_input("Price per ton ($)", min_value=1.0, value=25.0)
                vintage_year = st.number_input("Vintage Year", min_value=2020, max_value=2025, value=2024)
            
            documentation = st.file_uploader("Upload Verification Documents", type=['pdf', 'doc', 'docx'])
            
            if st.form_submit_button("List Credits"):
                st.success(f"Successfully listed {quantity} tons of {credit_type} credits at ${price}/ton")
    
    with tab3:
        st.markdown("### Market Analysis")
        
        # Price trends
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        prices = [25.0, 26.2, 27.8, 28.5, 29.1, 30.4, 31.2, 30.8, 31.5, 32.1, 32.9, 33.5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines+markers', name='Carbon Price',
                                line=dict(color='#1976D2', width=2)))
        fig.update_layout(title="Carbon Credit Price Trends", xaxis_title="Date", 
                         yaxis_title="Price ($/ton)", height=400)
        st.plotly_chart(fig, use_container_width=True)

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("## 🌱 GREENSTRIKAS")
        st.markdown(f"**Welcome, {st.session_state.user_display_name}**")
        st.markdown(f"*{st.session_state.user_type} Account*")
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📊 Navigation")
        
        nav_options = [
            ("🏠 Dashboard", "Dashboard"),
            ("🌱 Projects", "Projects"),
            ("🌍 Carbon Trading", "Carbon Trading"),
            ("🛡️ De-risking", "De-risking"),
            ("⛓️ Blockchain", "Blockchain"),
            ("🤖 AI Advisory", "AI Advisory"),
            ("🌍 SDG Tracker", "SDG Tracker"),
            ("📊 Analytics", "Analytics")
        ]
        
        for label, page in nav_options:
            if st.button(label, use_container_width=True, key=f"nav_{page}"):
                st.session_state.page = page
        
        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        
        # Quick action buttons
        if st.button("📈 Market Data", use_container_width=True):
            st.info("Market data would open here")
        if st.button("📰 News", use_container_width=True):
            st.info("Climate finance news would open here")
        if st.button("🔄 Portfolio", use_container_width=True):
            st.info("Portfolio management would open here")
        if st.button("📋 Reports", use_container_width=True):
            st.info("Report generation would open here")
        
        st.markdown("---")
        st.markdown("### ⚙️ Account")
        
        if st.button("🔐 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()

def render_analytics():
    """Render Analytics Dashboard"""
    st.subheader("📊 Advanced Analytics & Insights")
    
    tab1, tab2, tab3 = st.tabs(["🌍 Climate Impact", "💰 Financial Performance", "⚡ Risk Analytics"])
    
    with tab1:
        st.markdown("### Climate Impact Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total CO₂ Reduced", "45.6M MT", "+2.3M MT")
        with col2:
            st.metric("Renewable Energy Added", "12.5 GW", "+0.8 GW")
        with col3:
            st.metric("Green Jobs Created", "125,000", "+8,500")
        with col4:
            st.metric("Water Saved", "850M Liters", "+45M L")
        
        # Impact visualization
        col1, col2 = st.columns(2)
        
        with col1:
            sectors = ["Solar", "Wind", "Energy Efficiency", "Transport", "Waste"]
            co2_reduction = [35, 28, 20, 12, 5]
            
            fig = go.Figure(data=[go.Bar(x=sectors, y=co2_reduction, 
                                         marker_color=['#FFD700', '#87CEEB', '#90EE90', '#DDA0DD', '#F4A460'])])
            fig.update_layout(title="CO₂ Reduction by Sector (%)", yaxis_title="Percentage",
                            xaxis_title="Sector", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            months = pd.date_range(start='2024-01-01', periods=12, freq='M')
            impact_data = np.cumsum(np.random.uniform(1000, 5000, 12))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=impact_data, mode='lines+markers',
                                    name='Monthly Impact',
                                    line=dict(color='#2E7D32', width=3)))
            fig.update_layout(title="Cumulative Climate Impact", 
                            yaxis_title="Impact Units",
                            xaxis_title="Month", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Financial Performance Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Platform Revenue", "$15.2M", "+23%")
        with col2:
            st.metric("Transaction Volume", "$2.3B", "+18%")
        with col3:
            st.metric("Average Deal Size", "$45M", "+$5M")
        with col4:
            st.metric("Platform Fees", "1.2%", "-0.1%")
        
        # Revenue breakdown
        revenue_streams = ["Transaction Fees", "Management Fees", "Carry Interest", "Subscriptions", "Verification"]
        revenue_values = [40, 30, 15, 10, 5]
        
        fig = px.pie(values=revenue_values, names=revenue_streams, 
                    title="Revenue Stream Breakdown",
                    hole=0.4)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Risk Analytics Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Portfolio VaR (95%)", "$12.3M", "-$0.8M", delta_color="inverse")
        with col2:
            st.metric("Default Rate", "0.8%", "-0.2%", delta_color="inverse")
        with col3:
            st.metric("Liquidity Ratio", "2.3x", "+0.1x")
        with col4:
            st.metric("Currency Exposure", "15%", "-2%", delta_color="inverse")
        
        # Risk matrix
        st.markdown("### Risk Heat Map")
        
        risk_categories = ["Credit Risk", "Market Risk", "Operational Risk", "Regulatory Risk"]
        projects = ["Project A", "Project B", "Project C", "Project D"]
        
        risk_matrix = np.random.uniform(1, 5, (4, 4))
        
        fig = px.imshow(risk_matrix, 
                       labels=dict(x="Projects", y="Risk Categories", color="Risk Score"),
                       x=projects, y=risk_categories,
                       color_continuous_scale="RdYlGn_r",
                       aspect="auto")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# Main Application Controller
def main():
    """Main application controller"""
    
    # Check authentication
    if not st.session_state.authenticated:
        render_advanced_login()
        return
    
    # Render sidebar navigation
    render_sidebar()
    
    # Page routing
    if st.session_state.page == "Dashboard":
        render_dashboard()
    elif st.session_state.page == "Projects":
        render_projects()
    elif st.session_state.page == "Carbon Trading":
        render_carbon_trading()
    elif st.session_state.page == "De-risking":
        render_government_derisking()
    elif st.session_state.page == "Blockchain":
        render_blockchain_verification()
    elif st.session_state.page == "AI Advisory":
        render_ai_advisory()
    elif st.session_state.page == "SDG Tracker":
        render_sdg_tracker()
    elif st.session_state.page == "Analytics":
        render_analytics()
    else:
        render_dashboard()

# Run the application
if __name__ == "__main__":
    main()
