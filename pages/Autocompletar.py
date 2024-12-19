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
        ratings_df = ratings_df[ratings_df['rating'] == 0]
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

# Función para actualizar la lista de películas aleatorias
def update_random_movies_auto():
    st.session_state.auto_random_movies = data.sample(n=st.session_state.num_movies)
    save_num_movies(st.session_state.num_movies)  # Guardar el número de películas seleccionado

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

# Función para mostrar películas
def display_movies(movies):
    colums = 5
    grid = [movies.iloc[i: i + colums] for i in range(0, len(movies), colums)]

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

                st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key,
                )

def main():
    st.set_page_config(layout="wide")
    st.title("Perfil de usuario")

    file_path = "CSV/peliculas_limpio.csv"
    image_links_path = "CSV/link_imagenes.csv"
    global data
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)

    data = pd.merge(data, image_links, on="title", how="left")

    # Cargar ratings existentes
    global existing_ratings
    existing_ratings = load_existing_ratings()

    # Cargar número de películas guardado
    default_num_movies = load_saved_num_movies()

    st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        key="num_movies",
        on_change=update_random_movies_auto,
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == default_num_movies][0],
    )

    if "num_movies" not in st.session_state:
        st.session_state.num_movies = default_num_movies

    if "auto_random_movies" not in st.session_state:
        update_random_movies_auto()

    # Sugerencias dinámicas
    st.subheader("Sugerencias dinámicas")
    selected_movie = st.selectbox(
        "Escribe y selecciona una película:", 
        options=[""] + data["title"].tolist(), 
        key="autocomplete"
    )

    # Lógica para mostrar resultados basados en la selección
    if selected_movie == "":
        if st.session_state.get("enter_pressed", False):  # Mostrar todas al presionar Enter
            st.session_state.auto_random_movies = data.sample(n=st.session_state.num_movies)
        else:  # No mostrar nada si el campo está vacío y no se presionó Enter
            st.session_state.auto_random_movies = pd.DataFrame()
    else:
        # Filtrar películas por la selección
        search_results = data[data["title"] == selected_movie]
        st.session_state.auto_random_movies = search_results.head(st.session_state.num_movies)

    # Mostrar películas seleccionadas
    if not st.session_state.auto_random_movies.empty:
        display_movies(st.session_state.auto_random_movies)

    # Capturar evento Enter
    streamlit_js_eval(
        js_expressions="document.addEventListener('keydown', e => { if (e.key === 'Enter') { window.parent.postMessage({ type: 'enter_pressed' }, '*') } })",
        key="enter_listener"
    )
    st.session_state.enter_pressed = st.query_params.get("enter_pressed", False)

    # Botón para recargar la página
    if st.button("Recargar página"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

if __name__ == "__main__":
    main()
