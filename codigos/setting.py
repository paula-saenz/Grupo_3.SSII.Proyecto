import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os 

# Ruta para almacenar los ajustes de las ventanas
settings_path = "CSV/settings.csv"

#fucnion para ver si existe el setting.csv
def setting_exist():
    # Crear un DataFrame con los valores iniciales
    settings_df = pd.DataFrame({
        "window": ["galería", "perfil", "recomendaciones"],
        "num_movies": [15, 15, 15]
    })
    # Guardar el archivo
    settings_df.to_csv(settings_path, index=False)

# Función para cargar o inicializar el archivo de configuración
def load_settings_galeria():
    if not os.path.exists(settings_path):
        setting_exist()
    else:
        # Cargar el archivo existente
        settings_df = pd.read_csv(settings_path)
        galeria = "galería"
        # Verificar si las ventanas necesarias están presentes; si no, agregarlas
        if  galeria not in settings_df["window"].values:
            new_row = {"window": galeria, "num_movies": 15}
            settings_df = pd.concat([settings_df, pd.DataFrame([new_row])], ignore_index=True)
            # Guardar cualquier actualización
        settings_df.to_csv(settings_path, index=False)
    return settings_df

def load_settings_perfil():
    if not os.path.exists(settings_path):
        setting_exist()
    else:
        # Cargar el archivo existente
        settings_df = pd.read_csv(settings_path)
        # Verificar si las ventanas necesarias están presentes; si no, agregarlas
        required_windows = ["galería", "perfil", "recomendaciones"]
        for window in required_windows:
            if window not in settings_df["window"].values:
                new_row = {"window": window, "num_movies": 15}
                settings_df = pd.concat([settings_df, pd.DataFrame([new_row])], ignore_index=True)
        # Guardar cualquier actualización
        settings_df.to_csv(settings_path, index=False)
    return settings_df