import pandas as pd

df_sinopsis = pd.read_csv("CSV/peliculas_procesadas.csv", encoding="UTF-8")
print(df_sinopsis)

X = df_sinopsis["processed_synopsis"]
y = df_sinopsis["title"]