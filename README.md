# 📚 StudySpark AI — Smart Learning Assistant

StudySpark AI is an AI-powered learning assistant built with Python and Streamlit. It helps students summarize study materials, ask questions about PDFs, create flashcards and quizzes, and organize their study schedules.

## ✨ Features

- **AI Summarizer:** Generate concise summaries from study notes.
- **Chat With PDF:** Ask questions about uploaded PDF documents.
- **Flashcards & Quiz:** Create revision flashcards and multiple-choice quizzes.
- **Student Profile:** Save student profile information.
- **Study Planner:** Organize study tasks and track completion.
- **Progress Dashboard:** View learning activity and quiz performance.
- **Study History:** Review and export previously saved learning activities.
- **SQLite Database:** Store profile information and study history locally.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- SQLite
- PyPDF
- python-dotenv

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Sumasri-16/StudySpark-AI.git
cd StudySpark-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install streamlit google-genai pypdf python-dotenv
```

### 4. Configure the API key

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_actual_gemini_api_key
```

Replace the placeholder with your own Gemini API key. Never upload `.env` to GitHub.

### 5. Start the application

```bash
python -m streamlit run app.py
```

## 🔐 Security and Data

- API credentials should be stored in environment variables.
- The application uses SQLite for local profile and study-history storage.
- Local SQLite data is not automatically transferred to a cloud deployment.

## 👩‍💻 Author

**Sumasri**

GitHub: [Sumasri-16](https://github.com/Sumasri-16)
