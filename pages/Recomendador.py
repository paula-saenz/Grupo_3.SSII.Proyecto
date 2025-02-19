import streamlit as st
from codigos.Control_PLN import pln
from codigos.Control_VISTA import num_pelis, vistaPLN
from codigos.Control_CSV import ratings, CSV


def main():

    # INICIAR LA PÁGINA
    ratings.GENERAR_RATINGS()
    st.set_page_config(layout="wide")
    st.title("Recomendador de Películas Similares")



    # CARGAR Y PREPARAR LOS DATOS
    # Datos de CSV
    file_path = CSV.PELICULAS_LIMPIO_CSV()
    image_links_path = CSV.LINK_IMAGENES_CSV()

    # Cargar datos
    data, tfidf_matrix = pln.CARGAR_DATOS(file_path, image_links_path)
    numero_pelis_inicio = num_pelis.recomendador.CARGAR_NUM_RECOMENDADOR()



    # SE INICIALIZAN LOS ESTADOS EN CASO DE QUE NO EXISTAN
    # Inicialización de variables de estado
    if "page_changed" not in st.session_state:
        st.session_state.page_changed = True

    if "current_movie" not in st.session_state:
        st.session_state.current_movie = None

    if "num_movies_recomendador" not in st.session_state:
        st.session_state.num_movies_recomendador = numero_pelis_inicio



    # CAJA DE SELECCIÓN PARA SELECCIONAR LAS PELÍCULAS
    selected_movie = st.selectbox(
        "Selecciona una película:",
        options=data['title'].tolist(),
        key="movie_search"
    )



    # CAJA DE SELECCIÓN PARA SELECCIONAR EL NÚMERO DE PELÍCULAS
    num_recommendations = st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == st.session_state.num_movies_recomendador][0],
        key="num_movies_select_recomendador",
        on_change=num_pelis.recomendador.ACTUALIZAR_NUM_PELIS_RECOMENDADOR
    )

    if selected_movie:
        st.write(f"Película seleccionada: {selected_movie}")
        similar_movies = pln.PELIS_SIMILARES(selected_movie, data, tfidf_matrix, num_recommendations)

        if similar_movies:
            st.subheader(f"Películas similares a '{selected_movie}':")
            vistaPLN.VISTA_PLN(similar_movies)
    else:
        st.write("No se encontraron películas similares.")

    ratings.GUARDAR_RATINGS() # ---> ¡SI SE CAMBIA DE VENTANA MUY RÁPIDO NO GUARDA EL RATING PORQUE NO DA TIEMPO!

if __name__ == "__main__":
    main()
