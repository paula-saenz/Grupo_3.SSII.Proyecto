import streamlit as st
from streamlit_star_rating import st_star_rating
import pandas as pd
import os
from codigos.pln_sinopsis import load_data, find_similar_movies
from codigos.Control_VISTA import vista

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


# Función para ejecutar cuando se detecta un cambio de página
def on_page_change():
    st.write("Página cargada por primera vez")
    st.session_state.page_changed = False  # Reseteamos el estado

def main():
    st.set_page_config(layout="wide")
    st.title("Buscador")

    global data, tfidf_matrix, existing_ratings

    # Inicialización de variables de estado
    if "page_changed" not in st.session_state:
        st.session_state.page_changed = True
    if "current_movie" not in st.session_state:
        st.session_state.current_movie = None

    # Cargar datos
    data, tfidf_matrix = load_movie_data()
    existing_ratings = load_existing_ratings()

    # Selección de película
    selected_movie = st.multiselect(
        "Selecciona una película:",
        options=data['title'].tolist(),
        key="movie_search"
    )

    # Detección de cambio de película seleccionada
    if selected_movie != st.session_state.current_movie:
        st.session_state.current_movie = selected_movie
        st.session_state.page_changed = True

    # Ejecución en caso de cambio
    if st.session_state.page_changed:
        on_page_change()

    if selected_movie:
        st.session_state.auto_random_movies = data[data['title'].isin(selected_movie)]
        vista.VISTA_PELICULAS(st.session_state.auto_random_movies)
    else:
        st.write("Selecciona una o más películas para ver los detalles.")

    save_ratings_to_csv()

if __name__ == "__main__":
    main()
