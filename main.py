import os
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from loguru import logger


def main() -> None:
    """
    Main function to run the Dating-GPT application.

    This function loads environment variables, sets up the Streamlit page,
    creates an agent using the OpenAI model and a CSV file, and generates
    a response based on the user's input question.
    """
    # Set up Streamlit page
    st.set_page_config(page_title="Dating-GPT")
    st.header("Generate a dating plan with Dating-GPT")

    # Get user input
    user_question: str = st.text_area("Ask for a dating plan.")

    # Create an agent using the OpenAI model and a CSV file
    api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from environment variable
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.5, model="gpt-4")

    csv_file: str = "data/main.csv"
    agent = create_csv_agent(llm, csv_file, verbose=True)

    # Generate a response if the user input is not empty
    if user_question is not None and user_question != "":
        prompt: str = f"""Act as a date planner and generate a creative and flexible dating plan based on the context and requirements provided. 

        Context: You are given a location's summary of potential dating activities derived from Google reviews. 

        Requirements: Your plan should be adaptable to various user constraints such as time, preferences, and other specific requirements. 
        Ensure your responses are diverse and not limited to a fixed number of locations or repetitive suggestions. 
        Use your creativity to provide unique and engaging dating plans for each query. 
        Make sure the timing of the activities in the plan makes sense; for longer available hours, suggest more than one item in the plan. 
        As you currently do not have the ability to remember past conversations, ensure each response is tailored to the specific query at hand. 
        Do not include "overall rating" and "category" when giving the user your final answer. 

        Question: {user_question}

        Answer: """

        # Log the prompt
        logger.info(f"Prompt: {prompt}")

        # Run the agent and get the response
        response = agent.run(prompt)

        # Log the response
        logger.info(f"Response: {response}")

        # Write the response to the Streamlit page
        st.write(response)


if __name__ == "__main__":
    main()
