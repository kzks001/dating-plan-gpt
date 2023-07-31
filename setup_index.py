import os
import pinecone
from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from loguru import logger

dotenv_path = "./secrets.env"
load_dotenv(dotenv_path)

INDEX_NAME = "dating-plan-gpt-index"
DIMENSION = 1536


def create_pinecone_index_if_not_exists(index_name: str, dimension: int = 1536):
    """Create a pinecone index if it does not exist.

    Args:
        index_name (str): The name of the index to create.
    """
    logger.info("initializing pinecone...")
    if index_name in pinecone.list_indexes():
        logger.info(f"Index {index_name} already exists. Skipping index creation.")
        return

    logger.info(f"Creating index {index_name}")
    pinecone.create_index(name=index_name, dimension=dimension)


if __name__ == "__main__":
    pinecone.init(
        api_key=os.environ.get("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.environ.get("PINECONE_API_ENV"),  # next to api key in console
    )
    create_pinecone_index_if_not_exists(index_name=INDEX_NAME, dimension=DIMENSION)

    # load the data
    loader = CSVLoader(file_path="./data/reviews.csv")
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    logger.info("Indexing documents...")
    try:
        # docsearch = Pinecone.from_texts([t.page_content for t in documents], embeddings, index_name=INDEX_NAME)
        docsearch = Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    except Exception as e:
        logger.error(e)
        raise e
    else:
        logger.info("Documents indexed.")
