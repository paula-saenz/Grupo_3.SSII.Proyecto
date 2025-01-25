import pandas as pd
import streamlit as st
from codigos.Control_RECOMENDACIONES import CARGAR_DATOS, CREAR_MATRIZ_SIMILITUD, RECOMENDACION
from codigos.Control_VISTA import vista, num_pelis, select_box
from codigos.Control_CSV import ratings, CSV



# FUNCIÓN "SISTEMA_RECOMENDACIONES" --> GENERAR UN DF CON LAS RECOMENDACIONES
def SISTEMA_RECOMENDACIONES(matriz_similitud_recomendaciones, ratings_df, peliculas_no_votadas, num_movies_perfil):
    
    # CARGAR Y PREPARAR DATOS
    ratings_existentes = ratings.CARGAR_RATINGS()
    # Películas con un rating > 0
    peliculas_con_rating_df = []
    for title, rating in ratings_existentes.items():
        if rating > 0:
            peliculas_con_rating_df.append(title)



    # GENERA LAS RECOMENDACIONES, SI NO HAY GENERA PELÍCULAS ALEATORIAS
    if peliculas_con_rating_df:
        # Si hay películas con rating, genera recomendaciones
        recomendaciones = RECOMENDACION(matriz_similitud_recomendaciones, ratings_df, top_n=num_movies_perfil)
        
        # Combina las recomendaciones con los datos completos de las películas
        recomendaciones = recomendaciones.reset_index().merge(peliculas_no_votadas, on="title", how="left")
        # reset_index() --> Restablece el índice del DF en 0
        # merge --> Combina "recomendaciones" con "peliculas_no_votadas"

    else:
        # Si no hay películas con rating, selecciona películas al azar
        recomendaciones = peliculas_no_votadas.sample(n=num_movies_perfil)
        # .sample --> Método de pandas. Genera filas aleatorias de un DF

    # Devuelve las recomendaciones generadas o las películas seleccionadas al azar
    return recomendaciones



# FUNCIÓN "MAIN"
def main():

    # INICIAR LA PÁGINA
    ratings.GENERAR_RATINGS()
    st.set_page_config(layout="wide")
    st.title("PERFIL")

    
    # CARGAR Y PREPARAR LOS DATOS
    # Datos de Recomendaciones
    title_df, ratings_df = CARGAR_DATOS()
    matriz_similitud_recomendaciones = CREAR_MATRIZ_SIMILITUD(title_df)

    # Datos de CSV
    file_path = CSV.PELICULAS_LIMPIO_CSV()
    image_links_path = CSV.LINK_IMAGENES_CSV()
    
    # Datos para leer los CSV
    peliculas = pd.read_csv(file_path) 
    image_links = pd.read_csv(image_links_path)
    peliculas = pd.merge(peliculas, image_links, on="title", how="left")

    # Dato para cargar el número de películas de perfil
    default_num_movies = num_pelis.perfil.CARGAR_NUM_PERFIL()


    # GUARDADO DE PELÍCULAS NO VOTADAS
    # Estado para los ratings de las películas en caso de que no existe
    if 'rating_peli' not in st.session_state:
        st.session_state.rating_peli = ratings.CARGAR_RATINGS()

    # Dato para mostrar las películas no votadas
    peliculas_no_votadas = peliculas[
        peliculas['title'].apply(lambda title: title not in st.session_state.rating_peli)
    ]   # lambda --> Defina una función corta en una sola línea   
        # .apply --> Guardará una Serie de True y Falta dependiendo de la condición de lambda (Si es true se guarda la película, si es False no se guarda)

    # SE INICIALIZAN LOS ESTADOS EN CASO DE QUE NO EXISTAN
    # Estado para el número de películas
    if "num_movies_perfil" not in st.session_state:
        st.session_state.num_movies_perfil = default_num_movies

    # Estado para el guardado de las películas recomendadas
    if "recomendaciones" not in st.session_state or st.session_state.force_rerun == True:
        st.session_state.recomendaciones = SISTEMA_RECOMENDACIONES(matriz_similitud_recomendaciones, ratings_df, peliculas_no_votadas, st.session_state.num_movies_perfil)
        st.session_state.force_rerun = False  # Restablecer force_rerun
        
    # CAJA DE SELECCIÓN PARA SELECCIONAR EL NÚMERO DE PELÍCULAS
    select_box.SELECT_BOX(
        st.session_state.num_movies_perfil, 
        "num_movies_select_perfil", 
        num_pelis.perfil.ACTUALIZAR_NUM_PELIS_PERFIL
    )

    vista.VISTA_PELICULAS(st.session_state.recomendaciones)
    # DETALLES FINALES
    # Vista de las películas recomendadas en una cuadrícula
    #vista.VISTA_PELICULAS(st.session_state.recomendaciones)

    # Guardar los ratings actualizados
    ratings.GUARDAR_RATINGS()

# LLAMADA AL "MAIN"
if __name__ == "__main__":
    main()
