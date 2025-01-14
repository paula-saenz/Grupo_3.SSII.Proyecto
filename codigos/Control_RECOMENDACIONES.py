import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from codigos.Control_CSV import CSV

def CARGAR_DATOS():
    peliculas_limplio_csv = CSV.PELICULAS_LIMPIO_CSV()
    ratings_csv = CSV.RATINGS_CSV()

    peliculas_df = pd.read_csv(peliculas_limplio_csv)
    ratings_df = pd.read_csv(ratings_csv)
    
    df = peliculas_df[["title", "year", "genre", "director", "writer"]]
    df = df[df["title"].isin(ratings_df["title"])]
    
    df["genre"] = df["genre"].fillna("")
    df["director"] = df["director"].fillna("")
    df["writer"] = df["writer"].fillna("")
    
    return df, ratings_df

def CREAR_MATRIZ_SIMILITUD(df):
    tfidf_genre_vectorizer = TfidfVectorizer()
    tfidf_director_vectorizer = TfidfVectorizer()
    tfidf_writer_vectorizer = TfidfVectorizer()
    
    tfidf_genre = tfidf_genre_vectorizer.fit_transform(df["genre"]).toarray()
    tfidf_director = tfidf_director_vectorizer.fit_transform(df["director"]).toarray()
    tfidf_writer = tfidf_writer_vectorizer.fit_transform(df["writer"]).toarray()
    
    scaler = MinMaxScaler()
    year_en = scaler.fit_transform(df[["year"]])
    
    matriz_caract = np.hstack((year_en, tfidf_genre, tfidf_director, tfidf_writer))
    matriz_sim = cosine_similarity(matriz_caract)
    return pd.DataFrame(matriz_sim, index=df["title"], columns=df["title"])

def RECOMENDACION(similarity_df, data_df_ratings, top_n):
    peliculas_gustadas = data_df_ratings[data_df_ratings["rating"] >= 7]["title"].values
    peliculas_sin_rating = data_df_ratings[data_df_ratings["rating"] == 0]["title"].values
    
    recomendaciones = []
    for peli in peliculas_gustadas:
        if peli in similarity_df.index:
            pelis_similares = similarity_df[peli].sort_values(ascending=False).iloc[1:top_n + 1]
            peliculas_recomendadas = pelis_similares[pelis_similares.index.isin(peliculas_sin_rating)]
            recomendaciones.append(peliculas_recomendadas)
    
    if recomendaciones:
        recomendaciones_df = pd.concat(recomendaciones)
        recomendaciones_agrupadas = recomendaciones_df.groupby(recomendaciones_df.index).mean()
        return recomendaciones_agrupadas.sort_values(ascending=False).head(top_n)
    else:
        return pd.DataFrame()
    
    
    