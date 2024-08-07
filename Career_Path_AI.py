import streamlit as st
import os
import dotenv
from openai import AzureOpenAI

# Environment variables
dotenv.load_dotenv()
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Azure OpenAI client
client = AzureOpenAI(api_key=AOAI_KEY, azure_endpoint=AOAI_ENDPOINT, api_version="2024-05-01-preview")

st.title("Career Path AI 🎓")

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are an AI that recommends career paths based on user inputs."}]

# Button to reset the conversation
if st.sidebar.button("Reset Career Recommendations"):
    st.session_state.messages = [{"role": "system", "content": "You are an AI that recommends career paths based on user inputs."}]

# User questions for High Schoolers
education_level = st.radio("Are you currently in High School or College?", ["High School", "College"])

if education_level == "High School":
    enjoyed_classes = st.text_input("What classes do you enjoy the most?")
    best_classes = st.text_input("What classes are you the best at?")
    interests = st.text_area("What are you interested in?")
    skills = st.text_input("What are some important skills you have?")
    min_salary = st.number_input("What minimum amount of money do you want to earn annually?", min_value=0, value=30000, step=5000)

    if st.button("Get Career Paths"):
        prompt = f"""Based on the following information about a high school student, suggest a set of career paths they should consider:

        Interests: {interests}
        Enjoyed classes: {enjoyed_classes}
        Minimum desired salary: ${min_salary:,} per year
        Best classes: {best_classes}
        Skills: {skills}

        Please provide a list of at least 5 career paths that align with the student's interests, skills, and salary expectations. For each career path, briefly explain why it might be a good fit."""

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Generating career recommendations..."):
            response = client.chat.completions.create(
                model="gpt-35-turbo",
                messages=st.session_state.messages,
                stream=False,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.95,
            )
            response_content = response.choices[0].message.content
            st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})
# User questions for College students
elif education_level == "College":
    major = st.text_input("What is your major?")
    other_classes = st.text_input("What other classes are you taking?")
    best_class = st.text_input("What class are you best in?")
    interests = st.text_area("What are you interested in?")
    skills = st.text_input("What are some important skills you have?")
    desired_salary = st.number_input("How much money do you desire to earn annually?", min_value=0, value=50000, step=5000)

    if st.button("Get Career Paths"):
        prompt = f"""Based on the following information about a college student, suggest a set of career paths they should consider:

        Interests: {interests}
        Major: {major}
        Other classes: {other_classes}
        Best class: {best_class}
        Desired salary: ${desired_salary:,} per year
        Skills: {skills}

        Please provide a list of at least 5 career paths that align with the student's major, interests, skills, and salary expectations. For each career path, briefly explain why it might be a good fit and how it relates to their studies."""

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Generating career recommendations..."):
            response = client.chat.completions.create(
                model="gpt-35-turbo",
                messages=st.session_state.messages,
                stream=False,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.95,
            )
            response_content = response.choices[0].message.content
            st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})