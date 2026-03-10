import streamlit as st
import requests
import re

# ---------- PAGE ----------

st.set_page_config(
    page_title="Pookie Bear AI",
    page_icon="🐻",
    layout="wide"
)

# ---------- STYLE ----------

st.markdown("""
<style>

.stApp {
background-color:#0b2545;
}

h1 {
color:#f2c94c;
}

p {
color:white;
}

[data-testid="stChatMessageContent"] {
color:white !important;
}

.sidebar-title {
color:#f2c94c;
font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------

with st.sidebar:

    st.markdown('<p class="sidebar-title">🐻 Pookie Bear AI</p>', unsafe_allow_html=True)

    st.write("Smart AI assistant")

    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.write("---")

    st.write("Built with:")
    st.write("• Python")
    st.write("• Streamlit")
    st.write("• Groq AI")

# ---------- TITLE ----------

st.title("🐻 Pookie Bear AI")
st.caption("Ask anything")

# ---------- API KEY ----------

API_KEY = "PASTE_YOUR_GROQ_KEY_HERE"

# ---------- MEMORY ----------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY CHAT ----------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- MATH TOOL ----------

def detect_math(text):

    if re.search(r"[0-9]+\s*[\+\-\*\/]\s*[0-9]+", text):

        try:
            return str(eval(text))
        except:
            return None

    return None

# ---------- WEB SEARCH ----------

def search_web(query):

    try:

        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        data = requests.get(url).json()

        results = []

        if data.get("AbstractText"):
            results.append(data["AbstractText"])

        if data.get("RelatedTopics"):

            for topic in data["RelatedTopics"][:3]:

                if "Text" in topic:
                    results.append(topic["Text"])

        return " ".join(results)

    except:
        return ""

# ---------- USER INPUT ----------

prompt = st.chat_input("Ask Pookie Bear anything...")

if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        thinking = st.empty()
        thinking.write("🧠 Pookie Bear is thinking...")

        reply = None

        # ---------- MATH ----------

        math_result = detect_math(prompt)

        if math_result:

            reply = f"The answer is **{math_result}**"

        else:

            web_info = search_web(prompt)

            try:

                url = "https://api.groq.com/openai/v1/chat/completions"

                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }

                system_prompt = {
                    "role":"system",
                    "content":"""
You are Pookie Bear AI.

You are friendly, intelligent and helpful.

You are good at:

• answering questions
• coding
• maths
• science
• explaining topics clearly

If internet information is given, use it.
"""
                }

                messages = [system_prompt]

                if web_info:

                    messages.append({
                        "role":"system",
                        "content":f"Internet information: {web_info}"
                    })

                messages += st.session_state.messages

                data = {
                    "model":"llama3-70b-8192",
                    "messages":messages,
                    "temperature":0.6
                }

                response = requests.post(url, headers=headers, json=data)

                result = response.json()

                reply = result["choices"][0]["message"]["content"]

            except:

                reply = "Something went wrong."

        thinking.write(reply)

    st.session_state.messages.append({"role":"assistant","content":reply})