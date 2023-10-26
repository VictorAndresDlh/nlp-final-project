from wordcloud import WordCloud
import spacy
from PIL import Image
import numpy as np


# Function to preprocess text data for the word cloud
def preprocess_text(text, list_pos):
    # Load the Spanish language model for spaCy
    nlp = spacy.load("es_core_news_sm")
    # Parse the text with spaCy and extract relevant tokens
    doc = nlp(text.lower())
    words = [
        token.text
        for token in doc
        if token.pos_ in list_pos  # Only include certain parts of speech
        and token.text.lower()
        and not token.is_stop  # Exclude stopwords
        and token.text not in ["bogotá", "ciudad"] # Compare token.text with string and exclude words
    ]
    # Join the extracted tokens into a single string
    return " ".join(words)


# Function to generate and display a word cloud from text data
mask_image = np.array(
    Image.open("bogota.png")
)  # Load the mask image for the word cloud


def show_wordcloud(file_names, selected_file, list_pos):
    # Load and preprocess the selected candidate's text data
    with open(file_names[selected_file], "r", encoding="utf-8") as f:
        f = f.read()
        f = preprocess_text(f, list_pos)
    # Create a WordCloud object with specified parameters
    wordcloud = WordCloud(
        background_color="#0E1117",  # Set the background color of the word cloud
        colormap="Paired",  # Set the color map for the word cloud
        max_words=300,  # Set the maximum number of words to include in the word cloud
        max_font_size=40,  # Set the maximum font size for the words in the word cloud
        scale=3,  # Set the scale factor for the word cloud
        random_state=42,  # Set the random state for the word cloud
        mask=mask_image,  # Set the mask image for the word cloud
    ).generate(str(f))
    png_image = wordcloud.to_image()

    return png_image
