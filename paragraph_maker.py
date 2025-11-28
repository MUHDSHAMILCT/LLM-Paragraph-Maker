import os
import streamlit as st
from groq import Groq

# ----------------------
# CONFIGURATION
# ----------------------
API_KEY = "add_your_api_key"  # Replace or use st.sidebar to update
MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=API_KEY)

# ----------------------
# PARAGRAPH GENERATION
# ----------------------
def generate_paragraph(topic, tone, paragraphs, word_limit):
    prompt = (
        f"Write {paragraphs} paragraph(s) about '{topic}' in a {tone} tone. "
        f"Each paragraph should be around {word_limit} words. "
        "Write clearly, simply and in a student-friendly manner."
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You write clear and simple paragraphs."},
            {"role": "user", "content": prompt},
        ],
        model=MODEL,
        temperature=0.5,
        max_tokens=1000,
    )

    return response.choices[0].message.content


# ----------------------
# STREAMLIT UI
# ----------------------

st.set_page_config(page_title="LLM Paragraph Maker", page_icon="✍️", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
body { background: #f4f6ff; }
.block {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-top: 20px;
}
.stButton>button {
    background-color: #4f46e5;
    color: white;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align:center;'>✍️ LLM Paragraph Generator</h1>", unsafe_allow_html=True)
st.write("Create clean, simple, and attractive paragraphs instantly using Groq LLM.")

# --- Input Section ---
with st.container():
    topic = st.text_input("Enter Topic", placeholder="Eg: Importance of Fruits")
    tone = st.selectbox("Select Tone", ["Simple", "Formal", "Friendly", "Academic", "Exam-Style"])
    paragraphs = st.slider("Number of paragraphs", 1, 5, 1)
    word_limit = st.slider("Word limit per paragraph", 30, 300, 100)

    st.write("---")

    if st.button("Generate Paragraph"):
        if topic.strip() == "":
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating your paragraph..."):
                output = generate_paragraph(topic, tone, paragraphs, word_limit)

            # Display results
            st.markdown("<div class='block'>", unsafe_allow_html=True)
            st.subheader("Generated Paragraph")
            st.write(output)
            st.markdown("</div>", unsafe_allow_html=True)

            # Download
            st.download_button(
                label="Download as .txt",
                data=output,
                file_name=f"{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )