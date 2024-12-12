import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv

df = pd.read_csv("peliculas_limpio.csv", header=None)

titulo = df[1].tolist()
link = df[25].tolist()

archivo_salida = "link_imagenes.csv"

with open(archivo_salida, mode='w', encoding='utf-8', newline='') as csvfile:
    # Definir los encabezados
    fieldnames = ['title'] + ['imagen']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    
    # Escribir encabezados
    writer.writeheader()
    #recorrer la lista de links
    for i in range(1, len(link)):    
        #hacer scrap de la web
        url = link[i]
        page = requests.get(url)
        soup = BeautifulSoup (page.content, 'html.parser')
        #coger la imagen de la web
        try:
            carpeta= soup.find("div", class_="media-scorecard no-border")
            imagen= carpeta.find("rt-img").get("src")
            
            print(titulo[i])
            print(imagen)
            writer.writerow({
                'title': titulo[i],
                'imagen': imagen
            })

        except:
            print(f"La película {titulo[i]} no tiene imagen asociada" )

        print(f"Archivo '{archivo_salida}' creado con éxito.")




