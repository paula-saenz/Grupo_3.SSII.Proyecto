import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Descargar recursos necesarios de NLTK
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Cargar el CSV
input_csv = "CSV/peliculas_limpio.csv"
data_df = pd.read_csv(input_csv)

# Inicializar stopwords y stemmer
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')

# Lista para almacenar sinopsis procesadas
processed_synopsis = []

for texto in data_df['synopsis']:
    if isinstance(texto, str):
        # Paso 1: Convertir a minúsculas
        texto_lower = texto.lower()

        # Paso 2: Tokenización
        tokens = word_tokenize(texto_lower)

        # Paso 3: Filtrar tokens
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

        # Paso 4: Stemming
        stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

        # Paso 5: Unir los tokens procesados
        processed_text = ' '.join(stemmed_tokens)
        processed_synopsis.append(processed_text)
    else:
        processed_synopsis.append('')

# Añadir la columna de sinopsis procesadas al DataFrame
data_df['processed_synopsis'] = processed_synopsis

# Vectorización TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data_df['processed_synopsis'])

# Función para encontrar películas similares
def find_similar_movies(title, top_n=10):
    # Verificar si la película existe en el DataFrame
    if title not in data_df['title'].values:
        return f"No se encontró la película '{title}' en el dataset."

    # Obtener el índice de la película
    movie_idx = data_df[data_df['title'] == title].index[0]

    # Calcular similitudes de coseno
    cosine_similarities = cosine_similarity(tfidf_matrix[movie_idx], tfidf_matrix).flatten()

    # Obtener los índices de las películas más similares (excluyendo la película misma)
    similar_indices = cosine_similarities.argsort()[-top_n - 1:][::-1][1:]

    # Obtener títulos y similitudes
    similar_movies = [
        (data_df.iloc[idx]['title'], cosine_similarities[idx])
        for idx in similar_indices
    ]

    return similar_movies

# Prueba la funcionalidad
movie_title = "Incredibles 2"  # Cambia esto por el título que quieras buscar
similar_movies = find_similar_movies(movie_title)

print(f"Películas similares a '{movie_title}':")
for i, (title, similarity) in enumerate(similar_movies, start=1):
    print(f"{i}. {title} (Similitud: {similarity:.4f})")
