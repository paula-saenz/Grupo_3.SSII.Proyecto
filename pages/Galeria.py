import pandas as pd
import streamlit as st
from codigos.Control_VISTA import num_pelis, paginas_caratulas, vista, select_box
from codigos.Control_CSV import ratings, CSV

# FUNCIÓN "CONFIGURAR_PAGINACIÓN" --> GENERAR EL CAMBIO ENTRE PÁGINAS
def configurar_paginacion(total_peliculas, num_movies_galeria, peliculas_df):
    
    # CONFIGURA LA PAGINACIÓN PARA MOSTRAR LAS PELÍCULAS POR PÁGINAS
    
    # Cálculo de número total de páginas
    paginacion = (total_peliculas + num_movies_galeria - 1) // num_movies_galeria

    # Se inicializa el estado de la página actual
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    # Se configura la paginación
    paginas_caratulas.PAGINAS(paginacion)



    # OBTIENE LAS PELÍCULAS CORRESPONDIENTES A LA PÁGINA ACTUAL

    # Cálculo del inicio de la página
    start_idx = (st.session_state.current_page - 1) * num_movies_galeria

    # Cálculo del final de la página
    end_idx = start_idx + num_movies_galeria

    # Devuelve un subconjunto entre el inicio de la página y el final
    return peliculas_df.iloc[start_idx:end_idx]



# FUNCIÓN "MAIN"
def main():

    # INICIAR LA PÁGINA
    ratings.GENERAR_RATINGS()
    st.set_page_config(layout="wide")
    st.title("Galería de Películas")



    # CARGAR Y PREPARAR LOS DATOS
    
    # Dato para cargar ratings existentes
    ratings_existentes = ratings.CARGAR_RATINGS()
    # Dato para cargar el numeros de películas en galería
    numero_pelis_inicio = num_pelis.galeria.CARGAR_NUM_GALERIA()

    # Datos de CSV
    peliculas_limpio_csv = CSV.PELICULAS_LIMPIO_CSV()
    link_imagenes_csv = CSV.LINK_IMAGENES_CSV()

    # Datos para leer los CSV
    peliculas = pd.read_csv(peliculas_limpio_csv)
    link_imagenes = pd.read_csv(link_imagenes_csv)
    peliculas = pd.merge(peliculas, link_imagenes, on="title", how="left")

    # Dato para mostrar películas con rating
    peliculas_con_rating_df = peliculas[peliculas['title'].isin([
        title for title, rating in ratings_existentes.items() if rating > 0
    ])]

    # Dato para guardar el número de películas valoradas
    total_peliculas = len(peliculas_con_rating_df)



    # SE INICIALIZAN LOS ESTADOS EN CASO DE QUE NO EXISTAN

    # Configuración inicial del número de películas por galería
    if "num_movies_galeria" not in st.session_state:
        st.session_state.num_movies_galeria = numero_pelis_inicio




    # CAJA DE SELECCIÓN PARA SELECCIONAR EL NÚMERO DE PELÍCULAS

    select_box.SELECT_BOX(
        st.session_state.num_movies_galeria,
        "num_movies_select_galeria",
        num_pelis.galeria.ACTUALIZAR_NUM_PELIS_GALERIA
    )



    # DETALLES FINALES

    # Mostrar el total de películas valoradas
    st.markdown(f"### Total de películas valoradas: **{total_peliculas}**")

    # Configurar y manejar la paginación
    num_movies_galeria = st.session_state.num_movies_galeria

    # Configura la paginación para mostrar las películas por páginas.
    paginación = configurar_paginacion(
        len(peliculas_con_rating_df), 
        num_movies_galeria, 
        peliculas_con_rating_df
    )

    # Vista de las películas valoradas en una cuadrícula por paginación
    vista.VISTA_PELICULAS(paginación)

    # Guardar las valoraciones actualizadas
    ratings.GUARDAR_RATINGS()



# LLAMADA AL "MAIN"
if __name__ == "__main__":
    main()