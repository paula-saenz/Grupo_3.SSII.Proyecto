import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Descargar paquetes NLTK 
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Inicializar stopwords y stemmer a ingles
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')

# Procesar sinopsis
def process_synopsis(texto):
    # Paso 1: Verificar si el texto es una cadena
    if isinstance(texto, str):
        # Paso 2: Convertir todo el texto a minúsculas
        texto_lower = texto.lower()
        
        # Paso 3: Dividir el texto en palabras individuales
        tokens = word_tokenize(texto_lower)
        
        # Paso 4: Filtrar las palabras
        filtered_tokens = []
        for word in tokens:
            # Mantener solo palabras alfanuméricas que no sean stop words
            if word.isalnum() and word not in stop_words:
                filtered_tokens.append(word)
        
        # Paso 5: Aplicar stemming a las palabras filtradas
        stemmed_tokens = []
        for word in filtered_tokens:
            stemmed_word = stemmer.stem(word)
            stemmed_tokens.append(stemmed_word)
        
        # Paso 6: Unir las palabras procesadas en una sola cadena
        return ' '.join(stemmed_tokens)
    
    # Si el texto no es una cadena, devolver una cadena vacía
    return ''

# Cargar datos 
def load_data(file_path, image_links_path):
    data_df = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)
    data_df = pd.merge(data_df, image_links, on="title", how="left")
    
    data_df['processed_synopsis'] = data_df['synopsis'].apply(process_synopsis)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data_df['processed_synopsis'])
    
    return data_df, tfidf_matrix

def find_similar_movies(title, data_df, tfidf_matrix, top_n):
    if title not in data_df['title'].values:
        return []

    movie_idx = data_df[data_df['title'] == title].index[0]
    cosine_similarities = cosine_similarity(tfidf_matrix[movie_idx], tfidf_matrix).flatten()

    # Ordenar los índices por similitud (de mayor a menor)
    similar_indices = cosine_similarities.argsort()[::-1]

    # Eliminar el primer índice (que es la película original) y tomar los top_n
    similar_indices = similar_indices[1:top_n+1]

    # Crear una lista de diccionarios con la información de las películas similares
    similar_movies = []
    for idx in similar_indices:
        similar_movies.append({
            'title': data_df.iloc[idx]['title'],
            'genre': data_df.iloc[idx]['genre'],
            'year': data_df.iloc[idx]['year'],
            'imagen': data_df.iloc[idx]['imagen'],
            'similarity': cosine_similarities[idx]
        })

    return similar_movies
