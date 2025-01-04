import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
#from codigos.setting import load_settings_galeria

settings_path = "CSV/settings.csv"

def load_settings_galeria():
    if not os.path.exists(settings_path):
        # Crear un DataFrame con los valores iniciales
        settings_df = pd.DataFrame({
            "window": ["galería", "perfil", "recomendaciones"],
            "num_movies": [15, 15, 15]
        })
        # Guardar el archivo
        settings_df.to_csv(settings_path, index=False)
    else:
        # Cargar el archivo existente
        settings_df = pd.read_csv(settings_path)
        galeria = "galería"
        # Verificar si las ventanas necesarias están presentes; si no, agregarlas
        if  galeria not in settings_df["window"].values:
            new_row = {"window": galeria, "num_movies": 15}
            settings_df = pd.concat([settings_df, pd.DataFrame([new_row])], ignore_index=True)
            # Guardar cualquier actualización
        settings_df.to_csv(settings_path, index=False)
    return settings_df



# Función para cargar el número de películas de una ventana específica
def load_saved_num_movies(window_name):
    settings_df = load_settings_galeria()
    # Buscar el valor asociado con la ventana
    if window_name in settings_df["window"].values:
        return int(settings_df.loc[settings_df["window"] == window_name, "num_movies"])
    return 15

# Función para guardar el número de películas para una ventana específica
def save_num_movies(window_name, num_movies):
    settings_df = load_settings_galeria()
    if window_name in settings_df["window"].values:
        # Actualizar el valor correspondiente
        settings_df.loc[settings_df["window"] == window_name, "num_movies"] = num_movies
    else:
        # Agregar una nueva fila si la ventana no existe
        new_row = {"window": window_name, "num_movies": num_movies}
        settings_df = pd.concat([settings_df, pd.DataFrame([new_row])], ignore_index=True)
    # Guardar el archivo actualizado
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

    # Cargar número de películas guardado para la galería
    default_num_movies = load_saved_num_movies("galería")
    if "num_movies" not in st.session_state:
        st.session_state.num_movies = default_num_movies

    # Selector para elegir el número de películas por página
    st.session_state.num_movies = st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == default_num_movies][0]
    )
    save_num_movies("galería", st.session_state.num_movies)

    rated_movies = existing_ratings.keys()
    rated_movies_df = data[data['title'].isin(rated_movies)]

    st.write(f"Total de películas valoradas: {len(rated_movies_df)}")

    # Paginación
    num_movies = st.session_state.num_movies
    total_pages = (len(rated_movies_df) + num_movies - 1) // num_movies
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Anterior") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
    with col3:
        if st.button("➡️ Siguiente") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
    with col2:
        st.write(f"Página {st.session_state.current_page} de {total_pages}")

    # Mostrar las películas de la página actual
    start_idx = (st.session_state.current_page - 1) * num_movies
    end_idx = start_idx + num_movies
    page_movies_df = rated_movies_df.iloc[start_idx:end_idx]

    colums = 5
    grid = [page_movies_df.iloc[i:i+colums] for i in range(0, len(page_movies_df), colums)]

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
