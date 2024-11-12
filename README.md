# Dating-GPT

## TLDR

![](images/tldr.png)

## Background

This project aims to deliver a unique and interesting spin on dating by combining conversation potential with custom architectural design. It uses the gpt-4o-mini API by OpenAI to suggest dating plans based on the user's unique question. Imagine a dating plan that goes beyond your regular dinner and movie night - our model offers detailed plans for morning, afternoon and evening, carefully crafted to the individual's input.

Leveraging huge amounts of data and machine learning capabilities, it can generate human-like text that reads in a coherent and contextual manner. For this reason, it has vast potential in a variety of use cases - from generating creative content, intelligent virtual assistants, conversational AI, content curation, tutoring systems, code generation, and much more. This project underlines this potential by using the technology to enhance human experiences, like dating.

Note that the code uses gpt-4o-mini by default. Other versions of GPT can be enabled by changing ```gpt_model = "gpt-4o-mini"``` in ```main.py```.

## Getting Started

Following the commands will lead you to deploy a streamlit application locally.

### Setup Pinecone index

1. Create a Pinecone account and acquire an API key.
2. Create virtual environment
    ```bash
    python3.9 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run Python script to create Pinecone index and index data
    ```bash
    python setup_index.py
    ```

### Deploy locally

1. Clone this repository to your local machine.

```bash
git clone https://github.com/YourUsername/project-repo.git
```

2. Install the necessary Python packages.

```bash
pip3 install -r requirements.txt
```

3. Build the Docker image.

```bash
# export OPENAI_API_KEY=<insert api key> && streamlit run main.py
```

**Please replace `<your_api_key>` with your actual OpenAI API key in step 3.**

## Deploy via Docker Compose

1. Clone this repository to your local machine.

```bash
git clone https://github.com/YourUsername/project-repo.git
```

1. Set your OpenAI API key as an environment variable:

```bash
# OPENAI_API_KEY=<insert api key> docker-compose up --build
```

The service will now be accessible at `localhost:8527`.

## Examples

To use the application, navigate to `localhost:8527` in your web browser. You will be prompted to ask for a dating plan. Write your query into the input field and the model will create a unique dating plan for you based on your input.

For example:

-   User query: "I would like a romantic but adventurous park-themed dating plan."
-   Output: Detailed plan on activities for morning, afternoon, and night.

## Future Work

Future enhancements planned for this project include:

-   [x] Use Pinecone instead of Chroma
-   [x] Refactor main.py: add caching to pinecone client so it only gets initialized once
-   [ ] Add memory feature
-   [ ] Integrate with external APIs for more dynamic responses

## Contributors

[Samuel Koh](mailto:samuelkohzk@gmail.com)
