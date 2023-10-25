import pandas as pd
from sentence_transformers import SentenceTransformer, util
import chromadb
import ast

# Load the data from a CSV file and convert the "embeddings" column from a string to a list
df = pd.read_csv("final.csv")

# Load the pre-trained Sentence Transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Create a new column to store the embeddings
df["embeddings"] = model.encode(df['transcribe'], batch_size = 64).tolist()
df['id_database'] = df.apply(lambda x: str(x.name) + "-" + x['id'], axis=1)

# Create a new ChromaDB collection and add the data from the DataFrame to it
client = chromadb.Client()
try:
    collection = client.create_collection(
        name="alcalde_bogota", metadata={"hnsw:space": "cosine"}
    ) # Create a new ChromaDB collection with the specified name and metadata
    # Create the collection
    collection.add(
        ids=df["id_database"].tolist(),
        embeddings=df["embeddings"].tolist(),
        metadatas=df[
            ["video", "candidato", "date", "title", "webpage_url", "transcribe"]
        ].to_dict("records"),
    )  # Add the data from the DataFrame to the ChromaDB collection
except ValueError:
    collection = client.get_collection("alcalde_bogota")

candidatos = {
    "Juan Daniel Oviedo": "oviedo",
    "Carlos Fernando Galán": "galan",
    "Diego Molano": "molano",
    "Gustavo Bolivar": "bolivar",
}

# Define a function to query the ChromaDB collection for similar text
def query(text, selected_file):
    content = collection.query(
        query_texts=[text],  # The text to search for
        n_results=3,  # The number of results to return
        where = {"candidato": candidatos[selected_file]}
    )
    return (
        content["metadatas"][0],
        content["distances"][0],
    )  # Return the metadata for the matching documents
