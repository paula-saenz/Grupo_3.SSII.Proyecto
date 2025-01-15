import os
import pandas as pd
import streamlit as st
import csv

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
            ratings_df = ratings_df[ratings_df['rating'] != 0]
            return dict(zip(ratings_df['title'], ratings_df['rating'])) # Si existe, crea un diccionario con "title" y "rating"
            # zip --> Combina en pares, en este caso ({title1, rating1}, {title2, rating2}, ...)
        return {}
    
    # CREACIÓN DE LA FUNCIÓN "GUARDAR_RATINGS"
    def GUARDAR_RATINGS(): # NO SÉ QUE HE TOCADO, PERO FUNCIONA. SOLO GUARDA EL VALOR ANTERIOR AL SER NULL. NO SÉ SI SE HA LIADO CON ALGO EXTRA
        ratings_CSV = CSV.RATINGS_CSV()
        ratings_df = pd.read_csv(ratings_CSV)

        # ITERAR SOBRE TODOS LOS VALORES DEL ESTADO
        for key, value in st.session_state.items():
            if key.startswith("rating_"):
                title = key.replace("rating_", "")

                # ACTUALIZAR / AÑADIR CALIFICACIONES
                if title in ratings_df["title"].values:  # Si la película está en el Dataframe
                    # Obtener el valor anterior
                    previous_rating = ratings_df.loc[ratings_df["title"] == title, "rating"].values[0]

                    # Actualizar el rating solo si no es None
                    if value is not None:
                        ratings_df.loc[ratings_df["title"] == title, "rating"] = value
                    else:
                        # Si el nuevo valor es None, restaurar el valor anterior
                        ratings_df.loc[ratings_df["title"] == title, "rating"] = previous_rating

        # GUARDA LOS RATINGS EN EL CSV
        ratings_df.to_csv(ratings_CSV, index=False)
    
    def GENERAR_RATINGS():
        ratings_path = CSV.RATINGS_CSV()
        if not os.path.exists(ratings_path):
            
            df = pd.read_csv("CSV/peliculas_limpio.csv", header=None)

            titulo = df[1].tolist()

            with open("CSV/ratings.csv", mode='w', encoding='utf-8', newline='') as csvfile:
                # Definir los encabezados
                fieldnames = ['title'] + ['rating']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()
                for i in range(1, len(titulo
                    )):
                    writer.writerow({
                        'title': titulo[i],
                        'rating': int(0)
                    })