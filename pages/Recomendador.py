#buscar por peli (autocompletado) y que salgan las pelis mas parecidas a la buscada por sinopsis
#poder decidir uantas pelis salen en el recomendador
#poder votar las pelis
#guardar las votaciones en un csv que se cargue siempre que se inicie la app
#mostarr caratulas
#añadir: Hacer un autocompletar para buscar películas, esto en el de recomendaciones
import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
from streamlit_js_eval import streamlit_js_eval
import os
from codigos.setting import load_settings_recomendador, load_saved_num_movies_rec


# Ruta para almacenar el número de películas seleccionadas
settings_path_recomendador = "CSV/settings2.csv"

# Función para guardar el número de películas seleccionado
def save_num_movies(num_movies):
    settings_df = load_settings_recomendador()
    settings_df["num_movies"] = num_movies
    settings_df.to_csv(settings_path_recomendador, index=False)

# Función para actualizar la lista de películas aleatorias
def update_random_movies_recomendador():
    st.session_state.recomendador_random_movies = data.sample(n=st.session_state.num_movies)
    save_num_movies(st.session_state.num_movies)  # Guardar el número de películas seleccionado

def update_num_movies_rec():
    save_num_movies(st.session_state.num_movies_select)
    st.session_state.num_movies = st.session_state.num_movies_select

def load_existing_ratings():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        ratings_df = ratings_df[ratings_df['rating'] != 0]
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

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


def main():
    st.set_page_config(layout="wide")
    st.title("Recomendador")

    file_path = "CSV/peliculas_limpio.csv"
    image_links_path = "CSV/link_imagenes.csv"
    ratings_path = "CSV/ratings.csv"
    global data
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)

    data = pd.merge(data, image_links, on="title", how="left")

    # Cargar ratings existentes
    existing_ratings = load_existing_ratings()

    if not os.path.exists(ratings_path):
        ratings_df = data[["title"]].copy()
        ratings_df["rating"] = 0
        ratings_df.to_csv(ratings_path, index=False)

    # Cargar número de películas guardado
    default_num_movies = load_saved_num_movies_rec()
    rated_movies = existing_ratings.keys()
    rated_movies_df = data[data['title'].isin(rated_movies)]

    st.selectbox(label= "Selecciona el número de películas a mostrar", options=[5,10,15,20,25,30], 
                 key="num_movies", on_change=update_random_movies_recomendador, 
                 index=[i for i, x in enumerate([5,10,15,20,25,30]) if x == default_num_movies][0])

    if "num_movies" not in st.session_state:
        st.session_state.num_movies = default_num_movies
    

    if "recomendador_random_movies" not in st.session_state:
        update_random_movies_recomendador()

    colums = 5
    random_movies = st.session_state.recomendador_random_movies
    grid = [random_movies.iloc[i : i + colums] for i in range(0, len(random_movies), colums)]

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

    # Botón para recargar la página centrado
    col1, col2, col3, col4 = st.columns([0.5, 0.5, 0.5, 2])    
    with col4:
        if st.button("Recargar página"):
            streamlit_js_eval(js_expressions="parent.window.location.reload()")



if __name__ == "__main__":
    main()

    

        

