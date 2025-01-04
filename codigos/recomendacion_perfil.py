import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

# Cargar los datos
data_df = pd.read_csv("CSV/peliculas_limpio.csv")
data_df_ratings = pd.read_csv("CSV/ratings.csv")

# Crear DataFrame con las calificaciones
df_ratings = data_df_ratings[["title", "rating"]]

# Crear DataFrame con las características de las películas
df = data_df[["title", "year", "genre", "director", "writer"]]

# Verificar si el número de filas coincide
if df.shape[0] != df_ratings.shape[0]:
    raise ValueError("El número de filas en las películas y las calificaciones no coincide")

df["genre"] = df["genre"].fillna("")
df["director"] = df["director"].fillna("")
df["writer"] = df["writer"].fillna("")

# Instancias de TfidfVectorizer para cada columna
tfidf_genre_vectorizer = TfidfVectorizer()
tfidf_director_vectorizer = TfidfVectorizer()
tfidf_writer_vectorizer = TfidfVectorizer()

# Transformar las columnas con TF-IDF
tfidf_genre = tfidf_genre_vectorizer.fit_transform(df["genre"]).toarray()
tfidf_director = tfidf_director_vectorizer.fit_transform(df["director"]).toarray()
tfidf_writer = tfidf_writer_vectorizer.fit_transform(df["writer"]).toarray()

# Escalar el año
scaler = MinMaxScaler()
year_en = scaler.fit_transform(df[["year"]])

# Crear la matriz de características incluyendo el año y TF-IDF
matriz_caract = np.hstack((year_en, tfidf_genre, tfidf_director, tfidf_writer))

# Calcular la matriz de similitud
matriz_sim = cosine_similarity(matriz_caract)
similarity_df = pd.DataFrame(matriz_sim, index=df["title"], columns=df["title"])

def recomendar_peli(peli):
    # Verificar si la película está en el DataFrame
    if peli not in df_ratings['title'].values:
        return f"La película '{peli}' no se encuentra en la base de datos."
    
    # Obtener películas similares
    similar_movies = similarity_df[peli].sort_values(ascending=False)

    # Filtrar solo aquellas con rating igual a 0
    similar_movies_with_zero_rating = similar_movies[similar_movies.index.isin(df_ratings[df_ratings['rating'] == 0]['title'])]

    if not similar_movies_with_zero_rating.empty:
        return similar_movies_with_zero_rating.head(10)
    else:
        return f"No hay películas similares a '{peli}' con rating igual a 0."

# Ejemplo de uso
pelicula = "Ant-Man and The Wasp"
print(f"\nPeliculas similares a: {pelicula}")
print(recomendar_peli(pelicula))
