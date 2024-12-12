import pandas as pd
import csv

df = pd.read_csv("peliculas_limpio.csv", header=None)

titulo = df[1].tolist()

with open("ratings.csv", mode='w', encoding='utf-8', newline='') as csvfile:
    # Definir los encabezados
    fieldnames = ['title'] + ['rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()
    for i in range(1, len(titulo
        )):
        writer.writerow({
            'title': titulo[i],
            'rating': 0
        })
   
    
