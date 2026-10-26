import os
import json
import time
import re
import sqlite3
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="StudySpark AI | Smart Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# ACCESSIBLE DESIGN: HIGH CONTRAST AND CLEAR CONTROLS
# =========================================================
st.markdown("""
<style>
.stApp {
    background: #F4F6FF;
    color: #242044 !important;
}
.block-container {
    max-width: 1400px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #242044 !important;
}
h1, h2, h3, h4 {
    color: #312E81 !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #29256F, #5B21B6);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #E9D5FF !important;
}
.hero {
    background: linear-gradient(110deg, #6D28D9, #4338CA, #0369A1);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 24px;
    box-shadow: 0 8px 22px rgba(49, 46, 129, .16);
}
.hero h1, .hero p {
    color: #FFFFFF !important;
}
.hero p {
    font-size: 17px;
}
.feature-card {
    background: #FFFFFF !important;
    border: 2px solid #C4B5FD !important;
    border-radius: 16px;
    padding: 18px;
    min-height: 145px;
    box-shadow: 0 4px 12px rgba(49, 46, 129, .08);
}
.feature-card h3 {
    color: #312E81 !important;
    font-size: 21px !important;
    font-weight: 800 !important;
}
.feature-card p {
    color: #292524 !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
}
.stTextArea textarea,
.stTextInput input {
    background: #FFFFFF !important;
    color: #211747 !important;
    -webkit-text-fill-color: #211747 !important;
    border: 2px solid #A78BFA !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}
.stTextArea textarea::placeholder {
    color: #6B7280 !important;
    -webkit-text-fill-color: #6B7280 !important;
}
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #211747 !important;
    border: 2px solid #A78BFA !important;
    border-radius: 10px !important;
}
.stSelectbox div[data-baseweb="select"] *,
.stMultiSelect div[data-baseweb="select"] * {
    color: #211747 !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] {
    background: #FFFFFF !important;
}
[role="option"] {
    background: #FFFFFF !important;
    color: #211747 !important;
}
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 2px dashed #8B5CF6 !important;
    border-radius: 14px !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] *,
[data-testid="stFileUploaderDropzone"] * {
    color: #292044 !important;
    opacity: 1 !important;
}
[data-testid="stFileUploader"] button {
    background: #EDE9FE !important;
    color: #312E81 !important;
    border: 1px solid #8B5CF6 !important;
}
.stButton button,
.stDownloadButton button,
.stFormSubmitButton button {
    background: linear-gradient(90deg, #6D28D9, #4338CA) !important;
    color: #FFFFFF !important;
    border: 2px solid transparent !important;
    border-radius: 10px !important;
    min-height: 43px;
    font-weight: 700 !important;
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton button *,
.stDownloadButton button *,
.stFormSubmitButton button * {
    color: #FFFFFF !important;
}
.stButton button:hover,
.stDownloadButton button:hover,
.stFormSubmitButton button:hover {
    background: #312E81 !important;
    border-color: #A78BFA !important;
    box-shadow: 0 4px 12px rgba(49, 46, 129, .2) !important;
    transform: translateY(-1px);
}
.stButton button:focus,
.stDownloadButton button:focus,
.stFormSubmitButton button:focus {
    outline: 3px solid #F59E0B !important;
    outline-offset: 3px !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,.12) !important;
    border: 1px solid rgba(255,255,255,.35) !important;
    color: #FFFFFF !important;
    text-align: left !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #FFFFFF !important;
    color: #312E81 !important;
}
[data-testid="stSidebar"] .stButton button:hover * {
    color: #312E81 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #E5E7FF !important;
    gap: 6px;
    padding: 7px;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    background: #E5E7FF !important;
    border-radius: 8px !important;
    opacity: 1 !important;
}
.stTabs [data-baseweb="tab"] *,
.stTabs [data-baseweb="tab"] p {
    color: #312E81 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #FFFFFF !important;
    border-bottom: 3px solid #6D28D9 !important;
}
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #C4B5FD !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #312E81 !important;
}
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #C4B5FD !important;
    border-radius: 12px;
    padding: 14px;
}
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] * {
    color: #312E81 !important;
}
[data-testid="stRadio"] label,
[data-testid="stRadio"] label * {
    color: #242044 !important;
}
.info-card {
    background: #FFFFFF;
    border: 1px solid #C4B5FD;
    border-radius: 12px;
    padding: 15px;
}
.small-note {
    color: #4B5563 !important;
    font-size: 13px;
}
hr {
    border-color: #DDD6FE !important;
}
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] pre,
[data-testid="stExpander"] code,
[data-testid="stExpander"] p,
[data-testid="stExpander"] li {
    color: #242044 !important;
}
[data-testid="stExpander"] pre {
    background: #FFFFFF !important;
    border: 1px solid #DDD6FE !important;
    border-radius: 10px !important;
    padding: 16px !important;
    white-space: pre-wrap !important;
    overflow-wrap: anywhere !important;
}
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #DDD6FE !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #242044 !important;
}
[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 2px solid #7C3AED !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #211747 !important;
    -webkit-text-fill-color: #211747 !important;
    caret-color: #6D28D9 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #6B7280 !important;
    -webkit-text-fill-color: #6B7280 !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button {
    background: #6D28D9 !important;
    color: #FFFFFF !important;
}
[data-testid="stChatInput"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SQLITE DATABASE: PROFILE AND PERSISTENT STUDY HISTORY
# =========================================================
# Local database is created beside app.py. On hosting services with
# temporary filesystems, use a persistent database for long-term storage.
DB_PATH = os.getenv(
    "STUDYSPARK_DB_PATH",
    str(Path(__file__).with_name("studyspark.db"))
)


def db_connect():
    connection = sqlite3.connect(DB_PATH, timeout=20)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with db_connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_key TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL DEFAULT '',
                university TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS study_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_key TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                title TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '',
                content TEXT NOT NULL DEFAULT '',
                score REAL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_name_key
            ON study_history(name_key)
        """)


init_db()


def normalise_name(name):
    return re.sub(r"\s+", " ", (name or "").strip()).casefold()


def save_profile(name, course="", university=""):
    clean_name = re.sub(r"\s+", " ", (name or "").strip())
    if not clean_name:
        return False

    name_key = normalise_name(clean_name)
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    with db_connect() as connection:
        connection.execute("""
            INSERT INTO profiles (name, name_key, course, university, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name_key) DO UPDATE SET
                name = excluded.name,
                course = excluded.course,
                university = excluded.university
        """, (clean_name, name_key, course.strip(), university.strip(), now))

    return True


def get_profile(name):
    name_key = normalise_name(name)
    if not name_key:
        return None

    with db_connect() as connection:
        return connection.execute("""
            SELECT * FROM profiles WHERE name_key = ?
        """, (name_key,)).fetchone()


def save_history(
    name,
    activity_type,
    title,
    details="",
    content="",
    score=None,
):
    name_key = normalise_name(name)
    if not name_key:
        return

    now = time.strftime("%Y-%m-%d %H:%M:%S")

    with db_connect() as connection:
        connection.execute("""
            INSERT INTO study_history
            (name_key, activity_type, title, details, content, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name_key,
            activity_type,
            title,
            details,
            content,
            score,
            now,
        ))


def get_history(name, limit=200):
    name_key = normalise_name(name)
    if not name_key:
        return []

    with db_connect() as connection:
        rows = connection.execute("""
            SELECT * FROM study_history
            WHERE name_key = ?
            ORDER BY id DESC
            LIMIT ?
        """, (name_key, limit)).fetchall()

    return rows


def clear_history(name):
    name_key = normalise_name(name)
    if not name_key:
        return

    with db_connect() as connection:
        connection.execute("""
            DELETE FROM study_history WHERE name_key = ?
        """, (name_key,))


# =========================================================
# SESSION STATE
# =========================================================
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""

if "last_quiz" not in st.session_state:
    st.session_state.last_quiz = None
if "planner_tasks" not in st.session_state:
    st.session_state.planner_tasks = []

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

if "profile_course" not in st.session_state:
    st.session_state.profile_course = ""

if "profile_university" not in st.session_state:
    st.session_state.profile_university = ""    

# =========================================================
# GEMINI AI CONFIGURATION
# =========================================================

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "GEMINI_API_KEY is missing. "
            "Please configure it in your .env file."
        )
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception as error:
        st.error(f"Unable to initialize Gemini: {error}")
        return None


def generate_ai_response(prompt):
    client = get_gemini_client()

    if client is None:
        return None

    models = [
        "gemini-2.5-flash",
        "gemini-flash-latest",
    ]

    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            answer = (response.text or "").strip()

            if answer:
                return answer

        except Exception:
            continue

    st.error(
        "The AI service could not generate a response. "
        "Check your API key, internet connection, and model availability."
    )
    return None


# =========================================================
# SAVE ACTIVITY TO STUDY HISTORY
# =========================================================

def record_activity(
    activity_type,
    title,
    details="",
    content="",
    score=None,
):
    student_name = st.session_state.get("student_name", "").strip()

    if not student_name:
        return

    save_history(
        name=student_name,
        activity_type=activity_type,
        title=title,
        details=details,
        content=content,
        score=score,
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

PAGES = [
    "Home",
    "Student Profile",
    "AI Summarizer",
    "Chat With PDF",
    "Flashcards & Quiz",
    "Study Planner",
    "Progress Dashboard",
    "My History",
]

with st.sidebar:
    st.markdown("# 📚 StudySpark AI")
    st.caption("Your personal AI study companion")
    st.divider()

    st.markdown("### Navigation")

    for page_name in PAGES:
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            use_container_width=True,
        ):
            st.session_state.current_page = page_name
            st.rerun()

    st.divider()

    if st.session_state.student_name:
        st.markdown(
            f"**Student:** {st.session_state.student_name}"
        )
    else:
        st.caption("Create a student profile to get started.")

    st.caption("Learn smarter, one topic at a time.")


# =========================================================
# HELPER: PAGE TITLE
# =========================================================

def page_header(title, description):
    st.title(title)
    st.write(description)
    st.divider()


# =========================================================
# HOME PAGE
# =========================================================

def home_page():
    st.markdown("""
    <div class="hero">
        <h1>Welcome to StudySpark AI 📚</h1>
        <p>
            Your intelligent study companion for summarizing notes,
            understanding PDFs, practicing quizzes, and planning study sessions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Prepare Your Study Material")

    st.info(
        "Paste your notes or upload a PDF to begin. "
        "Your study activities can be saved in your history."
    )

    tab1, tab2 = st.tabs([
        "📝 Paste Notes",
        "📄 Upload PDF",
    ])

    with tab1:
        notes_input = st.text_area(
            "Enter your study notes",
            height=250,
            placeholder="Paste your class notes, textbook content, or study material here...",
            key="home_notes_input",
        )

        if st.button(
            "Save and Prepare Notes",
            key="save_notes_button",
            use_container_width=True,
        ):
            if len(notes_input.strip()) < 30:
                st.warning(
                    "Please enter at least 30 characters of study notes."
                )
            else:
                st.session_state.pdf_text = notes_input.strip()
                st.session_state.last_summary = ""

                record_activity(
                    "source",
                    "Pasted study notes",
                    details=f"{len(notes_input)} characters",
                    content=notes_input[:12000],
                )

                st.success("Your study notes are ready!")

    with tab2:
        uploaded_pdf = st.file_uploader(
            "Upload a PDF document",
            type=["pdf"],
            key="home_pdf_upload",
        )

        if uploaded_pdf is not None:
            if st.button(
                "Extract PDF Text",
                key="extract_pdf_button",
                use_container_width=True,
            ):
                try:
                    reader = PdfReader(uploaded_pdf)
                    extracted_pages = []
                    full_text = []

                    for page_number, page in enumerate(
                        reader.pages,
                        start=1,
                    ):
                        page_text = (
                            page.extract_text() or ""
                        ).strip()

                        if page_text:
                            extracted_pages.append({
                                "page": page_number,
                                "text": page_text,
                            })
                            full_text.append(page_text)

                    extracted_text = "\n\n".join(full_text)

                    if len(extracted_text.strip()) < 30:
                        st.warning(
                            "Very little text was extracted. "
                            "The PDF may be scanned or image-based."
                        )
                    else:
                        st.session_state.pdf_text = extracted_text[:30000]
                        st.session_state.pdf_text_pages = extracted_pages
                        st.session_state.pdf_file_name = uploaded_pdf.name

                        record_activity(
                            "source",
                            uploaded_pdf.name,
                            details=(
                                f"{len(extracted_pages)} pages extracted"
                            ),
                            content=extracted_text[:12000],
                        )

                        st.success(
                            f"Successfully extracted text from "
                            f"{len(extracted_pages)} pages."
                        )

                except Exception as error:
                    st.error(f"Unable to read the PDF: {error}")

    if st.session_state.pdf_text:
        st.success(
            f"Study material loaded: "
            f"{len(st.session_state.pdf_text):,} characters"
        )

        with st.expander("Preview study material"):
            st.text(
                st.session_state.pdf_text[:3000]
            )

    st.divider()
    st.subheader("Explore Study Tools")

    columns = st.columns(3)

    features = [
        (
            "✨ AI Summarizer",
            "Create concise summaries from your notes.",
        ),
        (
            "💬 Chat With PDF",
            "Ask questions about your study material.",
        ),
        (
            "🧠 Flashcards & Quiz",
            "Test your knowledge with practice questions.",
        ),
        (
            "📅 Study Planner",
            "Organize your study schedule.",
        ),
        (
            "📊 Progress Dashboard",
            "Review your learning progress.",
        ),
        (
            "📜 My History",
            "Revisit your previous study activities.",
        ),
    ]

    for index, (title, description) in enumerate(features):
        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

    st.caption(
        "Tip: Start by loading your notes, then open the AI tools."
    )


# =========================================================
# STUDENT PROFILE PAGE
# =========================================================

def student_profile_page():
    page_header(
        "👤 Student Profile",
        "Manage your profile and personalize your study experience.",
    )

    existing_profile = get_profile(
        st.session_state.student_name
    ) if st.session_state.student_name else None

    default_name = (
        existing_profile["name"]
        if existing_profile
        else st.session_state.student_name
    )

    default_course = (
        existing_profile["course"]
        if existing_profile
        else ""
    )

    default_university = (
        existing_profile["university"]
        if existing_profile
        else ""
    )

    with st.form("student_profile_form"):
        student_name = st.text_input(
            "Student name",
            value=default_name,
            placeholder="Enter your name",
        )

        course = st.text_input(
            "Course / Program",
            value=default_course,
            placeholder="Example: MSc Data Science",
        )

        university = st.text_input(
            "College / University",
            value=default_university,
            placeholder="Enter your institution",
        )

        submitted = st.form_submit_button(
            "Save Profile",
            use_container_width=True,
        )

    if submitted:
        if not student_name.strip():
            st.error("Please enter your name.")
        else:
            saved = save_profile(
                student_name,
                course,
                university,
            )

            if saved:
                st.session_state.student_name = student_name.strip()
                st.session_state.profile_course = course.strip()
                st.session_state.profile_university = university.strip()

                st.success("Your profile has been saved!")
                st.rerun()

    st.divider()
    st.subheader("Profile Information")

    if st.session_state.student_name:
        st.write(
            f"**Name:** {st.session_state.student_name}"
        )
        st.write(
            f"**Course:** "
            f"{st.session_state.get('profile_course', '') or 'Not specified'}"
        )
        st.write(
            f"**University:** "
            f"{st.session_state.get('profile_university', '') or 'Not specified'}"
        )
    else:
        st.info("Save your profile to see your details here.")

    st.caption(
        "This profile is a convenience feature, not secure authentication. "
        "Avoid storing passwords or sensitive personal information."
    )
# =========================================================
# AI SUMMARIZER PAGE
# =========================================================

def ai_summarizer_page():
    page_header(
        "✨ AI Summarizer",
        "Turn lengthy study notes into clear, easy-to-revise summaries.",
    )

    text = st.session_state.get("pdf_text", "").strip()

    if not text:
        st.warning(
            "Please add study notes or upload a PDF on the Home page first."
        )
        if st.button("Go to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        return

    st.caption(
        f"Current source: {st.session_state.get('pdf_file_name', 'Study notes')} "
        f"({len(text):,} characters)"
    )

    summary_style = st.selectbox(
        "Choose summary style",
        [
            "Quick revision",
            "Detailed explanation",
            "Exam preparation",
            "Bullet points",
            "Simple language",
        ],
    )

    summary_length = st.select_slider(
        "Summary length",
        options=["Short", "Medium", "Long"],
        value="Medium",
    )

    if st.button(
        "Generate Summary",
        key="generate_summary",
        use_container_width=True,
    ):
        prompt = f"""
You are a helpful academic study assistant.

Summarize the following study material.

Summary style: {summary_style}
Desired length: {summary_length}

Instructions:
- Use only information supported by the supplied material.
- Preserve important definitions, concepts, and terminology.
- Organize the answer with meaningful headings.
- Make the explanation suitable for a student preparing for exams.
- Do not invent facts or claim that missing information appears in the source.

STUDY MATERIAL:
{text[:25000]}
"""

        result = generate_ai_response(prompt)

        if result:
            st.session_state.last_summary = result

            save_history(
                st.session_state.student_name,
                "summary",
                f"Summary: {summary_style}",
                details=f"Length: {summary_length}",
                content=result,
            )

    summary = st.session_state.get("last_summary", "")

    if summary:
        st.divider()
        st.subheader("Your Summary")
        st.markdown(summary)

        st.download_button(
            "Download Summary",
            data=summary,
            file_name="studyspark_summary.txt",
            mime="text/plain",
            use_container_width=True,
        )

# =========================================================
# CHAT WITH PDF PAGE
# =========================================================

def chat_with_pdf_page():
    page_header(
        "💬 Chat With PDF",
        "Ask questions about your uploaded PDF or saved study notes.",
    )

    text = st.session_state.get("pdf_text", "").strip()

    if not text:
        st.warning(
            "Please upload a PDF or save your notes on the Home page first."
        )
        return

    st.success("Your study material is ready for questions.")

    if st.button("Clear Current Chat", key="clear_pdf_chat"):
        st.session_state.chat_messages = []
        st.rerun()

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about your study material..."
    )

    if question:
        st.session_state.chat_messages.append({
            "role": "user",
            "content": question,
        })

        with st.chat_message("user"):
            st.markdown(question)

        previous_messages = st.session_state.chat_messages[-8:]
        conversation = "\n".join(
            f'{item["role"].upper()}: {item["content"]}'
            for item in previous_messages
        )

        prompt = f"""
You are StudySpark AI, a study assistant.

Answer the student's question using the study material below.

Rules:
- Prioritize the supplied material.
- Explain concepts clearly and accurately.
- If the answer is not present in the material, say so.
- You may provide a clearly labelled general explanation if helpful.
- Do not invent page numbers or quotations.

STUDY MATERIAL:
{text[:22000]}

RECENT CONVERSATION:
{conversation}

CURRENT QUESTION:
{question}
"""

        with st.chat_message("assistant"):
            answer = generate_ai_response(prompt)

            if answer:
                st.markdown(answer)

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer,
                })

                save_history(
                    st.session_state.student_name,
                    "chat",
                    f"Question: {question[:100]}",
                    details=question,
                    content=answer,
                )

# =========================================================
# FLASHCARDS AND QUIZ PAGE
# =========================================================

def flashcards_quiz_page():
    page_header(
        "🧠 Flashcards & Quiz",
        "Create revision flashcards and test your understanding.",
    )

    text = st.session_state.get("pdf_text", "").strip()

    if not text:
        st.warning(
            "Please prepare your study notes on the Home page first."
        )
        return

    mode = st.radio(
        "Choose a learning activity",
        ["Flashcards", "Multiple-choice quiz"],
        horizontal=True,
    )

    number_of_questions = st.slider(
        "Number of questions or flashcards",
        min_value=3,
        max_value=10,
        value=5,
    )

    if st.button(
        "Generate Learning Activity",
        key="generate_learning_activity",
        use_container_width=True,
    ):
        if mode == "Flashcards":
            prompt = f"""
Create exactly {number_of_questions} study flashcards
using the supplied material.

Return valid JSON in this format:
{{
  "flashcards": [
    {{"question": "Question", "answer": "Answer"}}
  ]
}}

Use concise questions and accurate answers.
Do not add facts unsupported by the material.

MATERIAL:
{text[:18000]}
"""
        else:
            prompt = f"""
Create exactly {number_of_questions} multiple-choice questions
based on the supplied study material.

Return valid JSON in this format:
{{
  "questions": [
    {{
      "question": "Question",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "answer": "A",
      "explanation": "Brief explanation"
    }}
  ]
}}

Rules:
- The answer must be one of A, B, C, or D.
- There must be four options for every question.
- Questions and answers must be supported by the material.

MATERIAL:
{text[:18000]}
"""

        result = generate_ai_response(prompt)

        if result:
            try:
                cleaned = re.sub(
                    r"^```(?:json)?\s*|\s*```$",
                    "",
                    result.strip(),
                    flags=re.IGNORECASE,
                )
                data = json.loads(cleaned)

                if mode == "Flashcards":
                    cards = data.get("flashcards", [])
                    if not cards:
                        raise ValueError("No flashcards were generated.")

                    st.session_state.last_quiz = {
                        "type": "flashcards",
                        "items": cards,
                    }
                else:
                    questions = data.get("questions", [])
                    if not questions:
                        raise ValueError("No quiz questions were generated.")

                    st.session_state.last_quiz = {
                        "type": "quiz",
                        "items": questions,
                    }

            except (json.JSONDecodeError, ValueError) as error:
                st.error(
                    f"Could not process the generated activity: {error}"
                )

    activity = st.session_state.get("last_quiz")

    if not activity:
        return

    if activity["type"] == "flashcards":
        st.divider()
        st.subheader("Your Flashcards")

        for index, card in enumerate(activity["items"], start=1):
            with st.expander(
                f"Flashcard {index}: {card.get('question', 'Question')}"
            ):
                st.markdown("**Answer**")
                st.write(card.get("answer", "No answer provided."))

        flashcard_text = "\n\n".join(
            f"Question: {card.get('question', '')}\n"
            f"Answer: {card.get('answer', '')}"
            for card in activity["items"]
        )

        st.download_button(
            "Download Flashcards",
            data=flashcard_text,
            file_name="studyspark_flashcards.txt",
            mime="text/plain",
            use_container_width=True,
        )

        if st.button("Save Flashcards to History"):
            save_history(
                st.session_state.student_name,
                "flashcards",
                "Generated flashcards",
                details=f"{len(activity['items'])} cards",
                content=flashcard_text,
            )
            st.success("Flashcards saved to your history.")

    else:
        st.divider()
        st.subheader("Answer the Questions")

        questions = activity["items"]
        answers = {}

        with st.form("quiz_answer_form"):
            for index, item in enumerate(questions):
                st.markdown(
                    f"**Question {index + 1}. "
                    f"{item.get('question', '')}**"
                )

                options = item.get("options", {})
                choices = list(options.keys())

                if not choices:
                    st.warning("This question has no available options.")
                    continue

                answers[index] = st.radio(
                    f"Choose your answer for question {index + 1}",
                    choices,
                    format_func=lambda key, opts=options:
                        f"{key}. {opts.get(key, '')}",
                    key=f"quiz_answer_{index}",
                    index=None,
                )

                st.write("")

            submitted = st.form_submit_button(
                "Submit Quiz",
                use_container_width=True,
            )

        if submitted:
            score = 0
            review = []

            for index, item in enumerate(questions):
                correct_answer = str(
                    item.get("answer", "")
                ).strip().upper()

                selected = answers.get(index)
                is_correct = selected == correct_answer

                if is_correct:
                    score += 1

                review.append({
                    "question": item.get("question", ""),
                    "selected": selected or "Not answered",
                    "correct": correct_answer,
                    "explanation": item.get("explanation", ""),
                    "is_correct": is_correct,
                })

            st.session_state.quiz_result = {
                "score": score,
                "total": len(questions),
                "review": review,
            }

            save_history(
                st.session_state.student_name,
                "quiz",
                "Multiple-choice quiz",
                details=f"Score: {score}/{len(questions)}",
                content=json.dumps(review, ensure_ascii=False),
                score=score,
            )

    quiz_result = st.session_state.get("quiz_result")

    if activity["type"] == "quiz" and quiz_result:
        st.divider()
        st.subheader("Quiz Results")

        score = quiz_result["score"]
        total = quiz_result["total"]

        st.metric(
            "Your Score",
            f"{score}/{total}",
            delta=f"{(score / total) * 100:.1f}%" if total else "0%",
        )

        for index, item in enumerate(quiz_result["review"], start=1):
            label = "Correct" if item["is_correct"] else "Incorrect"

            with st.expander(f"Question {index}: {label}"):
                st.write(item["question"])
                st.write(f"Your answer: {item['selected']}")
                st.write(f"Correct answer: {item['correct']}")
                st.write(item["explanation"])

# =========================================================
# STUDY PLANNER PAGE
# =========================================================

def study_planner_page():
    page_header(
        "📅 Study Planner",
        "Create a daily study schedule and track completed tasks.",
    )

    with st.form("study_planner_form"):
        subject = st.text_input(
            "Subject or topic",
            placeholder="Example: Deep Learning",
        )

        study_date = st.date_input("Study date")

        hours = st.number_input(
            "Study duration (hours)",
            min_value=0.5,
            max_value=12.0,
            value=1.0,
            step=0.5,
        )

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"],
        )

        submitted = st.form_submit_button(
            "Add Study Task",
            use_container_width=True,
        )

    if submitted:
        if not subject.strip():
            st.warning("Please enter a subject or topic.")
        else:
            task = {
                "subject": subject.strip(),
                "date": study_date.isoformat(),
                "hours": float(hours),
                "priority": priority,
                "completed": False,
            }

            st.session_state.planner_tasks.append(task)

            save_history(
                st.session_state.student_name,
                "planner",
                f"Study task: {subject.strip()}",
                details=(
                    f"Date: {study_date.isoformat()}, "
                    f"Duration: {hours} hours, Priority: {priority}"
                ),
                content=json.dumps(task),
            )

            st.success("Study task added!")

    st.divider()
    st.subheader("Your Study Schedule")

    tasks = st.session_state.planner_tasks

    if not tasks:
        st.info("You haven't added any study tasks yet.")
        return

    for index, task in enumerate(tasks):
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.markdown(f"**{task['subject']}**")
                st.write(
                    f"Date: {task['date']} · "
                    f"Duration: {task['hours']} hours"
                )
                st.write(f"Priority: {task['priority']}")

                if task["completed"]:
                    st.success("Completed")
                else:
                    st.caption("Not completed")

            with right:
                if not task["completed"]:
                    if st.button(
                        "Complete",
                        key=f"complete_task_{index}",
                    ):
                        task["completed"] = True

                        save_history(
                            st.session_state.student_name,
                            "planner",
                            f"Completed: {task['subject']}",
                            details=f"Study date: {task['date']}",
                        )
                        st.rerun()

                if st.button(
                    "Delete",
                    key=f"delete_task_{index}",
                ):
                    st.session_state.planner_tasks.pop(index)
                    st.rerun()

    completed = sum(
        1 for task in tasks if task["completed"]
    )

    st.divider()
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tasks", len(tasks))
    col2.metric("Completed", completed)
    col3.metric("Remaining", len(tasks) - completed)

    total_hours = sum(task["hours"] for task in tasks)
    st.write(f"**Total planned study time:** {total_hours:g} hours")

    schedule_text = "\n".join(
        f"{task['date']} | {task['subject']} | "
        f"{task['hours']} hours | {task['priority']} | "
        f"{'Completed' if task['completed'] else 'Pending'}"
        for task in tasks
    )

    st.download_button(
        "Download Study Schedule",
        data=schedule_text,
        file_name="studyspark_study_plan.txt",
        mime="text/plain",
        use_container_width=True,
    )

# =========================================================
# PROGRESS DASHBOARD PAGE
# =========================================================

def progress_dashboard_page():
    page_header(
        "📊 Progress Dashboard",
        "Review your quiz performance and study activity.",
    )

    student_name = st.session_state.student_name.strip()

    if not student_name:
        st.info("Create a student profile to track your progress.")
        return

    history = get_history(student_name, limit=500)

    if not history:
        st.info(
            "No study history is available yet. "
            "Generate a summary or complete a quiz to begin tracking."
        )
        return

    total_activities = len(history)
    summaries = sum(
        1 for item in history
        if item["activity_type"] == "summary"
    )
    quizzes = [
        item for item in history
        if item["activity_type"] == "quiz"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Activities", total_activities)
    col2.metric("Summaries Created", summaries)
    col3.metric("Quizzes Completed", len(quizzes))

    st.divider()
    st.subheader("Quiz Performance")

    valid_scores = [
        float(item["score"])
        for item in quizzes
        if item["score"] is not None
    ]

    if valid_scores:
        average_score = sum(valid_scores) / len(valid_scores)

        st.metric(
            "Average Correct Answers",
            f"{average_score:.2f}",
        )

        chart_data = {
            "Quiz": list(range(1, len(valid_scores) + 1)),
            "Correct Answers": valid_scores,
        }

        st.line_chart(
            chart_data,
            x="Quiz",
            y="Correct Answers",
        )

        st.caption(
            "The chart shows correct answers for each saved quiz. "
            "Scores are not percentages unless the quiz totals are identical."
        )
    else:
        st.info("Complete a quiz to see your quiz performance.")

    st.divider()
    st.subheader("Recent Activities")

    for item in history[:10]:
        with st.expander(
            f"{item['title']} — {item['created_at']}"
        ):
            st.write(f"Type: {item['activity_type']}")
            if item["details"]:
                st.write(item["details"])


# =========================================================
# MY HISTORY PAGE
# =========================================================

def my_history_page():
    page_header(
        "📜 My History",
        "Review previously saved study activities.",
    )

    student_name = st.session_state.student_name.strip()

    if not student_name:
        st.warning(
            "Please create a student profile to view your study history."
        )
        return

    history = get_history(student_name, limit=500)

    if not history:
        st.info("No previous study activities have been saved.")
        return

    activity_types = sorted({
        item["activity_type"] for item in history
    })

    selected_type = st.selectbox(
        "Filter by activity",
        ["All activities"] + activity_types,
    )

    if selected_type != "All activities":
        displayed_history = [
            item for item in history
            if item["activity_type"] == selected_type
        ]
    else:
        displayed_history = history

    st.write(f"**Activities shown:** {len(displayed_history)}")

    for index, item in enumerate(displayed_history):
        with st.expander(
            f"{item['title']} — {item['created_at']}"
        ):
            st.write(f"**Type:** {item['activity_type']}")

            if item["details"]:
                st.write(f"**Details:** {item['details']}")

            if item["score"] is not None:
                st.write(f"**Score:** {item['score']}")

            if item["content"]:
                st.text_area(
                    "Saved content",
                    value=item["content"],
                    height=150,
                    key=f"history_content_{item['id']}_{index}",
                    disabled=True,
                )

    st.divider()

    history_export = "\n\n".join(
        (
            f"Title: {item['title']}\n"
            f"Type: {item['activity_type']}\n"
            f"Date: {item['created_at']}\n"
            f"Details: {item['details']}\n"
            f"Content: {item['content']}"
        )
        for item in displayed_history
    )

    st.download_button(
        "Export Displayed History",
        data=history_export,
        file_name="studyspark_history.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.warning(
        "Clearing history permanently deletes the saved activity records "
        "for this student."
    )

    confirm_clear = st.checkbox(
        "I understand that clearing history cannot be undone.",
        key="confirm_clear_history",
    )

    if st.button(
        "Clear All My History",
        use_container_width=True,
        disabled=not confirm_clear,
    ):
        clear_history(student_name)
        st.session_state.last_summary = ""
        st.session_state.last_quiz = None
        st.session_state.quiz_result = None
        st.success("Your study history has been cleared.")
        st.rerun() 

# =========================================================
# MAIN PAGE ROUTING
# =========================================================

page = st.session_state.current_page

if page == "Home":
    home_page()

elif page == "Student Profile":
    student_profile_page()

elif page == "AI Summarizer":
    ai_summarizer_page()

elif page == "Chat With PDF":
    chat_with_pdf_page()

elif page == "Flashcards & Quiz":
    flashcards_quiz_page()

elif page == "Study Planner":
    study_planner_page()

elif page == "Progress Dashboard":
    progress_dashboard_page()

elif page == "My History":
    my_history_page()

else:
    st.session_state.current_page = "Home"
    st.rerun()

