import pandas as pd
from sentence_transformers import SentenceTransformer, util
import chromadb
import ast

# Load the data from a CSV file and convert the "embeddings" column from a string to a list
df = pd.read_csv("data_test.csv")
df["embeddings"] = df["embeddings"].apply(ast.literal_eval)

# Load the pre-trained Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Create a new ChromaDB collection and add the data from the DataFrame to it
client = chromadb.Client()
collection = client.create_collection(
    name="alcalde_bogota", metadata={"hnsw:space": "cosine"}
)  # Create a new ChromaDB collection with the specified name and metadata

collection.add(
    ids=df["id_database"].tolist(),
    embeddings=df["embeddings"].tolist(),
    metadatas=df[
        ["start", "end", "text", "views", "publish_date", "url", "title"]
    ].to_dict("records"),
)  # Add the data from the DataFrame to the ChromaDB collection


# Define a function to query the ChromaDB collection for similar text
def query(text):
    content = collection.query(
        query_texts=[text],  # The text to search for
        n_results=3,  # The number of results to return
    )
    return (
        content["metadatas"][0],
        content["distances"][0],
    )  # Return the metadata for the matching documents
