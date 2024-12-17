import pandas as pd
df = pd.read_csv("CSV/peliculas1.csv", header=None)

print(df)
resultado = df.drop_duplicates(1)
print(resultado)

resultado.to_csv("CSV/peliculas_limpio.csv", index=False, header=False)