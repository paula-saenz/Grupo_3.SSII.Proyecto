import os
import pandas as pd
import streamlit as st

# CREACIÓN DE LA CLASE "CSV"
class CSV:   

    # CREACIÓN DE LA FUNCIÓN "RATINGS_CSV"
    def RATINGS_CSV():
        return "CSV/ratings.csv"
    
    # CREACIÓN DE LA FUNCIÓN "PELICULAS_LIMPIO_CSV"
    def PELICULAS_LIMPIO_CSV(): 
        return "CSV/peliculas_limpio.csv"

    # CREACIÓN DE LA FUNCIÓN "LINK_IMAGENES_CSV"
    def LINK_IMAGENES_CSV(): 
        return "CSV/link_imagenes.csv"
    
    def SETTINGS_CSV():
        return "CSV/settings.csv"
    
    def SETTINGS1_CSV():
        return "CSV/settings1.csv"
# CREACIÓN DE LA CLASE "RATINGS"
class ratings:

    # CREACIÓN DE LA FUNCIÓN "CARGAR_RATINGS"
    def CARGAR_RATINGS():
        ratings_CSV = CSV.RATINGS_CSV()

        # VERIFICA SI "RATINGS.CSV" EXISTE, SI NO CREA UN DICCIONARIO VACÍO
        if os.path.exists(ratings_CSV):
            ratings_df = pd.read_csv(ratings_CSV)
            return dict(zip(ratings_df['title'], ratings_df['rating'])) # Si existe, crea un diccionario con "title" y "rating"
            # zip --> Combina en pares, en este caso ({title1, rating1}, {title2, rating2}, ...)
        return {}
    
    # CREACIÓN DE LA FUNCIÓN "GUARDAR_RATINGS"
    def GUARDAR_RATINGS():
        ratings_CSV = CSV.RATINGS_CSV()
        if os.path.exists(ratings_CSV):
            ratings_df = pd.read_csv(ratings_CSV)
        else:
            ratings_df = pd.DataFrame(columns=["title", "rating"]) # Si no existe, lo crea de 0 con las columnas "title" y "rating"

        # ITERAR SOBRE TODOS LOS VALORES DEL ESTADO
        for key, value in st.session_state.items(): # Mira el nombre del estado ("key") y su valor asociado (value)
            if key.startswith("rating_"): # Filtra todos los estados que comiencen por "rating_", asegurando que solo se procesen los ratings del estado y no otros datos
                title = key.replace("rating_", "") # Elimina el prefijo "rating_" (Ejemplo: key = "rating_Peli1", entonces title = "Peli1")

                # ACTUALIZAR / AÑADIR CALIFICACIONES
                if title in ratings_df["title"].values: # Si la película está en el Dataframe
                    ratings_df.loc[ratings_df["title"] == title, "rating"] = value # Actualiza la columna "rating" con el nuevo valor
                else:
                    ratings_df = pd.concat( # Si no está crea un nuevo Dataframe con el rating actual
                        # concat --> Combina el nuevo Dataframe con el anterior en vez de sustituirlo
                        [ratings_df, pd.DataFrame([{"title": title, "rating": value}])],
                        ignore_index=True,
                    )

        # GUARDA LOS RATINGS EN EL CSV
        ratings_df.to_csv(ratings_CSV, index=False)
        