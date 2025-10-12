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

# Enhanced Authentication System
def authenticate_user(username: str, password: str, user_type: str) -> bool:
    """Enhanced authentication system with role-based access"""
    mock_users = {
        'investor': {'password': 'investor123', 'type': 'Investor', 'name': 'Global Investment Fund'},
        'developer': {'password': 'developer123', 'type': 'Developer', 'name': 'GreenTech Solutions'},
        'admin': {'password': 'admin123', 'type': 'Admin', 'name': 'Platform Administrator'},
        'government': {'password': 'gov123', 'type': 'Government', 'name': 'Climate Finance Agency'},
        'demo': {'password': 'demo123', 'type': 'Investor', 'name': 'Demo Investor'}
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
    return False

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
        ("👥 Registered Investors", "3,847", "+234", "normal"),
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

def render_advanced_login():
    """Render enhanced login page"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">🌱 Welcome to GREENSTRIKAS</h1>
        <p style="margin: 0.5rem 0 0 0;">Transforming Climate Finance Through Innovation</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            Integrated Climate Finance Ecosystem | Blockchain Secured | AI Powered
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Sign In to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            user_type = st.selectbox("🎯 Account Type", ["Investor", "Developer", "Government", "Admin"])
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("🚀 Sign In", use_container_width=True)
            with col_b:
                demo = st.form_submit_button("👁️ Demo Access", use_container_width=True)
            
            if submit:
                if authenticate_user(username, password, user_type):
                    st.success(f"Welcome back, {st.session_state.user_display_name}!")
