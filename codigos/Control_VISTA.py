import pandas as pd
import streamlit as st
import os
from streamlit_star_rating import st_star_rating
from codigos.Control_CSV import ratings, CSV

# CREACIÓN DE LA CLASE "VISTA"
class vista:

    # CREACIÓN DE LA FUNCIÓN "VISTA_PELÍCULAS" CON EL PARÁMETRO "PELÍCULAS", SIENDO ESTE EL DATAFRAME DE LAS PELÍCULAS
    def VISTA_PELICULAS(peliculas):
        # CARGAR EL CSV DE "RATINGS".
        ratings_CSV = ratings.CARGAR_RATINGS()


        # SE CREA UN GRID VACÍO CON UN MÁXIMO DE 5 COLUMNAS.
        columnas = 5
        grid = []

        for i in range(0, len(peliculas), columnas): # Dividir el DataFrame en bloques del tamaño especificado por "columnas".
            # 0 [inicio] --> Indica que el grid comienza en 0 (no hay películas).
            # len(películas) [fin] --> Indica que acaba en el número de películas totales - 1.
            # columnas [paso] --> Va saltando de longitud de columna en longitud de columna (en este caso de 5 en 5).

            filas = peliculas.iloc[i: i + columnas]
            # .iloc -->  Método de indexación de PANDAS. Permite seleccionar filas o columnas de un Dataframe o Series basados en números enteros.
                # peliculas.iloc --> "películas" es un Dataframe, por lo que se utiliza .iloc para seleccionar subconjuntos de filas basados en su posición numérica.
            # [i: i + columnas] --> Indica que va desde i (comienza en 0), hasta i + columnas (0 + 5). Quiere decir que la primera fila es de [0, 1, 2, 3, 4], luego [5, 6, 7, 8, 9], etc...

            grid.append(filas)


        # SE INTRODUCEN ELEMENTOS EN EL GRID
        for fila in grid:
            cols = st.columns(columnas) # Crea un conjunto de columnas en la interfaz de StreamLit

            for i, peli in enumerate(fila.iterrows()):
                peli = peli[1]
                titulo = f"rating_{peli['title']}"

                # SE USAN LOS RATINGS YA EXISTENTES EN EL ESTADO.
                # EN EL CASO DE QUE NO ESTÉ, SE INTERPRETA COMO UN 0
                if titulo not in st.session_state:
                    st.session_state[titulo] = ratings_CSV.get(peli['title'], 0)

                # SE MUESTRA TODA LA INFORMACIÓN EN LAS COLUMNAS
                with cols[i]: # Se entra dentro de cada columna específica
                    st.subheader(peli["title"])

                    if pd.notna(peli["imagen"]): # Si existe la imagen se muestra, si no se muestra un mensaje
                    # notna --> Método de PANDAS. Detecta sin un valor existe

                        st.image(peli["imagen"], use_container_width=True)
                    else:
                        st.write("Imagen no disponible")

                    st.write(f"Género: {peli['genre']}")
                    st.write(f"Año: {peli['year']}")

                    # SE MUESTRAN LAS ESTRELLAS Y SE GUARDAN EN EL ESTADO CON EL KEY DE "TITLE"
                    st_star_rating(
                        label="", # No muestra título junto a las estrellas
                        maxValue=10, # Máximo 10 estrellas
                        defaultValue=st.session_state[titulo], # Usa el valor almacenado en el estado como "default"
                        key=titulo, # La clave única será el "titulo"
                    )

# CREACIÓN DE LA CLASE "NUM_PELIS"
class num_pelis:
    class perfil:
        def GUARDAR_NUM_PELIS_PERFIL(num_movies_perfil):
            settings_df = num_pelis.perfil.GUARDAR_NUM_PERFIL()
            settings_df["num_movies_perfil"] = num_movies_perfil
            settings_df.to_csv(CSV.SETTINGS1_CSV(), index=False)    

            # CREACIÓN DE LA FUNCIÓN "ACTUALIZAR_NUM_PELIS"
        def ACTUALIZAR_NUM_PELIS_PERFIL():
            num_pelis.perfil.GUARDAR_NUM_PELIS_PERFIL(st.session_state.num_movies_select_perfil)
            st.session_state.num_movies_perfil = st.session_state.num_movies_select_perfil

        def GUARDAR_NUM_PERFIL():
            if not os.path.exists(CSV.SETTINGS1_CSV()):
                settings_df = pd.DataFrame({"num_movies_perfil": [15]})
                settings_df.to_csv(CSV.SETTINGS1_CSV(), index=False)
            else:
                settings_df = pd.read_csv(CSV.SETTINGS1_CSV())
            return settings_df

        # CREACIÓN DE LA FUNCIÓN "CARGAR_NUM_GALERIA"
        def CARGAR_NUM_PERFIL():
            settings_df = num_pelis.perfil.GUARDAR_NUM_PERFIL()
            return int(settings_df["num_movies_perfil"].iloc[0])

    # CREACIÓN DE LA SUBCLASE "GALERÍA"
    class galeria:
        
        # CREACIÓN DE LA FUNCIÓN "GUARDAR_NUM_PELIS" CON EL PARÁMETRO "NUM_MOVIES" INDICANDO EL NÚMERO DE PELÍCULAS VISIBLES MÁXIMAS EN VENTANA
        def GUARDAR_NUM_PELIS_GALERIA(num_movies_galeria):
            settings_df = num_pelis.galeria.GUARDAR_NUM_GALERIA()
            settings_df["num_movies_galeria"] = num_movies_galeria
            settings_df.to_csv(CSV.SETTINGS_CSV(), index=False)

        # CREACIÓN DE LA FUNCIÓN "ACTUALIZAR_NUM_PELIS"
        def ACTUALIZAR_NUM_PELIS_GALERIA():
            num_pelis.galeria.GUARDAR_NUM_PELIS_GALERIA(st.session_state.num_movies_select_galeria)
            st.session_state.num_movies_galeria = st.session_state.num_movies_select_galeria

        # CREACIÓN DE LA FUNCIÓN "GUARDAR_NUM_GALERIA"
        def GUARDAR_NUM_GALERIA():
            if not os.path.exists(CSV.SETTINGS_CSV()):
                settings_df = pd.DataFrame({"num_movies_galeria": [15]})
                settings_df.to_csv(CSV.SETTINGS_CSV(), index=False)
            else:
                settings_df = pd.read_csv(CSV.SETTINGS_CSV())
            return settings_df

        # CREACIÓN DE LA FUNCIÓN "CARGAR_NUM_GALERIA"
        def CARGAR_NUM_GALERIA():
            settings_df = num_pelis.galeria.GUARDAR_NUM_GALERIA()
            return int(settings_df["num_movies_galeria"].iloc[0])
        
class paginas_caratulas:
    def PAGINAS(paginacion):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Anterior") and st.session_state.current_page > 1:
                st.session_state.current_page -= 1
        with col3:
            if st.button("➡️ Siguiente") and st.session_state.current_page < paginacion:
                st.session_state.current_page += 1
        with col2:
            st.write(f"Página {st.session_state.current_page} de {paginacion}")

        

    