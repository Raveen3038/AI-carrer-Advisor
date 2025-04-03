import streamlit as st
import fitz  
import docx2txt
import google.generativeai as genai
import os

# Configure Google Gemini API
API_KEY = "AIzaSyC2fNUqnSgqqosP9ZtwhGZv9LPONVy-sjc"  # Replace with your valid Gemini API key
genai.configure(api_key=API_KEY)

def extract_text(file):
    """Extracts text from PDF or DOCX files."""
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text("text") for page in doc])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    else:
        return None

def generate_feedback(resume_text):
    """Generates AI feedback for the uploaded resume."""
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    try:
        response = model.generate_content(f"Review the following resume and provide suggestions: {resume_text}")
        return response.text
    except Exception as e:
        return f"Error generating feedback: {e}"

def compare_with_job(resume_text, job_description):
    """Compares resume with job description and provides insights."""
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    try:
        response = model.generate_content(
            f"Compare this resume to the given job description and suggest improvements:\n\nResume: {resume_text}\n\nJob Description: {job_description}"
        )
        return response.text
    except Exception as e:
        return f"Error in job comparison: {e}"

# Streamlit UI
st.title("📄 AI Resume & Career Advisor")
st.write("Upload your resume and get AI-powered feedback!")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
job_desc = st.text_area("📌 Paste Job Description (Optional)")

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    if resume_text:
        st.subheader("✅ Resume Analysis")
        feedback = generate_feedback(resume_text)
        st.write(feedback)
        
        if job_desc:
            st.subheader("🎯 Job Fit Analysis")
            comparison = compare_with_job(resume_text, job_desc)
            st.write(comparison)
    else:
        st.error("⚠ Unsupported file format. Please upload a valid PDF or DOCX.")
