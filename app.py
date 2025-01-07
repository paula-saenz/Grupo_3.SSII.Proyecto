import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
from codigos.recomendaciones_perfil import load_and_prepare_data, create_similarity_matrix, recomendar_peliculas_top_rated

def load_settings_perfil():
    settings_path_perfil = "CSV/settings1.csv"
    if os.path.exists(settings_path_perfil):
        return pd.read_csv(settings_path_perfil)
    else:
        return pd.DataFrame({"num_movies": [10]})

def load_saved_num_movies_per():
    settings_df = load_settings_perfil()
    return settings_df["num_movies"].iloc[0]

def save_num_movies(num_movies):
    settings_df = load_settings_perfil()
    settings_df["num_movies"] = num_movies
    settings_df.to_csv("CSV/settings1.csv", index=False)

def update_num_movies_per():
    save_num_movies(st.session_state.num_movies_select)
    st.session_state.num_movies = st.session_state.num_movies_select
    st.session_state.current_page = 1

def load_existing_ratings():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        ratings_df = ratings_df[ratings_df['rating'] != 0]
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

def save_ratings_to_csv():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
    else:
        ratings_df = pd.DataFrame(columns=["title", "rating"])

    for key, value in st.session_state.items():
        if key.startswith("rating_"):
            title = key.replace("rating_", "")
            if title in ratings_df["title"].values:
                ratings_df.loc[ratings_df["title"] == title, "rating"] = value
            else:
                ratings_df = pd.concat(
                    [ratings_df, pd.DataFrame([{"title": title, "rating": value}])],
                    ignore_index=True,
                )
    ratings_df.to_csv(ratings_path, index=False)

def update_random_movies_auto():
    st.session_state.auto_random_movies = data.sample(n=st.session_state.num_movies)
    save_num_movies(st.session_state.num_movies)  # Guardar el número de películas seleccionado

def get_recommendations(similarity_df, data_df_ratings, data, num_movies):
    existing_ratings = load_existing_ratings()
    rated_movies = [title for title, rating in existing_ratings.items() if rating > 0]

    if rated_movies:
        recomendaciones = recomendar_peliculas_top_rated(similarity_df, data_df_ratings, top_n=num_movies)
        recomendaciones = recomendaciones.reset_index().merge(data, on="title", how="left")
    else:
        st.warning("No hay películas calificadas. Mostrando películas aleatorias.")
        recomendaciones = data.sample(n=num_movies)

    return recomendaciones

def main():
    st.set_page_config(layout="wide")
    st.title("Galería de Películas Recomendadas")

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

    if not os.path.exists(ratings_valorado_path):
        ratings_df = data[["title"]].copy()
        ratings_df["rating"] = 0
        ratings_df.to_csv(ratings_valorado_path, index=False)

    default_num_movies = load_saved_num_movies_per()
    if "num_movies" not in st.session_state:
        st.session_state.num_movies = default_num_movies

    st.selectbox(
        label="Selecciona el número de películas a mostrar",
        options=[5, 10, 15, 20, 25, 30],
        index=[i for i, x in enumerate([5, 10, 15, 20, 25, 30]) if x == st.session_state.num_movies][0],
        key="num_movies_select",
        on_change=update_num_movies_per
    )

    if "recomendaciones" not in st.session_state or st.button("Actualizar recomendaciones"):
        st.session_state.recomendaciones = get_recommendations(similarity_df, data_df_ratings, data, st.session_state.num_movies)

    recomendaciones = st.session_state.recomendaciones

    # Manejo de la paginación
    num_movies = st.session_state.num_movies
    total_pages = (len(recomendaciones) + num_movies - 1) // num_movies
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Anterior") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
    with col3:
        if st.button("➡️ Siguiente") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
    with col2:
        st.write(f"Página {st.session_state.current_page} de {total_pages}")

    # Dividir las películas en páginas
    start_idx = (st.session_state.current_page - 1) * num_movies
    end_idx = start_idx + num_movies
    page_movies_df = recomendaciones.iloc[start_idx:end_idx]

    # Mostrar las películas en una cuadrícula
    colums = 5
    grid = [page_movies_df.iloc[i:i+colums] for i in range(0, len(page_movies_df), colums)]
    for row in grid:
        cols = st.columns(colums)
        for i, (_, movie) in enumerate(row.iterrows()):
            movie_key = f"rating_{movie['title']}"

            if movie_key not in st.session_state:
                st.session_state[movie_key] = load_existing_ratings().get(movie['title'], 0)

            with cols[i]:
                st.subheader(movie["title"])
                if pd.notna(movie["imagen"]):
                    st.image(movie["imagen"], use_container_width=True)
                else:
                    st.write("Imagen no disponible")

                st.write(f"Género: {movie['genre']}")
                st.write(f"Año: {movie['year']}")

                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key,
                )

    save_ratings_to_csv()

if __name__ == "__main__":
    main()