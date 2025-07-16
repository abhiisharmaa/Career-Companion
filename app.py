import streamlit as st
import plotly.graph_objects as go

# --- MODULE IMPORTS ---
# All functions are now imported from 'modules' directory.
from modules.resume_parser import parse_resume
from modules.jd_processor import extract_jd_skills
from modules.match_score import compare_skills
from modules.learning_advisor import generate_learning_resources
from modules.resume_booster import suggest_resume_improvements
from modules.cover_letter_agent import generate_cover_letter

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Career Companion",
    page_icon="🧠",
    layout="wide",
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #F0F2F6;
    }

    /* General card-like container style */
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlock"] {
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Increase font size for tabs */
    [data-testid="stTabs"] button {
        font-size: 18px;
    }

    /* Title styling */
    h1 {
        color: #1E3A8A; /* A deep blue */
        font-weight: bold;
    }

    /* Subheader styling */
    h2, h3 {
        color: #4B5563; /* A soft gray */
    }

    /* Primary button styling */
    .stButton > button[kind="primary"] {
        border-radius: 20px;
        border: 2px solid #1E3A8A;
        background-color: #1E3A8A;
        color: white;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 100%;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: white;
        color: #1E3A8A;
        border-color: #1E3A8A;
    }

    /* Secondary button styling */
     .stButton > button[kind="secondary"] {
        border-radius: 20px;
        border: 1px solid #D1D5DB;
        background-color: #FFFFFF;
        color: #374151;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        width: 100%;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #F9FAFB;
        color: #1E3A8A;
        border-color: #1E3A8A;
    }

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2111/2111494.png", width=80)  # Placeholder icon
    st.header("How It Works")
    st.write("""
    1.  **Upload** your resume in PDF format.
    2.  **Paste** the job description you're interested in.
    3.  **Analyze** to see your match score and skill gaps.
    4.  **Explore** the tabs for personalized resume feedback and a generated cover letter.
    """)
    st.divider()
    st.info("Built with ❤️ by Abhinandan")

# --- HEADER SECTION ---
st.title("🧠 AI Career Companion")
st.subheader("Match your resume to any job, get feedback, and generate a cover letter in seconds!")
st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("📄 Step 1: Your Resume")
        resume_file = st.file_uploader("Upload your Resume (PDF)", type="pdf", label_visibility="collapsed")

with col2:
    with st.container(border=True):
        st.subheader("🎯 Step 2: The Job Description")
        job_description = st.text_area("Paste the Job Description here", height=162, label_visibility="collapsed")

# --- ANALYSIS BUTTON ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🧪 Analyze My Fit", use_container_width=True, type="primary"):
    if not resume_file or not job_description:
        st.error("⚠️ Please upload a resume AND paste a job description before analyzing.")
    else:
        with st.spinner("🧠 Analyzing your resume and the job description... This may take a moment."):
            # Save uploaded file temporarily to be read by the parser
            with open("temp_resume.pdf", "wb") as f:
                f.write(resume_file.getbuffer())

            # --- Processing Logic using your imported functions ---
            resume_data = parse_resume("temp_resume.pdf")
            jd_skills = extract_jd_skills(job_description)

            # Store key data in session state for reuse across tabs
            st.session_state.resume_data = resume_data
            st.session_state.job_description = job_description
            st.session_state.jd_skills = jd_skills
            st.session_state.results = compare_skills(resume_data["skills"], jd_skills)
            st.success("Analysis Complete! Explore the results below.")

# --- RESULTS SECTION ---
if "results" in st.session_state:
    st.divider()
    results = st.session_state.results
    match_score = results['match_score']

    # Create tabs for different results
    tab1, tab2, tab3 = st.tabs(["📊 Match Analysis", "📈 Resume Feedback", "✍️ Cover Letter"])

    # --- TAB 1: MATCH ANALYSIS ---
    with tab1:
        st.header("Match Analysis Results")

        # Gauge Chart for Match Score
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number", value=match_score, number={'suffix': "%"},
            title={'text': "Compatibility Score"},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1E3A8A"},
                'steps': [
                    {'range': [0, 50], 'color': '#FEE2E2'},
                    {'range': [50, 75], 'color': '#FEF3C7'},
                    {'range': [75, 100], 'color': '#D1FAE5'}],
            }
        ))
        gauge_fig.update_layout(height=300)
        st.plotly_chart(gauge_fig, use_container_width=True)

        # Matched and Missing Skills
        col1, col2 = st.columns(2)
        with col1:
            st.info("✅ **Skills You Have**")
            st.write(", ".join(results['matched_skills']))
        with col2:
            st.warning("❌ **Skills to Build**")
            st.write(", ".join(results['missing_skills']))

        st.divider()

        # Learning Plan Generation
        st.subheader("📘 Personalized Learning Plan")
        if st.button("Show Me How to Build These Skills", use_container_width=True, type="secondary"):
            if results['missing_skills']:
                with st.spinner("👩‍🏫 Generating learning resources..."):
                    learning_plan = generate_learning_resources(results['missing_skills'])
                    st.session_state.learning_plan = learning_plan
            else:
                st.info("You have all the required skills! No learning plan needed.")
                st.balloons()
                if 'learning_plan' in st.session_state:
                    del st.session_state.learning_plan

        if 'learning_plan' in st.session_state:
            st.markdown(st.session_state.learning_plan)
            st.download_button(
                "📥 Download Plan", st.session_state.learning_plan, "learning_plan.md",
                use_container_width=True
            )

    # --- TAB 2: RESUME FEEDBACK ---
    with tab2:
        st.header("Resume Improvement Suggestions")
        st.write("Get AI-powered tips on how to tailor your resume specifically for this job description.")

        if st.button("🪄 Suggest Resume Improvements", use_container_width=True, type="secondary"):
            with st.spinner("🔍 Analyzing your resume for improvement opportunities..."):
                tips = suggest_resume_improvements(
                    st.session_state.resume_data["raw_text"],
                    st.session_state.job_description
                )
                st.session_state.resume_tips = tips

        if "resume_tips" in st.session_state:
            st.markdown(st.session_state.resume_tips)
            st.download_button(
                "📥 Download Tips", st.session_state.resume_tips, "resume_improvements.md",
                use_container_width=True
            )

    # --- TAB 3: COVER LETTER ---
    with tab3:
        st.header("AI-Generated Cover Letter")
        st.write(
            "Generate a draft cover letter that highlights your matching skills and addresses the job requirements.")

        if st.button("✍️ Generate My Cover Letter", use_container_width=True, type="secondary"):
            with st.spinner("✍️ Crafting your personalized cover letter..."):
                cover_letter = generate_cover_letter(
                    st.session_state.resume_data["raw_text"],
                    st.session_state.job_description
                )
                st.session_state.cover_letter = cover_letter

        if "cover_letter" in st.session_state:
            st.text_area(
                "Your letter is ready:",
                value=st.session_state.cover_letter,
                height=400,
                label_visibility="collapsed"
            )
            st.download_button(
                "📩 Download Cover Letter", st.session_state.cover_letter, "cover_letter.txt",
                use_container_width=True
            )