import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
from codigos.Control_VISTA import num_pelis, paginas_caratulas, vista
from codigos.Control_CSV import ratings, CSV

def main():
    st.set_page_config(layout="wide")
    st.title("Galería")

    # Cargar todos los csv
    peliculas_limpio_csv = CSV.PELICULAS_LIMPIO_CSV()
    link_imagenes_csv = CSV.LINK_IMAGENES_CSV()
    ratings_csv = CSV.RATINGS_CSV()
    
    # Cargar los datos
    peliculas = pd.read_csv(peliculas_limpio_csv)
    link_imagenes = pd.read_csv(link_imagenes_csv)

    # Unir los DataFrames de películas y enlaces de imágenes
    peliculas = pd.merge(peliculas, link_imagenes, on="title", how="left")

    # Cargar los ratings existentes
    hay_ratings = ratings.CARGAR_RATINGS()

    # Si no existe el CSV de ratings, crearlo con valores por defecto
    if not os.path.exists(ratings_csv):
        ratings_df = peliculas[["title"]].copy()
        ratings_df["rating"] = 0
        ratings_df.to_csv(ratings_csv, index=False)

    # Filtrar las películas con rating > 0
    peliculas_con_valor_df = peliculas[peliculas['title'].isin([title for title, rating in hay_ratings.items() if rating > 0])]

    numero_pelis_inicio = num_pelis.galeria.CARGAR_NUM_GALERIA()
    if "num_movies_galeria" not in st.session_state:
        st.session_state.num_movies_galeria = numero_pelis_inicio


    st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == st.session_state.num_movies_galeria][0],
        key="num_movies_select_galeria",
        on_change=num_pelis.galeria.ACTUALIZAR_NUM_PELIS_GALERIA
    )

    st.write(f"Total de películas valoradas: {len(peliculas_con_valor_df)}")

    num_movies_galeria = st.session_state.num_movies_galeria
    paginacion = (len(peliculas_con_valor_df) + num_movies_galeria - 1) // num_movies_galeria
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    paginas_caratulas.PAGINAS(paginacion)

    start_idx = (st.session_state.current_page - 1) * num_movies_galeria
    end_idx = start_idx + num_movies_galeria
    page_movies_df = peliculas_con_valor_df.iloc[start_idx:end_idx]

    vista.VISTA_PELICULAS(page_movies_df)
    ratings.GUARDAR_RATINGS()

if __name__ == "__main__":
    main()
