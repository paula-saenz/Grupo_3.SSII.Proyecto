import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating

# Función para actualizar la lista de películas aleatorias
def update_random_movies():
    st.session_state.random_movies = data.sample(n=st.session_state.num_movies)

# Guardar calificaciones en un CSV
def save_ratings_to_csv():
    ratings = [
        {"title": key.replace("rating_", ""), "rating": value}
        for key, value in st.session_state.items()
        if key.startswith("rating_")
    ]
    ratings_df = pd.DataFrame(ratings)
    ratings_df.to_csv("user_ratings.csv", index=False)
    st.sidebar.success("¡Calificaciones guardadas en 'user_ratings.csv'!")

def main():
    # Configuración de la página
    st.set_page_config(layout="wide")
    st.title("Perfil de usuario")

    # Cargar los datos desde CSV
    file_path = 'CSV/peliculas_limpio.csv'
    image_links_path = 'CSV/link_imagenes.csv'
    global data  # Hacemos global para que sea accesible en la función de actualización
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)

    # Combinar datos de películas con enlaces de imágenes
    data = pd.merge(data, image_links, on='title', how='left')

    # Sidebar: Número de películas a mostrar
    st.sidebar.header("Configuración")
    num_movies = st.sidebar.number_input(
        "Número de películas a mostrar:",
        min_value=1,
        max_value=30,
        value=15,
        step=1,
        key="num_movies",
        on_change=update_random_movies  # Actualiza películas al cambiar el número
    )

    # Inicializar películas aleatorias si no existen en el estado
    if 'random_movies' not in st.session_state:
        update_random_movies()

    # Crear grid de películas
    colums = 5
    random_movies = st.session_state.random_movies
    grid = [random_movies.iloc[i:i+colums] for i in range(0, len(random_movies), colums)]

    # Mostrar las películas
    for row in grid:
        cols = st.columns(colums)
        for i, movie in enumerate(row.iterrows()):
            movie = movie[1]  # Datos de la película
            movie_key = f"rating_{movie['title']}"

            # Inicializar calificación si no existe
            if movie_key not in st.session_state:
                st.session_state[movie_key] = 0

            with cols[i]:
                st.subheader(movie['title'])
                if pd.notna(movie['imagen']):
                    st.image(movie['imagen'], use_container_width=True)
                else:
                    st.write("Imagen no disponible")

                st.write(f"Género: {movie['genre']}")
                st.write(f"Año: {movie['year']}")

                # Widget de calificación
                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state.get(movie_key, 0),
                    key=movie_key
                )
                

    # calificaciones se guardan automaticamente en un CSV
    st.sidebar.button("Guardar calificaciones", on_click=save_ratings_to_csv)

    # Mostrar calificaciones en la barra lateral
    st.sidebar.write("Calificaciones guardadas:")
    for key, value in st.session_state.items():
        if key.startswith("rating_"):
            st.sidebar.write(f"{key.replace('rating_', '')}: {value}")

if __name__ == "__main__":
    main()
