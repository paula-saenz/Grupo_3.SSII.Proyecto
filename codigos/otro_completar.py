import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os

# Función para cargar ratings existentes
def load_existing_ratings():
    ratings_path = "CSV/ratings.csv"
    if os.path.exists(ratings_path):
        ratings_df = pd.read_csv(ratings_path)
        return dict(zip(ratings_df['title'], ratings_df['rating']))
    return {}

# Guardar calificaciones en un CSV
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

# Función para mostrar películas
def display_movies(movies):
    colums = 5
    grid = [movies.iloc[i: i + colums] for i in range(0, len(movies), colums)]

    for row in grid:
        cols = st.columns(colums)
        for i, movie in enumerate(row.iterrows()):
            movie = movie[1]
            movie_key = f"rating_{movie['title']}"

            # Usar el rating existente o 0 si no existe
            if movie_key not in st.session_state:
                st.session_state[movie_key] = existing_ratings.get(movie['title'], 0)

            with cols[i]:
                st.subheader(movie["title"])
                if pd.notna(movie["imagen"]):
                    st.image(movie["imagen"], use_container_width=True)
                else:
                    st.write("Imagen no disponible")

                st.write(f"Género: {movie['genre']}")
                st.write(f"Año: {movie['year']}")

                # Mostrar el selector de estrellas y guardar la calificación
                rating = st_star_rating(
                    label="",
                    maxValue=10,
                    defaultValue=st.session_state[movie_key],
                    key=movie_key,
                )

def main():
    st.set_page_config(layout="wide")
    st.title("Perfil de usuario")

    file_path = "CSV/peliculas_limpio.csv"
    image_links_path = "CSV/link_imagenes.csv"
    global data
    data = pd.read_csv(file_path)
    image_links = pd.read_csv(image_links_path)

    data = pd.merge(data, image_links, on="title", how="left")

    # Cargar ratings existentes
    global existing_ratings
    existing_ratings = load_existing_ratings()

    # Sugerencias dinámicas
    st.subheader("Sugerencias dinámicas")

    # Campo de búsqueda con opciones dinámicas
    search = st.text_input("Escribe el inicio de una película:", key="search_input")
    if search:
        # Filtrar títulos dinámicamente
        suggestions = [title for title in data['title'] if title.lower().startswith(search.lower())]
        if suggestions:
            selected_title = st.selectbox("Resultados coincidentes:", suggestions)
        else:
            selected_title = None
            st.write("No se encontraron películas que comiencen con ese texto.")

        # Mostrar películas al presionar ENTER
        if st.button("Buscar"):
            if selected_title:
                filtered_movies = data[data['title'] == selected_title]
            else:
                filtered_movies = data[data['title'].str.startswith(search, na=False, case=False)]

            display_movies(filtered_movies)
            save_ratings_to_csv()

if __name__ == "__main__":
    main()