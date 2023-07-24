import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_csv_agent

# from langchain.agents import load_tools
from langchain.llms import OpenAI


def main():
    load_dotenv("./secrets.env")

    st.set_page_config(page_title="Dating-GPT")
    st.header("Generate a dating plan with Dating-GPT")

    user_question = st.text_input("Ask for a dating plan.")

    llm = OpenAI(temperature=0.5)
    csv_file = "./data/places.csv"
    agent = create_csv_agent(llm, csv_file, verbose=True)

    if user_question is not None and user_question != "":
        prompt = f"""Answer the question based on the context, and requirements below. 

        context: In the context of building meaningful connections and potential romantic partnerships, 
        dating involves the process of getting to know someone better through shared experiences and interactions. 
        This includes spending time together, going on dates, and discovering each other's interests, values, and personality traits. 
        Our aim is to optimize the environment for successful interactions and create opportunities for genuine connections to flourish.

        requirements: Give 3 unique locations, one each for morning, afternoon and night. 
        Be as detailed as possible for what to do at each location.
        Use only the provided CSV file.

        The timings are as follows: morning - 8am-12pm
        afternoon - 12pm - 6pm
        night 6pm-11pm

        question: {user_question}

        answer: """

        response = agent.run(prompt)
        st.write(response)


if __name__ == "__main__":
    main()
