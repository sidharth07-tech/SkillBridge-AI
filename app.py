import streamlit as st
import os
import re
from dotenv import load_dotenv
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ADVANCED UI / CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    margin-bottom: 0;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
}

/* Cards */
.custom-card {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(148, 163, 184, 0.25);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
}

/* Score Card */
.score-card {
    text-align: center;
    background: linear-gradient(135deg, #1e3a8a, #312e81);
    padding: 30px;
    border-radius: 20px;
    margin: 20px 0;
    border: 1px solid #6366f1;
}

.score-number {
    font-size: 4rem;
    font-weight: bold;
    color: #67e8f9;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 55px;
    font-size: 18px;
    font-weight: bold;
    border: none;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
}

/* Input Fields */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div {
    border-radius: 10px !important;
}

/* Section headings */
h2, h3 {
    color: #e2e8f0;
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GEMINI API CONFIGURATION
# ============================================================

load_dotenv()

api_key = None

# Try Streamlit Cloud Secrets first
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


# If Streamlit Secrets doesn't work, try local .env
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")


# Stop if API key is missing
if not api_key:
    st.error("❌ Gemini API key not found.")
    st.info("Please configure GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()


# Create Gemini Client
try:
    client = genai.Client(api_key=api_key)

except Exception as e:
    st.error("❌ Unable to initialize Gemini API.")
    st.error(str(e))
    st.stop()


# ============================================================
# FUNCTIONS
# ============================================================

def extract_score(text):
    """
    Extract Skill Match Score from AI response.
    """

    patterns = [
        r"SKILL_MATCH_SCORE\s*:\s*(\d+)",
        r"Skill Match Score\s*:\s*(\d+)",
        r"(\d+)%"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            score = int(match.group(1))

            if 0 <= score <= 100:
                return score

    return 50


def get_score_message(score):

    if score >= 80:
        return "Excellent! You have a strong foundation for this career. 🚀"

    elif score >= 60:
        return "Good progress! A few important skills can make you stronger. 💪"

    elif score >= 40:
        return "You have a foundation, but you should focus on developing key skills. 📚"

    else:
        return "You are at the beginning of your journey. Follow the roadmap and keep learning! 🌱"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<h1 class="main-title">🎯 SkillBridge AI</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Your Skills. Your Path. Your Future.</p>',
    unsafe_allow_html=True
)


st.markdown("""
<div class="custom-card">

<h3>🤖 AI-Powered Career & Skill Development Assistant</h3>

<p>
Discover the skills required for your dream career, identify your skill gaps,
and receive a personalized learning roadmap designed for your career goals.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# USER INPUT SECTION
# ============================================================

st.markdown("## 👤 Build Your Career Profile")

col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "👤 Your Name",
        placeholder="Enter your name"
    )

    education = st.text_input(
        "🎓 Your Education",
        placeholder="Example: B.E Computer Science"
    )

    career_goal = st.text_input(
        "🎯 Desired Job Role",
        placeholder="Example: Data Analyst"
    )


with col2:

    experience_level = st.selectbox(
        "📊 Experience Level",
        [
            "Student / Beginner",
            "Fresher",
            "Intern",
            "1-2 Years Experience",
            "3+ Years Experience"
        ]
    )

    company = st.text_input(
        "🏢 Dream Company",
        placeholder="Example: Google, TCS, Microsoft"
    )

    learning_time = st.selectbox(
        "⏳ Weekly Learning Time",
        [
            "3-5 Hours",
            "5-10 Hours",
            "10-15 Hours",
            "15+ Hours"
        ]
    )


current_skills = st.text_area(
    "💻 Your Current Skills",
    placeholder="Example: Python, Java, SQL, Excel",
    height=120
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("---")

analyze = st.button(
    "🚀 Analyze My Skills & Build My Career Roadmap"
)


# ============================================================
# AI ANALYSIS
# ============================================================

if analyze:

    if not name or not education or not current_skills or not career_goal or not company:

        st.warning("⚠️ Please fill in all required fields.")

    else:

        prompt = f"""
You are SkillBridge AI, an intelligent Career and Skill Development Agent.

Analyze the following user profile carefully.

USER PROFILE:

Name: {name}

Education:
{education}

Current Skills:
{current_skills}

Desired Job Role:
{career_goal}

Experience Level:
{experience_level}

Target Company:
{company}

Available Weekly Learning Time:
{learning_time}


YOUR TASK:

Analyze the user's profile and provide personalized career guidance.

IMPORTANT:

First calculate an estimated Skill Match Score from 0 to 100.

Write the score EXACTLY in this format:

SKILL_MATCH_SCORE: number


Then provide the following sections.


## 🎯 Career Analysis

Explain whether the user's background is suitable for the desired career.


## 📊 Why This Score Was Given

Explain clearly why the Skill Match Score was assigned.


## ✅ Current Skills

List the user's strengths and relevant skills.


## ❌ Skills to Improve

List important missing or weak skills.


## 🏢 Target Company Preparation

Provide general preparation guidance for working toward opportunities at the target company.

Do NOT claim access to confidential company hiring requirements.

Clearly state that actual job requirements may vary.


## 📚 Personalized Learning Roadmap

Create a practical roadmap.

Divide it into:

### Phase 1: Foundation Skills

### Phase 2: Core Technical Skills

### Phase 3: Advanced Skills

### Phase 4: Projects and Portfolio

Make the roadmap suitable for the user's experience level and weekly learning time.


## 💡 Recommended Projects

Suggest 3 practical portfolio projects relevant to the desired job role.

For each project provide:

1. Project Name
2. Skills Used
3. Brief Description


## 💼 Suggested Job Roles

Suggest suitable beginner or entry-level roles.


## 🎯 Final Career Advice

Provide encouraging but realistic career advice.

Use simple language.

Do NOT guarantee employment.

Do NOT claim that completing the roadmap guarantees a job.

Keep the response structured, practical, personalized, and suitable for a student or beginner.
"""


        try:

            with st.spinner(
                "🤖 SkillBridge AI is analyzing your profile..."
            ):

                # ====================================================
                # GEMINI AI MODEL
                # ====================================================

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                analysis = response.text


            # ====================================================
            # SUCCESS MESSAGE
            # ====================================================

            st.success("🎉 Analysis Completed Successfully!")


            # ====================================================
            # SKILL MATCH SCORE
            # ====================================================

            score = extract_score(analysis)


            # Remove score line from displayed AI analysis
            analysis = re.sub(
                r"SKILL_MATCH_SCORE\s*:\s*\d+",
                "",
                analysis,
                flags=re.IGNORECASE
            )


            st.markdown(
                f"""
                <div class="score-card">

                <h2>📊 Skill Match Score</h2>

                <div class="score-number">
                {score}%
                </div>

                <p>
                Estimated compatibility between your current skills
                and your desired career.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.progress(score / 100)

            st.info(get_score_message(score))


            # ====================================================
            # DISCLAIMER
            # ====================================================

            st.caption(
                "⚠️ The Skill Match Score is an AI-generated estimate "
                "based on the information provided. It does not guarantee "
                "employment or represent official company hiring requirements."
            )


            # ====================================================
            # AI ANALYSIS RESULT
            # ====================================================

            st.markdown("---")

            st.markdown("## 🤖 Your Personalized Career Report")

            st.markdown(analysis)


            # ====================================================
            # DOWNLOAD REPORT
            # ====================================================

            report = f"""
SKILLBRIDGE AI - PERSONALIZED CAREER REPORT

Name: {name}

Education: {education}

Desired Job Role: {career_goal}

Target Company: {company}

SKILL MATCH SCORE: {score}%

--------------------------------------------------

{analysis}
"""


            st.download_button(
                label="📥 Download My Career Report",
                data=report,
                file_name="SkillBridge_AI_Career_Report.txt",
                mime="text/plain"
            )


        except Exception as e:

            st.error(
                "❌ Something went wrong while analyzing your profile."
            )

            st.error(str(e))

            st.info(
                "Please check your Gemini API key, internet connection, "
                "and API availability."
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown("---")

st.markdown("## ⚡ How SkillBridge AI Works")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("""
    ### 👤 1. Profile

    Enter your education,
    skills and career goal.
    """)


with col2:

    st.markdown("""
    ### 🤖 2. AI Analysis

    Our AI analyzes your
    career profile.
    """)


with col3:

    st.markdown("""
    ### 📊 3. Skill Gap

    Discover missing
    and important skills.
    """)


with col4:

    st.markdown("""
    ### 🚀 4. Roadmap

    Get a personalized
    learning plan.
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<hr>

🎯 <b>SkillBridge AI</b><br>

Your Skills • Your Path • Your Future

<br><br>

Developed for AI Hackathon | Labour Welfare & Skill Development

</div>
""", unsafe_allow_html=True)
