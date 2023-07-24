import os
import streamlit as st
import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAIChat
from loguru import logger


def main() -> None:
    """
    Main function to run the Dating-GPT application.

    This function loads environment variables, sets up the Streamlit page,
    creates an agent using the OpenAI model and a CSV file, and generates
    a response based on the user's input question.
    """
    # Load environment variables
    # load_dotenv("./secrets.env")

    # Set up Streamlit page
    st.set_page_config(page_title="Dating-GPT")
    st.header("Generate a dating plan with Dating-GPT")

    # Get user input
    user_question: str = st.text_input("Ask for a dating plan.")

    # Create an agent using the OpenAI model and a CSV file
    api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from environment variable
    llm = OpenAIChat(openai_api_key=api_key, temperature=0.5, model="gpt-4")

    csv_file: str = "./data/places.csv"
    agent = create_csv_agent(llm, csv_file, verbose=True)

    # Generate a response if the user input is not empty
    if user_question is not None and user_question != "":
        prompt: str = f"""Answer the question based on the context, and requirements below. 

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
