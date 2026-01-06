from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv()


#langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot with Ollama"


## Prompt Template
Prompt=ChatPromptTemplate.from_messages([
    ("system","you are a helpful assistant. please response to the user question"),
    ("user","question: {question}")
])

def generate_response(question,engine,temperature,max_tokens):
    
    llm=Ollama(model=engine)
    output_parser=StrOutputParser()
    chain=Prompt | llm | output_parser
    answer=chain.invoke({"question":question})
    return answer

## Title of the app
st.title("Enhaced Q&A Chatbot with Ollama")

##Drop down for model selection 
engine=st.sidebar.selectbox("Select the model",["gemma:2b","llama3"])

## Adjusting the temperature and max tokens
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

# main interface for user input
st.write("Go ahead and ask a question")
user_input=st.text_input("Ask a question about your data")
if user_input:
    response=generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)

else:
    st.write("Please enter a question")
