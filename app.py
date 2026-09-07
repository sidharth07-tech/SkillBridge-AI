import streamlit as st
import os
import re
from dotenv import load_dotenv
from google import genai


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# =========================================================
# SESSION STATE
# =========================================================

if "theme" not in st.session_state:
    st.session_state.theme = "Dark 🌙"

if "result" not in st.session_state:
    st.session_state.result = None

if "score" not in st.session_state:
    st.session_state.score = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🎯 SkillBridge AI")

    st.markdown(
        """
        <div style="opacity:0.7;">
        AI-Powered Career & Skill Development Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🎨 Appearance")

    theme = st.radio(
        "Choose your theme",
        ["🌙 Dark Mode", "☀️ Light Mode"],
        label_visibility="collapsed"
    )

    if theme == "🌙 Dark Mode":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

    st.divider()

    st.markdown("### 🚀 How It Works")

    st.markdown("""
    **1️⃣ Enter your profile**

    **2️⃣ Choose your career**

    **3️⃣ Select target company**

    **4️⃣ AI analyzes your skills**

    **5️⃣ Get your roadmap**
    """)

    st.divider()

    st.caption("Powered by Google Gemini AI 🤖")


# =========================================================
# THEME COLORS
# =========================================================

if st.session_state.theme == "dark":

    bg = "#0B1120"
    card = "#151E2E"
    card_2 = "#1B263B"
    text = "#F8FAFC"
    secondary = "#94A3B8"
    border = "#293548"

    gradient_1 = "#6366F1"
    gradient_2 = "#8B5CF6"

else:

    bg = "#F3F6FB"
    card = "#FFFFFF"
    card_2 = "#F8FAFC"
    text = "#172033"
    secondary = "#64748B"
    border = "#E2E8F0"

    gradient_1 = "#4F46E5"
    gradient_2 = "#7C3AED"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(f"""
<style>

/* ===============================
   GLOBAL
================================ */

.stApp {{
    background:
        radial-gradient(
            circle at top right,
            {gradient_1}22,
            transparent 35%
        ),
        {bg};
    color: {text};
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}}


/* ===============================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {{
    background-color: {card};
    border-right: 1px solid {border};
}}


/* ===============================
   HERO SECTION
================================ */

.hero {{
    padding: 55px 40px;
    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            {gradient_1},
            {gradient_2}
        );

    color: white;

    margin-bottom: 30px;

    box-shadow:
        0px 15px 40px rgba(0,0,0,0.18);
}}

.hero-title {{
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 10px;
}}

.hero-subtitle {{
    font-size: 20px;
    opacity: 0.9;
}}

.hero-description {{
    font-size: 16px;
    opacity: 0.8;
    margin-top: 20px;
}}


/* ===============================
   CARDS
================================ */

.custom-card {{
    background: {card};

    border:
        1px solid {border};

    border-radius: 22px;

    padding: 28px;

    margin-bottom: 25px;

    box-shadow:
        0px 8px 30px rgba(0,0,0,0.06);
}}


/* ===============================
   INPUT LABELS
================================ */

label {{
    color: {text} !important;
    font-weight: 600 !important;
}}


/* ===============================
   INPUT BOXES
================================ */

.stTextInput input,
.stTextArea textarea {{
    border-radius: 12px !important;
}}


/* ===============================
   BUTTON
================================ */

.stButton > button {{

    background:
        linear-gradient(
            135deg,
            {gradient_1},
            {gradient_2}
        ) !important;

    color: white !important;

    border: none !important;

    border-radius: 14px !important;

    padding: 15px !important;

    font-size: 18px !important;

    font-weight: 700 !important;

    transition: 0.3s;

    box-shadow:
        0px 8px 20px {gradient_1}55;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
}}


/* ===============================
   SCORE CARD
================================ */

.score-container {{

    background:
        linear-gradient(
            135deg,
            {gradient_1}22,
            {gradient_2}22
        );

    border:
        1px solid {gradient_1}55;

    border-radius: 25px;

    padding: 35px;

    text-align: center;

    margin-bottom: 25px;
}}

.score-number {{

    font-size: 70px;

    font-weight: 800;

    color: {gradient_1};
}}

.score-label {{

    font-size: 24px;

    font-weight: 700;
}}

.score-description {{

    color: {secondary};

    margin-top: 10px;
}}


/* ===============================
   SECTION TITLE
================================ */

.section-title {{

    font-size: 27px;

    font-weight: 750;

    margin-bottom: 15px;
}}


/* ===============================
   FOOTER
================================ */

.footer {{

    text-align: center;

    padding: 30px;

    color: {secondary};

    margin-top: 40px;
}}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(f"""
<div class="hero">

<div class="hero-title">
🎯 SkillBridge AI
</div>

<div class="hero-subtitle">
Your Skills. Your Path. Your Future.
</div>

<div class="hero-description">
Discover your skill gaps, measure your career readiness,
and receive a personalized learning roadmap powered by Artificial Intelligence.
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FEATURE CARDS
# =========================================================

feature1, feature2, feature3 = st.columns(3)

with feature1:
    st.metric(
        "🎯 Career Analysis",
        "AI Powered"
    )

with feature2:
    st.metric(
        "📊 Skill Match",
        "Personalized"
    )

with feature3:
    st.metric(
        "📚 Learning Path",
        "Step-by-Step"
    )


st.write("")
st.write("")


# =========================================================
# USER PROFILE
# =========================================================

st.markdown(
    '<div class="section-title">👤 Build Your Career Profile</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="custom-card">',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "👤 Your Name",
        placeholder="Example: Sidharth"
    )

    education = st.text_input(
        "🎓 Your Education",
        placeholder="Example: B.E Computer Science"
    )


with col2:

    career_goal = st.text_input(
        "🎯 Desired Job Role",
        placeholder="Example: Data Analyst"
    )

    company = st.text_input(
        "🏢 Target Company",
        placeholder="Example: Google, Microsoft, TCS"
    )


current_skills = st.text_area(
    "💻 Your Current Skills",
    placeholder="Example: Python, Java, SQL, HTML",
    height=140
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze = st.button(
    "🚀 Analyze My Career Profile",
    use_container_width=True
)


# =========================================================
# AI ANALYSIS
# =========================================================

if analyze:

    if not all([
        name,
        education,
        current_skills,
        career_goal,
        company
    ]):

        st.warning(
            "⚠️ Please complete all fields before analyzing your profile."
        )

    else:

        prompt = f"""
You are SkillBridge AI, an intelligent Career and Skill Development Agent.

Analyze the following profile:

Name: {name}

Education: {education}

Current Skills: {current_skills}

Desired Job Role: {career_goal}

Target Company: {company}


YOUR TASK:

1. Analyze the user's education and current skills.

2. Identify important skills generally required for the desired job role.

3. Compare current skills with the commonly required skills.

4. Identify skill gaps.

5. Calculate an estimated Skill Match Score between 0 and 100.


IMPORTANT:

Start your response EXACTLY like this:

SKILL_MATCH_SCORE: number


Replace number with only a number from 0 to 100.


Then provide:


## 🎯 Career Analysis


## ✅ Current Skills


## ❌ Skills to Improve


## 🏢 Target Company Preparation

Give general preparation advice.

Company-specific hiring requirements may vary.


## 📚 Personalized Learning Roadmap

Give a clear step-by-step roadmap.


## 💡 Recommended Projects

Suggest three practical projects.


## 💼 Suggested Job Roles


RULES:

- Keep responses beginner-friendly.
- Be practical and encouraging.
- Do not guarantee employment.
- The Skill Match Score is only an estimate.
- Do not claim access to confidential company requirements.
"""

        try:

            with st.spinner(
                "🤖 SkillBridge AI is analyzing your career profile..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

            result = response.text


            # =========================================================
            # EXTRACT SCORE
            # =========================================================

            score_match = re.search(
                r"SKILL_MATCH_SCORE:\s*(\d+)",
                result,
                re.IGNORECASE
            )


            if score_match:

                score = int(score_match.group(1))

                score = max(
                    0,
                    min(score, 100)
                )

                result = re.sub(
                    r"SKILL_MATCH_SCORE:\s*\d+\s*",
                    "",
                    result,
                    flags=re.IGNORECASE
                )

                st.session_state.score = score


            st.session_state.result = result


        except Exception as e:

            st.error(
                "❌ Something went wrong while analyzing your profile."
            )

            st.error(str(e))


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.result:

    st.write("")
    st.divider()

    st.markdown(
        '<div class="section-title">📊 Your Career Readiness</div>',
        unsafe_allow_html=True
    )


    # =========================================================
    # SCORE
    # =========================================================

    if st.session_state.score is not None:

        score = st.session_state.score

        st.markdown(f"""
        <div class="score-container">

        <div class="score-label">
        🎯 Skill Match Score
        </div>

        <div class="score-number">
        {score}%
        </div>

        <div class="score-description">
        Estimated compatibility between your current skills
        and your selected career path.
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.progress(score)


        if score >= 75:

            st.success(
                "🎉 Excellent! You already have a strong foundation."
            )

        elif score >= 50:

            st.info(
                "👍 Good progress! Focus on a few important skill gaps."
            )

        else:

            st.warning(
                "🚀 You have a starting foundation. "
                "Follow the roadmap to improve your career readiness."
            )


    # =========================================================
    # ANALYSIS CARD
    # =========================================================

    st.write("")

    st.markdown(
        '<div class="section-title">🤖 Personalized Career Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="custom-card">',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state.result)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =========================================================
    # DOWNLOAD BUTTON
    # =========================================================

    st.download_button(
        label="📥 Download My Career Report",
        data=st.session_state.result,
        file_name="SkillBridge_AI_Career_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

🎯 <b>SkillBridge AI</b>

<br><br>

AI-Powered Career & Skill Development Assistant

<br>

Your Skills • Your Path • Your Future

</div>
""", unsafe_allow_html=True)