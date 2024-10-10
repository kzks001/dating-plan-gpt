import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from loguru import logger

dotenv_path = "./secrets.env"
load_dotenv(dotenv_path)

INDEX_NAME = "dating-plan-gpt-index"
DIMENSION = 1536


def create_pinecone_index_if_not_exists(
    pinecone, index_name: str, dimension: int = 1536
):
    """Create a pinecone index if it does not exist.

    Args:
        index_name (str): The name of the index to create.
    """
    existing_indexes = [index_info["name"] for index_info in pinecone.list_indexes()]
    logger.info("initializing pinecone...")
    if INDEX_NAME not in existing_indexes:
        pinecone.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        logger.info(f"Creating Index {index_name}.")
    logger.info(f"Index {index_name} already exists. Skipping index creation.")

    return pc.Index(index_name)


if __name__ == "__main__":
    pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY"),  # find at app.pinecone.io
    )
    index = create_pinecone_index_if_not_exists(
        pc, index_name=INDEX_NAME, dimension=DIMENSION
    )

    # load the data
    loader = CSVLoader(file_path="./data/reviews.csv")
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    logger.info("Indexing documents...")
    try:
        vector_store = PineconeVectorStore(index=index, embedding=embeddings)
        # docsearch = Pinecone.from_texts([t.page_content for t in documents], embeddings, index_name=INDEX_NAME)
        vector_store.add_documents(documents=documents)
    except Exception as e:
        logger.error(e)
        raise e
    else:
        logger.info("Documents indexed.")
