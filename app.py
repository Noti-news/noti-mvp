import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Notì – AI News", page_icon="📰")

st.title("📰 Notì – Your Daily News, Reimagined")

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

