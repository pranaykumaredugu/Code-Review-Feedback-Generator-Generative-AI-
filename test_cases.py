# streamlit_app.py
import os
import sys
from dotenv import load_dotenv

# Load .env file FIRST before anything else
load_dotenv()

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.prompt import build_prompt
from app.model import call_llm
from app.parser import parse_response

st.set_page_config(
    page_title="Code Review AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Sora:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
    .main-title { font-size: 2.4rem; font-weight: 700; color: #c0392b; margin-bottom: 0.2rem; }
    .subtitle { color: #666; font-size: 1rem; margin-bottom: 2rem; }
    .quality-badge { display: inline-block; padding: 6px 18px; border-radius: 20px; font-weight: 600; font-size: 1rem; }
    .badge-high   { background: #d4edda; color: #155724; }
    .badge-medium { background: #fff3cd; color: #856404; }
    .badge-low    { background: #f8d7da; color: #721c24; }
    .section-title { font-weight: 600; font-size: 1.05rem; margin: 0.4rem 0; color: #333; }
    .issue-item { background: #fff5f5; border-left: 3px solid #e74c3c; padding: 8px 12px; margin: 6px 0; border-radius: 0 6px 6px 0; font-size: 0.92rem; }
    .suggestion-item { background: #f0f7ff; border-left: 3px solid #3498db; padding: 8px 12px; margin: 6px 0; border-radius: 0 6px 6px 0; font-size: 0.92rem; }
    .summary-box { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 14px 16px; font-size: 0.95rem; color: #444; margin-top: 6px; }
    .divider { border-top: 1px solid #eee; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔍 Code Review AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste your code below and get instant AI-powered feedback on issues, quality, and improvements.</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Read key from .env automatically
env_api_key = os.getenv("GROQ_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        value=env_api_key,
        help="Auto-loaded from .env file. You can also paste it manually here."
    )
    if env_api_key:
        st.success("✅ Key loaded from .env file!")
    else:
        st.warning("⚠️ No key found in .env file. Paste it above.")
    st.caption("Get your key at [console.groq.com](https://console.groq.com)")
    st.markdown("---")
    st.markdown("**About this app**")
    st.caption(
        "Built as part of Innomatics Research Labs Generative AI curriculum. "
        "Uses Groq LLM (Llama3) with structured JSON output parsing."
    )

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📝 Your Code")
    code_input = st.text_area(
        label="Paste code here",
        height=320,
        placeholder="# Paste any code snippet here\nfor i in range(5):\nprint(i)",
        label_visibility="collapsed",
    )

    st.caption("Try an example:")
    eg_col1, eg_col2, eg_col3 = st.columns(3)

    with eg_col1:
        if st.button("🐛 Syntax Error"):
            st.session_state["example"] = "for i in range(5):\nprint(i)"
    with eg_col2:
        if st.button("📛 Bad Naming"):
            st.session_state["example"] = "def f(x,y):\n    a=x+y\n    b=a*2\n    return b"
    with eg_col3:
        if st.button("✅ Good Code"):
            st.session_state["example"] = (
                "def calculate_area(radius: float) -> float:\n"
                "    \"\"\"Returns area of a circle.\"\"\"\n"
                "    import math\n"
                "    return math.pi * radius ** 2"
            )

    if "example" in st.session_state and not code_input.strip():
        code_input = st.session_state["example"]

    run_btn = st.button("🚀 Review My Code", use_container_width=True, type="primary")

with col_right:
    st.subheader("📊 Review Results")

    if run_btn:
        if not code_input.strip():
            st.error("Please paste some code first!")
        elif not api_key_input.strip():
            st.error("Please enter your Groq API key in the sidebar.")
        else:
            with st.spinner("🤖 Analyzing your code with Groq AI..."):
                try:
                    prompt = build_prompt(code_input)
                    raw = call_llm(prompt, api_key_input)
                    result = parse_response(raw)

                    quality = result["code_quality_level"]
                    badge_class = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(quality, "badge-medium")
                    emoji = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}.get(quality, "⚪")

                    st.markdown(
                        f'<div style="margin-bottom:16px">Code Quality: '
                        f'<span class="quality-badge {badge_class}">{emoji} {quality}</span></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown('<div class="section-title">📋 Review Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="summary-box">{result["review_summary"]}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    st.markdown('<div class="section-title">🐛 Identified Issues</div>', unsafe_allow_html=True)
                    if result["identified_issues"]:
                        for issue in result["identified_issues"]:
                            st.markdown(f'<div class="issue-item">⚠️ {issue}</div>', unsafe_allow_html=True)
                    else:
                        st.success("✅ No issues found!")

                    st.markdown("<br>", unsafe_allow_html=True)

                    st.markdown('<div class="section-title">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
                    if result["improvement_suggestions"]:
                        for s in result["improvement_suggestions"]:
                            st.markdown(f'<div class="suggestion-item">💡 {s}</div>', unsafe_allow_html=True)
                    else:
                        st.success("✅ Code looks great — no suggestions!")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    else:
        st.info("👈 Paste your code on the left and click **Review My Code**.")
