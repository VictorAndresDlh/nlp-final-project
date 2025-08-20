# PoliticalNLP - Bogotá 2023 Election Analysis

A Natural Language Processing application for analyzing and exploring the discourse of Bogotá mayoral candidates in the 2023 election.

## Team Members
- Víctor Andrés De La Hoz
- Anthony Bossa  
- Juliana de Mier

## Project Overview

This Streamlit application provides an interactive platform to explore and analyze the speeches and debates of four candidates who ran for Mayor of Bogotá in 2023:

- **Juan Daniel Oviedo**
- **Carlos Fernando Galán** 
- **Diego Molano**
- **Gustavo Bolívar**

## Features

### 🔍 Semantic Search
- Search for specific topics or keywords across candidate speeches
- Find relevant video segments where candidates discussed particular themes
- Uses vector embeddings and cosine similarity for accurate content matching
- Displays matching video clips with highlighted search terms

### ☁️ Word Cloud Generation
- Generate visual word clouds showing the most frequently used terms by each candidate
- Filter by parts of speech (nouns, verbs, adjectives, proper nouns)
- Custom mask using Bogotá city silhouette
- Real-time generation based on selected filters

## Technology Stack

- **Frontend**: Streamlit
- **NLP Processing**: spaCy (Spanish language model)
- **Vector Database**: ChromaDB
- **Embeddings**: SentenceTransformers (all-MiniLM-L12-v2)
- **Visualization**: WordCloud, Matplotlib, Pillow
- **Data Processing**: Pandas, NumPy

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PoliticalNLP
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the Spanish spaCy model (included in requirements):
```bash
python -m spacy download es_core_news_sm
```

## Usage

### Running the Application

Start the Streamlit application:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501`

### Using the Interface

1. **Select a Candidate**: Use the sidebar to choose which candidate to analyze
2. **Search Topics**: Enter keywords in the search box to find relevant speech segments
3. **Generate Word Clouds**: Select parts of speech to include and view the candidate's most common terms

## File Structure

```
├── main.py              # Main Streamlit application
├── vectordb.py          # Vector database setup and query functions
├── create_wordcloud.py  # Word cloud generation utilities
├── final.csv           # Processed candidate speech data
├── requirements.txt    # Python dependencies
├── bogota.png          # Mask image for word clouds
└── candidate_files/    # Individual candidate text files
    ├── oviedo.txt
    ├── galan.txt
    ├── molano.txt
    └── bolivar.txt
```

## Data Processing

The application processes candidate speeches through several stages:

1. **Text Preprocessing**: Cleaning and tokenization using spaCy
2. **Embedding Generation**: Converting text to vector representations using SentenceTransformers
3. **Vector Storage**: Storing embeddings in ChromaDB for efficient similarity search
4. **POS Filtering**: Extracting specific parts of speech for word cloud generation

## Technical Details

### Vector Search
- Uses `all-MiniLM-L12-v2` model for generating sentence embeddings
- ChromaDB collection with cosine similarity metric
- Returns top 3 most similar segments with confidence scores

### Word Cloud Generation
- Filters out common stopwords and location names ("bogotá", "ciudad")
- Supports filtering by grammatical categories (NOUN, VERB, ADJ, PROPN)
- Custom visualization with Bogotá city silhouette mask

## Development

### Adding New Candidates
1. Add candidate text file to the project directory
2. Update `file_names` dictionary in `main.py`
3. Update `candidatos` mapping in `vectordb.py`

### Extending Functionality
- Modify `preprocess_text()` in `create_wordcloud.py` for different text processing
- Adjust embedding model in `vectordb.py` for different languages or domains
- Customize word cloud appearance in `show_wordcloud()` function

## Requirements

See `requirements.txt` for complete list of dependencies. Key packages:
- streamlit
- spacy
- sentence-transformers
- chromadb
- wordcloud
- pandas
- numpy

## License

This project was developed as part of a Natural Language Processing course assignment.