import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os 

# Ruta para almacenar los ajustes de las ventanas
settings_path_galeria = "CSV/settings.csv"

def load_settings_galeria():
    if not os.path.exists(settings_path_galeria):
        settings_df = pd.DataFrame({"num_movies": [15]})
        settings_df.to_csv(settings_path_galeria, index=False)
    else:
        settings_df = pd.read_csv(settings_path_galeria)
    return settings_df

def load_saved_num_movies_gal():
    settings_df = load_settings_galeria()
    return int(settings_df["num_movies"].iloc[0])


# Ruta para almacenar los ajustes de las ventanas
settings_path_perfil = "CSV/settings1.csv"

def load_settings_perfil():
    if not os.path.exists(settings_path_perfil):
        settings_df = pd.DataFrame({"num_movies": [15]})
        settings_df.to_csv(settings_path_perfil, index=False)
    else:
        settings_df = pd.read_csv(settings_path_perfil)
    return settings_df

def load_saved_num_movies_per():
    settings_df = load_settings_perfil()
    return int(settings_df["num_movies"].iloc[0])


# Ruta para almacenar los ajustes de las ventanas
settings_path_recomendador = "CSV/settings2.csv"

def load_settings_recomendador():
    if not os.path.exists(settings_path_recomendador):
        settings_df = pd.DataFrame({"num_movies": [15]})
        settings_df.to_csv(settings_path_recomendador, index=False)
    else:
        settings_df = pd.read_csv(settings_path_recomendador)
    return settings_df

def load_saved_num_movies_rec():
    settings_df = load_settings_recomendador()
    return int(settings_df["num_movies"].iloc[0])
