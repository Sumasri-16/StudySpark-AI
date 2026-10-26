
import os
import json
import time
import re
import html

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

/* Sidebar */
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

/* Welcome banner */
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

/* Feature cards */
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

/* Inputs */
.stTextArea textarea,
.stTextInput input {
    background: #FFFFFF !important;
    color: #211747 !important;
    -webkit-text-fill-color: #211747 !important;
    border: 2px solid #A78BFA !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}
.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #6B7280 !important;
    -webkit-text-fill-color: #6B7280 !important;
}

/* Dropdowns */
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

/* File uploader */
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

/* Buttons */
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
}

/* Sidebar navigation */
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

/* Tabs */
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

/* Expander and metrics */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #C4B5FD !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #312E81 !important;
}
[data-testid="stExpander"] pre,
[data-testid="stExpander"] code,
[data-testid="stExpander"] p,
[data-testid="stExpander"] li {
    background: #FFFFFF !important;
    color: #242044 !important;
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

/* Chat messages and question input */
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

/* Other panels */
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
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================
DEFAULTS = {
    "page": "Home",
    "notes": "",
    "source_name": "",
    "source_pages": [],
    "summary": "",
    "summary_style": "Quick revision",
    "study_data": None,
    "history": [],
    "chat_messages": [],
    "planner_tasks": [],
    "planner_completed": [],
    "difficulty": "Beginner",
    "days": 7,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state.page = page


def source_ready():
    return len(st.session_state.notes.strip()) >= 30


# =========================================================
# GEMINI API
# =========================================================
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add your key to the local .env file."
        )
    return genai.Client(api_key=api_key)


def call_ai(prompt):
    """Try available models and retry temporary service errors."""
    client = get_client()
    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-flash-lite-latest",
    ]
    errors = []

    for model in models:
        for attempt in range(2):
            try:
                with st.spinner(f"Generating with {model}..."):
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )
                result = (response.text or "").strip()
                if not result:
                    raise ValueError("The AI returned an empty response.")
                return result
            except Exception as exc:
                errors.append(f"{model}: {exc}")
                message = str(exc).lower()
                temporary = any(word in message for word in [
                    "503", "unavailable", "high demand", "429",
                    "resource exhausted", "500", "overloaded",
                    "deadline exceeded", "internal error",
                ])
                if temporary and attempt == 0:
                    time.sleep(2)
                    continue
                break

    raise RuntimeError(
        "Gemini could not generate a response. Please try again later. "
        "Last error: " + (errors[-1] if errors else "Unknown error")
    )


def call_ai_json(prompt):
    text = call_ai(prompt)
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("The AI response was not valid JSON.")
    return json.loads(text[start:end + 1])


# =========================================================
# SOURCE HELPERS
# =========================================================
def extract_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": number, "text": text})
    return pages


def save_source(text, filename="Pasted notes", pages=None):
    text = text.strip()
    if len(text) < 30:
        st.error("Please provide at least 30 characters of readable notes.")
        return False

    st.session_state.notes = text[:30000]
    st.session_state.source_name = filename
    st.session_state.source_pages = pages or []
    st.session_state.summary = ""
    st.session_state.study_data = None
    st.session_state.chat_messages = []
    st.success(
        f"Notes are ready! {len(st.session_state.notes):,} characters saved."
    )
    return True


def require_source():
    if not source_ready():
        st.warning(
            "First add your notes on the Home page and click "
            "**Save and Prepare Notes**."
        )
        return None
    return st.session_state.notes


def download_json(label, data, filename):
    st.download_button(
        label=label,
        data=json.dumps(data, indent=2, ensure_ascii=False),
        file_name=filename,
        mime="application/json",
        use_container_width=True,
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("# 📚 StudySpark AI")
    st.caption("Your personal AI learning companion")
    st.divider()

    st.markdown("### 🧭 Navigate")

    navigation = [
        ("🏠 Home", "Home"),
        ("📝 AI Summarizer", "AI Summarizer"),
        ("💬 Chat With PDF", "Chat With PDF"),
        ("🎯 Flashcards & Quiz", "Flashcards & Quiz"),
        ("📅 Study Planner", "Study Planner"),
        ("📊 Progress Dashboard", "Progress Dashboard"),
    ]

    for label, page in navigation:
        if st.button(
            label,
            key=f"nav_{page}",
            use_container_width=True,
        ):
            go_to(page)
            st.rerun()

    st.divider()
    st.markdown("### ⚙️ Study Settings")

    st.session_state.difficulty = st.selectbox(
        "Quiz difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner", "Intermediate", "Advanced"].index(
            st.session_state.difficulty
        ),
    )

    st.session_state.days = st.number_input(
        "Days for your study plan",
        min_value=1,
        max_value=30,
        value=int(st.session_state.days),
    )

    if source_ready():
        st.success("✅ Study notes are ready")
        st.caption(st.session_state.source_name or "Study material")
    else:
        st.info("📄 Add notes on the Home page to get started.")

    st.divider()
    st.caption("StudySpark AI · Learn smarter, every day")


# =========================================================
# MAIN HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <h1>📚 StudySpark AI</h1>
    <p>Upload once. Learn in different ways. Track your progress.</p>
    <p>Summaries · PDF Q&A · Flashcards · Quizzes · Study plans</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HOME: UPLOAD AND PASTE NOTES
# =========================================================
if st.session_state.page == "Home":
    st.markdown("## 👋 Welcome to your study workspace")
    st.write(
        "Start here. Upload your lecture PDF or paste your notes, "
        "save them once, and then choose any learning tool below."
    )

    if source_ready():
        st.success(
            f"Your source is ready: "
            f"{st.session_state.source_name or 'Study notes'}"
        )
        st.caption(
            f"{len(st.session_state.notes):,} characters available to study."
        )

    st.markdown("### Step 1 — Add your study material")

    pasted = st.text_area(
        "Paste your notes here",
        value="",
        height=180,
        placeholder="Paste your lecture notes, textbook excerpt, or revision material...",
        key="home_pasted_notes",
    )

    pdf = st.file_uploader(
        "Or upload a text-based PDF",
        type=["pdf"],
        key="home_pdf",
        help="Choose a PDF from your computer. Selectable text works best.",
    )

    if pdf is not None:
        st.info(
            f"Selected file: {pdf.name} · {pdf.size / 1024:.1f} KB"
        )

    if st.button(
        "💾 Save and Prepare Notes",
        type="primary",
        use_container_width=True,
    ):
        content = pasted.strip()
        pages = []
        filename = "Pasted notes"

        if pdf is not None:
            try:
                with st.spinner("Reading your PDF..."):
                    pages = extract_pdf(pdf)

                pdf_text = "\n\n".join(
                    f"[Page {item['page']}]\n{item['text']}"
                    for item in pages
                )

                if content and pdf_text:
                    content = (
                        content + "\n\n--- PDF CONTENT ---\n\n" + pdf_text
                    )
                    filename = f"Notes and {pdf.name}"
                elif pdf_text:
                    content = pdf_text
                    filename = pdf.name
                elif not content:
                    st.error(
                        "No selectable text was found in this PDF. "
                        "It may be scanned or image-only. Please paste "
                        "the text or use an OCR tool first."
                    )

            except Exception as exc:
                st.error(f"Could not read this PDF: {exc}")
                content = ""

        if content.strip():
            save_source(content, filename, pages)

    st.divider()
    st.markdown("### Step 2 — What would you like to do?")

    feature_columns = st.columns(2, gap="medium")

    features = [
        (
            "📝 AI Summarizer",
            "Create quick revision notes, key points, definitions, and exam questions.",
            "AI Summarizer",
        ),
        (
            "💬 Chat With PDF",
            "Ask questions about your study material and get source-based answers.",
            "Chat With PDF",
        ),
        (
            "🎯 Flashcards & Quiz",
            "Generate flashcards, practise MCQs, and check your score.",
            "Flashcards & Quiz",
        ),
        (
            "📅 Study Planner",
            "Create a daily revision schedule based on your notes.",
            "Study Planner",
        ),
    ]

    for index, (title, description, page) in enumerate(features):
        with feature_columns[index % 2]:
            st.markdown(
                f'<div class="feature-card">'
                f'<h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True,
            )

            if st.button(
                f"Open {title}",
                key=f"home_feature_{page}",
                use_container_width=True,
            ):
                go_to(page)
                st.rerun()

    st.divider()
    st.markdown("### Step 3 — Review your progress")

    if st.button(
        "📊 Open Progress Dashboard",
        use_container_width=True,
    ):
        go_to("Progress Dashboard")
        st.rerun()

    st.caption(
        "Tip: Save your notes before opening any learning tool. "
        "You only need to upload them once per active session."
    )


# =========================================================
# AI SUMMARIZER
# =========================================================
elif st.session_state.page == "AI Summarizer":
    st.markdown("## 📝 AI Notes Summarizer")
    st.write("Create clear revision notes from your saved source material.")

    source = require_source()

    if source:
        st.info(
            f"Using: {st.session_state.source_name or 'Saved study notes'}"
        )

        style = st.selectbox(
            "Choose your summary style",
            [
                "Quick revision",
                "Detailed notes",
                "Exam preparation",
                "Key points and definitions",
            ],
        )

        if st.button(
            "✨ Generate Summary",
            type="primary",
            use_container_width=True,
        ):
            prompt = f"""
You are a careful study assistant. Use only the supplied notes.
Do not invent facts. If a detail is missing, say the notes do not
provide it. Preserve important terminology.

Write a student-friendly Markdown response with:
1. A clear title
2. Short overview
3. Main ideas and important points
4. Important terms and definitions where available
5. A revision checklist
6. Five possible exam questions based only on the source

Summary style: {style}

SOURCE:
{source[:18000]}
"""
            try:
                result = call_ai(prompt)
                st.session_state.summary = result
                st.success("Summary created successfully!")
            except Exception as exc:
                st.error(f"Summary generation failed: {exc}")

        if st.session_state.summary:
            st.divider()
            st.markdown("### Your Summary")
            st.markdown(st.session_state.summary)

            st.download_button(
                "⬇️ Download Summary (.md)",
                data=st.session_state.summary,
                file_name="studyspark_summary.md",
                mime="text/markdown",
                use_container_width=True,
            )

            st.download_button(
                "⬇️ Download Summary (.txt)",
                data=st.session_state.summary,
                file_name="studyspark_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )


# =========================================================
# CHAT WITH PDF — READABLE SOURCE AND CHAT INPUT
# =========================================================
elif st.session_state.page == "Chat With PDF":
    st.markdown("## 💬 Chat With Your Study Material")
    st.write(
        "Ask questions about your saved notes. Answers should be "
        "based on the extracted text, not unrelated information."
    )

    source = require_source()

    if source:
        st.success(
            f"Source ready: {st.session_state.source_name or 'Study notes'}"
        )

        with st.expander("📄 View saved source", expanded=False):
            st.markdown(
                "<div style='background:#FFFFFF; color:#242044; "
                "padding:16px; border:1px solid #C4B5FD; "
                "border-radius:10px; white-space:pre-wrap; "
                "overflow-wrap:anywhere;'>"
                + html.escape(source[:8000])
                + "</div>",
                unsafe_allow_html=True,
            )

        if st.button("🧹 Clear Conversation"):
            st.session_state.chat_messages = []
            st.rerun()

        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(
            "Type your question about these notes and press Enter..."
        )

        if question and question.strip():
            question = question.strip()

            st.session_state.chat_messages.append({
                "role": "user",
                "content": question,
            })

            with st.chat_message("user"):
                st.markdown(question)

            prompt = f"""
You are StudySpark AI, a helpful study assistant.
Answer the student's question using only the source text.
If the answer is not supported by the source, say so.
When the source contains [Page N] labels, cite the relevant page
when you can identify it. Do not invent page references.
Explain the answer clearly and briefly.

SOURCE:
{source[:18000]}

QUESTION:
{question}
"""
            try:
                answer = call_ai(prompt)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer,
                })
                with st.chat_message("assistant"):
                    st.markdown(answer)
            except Exception as exc:
                st.error(f"Could not answer your question: {exc}")

        st.caption(
            "Tip: Ask one clear question at a time. "
            "If the AI service is busy, please try again later."
        )


# =========================================================
# FLASHCARDS AND QUIZ
# =========================================================
elif st.session_state.page == "Flashcards & Quiz":
    st.markdown("## 🎯 Flashcards and Practice Quiz")
    st.write(
        "Generate study cards and a multiple-choice quiz from your notes."
    )

    source = require_source()

    if source:
        if st.button(
            "🚀 Generate Flashcards and Quiz",
            type="primary",
            use_container_width=True,
        ):
            prompt = f"""
Create study material using only the source below.
Return valid JSON only, without Markdown fences:
{{
  "flashcards": [
    {{"question": "Question", "answer": "Answer"}}
  ],
  "quiz": [
    {{
      "question": "Question",
      "options": ["A. Option", "B. Option", "C. Option", "D. Option"],
      "correct_answer": "Exact full text of one option",
      "explanation": "Short explanation supported by the source"
    }}
  ]
}}
Create exactly 5 flashcards and 5 multiple-choice questions.
Every quiz question must have four distinct options. The correct_answer
must exactly match one option. Avoid ambiguous questions.
Difficulty: {st.session_state.difficulty}

SOURCE:
{source[:15000]}
"""
            try:
                data = call_ai_json(prompt)
                cards = data.get("flashcards", [])
                questions = data.get("quiz", [])

                if len(cards) != 5 or len(questions) != 5:
                    raise ValueError(
                        "The AI did not return five cards and five questions. "
                        "Please try generating again."
                    )

                for question in questions:
                    options = question.get("options", [])
                    if (
                        len(options) != 4
                        or question.get("correct_answer") not in options
                    ):
                        raise ValueError(
                            "One quiz question has invalid answer options. "
                            "Please generate the quiz again."
                        )

                st.session_state.study_data = data
                st.success("Flashcards and quiz are ready!")
            except Exception as exc:
                st.error(f"Could not generate study material: {exc}")

        data = st.session_state.study_data

        if data:
            flashcard_tab, quiz_tab = st.tabs([
                "🗂️ Flashcards",
                "📝 Practice Quiz",
            ])

            with flashcard_tab:
                st.markdown("### Review your flashcards")
                for number, card in enumerate(data["flashcards"], 1):
                    with st.expander(
                        f"Card {number}: {card['question']}"
                    ):
                        st.write(card["answer"])

            with quiz_tab:
                st.markdown("### Test your knowledge")

                with st.form("studyspark_quiz_form"):
                    answers = []
                    for number, question in enumerate(data["quiz"]):
                        st.markdown(
                            f"**{number + 1}. {question['question']}**"
                        )
                        answer = st.radio(
                            "Select an answer",
                            question["options"],
                            index=None,
                            key=f"quiz_answer_{number}",
                        )
                        answers.append(answer)

                    submitted = st.form_submit_button(
                        "✅ Check My Answers",
                        use_container_width=True,
                    )

                if submitted:
                    if any(answer is None for answer in answers):
                        st.warning("Please answer every question first.")
                    else:
                        score = sum(
                            answers[i] == question["correct_answer"]
                            for i, question in enumerate(data["quiz"])
                        )

                        st.metric("Your score", f"{score}/5")
                        weak_topics = []

                        for i, question in enumerate(data["quiz"]):
                            if answers[i] == question["correct_answer"]:
                                st.success(f"Question {i + 1}: Correct!")
                            else:
                                st.error(f"Question {i + 1}: Incorrect")
                                weak_topics.append(question["question"])

                            st.write(
                                f"**Correct answer:** "
                                f"{question['correct_answer']}"
                            )
                            st.caption(question.get("explanation", ""))

                        st.session_state.history.append({
                            "score": score,
                            "total": 5,
                            "weak_topics": weak_topics,
                            "date": time.strftime("%Y-%m-%d %H:%M"),
                        })

                        if weak_topics:
                            st.warning(
                                "Review these questions: "
                                + "; ".join(weak_topics)
                            )
                        else:
                            st.success(
                                "Excellent! You answered every question correctly."
                            )

            download_json(
                "⬇️ Download Flashcards and Quiz (.json)",
                data,
                "studyspark_flashcards_quiz.json",
            )


# =========================================================
# STUDY PLANNER
# =========================================================
elif st.session_state.page == "Study Planner":
    st.markdown("## 📅 Smart Study Planner")
    st.write(
        "Create a revision plan using your notes and the number of days "
        "you have available."
    )

    source = require_source()

    if source:
        st.info(f"Study period: {int(st.session_state.days)} days")

        if st.button(
            "✨ Generate My Study Plan",
            type="primary",
            use_container_width=True,
        ):
            prompt = f"""
Create a realistic study plan using only the topics found in the notes.
Return JSON only:
{{
  "tasks": [
    {{
      "day": 1,
      "topic": "Topic",
      "tasks": ["Task 1", "Task 2"],
      "goal": "Learning goal"
    }}
  ]
}}
Create exactly {int(st.session_state.days)} entries.
Spread the topics sensibly. Include practice and revision.
Do not invent topics unrelated to the source.

SOURCE:
{source[:12000]}
"""
            try:
                plan = call_ai_json(prompt)
                tasks = plan.get("tasks", [])

                if len(tasks) != int(st.session_state.days):
                    raise ValueError(
                        "The returned plan has the wrong number of days. "
                        "Please try again."
                    )

                st.session_state.planner_tasks = tasks
                st.session_state.planner_completed = [
                    False for _ in tasks
                ]
                st.success("Your study plan is ready!")
            except Exception as exc:
                st.error(f"Could not create your plan: {exc}")

        tasks = st.session_state.planner_tasks

        if tasks:
            completed = 0

            for index, task in enumerate(tasks):
                with st.expander(
                    f"Day {task.get('day', index + 1)} — "
                    f"{task.get('topic', 'Study session')}",
                    expanded=(index == 0),
                ):
                    st.write(f"**Goal:** {task.get('goal', '')}")

                    for item in task.get("tasks", []):
                        st.markdown(f"- {item}")

                    done = st.checkbox(
                        "Mark this day as complete",
                        value=st.session_state.planner_completed[index],
                        key=f"planner_done_{index}",
                    )
                    st.session_state.planner_completed[index] = done

                    if done:
                        completed += 1

            progress = completed / len(tasks)
            st.progress(progress)
            st.write(f"Completed {completed} of {len(tasks)} days.")

            download_json(
                "⬇️ Download Study Plan (.json)",
                {"tasks": tasks},
                "studyspark_study_plan.json",
            )


# =========================================================
# PROGRESS DASHBOARD
# =========================================================
elif st.session_state.page == "Progress Dashboard":
    st.markdown("## 📊 Your Progress Dashboard")
    st.write(
        "Review your quiz results and identify which questions need more work."
    )

    history = st.session_state.history

    if not history:
        st.info(
            "Your dashboard will fill in after you complete a quiz. "
            "Open Flashcards & Quiz, generate a quiz, and check your answers."
        )

        if st.button("🎯 Go to Flashcards & Quiz"):
            go_to("Flashcards & Quiz")
            st.rerun()
    else:
        attempts = len(history)
        average = sum(item["score"] for item in history) / attempts
        latest = history[-1]["score"]

        c1, c2, c3 = st.columns(3)
        c1.metric("Quiz attempts", attempts)
        c2.metric("Average score", f"{average:.1f}/5")
        c3.metric("Latest score", f"{latest}/5")

        st.markdown("### 📈 Quiz Score History")
        st.line_chart([item["score"] for item in history])

        st.markdown("### 🔍 Questions to Revise")
        weak_topics = [
            topic
            for item in history
            for topic in item.get("weak_topics", [])
        ]

        if weak_topics:
            counts = {}
            for topic in weak_topics:
                counts[topic] = counts.get(topic, 0) + 1

            for topic, count in sorted(
                counts.items(),
                key=lambda item: item[1],
                reverse=True,
            ):
                st.markdown(f"- **{topic}** — missed {count} time(s)")
        else:
            st.success("No incorrect answers recorded in your quiz history.")

        st.markdown("### 📝 Attempt History")
        for number, item in enumerate(history, 1):
            st.write(
                f"**Attempt {number}:** {item['score']}/{item['total']} "
                f"· {item['date']}"
            )

        st.caption(
            "Progress is kept in the active Streamlit session. "
            "It is not yet stored permanently in a database."
        )

        if st.button("🗑️ Clear Quiz History"):
            st.session_state.history = []
            st.rerun()


# =========================================================
# FOOTER
# =========================================================
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px;">
    <p style="color:#312E81 !important; font-weight:800;">
        📚 StudySpark AI · Learn Smarter, Every Day ✨
    </p>
    <p style="color:#4B5563 !important;">
        Summaries · PDF Q&A · Flashcards · Quizzes · Study Planning
    </p>
</div>
""", unsafe_allow_html=True)
