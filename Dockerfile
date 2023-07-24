# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use an argument for the API key
ARG OPENAI_API_KEY

# Set the environment variable in the container
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Make port 8501 available to the world outside this container
EXPOSE 8527

# Run main.py when the container launches
CMD streamlit run main.py