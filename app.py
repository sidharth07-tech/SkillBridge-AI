import streamlit as st
import os
import time
import re
from dotenv import load_dotenv
from google import genai


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Streamlit Cloud Secrets support
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #111827;
    color: white;
}

.main {
    background-color: #111827;
}

h1, h2, h3 {
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #2b2d38;
    color: white;
    border-radius: 10px;
}

div[data-testid="stSelectbox"] div {
    border-radius: 10px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 25px;
    font-weight: bold;
}

.result-box {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    "<h1 style='text-align: center;'>🎯 SkillBridge AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size:18px;'>"
    "Your Skills. Your Path. Your Future."
    "</p>",
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# INTRODUCTION BOX
# =========================================================

st.markdown("""
<div class="result-box">

<h2>🤖 AI-Powered Career & Skill Development Assistant</h2>

<p style="font-size:17px;">
Discover the skills required for your dream career, identify your skill gaps,
and receive a personalized learning roadmap designed for your career goals.
</p>

</div>
""", unsafe_allow_html=True)


st.write("")
st.write("")


# =========================================================
# PROFILE FORM
# =========================================================

st.markdown("# 👥 Build Your Career Profile")

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

    job_role = st.text_input(
        "🎯 Desired Job Role",
        placeholder="Example: Data Analyst"
    )


with col2:

    experience = st.selectbox(
        "📊 Experience Level",
        [
            "Student / Beginner",
            "Fresher",
            "0-1 Years Experience",
            "1-3 Years Experience",
            "3+ Years Experience"
        ]
    )

    company = st.text_input(
        "🏢 Dream Company",
        placeholder="Example: Google, TCS, Microsoft"
    )

    learning_time = st.selectbox(
        "⌛ Weekly Learning Time",
        [
            "3-5 Hours",
            "5-10 Hours",
            "10-15 Hours",
            "15+ Hours"
        ]
    )


skills = st.text_area(
    "💻 Your Current Skills",
    placeholder="Example: Python, Java, SQL, Excel"
)


st.write("")
st.write("")


# =========================================================
# LOCAL FALLBACK ANALYSIS
# =========================================================

def create_fallback_analysis(job_role, skills, company):

    skills_list = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    role_lower = job_role.lower()

    if "data" in role_lower and "analyst" in role_lower:
        required_skills = [
            "Advanced Excel",
            "SQL",
            "Python",
            "Power BI or Tableau",
            "Statistics",
            "Data Visualization"
        ]

    elif "software" in role_lower or "developer" in role_lower:
        required_skills = [
            "Programming Language",
            "Data Structures and Algorithms",
            "Object Oriented Programming",
            "Git and GitHub",
            "Database Management",
            "Projects and Problem Solving"
        ]

    elif "web" in role_lower:
        required_skills = [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Backend Development",
            "Git and GitHub"
        ]

    elif "ai" in role_lower or "machine learning" in role_lower:
        required_skills = [
            "Python",
            "Mathematics and Statistics",
            "Machine Learning",
            "Data Analysis",
            "Deep Learning Basics",
            "AI Projects"
        ]

    else:
        required_skills = [
            "Communication Skills",
            "Technical Fundamentals",
            "Problem Solving",
            "Industry Knowledge",
            "Projects",
            "Interview Preparation"
        ]

    current_skills = ", ".join(skills_list)

    missing_skills = []

    for required in required_skills:

        found = False

        for user_skill in skills_list:
            if required.lower() in user_skill.lower():
                found = True

        if not found:
            missing_skills.append(required)

    if len(missing_skills) == 0:
        missing_skills = [
            "Advanced Projects",
            "Interview Preparation",
            "Industry-Level Experience"
        ]

    company_text = company if company.strip() else "your target companies"

    result = f"""

## 🎯 Career Analysis

Your selected career goal is **{job_role}**.

You currently have skills in:

**{current_skills if current_skills else "Skills need to be added"}**

Your learning journey should focus on improving the technical and practical skills
required for a **{job_role}** role.

Since you are interested in **{company_text}**, you should also focus on
strong projects, problem-solving skills, communication, and interview preparation.

---

## ✅ Current Skills

{chr(10).join([f"- {skill}" for skill in skills_list]) if skills_list else "- No skills entered"}

---

## ❌ Skills to Improve

{chr(10).join([f"- {skill}" for skill in missing_skills])}

---

## 📚 Personalized Learning Roadmap

### Step 1: Strengthen Your Fundamentals

Focus on the basic concepts required for **{job_role}**.

### Step 2: Learn Missing Technical Skills

Start learning:

{chr(10).join([f"- {skill}" for skill in missing_skills[:3]])}

### Step 3: Build Practical Projects

Create at least **2-3 projects** related to **{job_role}**.

### Step 4: Improve Your Portfolio

Upload your projects to GitHub and create a strong resume.

### Step 5: Prepare for Interviews

Practice:

- Technical questions
- Problem-solving
- Communication skills
- Mock interviews

---

## 💼 Suggested Entry-Level Job Roles

- Junior {job_role}
- {job_role} Intern
- Trainee
- Associate

---

## 🏢 Company Preparation Advice

For companies like **{company_text}**, focus on:

- Strong fundamentals
- Practical projects
- Problem-solving
- Communication
- Resume preparation
- Technical interview preparation

---

### ⭐ Final Advice

Follow your learning roadmap consistently and build practical projects.
Skill development takes time, so focus on continuous improvement.

"""

    return result


# =========================================================
# GEMINI AI FUNCTION WITH RETRIES
# =========================================================

def analyze_with_ai(
    name,
    education,
    skills,
    job_role,
    company,
    experience,
    learning_time
):

    if not api_key:
        return None, "Gemini API key not found."

    try:

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are SkillBridge AI, an intelligent Career and Skill Development Assistant.

Analyze the following user's career profile and provide personalized career guidance.

USER PROFILE:

Name: {name}

Education: {education}

Current Skills: {skills}

Desired Job Role: {job_role}

Dream Company: {company}

Experience Level: {experience}

Weekly Learning Time: {learning_time}


Your responsibilities:

1. Analyze the user's career goal.
2. Analyze the user's current skills.
3. Identify important skills required for the desired job role.
4. Identify missing skills or skill gaps.
5. Consider the user's dream company if provided.
6. Create a personalized learning roadmap.
7. Suggest suitable beginner or entry-level job roles.
8. Give practical advice for improving employability.

IMPORTANT:

- Do not guarantee that the user will get a job.
- Be encouraging.
- Keep the advice practical.
- Use simple language.
- Provide a clear step-by-step roadmap.

Use EXACTLY these sections:

## 🎯 Career Analysis

## ✅ Current Skills

## ❌ Skills to Improve

## 🏢 Skills Recommended for the Dream Company

## 📚 Personalized Learning Roadmap

## 💼 Suggested Job Roles

## ⭐ Final Career Advice
"""

        # Models to try
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.0-flash"
        ]

        last_error = ""

        for model_name in models_to_try:

            # Try 3 times for temporary overload
            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )

                    if response and response.text:
                        return response.text, None

                except Exception as e:

                    last_error = str(e)

                    # Wait before retrying
                    time.sleep(2 * (attempt + 1))

        return None, last_error

    except Exception as e:

        return None, str(e)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🚀 Analyze My Skills & Build My Career Roadmap",
    use_container_width=False
):

    # Validation
    if not education or not job_role or not skills:

        st.warning(
            "⚠️ Please enter your Education, Desired Job Role, and Current Skills."
        )

    else:

        with st.spinner("🤖 SkillBridge AI is analyzing your career profile..."):

            ai_result, error = analyze_with_ai(
                name,
                education,
                skills,
                job_role,
                company,
                experience,
                learning_time
            )

        # =====================================================
        # SHOW AI RESULT
        # =====================================================

        if ai_result:

            st.success("🎉 Your personalized career analysis is ready!")

            st.markdown("---")

            st.markdown(ai_result)

        # =====================================================
        # FALLBACK IF GEMINI IS BUSY
        # =====================================================

        else:

            st.warning(
                "⚠️ Gemini AI is temporarily busy. "
                "Showing your SkillBridge career analysis using our backup system."
            )

            fallback_result = create_fallback_analysis(
                job_role,
                skills,
                company
            )

            st.markdown("---")

            st.markdown(fallback_result)


# =========================================================
# HOW SKILLBRIDGE WORKS
# =========================================================

st.write("")
st.write("")
st.markdown("---")

st.markdown("# ⚡ How SkillBridge AI Works")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("""
### 👤 1. Profile

Enter your education, skills and career goal.
""")

with c2:

    st.markdown("""
### 🤖 2. AI Analysis

Our AI analyzes your career profile.
""")

with c3:

    st.markdown("""
### 📊 3. Skill Gap

Discover missing and important skills.
""")

with c4:

    st.markdown("""
### 🚀 4. Roadmap

Get a personalized learning plan.
""")


# =========================================================
# FOOTER
# =========================================================

st.write("")
st.markdown("---")

st.markdown(
    "<p style='text-align:center;'>"
    "🎯 <b>SkillBridge AI</b> | Your Skills. Your Path. Your Future."
    "</p>",
    unsafe_allow_html=True
)
