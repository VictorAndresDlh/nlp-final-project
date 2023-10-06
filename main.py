import io
import spacy
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Load the mask image for the word cloud
mask_image = np.array(Image.open("bogota.png"))


# Function to generate and display a word cloud from text data
def show_wordcloud(data):
    # Create a WordCloud object with specified parameters
    wordcloud = WordCloud(
        background_color="#0E1117",
        colormap="Paired",
        max_words=350,
        max_font_size=40,
        scale=3,
        random_state=42,
        mask=mask_image,
    ).generate(str(data))

    # Create a plot of the word cloud
    plt.figure(1, figsize=(10, 10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.tight_layout(pad=0)

    # Convert the plot to a PNG image
    png = io.BytesIO()
    plt.savefig(png, format="png", bbox_inches="tight", pad_inches=0)
    plt.clf()
    png.seek(0)
    png_image = Image.open(png)

    # Display the plot as an image in Streamlit, which removes the border
    st.image(png_image)


# Load the Spanish language model for spaCy
nlp = spacy.load("es_core_news_sm")


# Function to preprocess text data for the word cloud
def preprocess_text(text):
    # Parse the text with spaCy and extract relevant tokens
    doc = nlp(text.lower())
    words = [
        token.text
        for token in doc
        if token.pos_ in ["VERB", "NOUN", "ADJ", "PROPN"]
        and token.lemma_ not in "tener"
        and token.text.lower() not in ["bogotá", "bogota", "ciudad"]
    ]
    # Join the extracted tokens into a single string
    return " ".join(words)


# Configure the Streamlit page layout
st.set_page_config(layout="wide")
st.set_option("deprecation.showPyplotGlobalUse", False)

# Add a sidebar for selecting a candidate file
st.sidebar.title("Configuración")
file_names = {
    "Juan Daniel Oviedo": "oviedo.txt",
    "Carlos Fernando Galán": "galan.txt",
    "Diego Molano": "molano.txt",
    "Gustavo Bolivar": "bolivar.txt",
}
selected_file = st.sidebar.selectbox("Escoja un candidato", file_names.keys())

# Display the app title and selected candidate
st.title("Elecciones Bogotá 2023 :city_sunset:")
st.subheader(
    "En este dashboard, podrás explorar los temas más importantes de los candidatos a la alcaldía de Bogotá."
)
st.divider()
st.header(f"¿De qué habla {selected_file}?")
st.markdown(
    f"A continuación te mostramos las palabras más comunes usadas por el candidato {selected_file} tanto en entrevistas como en debates:"
)

# Load and preprocess the selected candidate's text data
with open(file_names[selected_file], "r", encoding="utf-8") as f:
    f = f.read()
    f = preprocess_text(f)

# Generate and display a word cloud from the preprocessed text data
show_wordcloud(f)
st.divider()
st.subheader("Siguientes pasos")
