import streamlit as st
from streamlit_star_rating import st_star_rating
import pandas as pd
import os
from codigos.pln_sinopsis import load_data, find_similar_movies
from codigos.Control_VISTA import num_pelis
from codigos.Control_CSV import ratings

# File paths
file_path = "CSV/peliculas_limpio.csv"
image_links_path = "CSV/link_imagenes.csv"
ratings_path = "CSV/ratings.csv"

def load_movie_data():
    return load_data(file_path, image_links_path)

def load_existing_ratings():
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        ratings_df = ratings_df[ratings_df['rating'] != 0]
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

def update_rating(title, rating):
    title = str(title)
    if isinstance(rating, (int, float)):
        st.session_state[f"rating_{title}"] = rating
        if 'existing_ratings' not in st.session_state:
            st.session_state.existing_ratings = {}
        st.session_state.existing_ratings[title] = rating
    else:
        st.error("El valor de rating debe ser un número (int o float).")

def save_ratings_to_csv():
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
    else:
        ratings_df = pd.DataFrame(columns=["title", "rating"])

    for key, value in st.session_state.items():
        if key.startswith("rating_"):
            title = key.replace("rating_", "")
            if isinstance(value, (int, float)):
                if title in ratings_df["title"].values:
                    ratings_df.loc[ratings_df["title"] == title, "rating"] = value
                else:
                    ratings_df = pd.concat(
                        [ratings_df, pd.DataFrame([{"title": title, "rating": value}])],
                        ignore_index=True,
                    )
    ratings_df.to_csv(ratings_path, index=False)

def display_movies(movies):
    colums = 5
    for i in range(0, len(movies), colums):
        row = movies[i:i+colums]
        cols = st.columns(colums)
        for j, movie in enumerate(row):
            with cols[j]:
                st.subheader(movie["title"])
                if pd.notna(movie["imagen"]):
                    st.image(movie["imagen"], use_container_width=True)
                else:
                    st.write("Imagen no disponible")

                st.write(f"Género: {movie['genre']}")
                st.write(f"Año: {movie['year']}")
                st.write(f"Similitud: {movie['similarity']:.2f}")

                movie_key = f"rating_{movie['title']}"
                if movie_key not in st.session_state:
                    st.session_state[movie_key] = existing_ratings.get(movie['title'], 0)

                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key,
                )

def main():
    st.set_page_config(layout="wide")
    st.title("Recomendador de Películas Similares")

    global data, tfidf_matrix, existing_ratings

    # Inicialización de variables de estado
    if "page_changed" not in st.session_state:
        st.session_state.page_changed = True
    if "current_movie" not in st.session_state:
        st.session_state.current_movie = None

    # Cargar datos
    data, tfidf_matrix = load_movie_data()
    existing_ratings = load_existing_ratings()

    numero_pelis_inicio = num_pelis.galeria.CARGAR_NUM_GALERIA()
    if "num_movies_recomendador" not in st.session_state:
        st.session_state.num_movies_recomendador = numero_pelis_inicio

    # Selección de película
    selected_movie = st.selectbox(
        "Selecciona una película:",
        options=data['title'].tolist(),
        key="movie_search"
    )

    # Detección de cambio de película seleccionada
    if selected_movie != st.session_state.current_movie:
        st.session_state.current_movie = selected_movie
        st.session_state.page_changed = True

    num_recommendations = st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == st.session_state.num_movies_recomendador][0],
        key="num_movies_select_recomendador",
        on_change=num_pelis.recomendador.ACTUALIZAR_NUM_PELIS_RECOMENDADOR
    )

    if selected_movie:
        st.write(f"Película seleccionada: {selected_movie}")
        similar_movies = find_similar_movies(selected_movie, data, tfidf_matrix, num_recommendations)

        if similar_movies:
            st.subheader(f"Películas similares a '{selected_movie}':")
            display_movies(similar_movies)
    else:
        st.write("No se encontraron películas similares.")

    ratings.GUARDAR_RATINGS()

if __name__ == "__main__":
    main()
