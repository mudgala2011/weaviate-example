import weaviate
import os
from weaviate.classes.init import Auth

# Setup Weaviate client
openai_key = os.getenv("OPENAI_API_KEY")
headers = {"X-OpenAI-Api-Key": openai_key}
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

wclient = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_CLUSTER_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers=headers,
)


def search_hr_leadership_resumes(limit=3):
    """
    Search for HR leadership resumes using hybrid search
    """
    resume_collection = wclient.collections.get("Resume_DB")

    # Query text that describes what we're looking for
    query_text = """HR specialist with leadership experience, team management, 
                   head of HR department, HR director, HR team lead"""

    # Perform hybrid search - no .do() needed in newer versions
    response = resume_collection.query.hybrid(
        query=query_text,
        limit=limit,
        alpha=0.5,  # Balance between vector and keyword search
    )

    return response


def display_results(results):
    """
    Display the search results in a readable format
    """
    try:
        # Access the results directly from the QueryReturn object
        resumes = results.objects

        print("\nSearch Results:")
        print(f"Number of results: {len(resumes)}")

        for idx, resume in enumerate(resumes, 1):
            print(f"\nResult #{idx}")
            # Score is accessed directly from metadata object
            print(
                f"Score: {resume.metadata.score if resume.metadata.score is not None else 'N/A'}"
            )
            print(
                f"Distance: {resume.metadata.distance if resume.metadata.distance is not None else 'N/A'}"
            )
            print(f"Resume ID: {resume.properties.get('resume_id', 'N/A')}")
            print(f"Category: {resume.properties.get('resume_category', 'N/A')}")
            print("Resume Text Preview: ")
            if "resume_text" in resume.properties:
                print(f"{resume.properties['resume_text'][:200]}...\n")
            print("-" * 80)
    except Exception as e:
        print(f"Error parsing results: {e}")
        print("Raw results type:", type(results))
        # Print full structure for debugging
        if hasattr(results, "objects") and results.objects:
            print("Properties available:", resume.properties.keys())
            print("Metadata structure:", resume.metadata)


if __name__ == "__main__":
    search_results = search_hr_leadership_resumes()
    display_results(search_results)
