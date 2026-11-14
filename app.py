import streamlit as st
from groq import Groq
import fitz

st.set_page_config(page_title="AI Paper Summarizer")
st.title("📚 AI Research Paper Summarizer")
st.write("Kuthla pan research paper upload kara, AI 1 minat madhe summary deil")

# API Key - adhi Secrets madhun ghe, nasel tar user kadun ghe
api_key = ""
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    api_key = st.text_input("Tuji Groq Key ithe tak (gsk_...)", type="password")
    if not api_key:
        st.warning("Key taklyashivay app chalu honar nahi")
        st.stop()

client = Groq(api_key=api_key)

pdf = st.file_uploader("PDF upload kara", type="pdf")

if pdf and st.button("Summarize Kara"):
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    text = text[:15000]

    if not text.strip():
        st.error("PDF madhe text sapadla nahi. Scanned PDF asel tar chalnar nahi.")
        st.stop()

    prompt = f"""
    Ha research paper summarize kar simple language madhe:
    {text}
    Format:
    1. Title & One Line Summary
    2. Problem Statement
    3. Methodology
    4. Key Findings (3 points)
    5. Conclusion
    """

    with st.spinner("Reading paper..."):
        try:
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("Summary ready!")
            st.write(res.choices[0].message.content)
        except Exception as e:
            st.error(f"Error ala: {e}")
            st.info("Groq Key barobar ahe ka check kar. Streamlit Secrets madhe GROQ_API_KEY takli ahe ka?")