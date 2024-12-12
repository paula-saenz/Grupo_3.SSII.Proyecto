#coger del csv el link y de ahi coger las caratulas

#hacer una lista con la ultima columna del csv, recorrerla y entrar al link, y de ahi hacer scrap

import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv

df = pd.read_csv("peliculas_limpio.csv", header=None)

titulo = df[1].tolist()
link = df[25].tolist()

diccionario = {}

#recorrer la lista de links
for i in range(1,4):    
    #hacer scrap de la web
    url = link[i]
    page = requests.get(url)
    soup = BeautifulSoup (page.content, 'html.parser')
    #coger la imagen de la web
    carpeta= soup.find("div", class_="media-scorecard no-border")
    imagen= carpeta.find("rt-img").get("src")
    diccionario[titulo[i]] = imagen
    
    print(titulo[i])
    print(imagen)

    with open("link_imagenes.csv", mode='w', encoding='utf-8', newline='') as csvfile:
            # Definir los encabezados
            fieldnames = ['Titulo'] + ['Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            
            # Escribir encabezados
            writer.writeheader()

            # Escribir los datos
            for categoria, meses in categorias_por_mes.items():
                row = {'Categoría': categoria}
                row.update({f'Mes {i+1}': meses[i] for i in range(12)})
                writer.writerow(row)

        print(f"Archivo '{archivo_salida}' creado con éxito.")




