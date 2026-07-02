# 🔍 Code Review AI

An AI-powered code review application that analyzes code using LLMs and provides intelligent feedback.

---

## 💡 What It Does

- Detects syntax errors
- Reviews code quality
- Suggests improvements
- Generates structured JSON output
- Built with Streamlit

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core language |
| Groq API (Llama 3) | AI model for code analysis |
| Prompt Templates | Structured input formatting for LLM |
| JSON Parser | Validated structured output |
| Streamlit | Web interface |

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/code-review-ai.git
cd code-review-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API Key

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the application

```bash
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```text
code_review_ai/
├── app/
│   ├── prompt.py        # Builds prompts for the LLM
│   ├── model.py         # Handles Groq API calls
│   └── parser.py        # Parses and validates JSON output
├── tests/
│   └── test_cases.py    # Test cases
├── main.py              # CLI entry point
├── streamlit_app.py     # Streamlit web app
├── requirements.txt
└── README.md
```

---

## 📸 Demo

| Input | Output |
|-------|--------|
| Code with syntax error | Detects indentation/syntax issues and rates **Low** |
| Code with poor naming | Suggests meaningful variable names and rates **Medium** |
| Clean well-written code | Reports no issues and rates **High** |

---

## 🚀 Sprint 2 – Deployment

- Deploy the Streamlit application.
- Add GitHub repository integration.
- Improve UI and user experience.
- Support multiple programming languages.
- Generate downloadable review reports.
