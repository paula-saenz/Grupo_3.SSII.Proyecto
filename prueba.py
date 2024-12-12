import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating

def main():
    st.set_page_config(layout="wide")  # Configuración de página
    st.title("Perfil de usuario")  # Título de la página    

    file_path = 'peliculas_limpio.csv'  # Ruta al archivo CSV
    data = pd.read_csv(file_path)  # Cargar datos desde el CSV

    # Definir cuántas películas mostrar
    #que pueda cambiarlo el usuario (hacerlo con un desplegable)
    num_movies = st.sidebar.number_input("Número de películas a mostrar:", min_value=1, max_value=30, value=15)
    

    # Guardar la selección de películas aleatorias en el estado de sesión para evitar que cambien
    if 'random_movies' not in st.session_state:
        st.session_state.random_movies = data.sample(n=num_movies)

    # Número de columnas para el grid
    colums = 5

    # Crear el grid de películas
    random_movies = st.session_state.random_movies
    grid = [random_movies.iloc[i:i+colums] for i in range(0, len(random_movies), colums)]

    # Mostrar las películas en un formato de grid
    for row in grid:
        cols = st.columns(colums)  # Crear las columnas

        for i, movie in enumerate(row.iterrows()):
            movie = movie[1]  # Obtener los datos de la película
            movie_key = f"rating_{movie['title']}"  # Clave única para cada película

            # Inicializar la calificación en el estado de sesión
            if movie_key not in st.session_state:
                st.session_state[movie_key] = 0

            with cols[i]:
                st.subheader(movie['title'])  # Mostrar título
                st.write(f"Género: {movie['genre']}")  # Mostrar género
                st.write(f"Año: {movie['year']}")  # Mostrar año

                # Widget para calificación
                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key
                )

                # Actualizar la calificación en el estado de sesión
                if rating != st.session_state[movie_key]:
                    st.session_state[movie_key] = rating

    # Opcional: Mostrar calificaciones en la barra lateral para depuración
    with st.sidebar:
        st.write("Calificaciones guardadas:")
        for key, value in st.session_state.items():
            if key.startswith("rating_"):
                st.write(f"{key}: {value}")


if __name__ == "__main__":
    main()
