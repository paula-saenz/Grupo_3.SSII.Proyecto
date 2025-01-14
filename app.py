import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
from codigos.Control_RECOMENDACIONES import CARGAR_DATOS, CREAR_MATRIZ_SIMILITUD, RECOMENDACION
from codigos.Control_VISTA import paginas_caratulas, vista, num_pelis
from codigos.Control_CSV import ratings, CSV


def SISTEMA_RECOMENDACIONES(similarity_df, data_df_ratings, data, num_movies_perfil):
    existing_ratings = ratings.CARGAR_RATINGS()
    rated_movies = [title for title, rating in existing_ratings.items() if rating > 0]

    if rated_movies:
        recomendaciones = RECOMENDACION(similarity_df, data_df_ratings, top_n=num_movies_perfil)
        if recomendaciones.empty:
            return data.sample(n=num_movies_perfil)
        recomendaciones = recomendaciones.reset_index().merge(data, on="title", how="left")
    else:
        recomendaciones = data.sample(n=num_movies_perfil)

    return recomendaciones





def main():
    ratings.GENERAR_RATINGS()
    st.set_page_config(layout="wide")
    st.title("PERFIL")
    

    if 'rating_peli' not in st.session_state:
        st.session_state.rating_peli = ratings.CARGAR_RATINGS()

    #st.dataframe(ratings.CARGAR_RATINGS()) -----> Quitar comentario para ver el DataFrame


    # Cargar y preparar los datos
    df, data_df_ratings = CARGAR_DATOS()
    similarity_df = CREAR_MATRIZ_SIMILITUD(df)

    file_path = CSV.PELICULAS_LIMPIO_CSV()
    image_links_path = CSV.LINK_IMAGENES_CSV()
    
    peliculas = pd.read_csv(file_path) 
    image_links = pd.read_csv(image_links_path)
    peliculas = pd.merge(peliculas, image_links, on="title", how="left")

    peliculas_no_votadas = peliculas[~peliculas['title'].isin(st.session_state.rating_peli.keys()) | (peliculas['title'].isin(st.session_state.rating_peli.keys()) & (st.session_state.rating_peli.values() == 0))]


    default_num_movies = num_pelis.perfil.CARGAR_NUM_PERFIL()
    if "num_movies_perfil" not in st.session_state:
        st.session_state.num_movies_perfil = default_num_movies


    st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == st.session_state.num_movies_perfil][0],
        key="num_movies_select_perfil",
        on_change=num_pelis.perfil.ACTUALIZAR_NUM_PELIS_PERFIL
    )

    if "recomendaciones" not in st.session_state or st.button("Actualizar recomendaciones"):
        st.session_state.recomendaciones = SISTEMA_RECOMENDACIONES(similarity_df, data_df_ratings, peliculas_no_votadas, st.session_state.num_movies_perfil)

    recomendaciones = st.session_state.recomendaciones

    # Manejo de la paginación
    num_movies_perfil = st.session_state.num_movies_perfil
    total_pages = (len(recomendaciones) + num_movies_perfil - 1) // num_movies_perfil
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    paginas_caratulas.PAGINAS(total_pages)

    # Dividir las películas en páginas
    start_idx = (st.session_state.current_page - 1) * num_movies_perfil
    end_idx = start_idx + num_movies_perfil
    page_movies_df = recomendaciones.iloc[start_idx:end_idx]

    # Mostrar las películas en una cuadrícula
    vista.VISTA_PELICULAS(page_movies_df)
    ratings.GUARDAR_RATINGS()

if __name__ == "__main__":
    main()