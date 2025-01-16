import streamlit as st
from streamlit_star_rating import st_star_rating
import pandas as pd
import os
from codigos.Control_PLN import pln
from codigos.Control_VISTA import vista
from codigos.Control_CSV import ratings, CSV

def main():
    ratings.GENERAR_RATINGS()
    st.set_page_config(layout="wide")
    st.title("Buscador")

    file_path = CSV.PELICULAS_LIMPIO_CSV()
    image_links_path = CSV.LINK_IMAGENES_CSV()


    # Inicialización de variables de estado
    if "page_changed" not in st.session_state:
        st.session_state.page_changed = True
    if "current_movie" not in st.session_state:
        st.session_state.current_movie = None

    # Cargar datos
    data, tfidf_matrix = pln.CARGAR_DATOS(file_path, image_links_path)

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

    if selected_movie:
        st.session_state.auto_random_movies = data[data['title'].isin(selected_movie)]
        vista.VISTA_PELICULAS(st.session_state.auto_random_movies)
    else:
        st.write("Selecciona una o más películas para ver los detalles.")

    ratings.GUARDAR_RATINGS()

if __name__ == "__main__":
    main()
