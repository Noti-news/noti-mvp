import streamlit as st
from openai import OpenAI
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Notì – AI News", page_icon="📰", layout="wide")

# Custom CSS for white background and global styling
st.markdown("""
    <style>
        body {
            background-color: #F9F9F9;
        }
        .stApp {
            background-color: #F9F9F9;
            color: #0D1B2A;
        }
    </style>
""", unsafe_allow_html=True)

# Carica il logo
logo = Image.open("logo.png")  # Assicurati che il file sia nella stessa cartella

# Layout a 3 colonne
col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    st.image(logo, width=180)  # Puoi cambiare la larghezza se vuoi più piccolo/grande
    st.markdown("""
        <div style="font-size:18px; color:#333333; margin-top:-10px;">
        Rethink your daily news: <b>faster</b>, <b>smarter</b>, <b>yours</b>
        </div>
    """, unsafe_allow_html=True)

with col2:
    today = datetime.today().strftime("%-d %B %Y")  # Es. "7 July 2025"
    st.markdown(f'<div style="font-size:32px; color:#333333;">{today}</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div style="text-align:right; font-size:28px; color:#0D1B2A;">⚙️ 👤</div>', unsafe_allow_html=True)

# Inizializza sessione
if "selected_topics" not in st.session_state:
    st.session_state.selected_topics = []
if "topics_show" not in st.session_state:
    st.session_state.topics_show = False

# HTML + CSS + logica
st.markdown("""
<style>
.button-box {
    border: 2px solid #0D1B2A;
    background-color: #FFFFFF;
    color: #0D1B2A;
    padding: 15px;
    text-align: center;
    border-radius: 10px;
    font-weight: bold;
    transition: all 0.3s ease;
    cursor: pointer;
}
.button-box:hover.topics {
    background-color: #00C2A8;
    color: white;
    border-color: #00C2A8;
}
.button-box:hover.not-for-me {
    background-color: #FF6B6B;
    color: white;
    border-color: #FF6B6B;
}
.container-row {
    display: flex;
    gap: 20px;
    margin-top: 30px;
}
.left-btn {
    flex: 2;
}
.right-btn {
    flex: 1;
}
</style>

<div class="container-row">
    <form method="post">
        <button class="button-box topics left-btn" name="show_topics" type="submit">Topics I Follow 💚</button>
    </form>
    <div class="button-box not-for-me right-btn">
        Not for me ❌
    </div>
</div>
""", unsafe_allow_html=True)

# Bottone dinamico che apre il menu
if st.session_state.get("topics_show") or "show_topics" in st.experimental_get_query_params():
    st.session_state.topics_show = True

if st.session_state.topics_show:
    st.session_state.selected_topics = st.multiselect(
        "🎯 Choose your favorite topics (max 3):",
        ["Politics", "Economy", "Technology", "Science", "Sports", "Art & Culture", "Environment", "Health", "Geopolitics"],
        default=st.session_state.selected_topics,
        max_selections=3
    )
 
# OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Interests selection
st.subheader("What are you interested in today?")
interests = st.multiselect(
    "Choose up to 3 topics",
    ["Politics", "Economy", "Technology", "Science", "Sports", "Art & Culture", "Environment", "Health", "Geopolitics"],
    max_selections=3
)

if st.button("Generate My News") and interests:
    with st.spinner("Generating your personalized news..."):
        prompt = (
            f"Write 3 short news summaries (max 80 words each) "
            f"based on current global topics, tailored to someone interested in: {', '.join(interests)}. "
            f"Write in a clear, neutral tone, without fluff. Format each with a title and summary."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            output = response.choices[0].message.content
            st.markdown("### 🗞️ Your News:")
            st.markdown(output)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
else:
    st.info("Select at least one interest and click the button.")

