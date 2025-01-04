import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

# Cargar los datos
data_df = pd.read_csv("CSV/peliculas_limpio.csv")
data_df_ratings = pd.read_csv("CSV/ratings.csv")

# Crear DataFrame con las características de las películas
df = data_df[["title", "year", "genre", "director", "writer"]]

# Asegurar que solo trabajamos con películas filtradas
df = df[df["title"].isin(data_df_ratings["title"])]

# Rellenar valores nulos
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

def recomendar_peliculas_top_rated(top_n=10):
    # Filtrar las películas con rating >= 8 (gustos del usuario)
    peliculas_gustadas = data_df_ratings[data_df_ratings["rating"] >= 8]["title"].values
    
    # Filtrar las películas de df que el usuario ha calificado positivamente
    df_gustadas = df[df["title"].isin(peliculas_gustadas)]
    
    # Crear una lista para almacenar las recomendaciones
    recomendaciones = []

    # Seleccionar las películas con rating 0 (no vistas por el usuario)
    peliculas_sin_rating = data_df_ratings[data_df_ratings["rating"] == 0]["title"].values
    
    # Recomendaciones para las películas que el usuario ha calificado positivamente
    for peli in peliculas_gustadas:
        if peli in similarity_df.index:
            # Obtener las películas similares basadas en la similitud
            similar_movies = similarity_df[peli].sort_values(ascending=False).iloc[1:top_n + 1]
            
            # Filtrar las películas similares para que no estén en las ya vistas por el usuario
            peliculas_recomendadas = similar_movies[similar_movies.index.isin(peliculas_sin_rating)]
            
            # Añadir las recomendaciones filtradas a la lista
            recomendaciones.append(peliculas_recomendadas)

    # Verificar si la lista de recomendaciones no está vacía
    if recomendaciones:
        # Combinar todas las recomendaciones
        recomendaciones_df = pd.concat(recomendaciones)

        # Agrupar y ordenar por promedio de similitud
        recomendaciones_agrupadas = recomendaciones_df.groupby(recomendaciones_df.index).mean()
        recomendaciones_ordenadas = recomendaciones_agrupadas.sort_values(ascending=False).head(top_n)

        return recomendaciones_ordenadas
    else:
        return "No hay recomendaciones disponibles."

# Ejemplo de uso
print("\nRecomendaciones basadas en tus gustos:")
print(recomendar_peliculas_top_rated())
