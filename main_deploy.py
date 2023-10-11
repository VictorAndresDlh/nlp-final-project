# Chroma and SQLite3 workaround
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import streamlit as st
from vectordb import query
from create_wordcloud import show_wordcloud

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
# Generate and display a word cloud from the preprocessed text data
st.image(show_wordcloud(file_names, selected_file))

# Add a divider and a subheader for the next steps
st.divider()
st.header(f"¿Qué dice {selected_file} sobre...?")
text = st.text_input("Escribe un texto para buscar en las entrevistas y debates")
if text:
    results, distances = query(text)
    _, col2, _, col4, _, col6, _ = st.columns([1, 5, 1, 5, 1, 5, 1])
    with col2:
        st.markdown(f"'{results[0]['text']}'")
        st.video(results[0]["url"])
        st.markdown(f"Distancia usando similaridad de coseno: {distances[0]:.2f}")
    with col4:
        st.markdown(f"'{results[1]['text']}'")
        st.video(results[1]["url"])
        st.markdown(f"Distancia usando similaridad de coseno: {distances[1]:.2f}")
    with col6:
        st.markdown(f"'{results[2]['text']}'")
        st.video(results[2]["url"])
        st.markdown(f"Distancia usando similaridad de coseno: {distances[2]:.2f}")
