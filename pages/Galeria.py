#todas las pelis que ha votado, por si quiere rapidamente cambiar la votacion
#tambien habra un buscador con autocompletar
#mostrar pelis votadas

import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
from streamlit_js_eval import streamlit_js_eval
import os

# Ruta para almacenar el número de películas seleccionadas
settings_path = "CSV/settings.csv"

# Función para cargar el número de películas guardado
def load_saved_num_movies():
    if os.path.exists(settings_path):
        settings_df = pd.read_csv(settings_path)
        if "num_movies" in settings_df.columns:
            return int(settings_df["num_movies"])
    return 15

# Función para guardar el número de películas seleccionado
def save_num_movies(num_movies):
    settings_df = pd.DataFrame({"num_movies": [num_movies]})
    settings_df.to_csv(settings_path, index=False)

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

    # Cargar los archivos CSV si existen, o inicializarlos
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
    else:
        ratings_df = pd.DataFrame(columns=["title", "rating"])

    # Procesar las calificaciones desde el estado de sesión
    for key, value in st.session_state.items():
        if key.startswith("rating_"):
            title = key.replace("rating_", "")
            # Actualizar o añadir en ratings_valorado
            if title in ratings_df["title"].values:
                ratings_df.loc[ratings_df["title"] == title, "rating"] = value
            else:
                ratings_df = pd.concat(
                    [ratings_df, pd.DataFrame([{"title": title, "rating": value}])],
                    ignore_index=True,
                )
    # Guardar los DataFrames actualizados
    ratings_df.to_csv(ratings_path, index=False)

def main():
    st.set_page_config(layout="wide")
    st.title("Galería")

    file_path = "CSV/peliculas_limpio.csv"
    image_links_path = "CSV/link_imagenes.csv"
    ratings_valorado_path = "CSV/ratings.csv"
    global data
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)

    data = pd.merge(data, image_links, on="title", how="left")

    # Cargar ratings existentes
    existing_ratings = load_existing_ratings()

    if not os.path.exists(ratings_valorado_path):
        ratings_df = data[["title"]].copy()
        ratings_df["rating"] = 0
        ratings_df.to_csv(ratings_valorado_path, index=False)

    # Cargar número de películas guardado
    default_num_movies = load_saved_num_movies()
    rated_movies = existing_ratings.keys()
    rated_movies_df = data[data['title'].isin(rated_movies)]

    st.write(f"Total de películas valoradas: {len(rated_movies_df)}")

    if "num_movies" not in st.session_state:
        st.session_state.num_movies = default_num_movies

    colums = 5
    grid = [rated_movies_df.iloc[i : i + colums] for i in range(0, len(rated_movies_df), colums)]

    for row in grid:
        cols = st.columns(colums)
        for i, movie in enumerate(row.iterrows()):
            movie = movie[1]
            movie_key = f"rating_{movie['title']}"

            # Usar el rating existente o 0 si no existe
            if movie_key not in st.session_state:
                st.session_state[movie_key] = existing_ratings.get(movie['title'], 0)

            with cols[i]:
                st.subheader(movie["title"])
                if pd.notna(movie["imagen"]):
                    st.image(movie["imagen"], use_container_width=True)
                else:
                    st.write("Imagen no disponible")

                st.write(f"Género: {movie['genre']}")
                st.write(f"Año: {movie['year']}")

                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key,
                )

    save_ratings_to_csv()

if __name__ == "__main__":
    main()
