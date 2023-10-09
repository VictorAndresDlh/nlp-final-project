from wordcloud import WordCloud
import io
import spacy
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import es_core_news_sm


# Function to preprocess text data for the word cloud
def preprocess_text(text):
    # Load the Spanish language model for spaCy
    nlp = es_core_news_sm.load()
    # Parse the text with spaCy and extract relevant tokens
    doc = nlp(text.lower())
    words = [
        token.text
        for token in doc
        if token.pos_
        in ["VERB", "NOUN", "ADJ", "PROPN"]  # Only include certain parts of speech
        and token.lemma_ not in "tener"  # Exclude certain lemmas
        and token.text.lower()
        not in ["bogotá", "bogota", "ciudad"]  # Exclude certain words
    ]
    # Join the extracted tokens into a single string
    return " ".join(words)


# Function to generate and display a word cloud from text data
mask_image = np.array(
    Image.open("bogota.png")
)  # Load the mask image for the word cloud


def show_wordcloud(file_names, selected_file):
    # Load and preprocess the selected candidate's text data
    with open(file_names[selected_file], "r", encoding="utf-8") as f:
        f = f.read()
        f = preprocess_text(f)
    # Create a WordCloud object with specified parameters
    wordcloud = WordCloud(
        background_color="#0E1117",  # Set the background color of the word cloud
        colormap="Paired",  # Set the color map for the word cloud
        max_words=350,  # Set the maximum number of words to include in the word cloud
        max_font_size=40,  # Set the maximum font size for the words in the word cloud
        scale=3,  # Set the scale factor for the word cloud
        random_state=42,  # Set the random state for the word cloud
        mask=mask_image,  # Set the mask image for the word cloud
    ).generate(str(f))

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

    return png_image
