import weaviate
import os
import csv
from weaviate.classes.init import Auth
import weaviate.classes.config as wc

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

# Create collection if it doesn't exist
res_db = wclient.collections.create(
    "Resume_DB",
    vector_config=[
        wc.Configure.Vectors.text2vec_openai(
            name="resume_vector", model="text-embedding-3-large", dimensions=1024
        )
    ],
    generative_config=wc.Configure.Generative.openai(model="gpt-3.5-turbo"),
    properties=[
        wc.Property(
            name="resume_id", data_type=wc.DataType.TEXT, skip_vectorization=True
        ),
        wc.Property(name="resume_text", data_type=wc.DataType.TEXT),
        wc.Property(name="resume_category", data_type=wc.DataType.TEXT),
    ],
)


def batch_import_resumes(file_path, batch_size=100):
    """
    Import resumes in batches for better performance
    """
    resume_collection = wclient.collections.get("Resume_DB")

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if exists

        batch = []
        total_processed = 0

        for row in reader:
            if len(row) >= 3:  # Ensure row has required columns
                properties = {
                    "resume_id": row[0],
                    "resume_text": row[1],
                    "resume_category": row[2],
                }
                batch.append(properties)

                if len(batch) >= batch_size:
                    try:
                        # Insert batch
                        with resume_collection.batch.fixed_size(
                            batch_size=batch_size
                        ) as batch_processor:
                            for item in batch:
                                batch_processor.add_object(properties=item)

                        total_processed += len(batch)
                        print(f"Processed {total_processed} resumes")
                        batch = []
                    except Exception as e:
                        print(f"Error processing batch: {e}")

        # Process remaining items
        if batch:
            try:
                with resume_collection.batch.fixed_size(
                    batch_size=len(batch)
                ) as batch_processor:
                    for item in batch:
                        batch_processor.add_object(properties=item)
                total_processed += len(batch)
                print(f"Processed {total_processed} resumes")
            except Exception as e:
                print(f"Error processing final batch: {e}")


if __name__ == "__main__":
    csv_file_path = "path/to/your/fileResume_cleaned.csv"
    batch_import_resumes(csv_file_path)
    print("Import completed!")
