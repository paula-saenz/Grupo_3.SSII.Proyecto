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
    ratings_path = "CSV/ratings_valorado.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

# Función para actualizar la lista de películas aleatorias
def update_random_movies():
    st.session_state.random_movies = data.sample(n=st.session_state.num_movies)
    save_num_movies(st.session_state.num_movies)  # Guardar el número de películas seleccionado

# Guardar calificaciones en un CSV
def save_ratings_to_csv():
    ratings_cero_path = "CSV/ratings_cero.csv"
    ratings_valorado_path = "CSV/ratings_valorado.csv"

    # Cargar los archivos CSV si existen, o inicializarlos
    if os.path.exists(ratings_cero_path):
        ratings_cero_df = pd.read_csv(ratings_cero_path)
    else:
        ratings_cero_df = pd.DataFrame(columns=["title", "rating"])

    if os.path.exists(ratings_valorado_path):
        ratings_valorado_df = pd.read_csv(ratings_valorado_path)
    else:
        ratings_valorado_df = pd.DataFrame(columns=["title", "rating"])

    # Procesar las calificaciones desde el estado de sesión
    for key, value in st.session_state.items():
        if key.startswith("rating_"):
            title = key.replace("rating_", "")

            # Si la calificación es 0, añadir al archivo ratings_cero
            if value == 0:
                if title not in ratings_cero_df["title"].values:
                    ratings_cero_df = pd.concat(
                        [ratings_cero_df, pd.DataFrame([{"title": title, "rating": value}])],
                        ignore_index=True,
                    )

            # Si la calificación es distinta de 0, añadir a ratings_valorado
            else:
                # Eliminar de ratings_cero si el título existe
                ratings_cero_df = ratings_cero_df[ratings_cero_df["title"] != title]

                # Actualizar o añadir en ratings_valorado
                if title in ratings_valorado_df["title"].values:
                    ratings_valorado_df.loc[ratings_valorado_df["title"] == title, "rating"] = value
                else:
                    ratings_valorado_df = pd.concat(
                        [ratings_valorado_df, pd.DataFrame([{"title": title, "rating": value}])],
                        ignore_index=True,
                    )

    # Guardar los DataFrames actualizados
    ratings_cero_df.to_csv(ratings_cero_path, index=False)
    ratings_valorado_df.to_csv(ratings_valorado_path, index=False)



def main():
    st.set_page_config(layout="wide")
    st.title("Perfil de usuario")

    file_path = "CSV/peliculas_limpio.csv"
    image_links_path = "CSV/link_imagenes.csv"
    ratings_cero_path = "CSV/ratings_cero.csv"
    global data
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)

    data = pd.merge(data, image_links, on="title", how="left")

    # Cargar ratings existentes
    existing_ratings = load_existing_ratings()

    if not os.path.exists(ratings_cero_path):
        ratings_df = data[["title"]].copy()
        ratings_df["rating"] = 0
        ratings_df.to_csv(ratings_cero_path, index=False)

    # Cargar número de películas guardado
    default_num_movies = load_saved_num_movies()

    st.selectbox(label= "Selecciona el número de películas a mostrar", options=[5,10,15,20,25,30], 
                 key="num_movies", on_change=update_random_movies, 
                 index=[i for i, x in enumerate([5,10,15,20,25,30]) if x == default_num_movies][0])

    if "num_movies" not in st.session_state:
        st.session_state.num_movies = default_num_movies
    

    if "random_movies" not in st.session_state:
        update_random_movies()

    colums = 5
    random_movies = st.session_state.random_movies
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


                # HECHO
                #añadir: poder votar
                #añadir: guardar votaciones en un csv que se cargue siempre que se inicie la app
                #scrapper para coger caratulas de pelis
                #añadir: poder escoger cuantas paelis aparecen en el recomendador

                # ----------------------------------------------------------------------------------

                # POR HACER
                #añadir: mostrar las películas recomendadas en función de las votaciones (pelis que no se hayan votado todavía)
                #añadir: poder tener un historial de las pelis que se han votado
                #añadir: Hacer un autocompletar para buscar películas
                #añadir: ratio con el que se recomiendan las películas
