import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating

def main():
    st.set_page_config(layout="wide") # Se configura para que ocupe todo el ancho de la web (incluye responsive)
    st.title("Recomendador Películas")

    file_path = 'peliculas_limpio.csv' # Se guarda el CSV en una variable
    data = pd.read_csv(file_path) # Se lee el CSV

    num_movies = 15 # Número de películas que aparecerán por pantalla
    random_movies = data.sample(n=num_movies) # Salen películas aleatorias

    colums = 5 # Número de columnas

    grid = [random_movies.iloc[i:i+colums] for i in range(0, len(random_movies), colums)] # Formación del Grid para las películas

    for row in grid:
        cols = st.columns(colums) # Se colocan los datos en esas columnas ya formadas

        for i, movie in enumerate(row.iterrows()):
            movie = movie[1] # Agarramos los datos de la película, ignorando el índice
            with cols[i]: # Recorremos columna por columna
                st.subheader(movie['title']) # Agarramos el título
                st.write(f"Género: {movie['genre']}") # Agarramos el género
                st.write(f"Año: {movie['year']}") # Agarramos el año
                st_star_rating(label="", maxValue=5, defaultValue=0, key=f"rating_{movie['title']}") # Poner 5 estrellas debajo de cada película.
                

                #añadir: poder votar
                #añadir: guardar votaciones en un csv que se cargue siempre que se inicie la app
                #añadir: mostrar las películas recomendadas en función de las votaciones (pelis que no se hayan votado todavía)
                #scrapper para coger caratulas de pelis
                #añadir: poder escoger cuantas paelis aparecen en el recomendador
                #añadir: poder tener un historial de las pelis que se han votado
                #añadir: Hacer un autocompletar para buscar películas
                #añadir: ratio con el que se recomiendan las películas


if __name__ == "__main__":
    main()
