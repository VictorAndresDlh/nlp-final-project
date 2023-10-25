# Chroma and SQLite3 workaround
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import streamlit as st
from vectordb import query
from create_wordcloud import show_wordcloud


# Define a function to generate the word cloud
@st.cache_data
def generate_wordcloud(file_names, selected_file, list_pos):
    return show_wordcloud(file_names, selected_file, list_pos)


@st.cache_data
def generate_query(text, selected_file):
    return query(text, selected_file)


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
# Add a divider and a subheader for the next steps
st.divider()
st.header(f"¿Qué dice {selected_file} sobre...?")
text = st.text_input("Escribe un texto para buscar en las entrevistas y debates")
if text:
    results, distances = generate_query(text, selected_file)
    _, col2, _, col4, _, col6, _ = st.columns([1, 5, 1, 5, 1, 5, 1])
    with col2:
        st.video(results[0]["webpage_url"])
        st.markdown(f"'{results[0]['transcribe']}'")
        st.markdown(f"Distancia usando similaridad de coseno: {distances[0]:.2f}")
    with col4:
        st.video(results[1]["webpage_url"])
        st.markdown(f"'{results[1]['transcribe']}'")
        st.markdown(f"Distancia usando similaridad de coseno: {distances[1]:.2f}")
    with col6:
        st.video(results[2]["webpage_url"])
        st.markdown(f"'{results[2]['transcribe']}'")
        st.markdown(f"Distancia usando similaridad de coseno: {distances[2]:.2f}")
st.divider()
st.header(f"¿De qué habla {selected_file}?")
st.markdown(
    f"A continuación te mostramos las palabras más comunes usadas por el candidato {selected_file} tanto en entrevistas como en debates:"
)
# Generate and display a word cloud from the preprocessed text data
dict_pos = {
    "noun_on": "NOUN",
    "verb_on": "VERB",
    "adj_on": "ADJ",
    "propn_on": "PROPN",
}  # Dictionary of parts of speech
col1, col2 = st.columns([7, 2])
with col2:
    st.markdown("Seleccione las partes de discurso a incluir en el wordcloud:")
    selected = []
    noun_on = st.toggle("Sustantivos", True)
    if noun_on:
        selected.append("noun_on")
    propn_on = st.toggle("Nombres propios", True)
    if propn_on:
        selected.append("propn_on")
    verb_on = st.toggle("Verbos", True)
    if verb_on:
        selected.append("verb_on")
    adj_on = st.toggle("Adjetivos", True)
    if adj_on:
        selected.append("adj_on")
    # Get the corresponding values for the selected keys
    list_pos = [dict_pos[key] for key in selected]
with col1:
    if list_pos == []:
        st.error("No se ha seleccionado ninguna parte de discurso")
    else:
        wordcloud = generate_wordcloud(file_names, selected_file, list_pos)
        st.image(wordcloud)

