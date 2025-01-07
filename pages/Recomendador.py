import streamlit as st
from streamlit_star_rating import st_star_rating
import pandas as pd
import os
from codigos.pln_sinopsis import load_data, find_similar_movies

# File paths
file_path = "CSV/peliculas_limpio.csv"
image_links_path = "CSV/link_imagenes.csv"
ratings_path = "CSV/ratings.csv"

def load_movie_data():
    return load_data(file_path, image_links_path)

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

def display_movies(movies):
    colums = 5
    for i in range(0, len(movies), colums):
        row = movies[i:i+colums]
        cols = st.columns(colums)
        for j, movie in enumerate(row):
            with cols[j]:
                st.subheader(movie["title"])
                if pd.notna(movie["imagen"]):
                    st.image(movie["imagen"], use_container_width=True)
                else:
                    st.write("Imagen no disponible")

                st.write(f"Género: {movie['genre']}")
                st.write(f"Año: {movie['year']}")
                st.write(f"Similitud: {movie['similarity']:.2f}")

                movie_key = f"rating_{movie['title']}"
                if movie_key not in st.session_state:
                    st.session_state[movie_key] = existing_ratings.get(movie['title'], 0)

                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key,
                )


def main():
    st.set_page_config(layout="wide")
    st.title("Recomendador de Películas Similares")

    global data, tfidf_matrix, existing_ratings
    data, tfidf_matrix = load_movie_data()
    existing_ratings = load_existing_ratings()

    selected_movie = st.selectbox(
        "Selecciona una película:",
        options=data['title'].tolist(),
        key="movie_search"
    )

    num_recommendations = st.selectbox(
        "Número de recomendaciones:",
        options=[5, 10, 15, 20, 25, 30],
        index=1 
    )

    if selected_movie:
        st.write(f"Película seleccionada: {selected_movie}")
        similar_movies = find_similar_movies(selected_movie, data, tfidf_matrix, num_recommendations)
        
        if similar_movies:
            st.subheader(f"Películas similares a '{selected_movie}':")
            display_movies(similar_movies)  # Pasamos directamente similar_movies
    else:
        st.write("No se encontraron películas similares.")


    save_ratings_to_csv()

if __name__ == "__main__":
    main()
