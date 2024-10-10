"""Python file to serve as the frontend"""

import os
from dotenv import load_dotenv
import streamlit as st
from loguru import logger
from pinecone import Pinecone
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

dotenv_path = "secrets.env"
load_dotenv(dotenv_path)

INDEX_NAME = "dating-plan-gpt-index"

st.set_page_config(page_title="DatingPlanGPT", page_icon=":robot:")


@st.cache_resource
def init_pinecone(index_name: str):
    """Initialize Pinecone client"""
    logger.info("initializing pinecone...")
    return Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY"),
    ).Index(index_name)


def load_chain() -> RetrievalQA:
    """Logic for loading the chain you want to use should go here."""
    llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings
    )

    prompt_template = """Act as a date planner and generate a creative and flexible dating plan based on the context and requirements provided. 
    Requirements: Your plan should be adaptable to various user constraints such as time, preferences, and other specific requirements. 
    Ensure your responses are diverse and not limited to a fixed number of locations or repetitive suggestions. 
    Use your creativity to provide unique and engaging dating plans for each query. 
    Make sure the timing of the activities in the plan makes sense; for longer available hours, suggest more than one item in the plan. 
    As you currently do not have the ability to remember past conversations, ensure each response is tailored to the specific query at hand. 
    Do not include "overall rating" and "category" when giving the user your final answer. 
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    When coming up with locations to suggest, you must use name field, which is the name of the restaruant/location/mall/museum. Do not use imaginary or made-up names.
    Also, Take into account of the caption, category and opening_hours field.
    Format the response in time-table like manner, and explain why you chose the locations you chose. Make them engaging and enticing.
    Question: {question}

    Answer: """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True,
    )

    return qa


if __name__ == "__main__":
    index = init_pinecone(INDEX_NAME)  # Initialize Pinecone client
    chain = load_chain(index)

    # From here down is all the StreamLit UI.
    st.header("Generate a dating plan with Dating-GPT")

    # Get user input
    user_input: str = st.text_area(
        "Ask for a dating plan.",
        placeholder="For e.g. I am available from 5pm to 9pm. Help me plan a date to a museum and japanese restaurant",
    )

    if user_input:
        output = chain({"query": user_input})
        st.write(output["result"])
