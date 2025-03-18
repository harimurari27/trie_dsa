import streamlit as st
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

from trie import trie

# ✅ Page configuration
st.set_page_config(page_title="Enhanced Trie Search", page_icon="🔍", layout="wide")

# ✅ Custom CSS for enhanced styling
st.markdown(
    """
    <style>
        /* 🌟 Background gradient with animation */
        body {
            background: linear-gradient(-45deg, #74EBD5, #ACB6E5, #FFD3B6, #FFAAA5);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 📌 Styling the Streamlit App */
        .stApp {
            background: rgba(255, 255, 255, 0.6); /* Glass effect */
            backdrop-filter: blur(10px);
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            padding: 20px;
        }

        /* 🌟 Title Styling */
        .title {
            font-size: 3em;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 20px;
        }

        /* 🔥 Card Styling with Glassmorphism */
        .card {
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 15px;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            transition: transform 0.3s, background 0.3s;
        }

        .card:hover {
            background: rgba(255, 255, 255, 0.7);
            transform: translateY(-10px);
        }

        .word {
            font-size: 1.5em;
            font-weight: bold;
            color: #1f77b4;
        }

        .meaning {
            font-size: 1.1em;
            color: #555555;
        }

        .no-result {
            color: #e74c3c;
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
        }

        .suggestions {
            color: #27ae60;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
        }

        /* 🚀 Footer Styling */
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.9em;
            color: #888888;
        }

        .footer a {
            color: #3498db;
            text-decoration: none;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Title
st.markdown("<div class='title'>📚 Enhanced Trie with Streamlit 🚀</div>", unsafe_allow_html=True)
st.write("Search words with **prefix matching**, auto-correction, and wildcard support!")

# ✅ Store query in session state for real-time updates
if "query" not in st.session_state:
    st.session_state.query = ""

# ✅ Callback function to update query dynamically
def update_query():
    st.session_state.query = st.session_state.new_query

# ✅ Input field with callback for real-time updates
st.text_input(
    "🔍 Start typing:",
    value=st.session_state.query,
    key="new_query",
    on_change=update_query
)

# ✅ Max suggestions slider
max_suggestions = st.slider("🎯 Max Suggestions", 1, 1000, 50)

# ✅ Display dynamic suggestions
query = st.session_state.query.strip().lower()
if query:
    results = []

    # Wildcard handling
    if "*" in query or "?" in query:
        results = trie.wildcard_search(query, limit=max_suggestions)
    else:
        # Prefix matching
        results = trie.search(query)

        # Auto-correction if no prefix match
        if not results:
            results = trie.auto_correct(query, max_distance=2, limit=max_suggestions)

    # ✅ Display Results
    if results:
        st.markdown(f"<div class='suggestions'>✅ Suggestions:</div>", unsafe_allow_html=True)

        # Two-column layout for better display
        cols = st.columns(2)

        for idx, (word, meaning) in enumerate(results):
            with cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class='card'>
                        <div class='word'>🔹 {word}</div>
                        <div class='meaning'>{meaning}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.markdown("<div class='no-result'>❌ No matches found.</div>", unsafe_allow_html=True)

# ✅ Footer
st.markdown(
    """
    <div class='footer'>
        Created with ❤️ using Streamlit | <a href="https://nltk.org/" target="_blank">NLTK WordNet</a>
    </div>
    """,
    unsafe_allow_html=True
)
