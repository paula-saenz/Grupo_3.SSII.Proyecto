import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
from streamlit_star_rating import st_star_rating
import os

# Función para cargar ratings existentes
def load_existing_ratings():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        ratings_df = ratings_df[ratings_df['rating'] != 0]
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

# Guardar calificaciones en un CSV
def save_ratings_to_csv():
    ratings_path = "CSV/ratings.csv"

    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
    else:
        ratings_df = pd.DataFrame(columns=["title", "rating"])

    for key, value in st.session_state.items():
        if key.startswith("rating_"):
            title = key.replace("rating_", "")
            if title in ratings_df["title"].values:
                ratings_df.loc[ratings_df["title"] == title, "rating"] = value
            else:
                ratings_df = pd.concat(
                    [ratings_df, pd.DataFrame([{"title": title, "rating": value}])],
                    ignore_index=True,
                )

    ratings_df.to_csv(ratings_path, index=False)

# Función para recomendar películas
def recomendar_peli(peli, similarity_df, df_ratings):
    if peli not in df_ratings['title'].values:
        return f"La película '{peli}' no se encuentra en la base de datos."
    
    # Obtener películas similares
    similar_movies = similarity_df[peli].sort_values(ascending=False)
    
    # Filtrar solo aquellas con rating igual a 0 y excluir la película buscada
    similar_movies_with_zero_rating = similar_movies[
        (similar_movies.index.isin(df_ratings[df_ratings['rating'] == 0]['title'])) & 
        (similar_movies.index != peli)
    ]
    
    return similar_movies_with_zero_rating.head(10) if not similar_movies_with_zero_rating.empty else f"No hay películas similares a '{peli}' con rating igual a 0."

def main():
    st.set_page_config(layout="wide")
    st.title("Recomendaciones de Películas")

    # Cargar datos
    data_df = pd.read_csv("CSV/peliculas_limpio.csv")
    data_df_ratings = pd.read_csv("CSV/ratings.csv")
    image_links = pd.read_csv("CSV/link_imagenes.csv")

    df = data_df[["title", "year", "genre", "director", "writer"]]
    df_ratings = data_df_ratings[["title", "rating"]]

    # Combinar datos con imágenes
    data_df = pd.merge(data_df, image_links, on="title", how="left")

    # Procesar características para similitud
    encoder = OneHotEncoder(sparse_output=False)
    genre_en = encoder.fit_transform(df[["genre"]])
    director_en = encoder.fit_transform(df[["director"]])
    writer_en = encoder.fit_transform(df[["writer"]])
    year_en = df[["year"]].values

    tfidf_vectorizer = TfidfVectorizer()
    title_en = tfidf_vectorizer.fit_transform(df["title"]).toarray()

    matriz_caract = np.hstack((year_en, genre_en, director_en, writer_en, title_en))
    matriz_sim = cosine_similarity(matriz_caract)
    similarity_df = pd.DataFrame(matriz_sim, index=df["title"], columns=df["title"])

    # Buscar película
    selected_movie = st.text_input("Escribe el título de una película para buscar recomendaciones:")

    # Mostrar recomendaciones
    if selected_movie:
        st.subheader(f"Películas similares a: {selected_movie}")
        recomendaciones = recomendar_peli(selected_movie, similarity_df, df_ratings)

        if isinstance(recomendaciones, str):
            st.write(recomendaciones)
        else:
            # Mostrar las películas recomendadas en formato de galería
            colums = 5
            recommended_titles = recomendaciones.index
            recommended_movies = data_df[data_df['title'].isin(recommended_titles)]
            grid = [recommended_movies.iloc[i : i + colums] for i in range(0, len(recommended_movies), colums)]

            for row in grid:
                cols = st.columns(colums)
                for i, movie in enumerate(row.iterrows()):
                    movie = movie[1]
                    movie_key = f"rating_{movie['title']}"

                    if movie_key not in st.session_state:
                        st.session_state[movie_key] = 0

                    with cols[i]:
                        st.subheader(movie["title"])
                        if pd.notna(movie["imagen"]):
                            st.image(movie["imagen"], use_container_width=True)
                        else:
                            st.write("Imagen no disponible")

                        st.write(f"Género: {movie['genre']}")
                        st.write(f"Año: {movie['year']}")

                        st_star_rating(
                            label="",
                            maxValue=10,
                            defaultValue=st.session_state[movie_key],
                            key=movie_key,
                        )

    # Guardar calificaciones
    save_ratings_to_csv()

if __name__ == "__main__":
    main()
