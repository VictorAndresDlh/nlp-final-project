import io
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode
from PIL import Image
import numpy as np

mask_image = np.array(Image.open('bogota.png'))
def show_wordcloud(data):
    wordcloud = WordCloud(
        background_color = "#0E1117",
        contour_width=0,
        colormap='Paired',
        max_words = 350,
        max_font_size = 40, 
        scale = 3,
        random_state = 42,
        mask=mask_image,
        margin=1,
    ).generate(str(data))

    fig = plt.figure(1, figsize = (10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.tight_layout(pad = 0)

    # Convert plot to PNG image
    png = io.BytesIO()
    plt.savefig(png, format='png', bbox_inches = 'tight', pad_inches = 0)
    plt.clf()
    png.seek(0)
    png_image = Image.open(png)

    # Display the plot as an image in Streamlit, which removes the border
    st.image(png_image)


nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('spanish'))
def preprocess_text(text):
    # Lowercasing the text
    text = text.lower()
    # Tokenizing the text
    words = nltk.word_tokenize(text)
    # Removing punctuation and stop words
    words = [word for word in words if word.isalpha() and word not in stop_words]
    # Removing accents
    #words = [unidecode(word) for word in words]
    return " ".join(words)

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# Add a sidebar
st.sidebar.title('Configuración')
# List of file names
file_names = {'Juan Daniel Oviedo': 'oviedo.txt',
              'Carlos Fernando Galán': 'galan.txt',
              'Diego Molano': 'molano.txt',
              'Gustavo Bolivar': 'bolivar.txt'}
selected_file = st.sidebar.selectbox('Escoja un candidato', file_names.keys())
# Title of the app
st.title('Elecciones Bogotá 2023')
st.subheader(f'¿De qué habla {selected_file}?')

with open(file_names[selected_file], 'r', encoding='utf-8') as f:
    f = f.read()
    f = preprocess_text(f)
 
#if st.sidebar.button("Generate Word Cloud"):
show_wordcloud(f)