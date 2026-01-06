import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()


#langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot with openai"



## Prompt Template
prompt=ChatPromptTemplate.from_messages([
    ("system","you are a helpful assistant. please response to the user question"),
    ("user","question: {question}")
])

def generate_response(question,api_key,llm,temperature,max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    output_parser=StrOutputParser()
    chain=prompt | llm | output_parser
    answer=chain.invoke({"question":question})
    return answer
    
    

## Title of the app
st.title("Enhaced Q&A Chatbot with OpenAI")
st.sidebar.title("settings")
api_key=st.sidebar.text_input("OpenAI API Key",type="password")

##Drop down for model selection 
llm=st.sidebar.selectbox("Select the model",["gpt-4o","gpt-4-turbo","gpt-3.5-turbo"])

## Adjusting the temperature and max tokens
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

# main interface for user input
st.write("Go ahead and ask a question")
user_input=st.text_input("Ask a question about your data")
if user_input:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)

else:
    st.write("Please enter a question")
