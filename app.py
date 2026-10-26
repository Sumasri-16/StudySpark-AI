
import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()

st.set_page_config(
    page_title="StudySpark AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudySpark AI")
st.subheader("AI Study Flashcard & Quiz Generator")
st.write("Turn your notes into flashcards and practice quizzes.")

notes = st.text_area(
    "Paste your study notes",
    height=200,
    placeholder="Paste your lecture notes here..."
)

pdf_file = st.file_uploader("Or upload a PDF", type=["pdf"])

if st.button("Generate Study Material", type="primary"):
    content = notes.strip()

    if pdf_file is not None:
        try:
            reader = PdfReader(pdf_file)
            pdf_text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
            content = content or pdf_text.strip()
        except Exception as error:
            st.error(f"Unable to read PDF: {error}")

    if not content:
        st.warning("Please paste notes or upload a readable PDF.")
    elif len(content) < 30:
        st.warning("Please provide at least 30 characters of notes.")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error(
            "API key missing. Create a Google AI Studio API key "
            "and add it to your .env file."
        )
    else:
        try:
            client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

            prompt = f"""
Create study material using only these notes.
Return valid JSON, with no Markdown fences, in this format:
{{
  "flashcards": [
    {{"question": "Question", "answer": "Answer"}}
  ],
  "quiz": [
    {{
      "question": "Question",
      "options": ["A. Option", "B. Option", "C. Option", "D. Option"],
      "correct_answer": "A. Option",
      "explanation": "Explanation"
    }}
  ]
}}
Create exactly 5 flashcards and 5 multiple-choice questions.
Each question must have four options and one correct answer.
Notes:
{content[:15000]}
"""

            with st.spinner("Generating your study material..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            result = response.text.strip()

            if result.startswith("```"):
                result = result.split("\n", 1)[1]
                result = result.rsplit("```", 1)[0].strip()

            data = json.loads(result)
            st.session_state["study_data"] = data
            st.success("Study material generated successfully!")

        except Exception as error:
            st.error(f"Generation failed: {error}")

data = st.session_state.get("study_data")

if data:
    flashcard_tab, quiz_tab = st.tabs(["Flashcards", "Quiz"])

    with flashcard_tab:
        st.header("Your Flashcards")
        for number, card in enumerate(data.get("flashcards", []), 1):
            with st.expander(f"Card {number}: {card['question']}"):
                st.write(card["answer"])

    with quiz_tab:
        st.header("Test Your Knowledge")

        with st.form("quiz_form"):
            selected_answers = {}

            for number, question in enumerate(data.get("quiz", [])):
                st.write(f"**{number + 1}. {question['question']}**")
                selected_answers[number] = st.radio(
                    "Select an answer",
                    question["options"],
                    index=None,
                    key=f"question_{number}"
                )

            submitted = st.form_submit_button("Check Answers")

        if submitted:
            score = 0
            questions = data.get("quiz", [])

            for number, question in enumerate(questions):
                correct = question["correct_answer"]
                if selected_answers[number] == correct:
                    score += 1
                    st.success(f"Question {number + 1}: Correct!")
                else:
                    st.error(f"Question {number + 1}: Incorrect.")

                st.write(f"Correct answer: {correct}")
                st.caption(question["explanation"])

            st.metric("Your score", f"{score}/{len(questions)}")

    st.download_button(
        "Download Study Material (JSON)",
        data=json.dumps(data, indent=2),
        file_name="study_material.json",
        mime="application/json"
    )
