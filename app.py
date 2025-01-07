import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
from codigos.recomendaciones_perfil import load_and_prepare_data, create_similarity_matrix, recomendar_peliculas_top_rated
from codigos.Control_VISTA import paginas_caratulas, vista, num_pelis

def load_existing_ratings():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        ratings_df = ratings_df[ratings_df['rating'] != 0]
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

def update_rating(title, rating):
    # Asegurarse de que 'title' sea un string para evitar problemas con claves no hashables
    title = str(title)

    # Verificar que el rating sea un número (entero o flotante)
    if isinstance(rating, (int, float)):
        # Actualizar el rating en session_state
        st.session_state[f"rating_{title}"] = rating
        # También actualizar en 'existing_ratings'
        if 'existing_ratings' not in st.session_state:
            st.session_state.existing_ratings = {}
        st.session_state.existing_ratings[title] = rating
    else:
        st.error("El valor de rating debe ser un número (int o float).")

def save_ratings_to_csv():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
    else:
        ratings_df = pd.DataFrame(columns=["title", "rating"])

    # Iterar sobre el session_state para obtener las calificaciones
    for key, value in st.session_state.items():
        if key.startswith("rating_"):  # Filtrar las claves que corresponden a ratings
            title = key.replace("rating_", "")  # Extraer el título
            if isinstance(value, (int, float)):  # Asegurarse de que el valor sea numérico
                # Verificar si ya existe el título en el DataFrame
                if title in ratings_df["title"].values:
                    ratings_df.loc[ratings_df["title"] == title, "rating"] = value
                else:
                    ratings_df = pd.concat(
                        [ratings_df, pd.DataFrame([{"title": title, "rating": value}])],
                        ignore_index=True,
                    )
    ratings_df.to_csv(ratings_path, index=False)


def update_random_movies_auto():
    st.session_state.auto_random_movies = data.sample(n=st.session_state.num_movies_perfil)
    num_pelis.perfil.GUARDAR_NUM_PELIS_PERFIL(st.session_state.num_movies_perfil)  # Guardar el número de películas seleccionado

def get_recommendations(similarity_df, data_df_ratings, data, num_movies_perfil):
    existing_ratings = load_existing_ratings()
    rated_movies = [title for title, rating in existing_ratings.items() if rating > 0]

    if rated_movies:
        recomendaciones = recomendar_peliculas_top_rated(similarity_df, data_df_ratings, top_n=num_movies_perfil)
        if recomendaciones.empty:
            return data.sample(n=num_movies_perfil)
        recomendaciones = recomendaciones.reset_index().merge(data, on="title", how="left")
    else:
        recomendaciones = data.sample(n=num_movies_perfil)

    return recomendaciones

def main():
    st.set_page_config(layout="wide")
    st.title("PERFIL")

    if 'rating_peli' not in st.session_state:
        st.session_state.rating_peli = load_existing_ratings()

    st.dataframe(st.session_state.rating_peli)

    # Cargar y preparar los datos
    df, data_df_ratings = load_and_prepare_data()
    similarity_df = create_similarity_matrix(df)

    file_path = "CSV/peliculas_limpio.csv"
    image_links_path = "CSV/link_imagenes.csv"
    ratings_valorado_path = "CSV/ratings.csv"
    
    global data
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)
    data = pd.merge(data, image_links, on="title", how="left")

    peliculas_no_votadas = data[~data['title'].isin(st.session_state.rating_peli.keys()) | (data['title'].isin(st.session_state.rating_peli.keys()) & (st.session_state.rating_peli.values() == 0))]


    if not os.path.exists(ratings_valorado_path):
        ratings_df = data[["title"]].copy()
        ratings_df["rating"] = 0
        ratings_df.to_csv(ratings_valorado_path, index=False)

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
        st.session_state.recomendaciones = get_recommendations(similarity_df, data_df_ratings, peliculas_no_votadas, st.session_state.num_movies_perfil)

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
    save_ratings_to_csv()

if __name__ == "__main__":
    main()