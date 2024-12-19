import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder

data_df=pd.read_csv("CSV/peliculas_limpio.csv")
data_df_ratings=pd.read_csv("CSV/ratings.csv")
df_ratings = data_df_ratings[["rating"]]
#cuando rating sea mayor a 8


df = data_df[["title", "year", "genre", "director", "writer"]]

#print(df)

if df.shape[0] != df_ratings.shape[0]:
    raise ValueError("El número de filas en las películas y las calificaciones no coincide")


encoder = OneHotEncoder(sparse_output= False)
title_en = encoder.fit_transform(df[["title"]])
genre_en = encoder.fit_transform(df[["genre"]])
director_en = encoder.fit_transform(df[["director"]])
writer_en = encoder.fit_transform(df[["writer"]])

year_en = df[["year"]].values
rating_en = df_ratings[["rating"]].values

matriz_caract = np.hstack((year_en,rating_en,title_en,genre_en,director_en,writer_en))

matriz_sim=cosine_similarity(matriz_caract)
#print(matriz_caract)

similarity_df=pd.DataFrame(matriz_sim, index=df["title"], columns=df["title"])
#print(similarity_df)

def recomendar_peli(peli):
    similar_movies = similarity_df[peli].sort_values(ascending=False).head(10)
    return similar_movies

pelicula = "Spider-Man: Into the Spider-Verse"
print(f"\nPeliculas similares a: {pelicula}")
print(recomendar_peli(pelicula))
