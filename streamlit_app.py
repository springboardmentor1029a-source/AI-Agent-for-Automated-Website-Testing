"""
Streamlit Deployment App for AI Website Testing Agent
Recreated with the same UI as the HTML version
"""

import streamlit as st
import os
import base64
from dotenv import load_dotenv
from ai_agent import AIWebsiteTester

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Agent - Automated Website Testing",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS
def inject_custom_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #6C5CE7;
        --accent-color: #00D2FF;
        --accent-secondary: #A29BFE;
        --dark-bg: #1a1f35;
        --light-bg: #F0F4F8;
        --text-dark: #0f172a;
        --text-light: #64748b;
        --white: #ffffff;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .main {
        padding: 0 !important;
    }
    
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation */
    .navbar {
        background: var(--white);
        box-shadow: var(--shadow);
        position: sticky;
        top: 0;
        z-index: 1000;
        padding: 1rem 0;
        margin-bottom: 0;
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .nav-logo-badge {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-lg);
    }
    
    .nav-logo-initial {
        color: var(--white);
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.03em;
    }
    
    .nav-brand-text {
        display: flex;
        flex-direction: column;
        line-height: 1.2;
    }
    
    .nav-brand-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-dark);
    }
    
    .nav-brand-subtitle {
        font-size: 0.75rem;
        color: var(--text-light);
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, 
            rgba(74, 144, 226, 0.2) 0%,
            rgba(108, 92, 231, 0.25) 50%,
            rgba(0, 210, 255, 0.15) 100%
        );
        padding: 80px 20px 60px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container {
        max-width: 1200px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(0, 1.1fr);
        gap: 3rem;
        align-items: center;
    }
    
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.15), rgba(108, 92, 231, 0.15));
        color: var(--primary-color);
        font-size: 0.85rem;
        font-weight: 600;
        width: fit-content;
        border: 1px solid rgba(74, 144, 226, 0.2);
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.2;
        color: var(--text-dark);
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-light);
        max-width: 520px;
        margin-bottom: 1.5rem;
    }
    
    .hero-actions {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-top: 0.5rem;
    }
    
    .hero-note {
        font-size: 0.9rem;
        color: var(--text-light);
    }
    
    .hero-card {
        width: 100%;
        max-width: 420px;
        border-radius: 16px;
        background: var(--white);
        box-shadow: var(--shadow-lg);
        overflow: hidden;
        border: 1px solid rgba(15, 23, 42, 0.06);
    }
    
    .hero-card-header {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 0.75rem 1rem;
        background: #0f172a;
        color: #e5e7eb;
        font-size: 0.8rem;
    }
    
    .dot {
        width: 10px;
        height: 10px;
        border-radius: 999px;
    }
    
    .dot.red { background: #ef4444; }
    .dot.yellow { background: #facc15; }
    .dot.green { background: #22c55e; }
    
    .hero-card-title {
        margin-left: 0.5rem;
        opacity: 0.85;
    }
    
    .hero-card-body {
        padding: 1.1rem 1.3rem 1.2rem;
        font-size: 0.92rem;
        color: var(--text-dark);
    }
    
    .hero-card-line {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-bottom: 0.75rem;
    }
    
    .hero-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--text-light);
    }
    
    .hero-value {
        font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
        font-size: 0.9rem;
        padding: 6px 8px;
        border-radius: 6px;
        background: #0f172a;
        color: #e5e7eb;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        background: #dcfce7;
        color: #166534;
        font-weight: 500;
    }
    
    /* Section Styles */
    .section {
        padding: 80px 20px;
    }
    
    .section-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-title {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 3rem;
        color: var(--text-dark);
        font-weight: 700;
    }
    
    /* About Section */
    .about {
        background: var(--light-bg);
    }
    
    .about-content {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 3rem;
        align-items: start;
    }
    
    .about-text p {
        margin-bottom: 1.5rem;
        color: var(--text-light);
        font-size: 1.1rem;
    }
    
    .about-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
    
    .stat-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .stat-card i {
        font-size: 2.5rem;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .stat-card h3 {
        font-size: 2rem;
        color: var(--text-dark);
        margin-bottom: 0.5rem;
    }
    
    .stat-card p {
        color: var(--text-light);
    }
    
    /* Features Section */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
    }
    
    .feature-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: var(--shadow);
        border-top: 4px solid var(--primary-color);
    }
    
    .feature-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
    }
    
    .feature-icon i {
        font-size: 1.5rem;
        color: var(--white);
    }
    
    .feature-card h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: var(--text-dark);
    }
    
    .feature-card p {
        color: var(--text-light);
        line-height: 1.8;
    }
    
    /* How It Works Section */
    .how-it-works {
        background: var(--light-bg);
    }
    
    .workflow {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .workflow-step {
        display: flex;
        gap: 2rem;
        margin-bottom: 3rem;
        align-items: start;
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        color: var(--white);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        flex-shrink: 0;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    .step-content h3 {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: var(--text-dark);
    }
    
    .step-content p {
        color: var(--text-light);
        line-height: 1.8;
    }
    
    /* Demo Section */
    .demo {
        background: var(--light-bg);
    }
    
    .demo-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }
    
    .demo-form {
        background: var(--white);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: var(--shadow);
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-group label {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: var(--text-dark);
    }
    
    .form-group label i {
        color: var(--primary-color);
    }
    
    /* Footer */
    .footer {
        background: var(--dark-bg);
        color: var(--white);
        padding: 3rem 20px 1rem;
    }
    
    .footer-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-section h3,
    .footer-section h4 {
        margin-bottom: 1rem;
    }
    
    .footer-section ul {
        list-style: none;
    }
    
    .footer-section ul li {
        margin-bottom: 0.5rem;
    }
    
    .footer-section a {
        color: var(--white);
        text-decoration: none;
        opacity: 0.8;
    }
    
    .footer-section i {
        margin-right: 8px;
    }
    
    .footer-bottom {
        text-align: center;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        opacity: 0.8;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 2rem;
        }
        .about-content {
            grid-template-columns: 1fr;
        }
        .demo-container {
            grid-template-columns: 1fr;
        }
        .workflow-step {
            flex-direction: column;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Initialize AI agent
@st.cache_resource
def get_ai_agent():
    """Initialize and cache the AI agent"""
    try:
        agent = AIWebsiteTester()
        return agent, None
    except Exception as e:
        return None, str(e)

# Inject CSS
inject_custom_css()

# Navigation
nav_html = """
<div class="navbar">
    <div class="nav-container">
        <div class="nav-brand">
            <div class="nav-logo-badge">
                <span class="nav-logo-initial">AI</span>
            </div>
            <div class="nav-brand-text">
                <span class="nav-brand-title">AI Test Agent</span>
                <span class="nav-brand-subtitle">Automated Web Testing</span>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)

# Hero Section
hero_html = """
<div class="hero">
    <div class="hero-container">
        <div class="hero-grid">
            <div class="hero-left">
                <div class="hero-pill">AI-Powered Website Testing</div>
                <h1 class="hero-title">Test any website using plain English instructions.</h1>
                <p class="hero-subtitle">
                    Type what you want to check — like login, search, or forms — and the agent automatically
                    generates and runs Playwright tests for you.
                </p>
                <div class="hero-actions">
                    <span class="hero-note">No test scripts required.</span>
                </div>
            </div>
            <div class="hero-right">
                <div class="hero-card">
                    <div class="hero-card-header">
                        <span class="dot red"></span>
                        <span class="dot yellow"></span>
                        <span class="dot green"></span>
                        <span class="hero-card-title">Example test instruction</span>
                    </div>
                    <div class="hero-card-body">
                        <p class="hero-card-line">
                            <span class="hero-label">Website</span>
                            <span class="hero-value">https://amazon.com</span>
                        </p>
                        <p class="hero-card-line">
                            <span class="hero-label">Instruction</span>
                            <span class="hero-value">Go to Amazon, search for "iphone 15", and check that results appear.</span>
                        </p>
                        <div class="hero-status">
                            <span class="status-badge"><i class="fas fa-check-circle"></i> Test ready to run</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# About Section
about_html = """
<div class="section about">
    <div class="section-container">
        <h2 class="section-title">About the Project</h2>
        <div class="about-content">
            <div class="about-text">
                <p>
                    The AI Agent for Automated Website Testing is an intelligent testing solution that leverages 
                    artificial intelligence and natural language processing to automate website testing. This innovative 
                    tool allows users to describe test scenarios in plain English, and the AI agent automatically 
                    converts these descriptions into executable test cases.
                </p>
                <p>
                    Traditional website testing requires extensive coding knowledge and time-consuming test script 
                    development. Our AI-powered solution eliminates these barriers by understanding natural language 
                    instructions and performing comprehensive website testing automatically.
                </p>
                <p>
                    The system combines cutting-edge AI technologies with robust web automation frameworks to provide 
                    accurate, reliable, and efficient testing capabilities. Whether you're testing functionality, 
                    performance, accessibility, or user experience, our AI agent handles it all.
                </p>
            </div>
            <div class="about-stats">
                <div class="stat-card">
                    <i class="fas fa-check-circle"></i>
                    <h3>100%</h3>
                    <p>Automated</p>
                </div>
                <div class="stat-card">
                    <i class="fas fa-language"></i>
                    <h3>Natural</h3>
                    <p>Language</p>
                </div>
                <div class="stat-card">
                    <i class="fas fa-clock"></i>
                    <h3>Fast</h3>
                    <p>Execution</p>
                </div>
                <div class="stat-card">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Reliable</h3>
                    <p>Results</p>
                </div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(about_html, unsafe_allow_html=True)

# Features Section
features_html = """
<div class="section">
    <div class="section-container">
        <h2 class="section-title">Project Features</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-comments"></i></div>
                <h3>Natural Language Processing</h3>
                <p>Describe test scenarios in plain English. The AI understands your instructions and converts them into test cases automatically.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-globe"></i></div>
                <h3>Multi-Browser Support</h3>
                <p>Test your websites across different browsers including Chrome, Firefox, Safari, and Edge for comprehensive coverage.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-mobile-alt"></i></div>
                <h3>Responsive Testing</h3>
                <p>Automatically test websites on various device sizes and screen resolutions to ensure mobile responsiveness.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
                <h3>Performance Analysis</h3>
                <p>Measure page load times, analyze performance metrics, and identify bottlenecks in your website.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-bug"></i></div>
                <h3>Bug Detection</h3>
                <p>Automatically detect broken links, JavaScript errors, console errors, and other common website issues.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-file-alt"></i></div>
                <h3>Detailed Reports</h3>
                <p>Generate comprehensive test reports with screenshots, error logs, and actionable insights for debugging.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-universal-access"></i></div>
                <h3>Accessibility Testing</h3>
                <p>Check WCAG compliance and identify accessibility issues to ensure your website is usable by everyone.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-sync"></i></div>
                <h3>Continuous Testing</h3>
                <p>Schedule automated tests to run continuously and get notified when issues are detected.</p>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(features_html, unsafe_allow_html=True)

# How It Works Section
how_it_works_html = """
<div class="section how-it-works">
    <div class="section-container">
        <h2 class="section-title">How It Works</h2>
        <div class="workflow">
            <div class="workflow-step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>Enter Website URL</h3>
                    <p>Provide the URL of the website you want to test. The system supports any publicly accessible website.</p>
                </div>
            </div>
            <div class="workflow-step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>Describe Test Scenario</h3>
                    <p>Write your test requirements in natural language. For example: "Check if the login button works" or "Verify all images load correctly".</p>
                </div>
            </div>
            <div class="workflow-step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>AI Processing</h3>
                    <p>The AI agent analyzes your instructions using NLP, understands the intent, and generates appropriate test cases.</p>
                </div>
            </div>
            <div class="workflow-step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h3>Automated Execution</h3>
                    <p>The system automatically executes the tests using web automation tools, interacting with the website as a real user would.</p>
                </div>
            </div>
            <div class="workflow-step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <h3>Results & Reports</h3>
                    <p>Receive detailed test results with screenshots, error logs, performance metrics, and recommendations for improvements.</p>
                </div>
            </div>
        </div>
    </div>
</div>
"""
st.markdown(how_it_works_html, unsafe_allow_html=True)

# Demo Section
st.markdown('<div class="section demo"><div class="section-container"><h2 class="section-title">Try It Now</h2><div class="demo-container">', unsafe_allow_html=True)

# Initialize agent
ai_agent, error = get_ai_agent()

if error:
    st.warning(f"⚠️ AI Agent initialization: {error}")
    st.info("💡 The agent will work in fallback mode without OpenAI API")
    ai_agent = None

# Create two columns for form and results
col_form, col_results = st.columns(2)

with col_form:
    st.markdown('<div class="demo-form">', unsafe_allow_html=True)
    
    with st.form("test_form"):
        st.markdown('<div class="form-group"><label><i class="fas fa-link"></i> Website URL</label></div>', unsafe_allow_html=True)
        website_url = st.text_input(
            "",
            placeholder="https://amazon.com",
            key="website_url",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="form-group"><label><i class="fas fa-comment-dots"></i> Test Instruction (Natural Language)</label></div>', unsafe_allow_html=True)
        test_instruction = st.text_area(
            "",
            placeholder='Example: Check if all images on the homepage load correctly and verify the contact form submission works.',
            height=120,
            key="test_instruction",
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="form-group"><label><i class="fas fa-globe"></i> Browser</label></div>', unsafe_allow_html=True)
        browser = st.selectbox(
            "",
            ["chrome", "firefox", "webkit"],
            index=0,
            key="browser",
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("🚀 Run Test", use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_results:
    st.markdown('<div class="demo-results" id="results">', unsafe_allow_html=True)
    
    # Run test when form is submitted
    if submitted:
        if not ai_agent:
            st.error("AI Agent not available. Please check your configuration.")
        elif not website_url or not test_instruction:
            st.warning("⚠️ Please fill in both Website URL and Test Instruction")
        else:
            # Validate URL
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            # Show progress
            with st.spinner("🔄 Running test... This may take a few moments"):
                try:
                    # Run the test
                    result = ai_agent.run_test(website_url, test_instruction, browser)
                    
                    # Display results
                    st.markdown("---")
                    st.header("📊 Test Results")
                    
                    # Status
                    if result.get("status") == "success":
                        st.success(f"✅ Test Passed")
                    else:
                        st.error(f"❌ Test Failed")
                    
                    # Test details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Website", result.get("websiteUrl", "N/A"))
                    with col2:
                        st.metric("Browser", result.get("browser", "N/A"))
                    
                    st.markdown(f"**Test Instruction:** {result.get('testInstruction', 'N/A')}")
                    
                    # Results
                    if result.get("results"):
                        st.subheader("📋 Results")
                        for res in result["results"]:
                            st.markdown(f"- {res}")
                    
                    # Validations
                    if result.get("validations"):
                        st.subheader("✅ Validations")
                        for val in result["validations"]:
                            status_icon = "✅" if val.get("status") == "pass" else "⚠️" if val.get("status") == "warning" else "❌"
                            st.markdown(f"{status_icon} **{val.get('type', 'N/A')}**: {val.get('message', 'N/A')}")
                    
                    # Screenshots
                    if result.get("screenshots"):
                        st.subheader("📸 Screenshots")
                        screenshots = result["screenshots"]
                        # Filter duplicates
                        seen = set()
                        unique_screenshots = []
                        for ss in screenshots:
                            if ss.get("name") and ss.get("name") not in seen and ss.get("base64"):
                                seen.add(ss.get("name"))
                                unique_screenshots.append(ss)
                        
                        if unique_screenshots:
                            cols = st.columns(min(len(unique_screenshots), 3))
                            for idx, screenshot in enumerate(unique_screenshots):
                                with cols[idx % len(cols)]:
                                    st.image(
                                        f"data:image/png;base64,{screenshot.get('base64')}",
                                        caption=screenshot.get("name", f"Screenshot {idx + 1}"),
                                        use_container_width=True
                                    )
                    
                    # Performance metrics
                    if result.get("performance"):
                        st.subheader("⚡ Performance Metrics")
                        perf = result["performance"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Load Time", f"{perf.get('loadTime', 0)}ms")
                        with col2:
                            st.metric("Page Size", f"{perf.get('pageSize', 'N/A')}KB")
                    
                    # Error details
                    if result.get("error"):
                        st.error(f"❌ Error: {result.get('error')}")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.exception(e)
    else:
        st.markdown('''
        <div class="results-placeholder">
            <i class="fas fa-clipboard-list"></i>
            <p>Test results will appear here</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div></div>', unsafe_allow_html=True)

# Footer
footer_html = """
<div class="footer">
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-section">
                <h3>AI Test Agent</h3>
                <p>Revolutionizing website testing with AI-powered automation.</p>
            </div>
            <div class="footer-section">
                <h4>Quick Links</h4>
                <ul>
                    <li><a href="#about">About</a></li>
                    <li><a href="#features">Features</a></li>
                    <li><a href="#how-it-works">How It Works</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Contact</h4>
                <ul>
                    <li><i class="fas fa-envelope"></i> support@aitestagent.com</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 AI Test Agent. All rights reserved.</p>
        </div>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
