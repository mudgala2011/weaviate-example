# Resume Vector Database Project

This project demonstrates how to create and manage a vector database for resume data using Weaviate. It includes functionality for processing resume data from a Kaggle dataset and storing it with vector embeddings for semantic search capabilities.

## Project Structure

```
bys-vdb/
├── data/
│   └── Resume/           # Extracted resume dataset
├── src/
│   ├── unzip_resumes.py  # Script to extract dataset
│   ├── create_collection.py  # Creates Weaviate collection
│   ├── import_resumes.py    # Imports data to Weaviate
│   └── query_resumes.py     # Query functionality
├── README.md
└── requirements.txt
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd bys-vdb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key
WEAVIATE_CLUSTER_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key
```

## Usage

1. Extract the resume dataset:
```bash
python src/unzip_resumes.py
```

2. Create Weaviate collection:
```bash
python src/create_collection.py
```

3. Import resumes to Weaviate:
```bash
python src/import_resumes.py
```

4. Query the database:
```bash
python src/query_resumes.py
```

## Features

- Resume data extraction and processing
- Vector database creation using Weaviate
- OpenAI embeddings integration
- Semantic search capabilities
- Batch processing for efficient data import

## Dependencies

See `requirements.txt` for full list of dependencies.

## Data Source

The resume dataset used in this project is sourced from Kaggle. Please ensure you have the proper permissions and citations when using the dataset.
[Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)


