import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot with Groq"

## Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant. please response to the user question"),
    ("user", "question: {question}")
])

def generate_response(question, api_key, model, temperature, max_tokens):
    llm_instance = ChatGroq(
        model=model,
        groq_api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens
    )
    output_parser = StrOutputParser()
    chain = prompt | llm_instance | output_parser
    answer = chain.invoke({"question": question})
    return answer

## Title of the app
st.title("Enhanced Q&A Chatbot with Groq")

# Sidebar settings
st.sidebar.title("Settings")

# API Key input
api_key = st.sidebar.text_input("Groq API Key", type="password")

# Model selection for Groq
model = st.sidebar.selectbox("Select the model", [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
])

## Adjusting the temperature and max tokens
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=2000, value=500)

# Main interface for user input
st.write("Go ahead and ask a question")
user_input = st.text_input("Ask a question")

if user_input and api_key:
    with st.spinner("Generating response..."):
        try:
            response = generate_response(user_input, api_key, model, temperature, max_tokens)
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
elif user_input and not api_key:
    st.warning("Please enter your Groq API key in the sidebar")
else:
    st.write("Please enter a question")