import streamlit as st
import pandas as pd
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

    peliculas = pd.read_csv(file_path)
    link_imagenes = pd.read_csv(image_links_path)
    peliculas = pd.merge(peliculas, link_imagenes, on="title", how="left")

    # Selección de película
    selected_movie = st.multiselect(
        "Selecciona una película:",
        options=peliculas['title'].tolist(),
        key="movie_search"
    )

    # Detección de cambio de película seleccionada
    if selected_movie != st.session_state.current_movie:
        st.session_state.current_movie = selected_movie
        st.session_state.page_changed = True

    if selected_movie:
        peliculas_seleccionadas = peliculas[peliculas['title'].isin(selected_movie)]
        vista.VISTA_PELICULAS(peliculas_seleccionadas)
    else:
        st.write("Selecciona una o más películas para ver los detalles.")

    ratings.GUARDAR_RATINGS()

if __name__ == "__main__":
    main()
