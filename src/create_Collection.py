"""
This module sets up a Weaviate vector database connection and creates a collection
for storing resume data with OpenAI embeddings.
"""

import os
import weaviate
from weaviate.classes.init import Auth
import weaviate.classes.config as wc
from weaviate.classes.config import Configure


def create_weaviate_client():
    """
    Creates and returns a Weaviate client instance using environment variables.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    weaviate_url = os.getenv("WEAVIATE_CLUSTER_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")

    if not all([openai_key, weaviate_url, weaviate_key]):
        raise ValueError("Missing required environment variables")

    headers = {"X-OpenAI-Api-Key": openai_key}

    return weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_key),
        headers=headers,
    )


def create_resume_collection(client):
    """
    Creates a Weaviate collection for storing resumes with OpenAI embeddings.

    Args:
        client: Weaviate client instance

    Returns:
        Created collection object
    """
    return client.collections.create(
        "Resume_DB1",
        vector_config=[
            Configure.Vectors.text2vec_openai(
                name="resume_vector", model="text-embedding-3-large", dimensions=1024
            )
        ],
        generative_config=Configure.Generative.openai(model="gpt-3.5-turbo"),
        properties=[
            wc.Property(
                name="resume_id", data_type=wc.DataType.TEXT, skip_vectorization=True
            ),
            wc.Property(name="resume_text", data_type=wc.DataType.TEXT),
            wc.Property(name="resume_category", data_type=wc.DataType.TEXT),
        ],
    )


def main():
    """
    Main function to set up Weaviate collection.
    """
    try:
        # Create Weaviate client
        wclient = create_weaviate_client()

        # Create resume collection
        res_db = create_resume_collection(wclient)

        # Verify collection creation
        resume_collection = wclient.collections.get("Resume_DB")
        print("Collection created successfully:")
        print(resume_collection)

    except Exception as e:
        print(f"Error creating collection: {e}")


if __name__ == "__main__":
    main()
