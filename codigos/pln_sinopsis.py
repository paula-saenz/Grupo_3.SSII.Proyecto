import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Descargar recursos necesarios de NLTK
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Cargar el CSV
input_csv = "CSV/peliculas_limpio.csv"
output_csv = "CSV/peliculas_PLN.csv"
data_df = pd.read_csv(input_csv)

# Inicializar stopwords y stemmer
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')  

# Lista para almacenar sinopsis procesadas
processed_synopsis = []  

for texto in data_df['synopsis']:
    # Paso 1: Verificar si el texto es una cadena
    if isinstance(texto, str):
        # Paso 2: Convertir a minúsculas
        texto_lower = texto.lower()
        
        # Paso 3: Tokenización
        tokens = word_tokenize(texto_lower)
        
        # Paso 4: Filtrar tokens (eliminar stopwords y caracteres no alfanuméricos)
        filtered_tokens = []  # Lista para almacenar tokens filtrados
        for word in tokens:
            if word.isalnum() and word not in stop_words:
                filtered_tokens.append(word)  # Agregar palabra a la lista si pasa los filtros
        
        # Paso 5: Aplicar stemming a los tokens filtrados
        stemmed_tokens = []  # Lista para almacenar tokens con stemming aplicado
        for word in filtered_tokens:
            stemmed_word = stemmer.stem(word)  # Aplicar stemming
            stemmed_tokens.append(stemmed_word)  # Agregar palabra lematizada a la lista
        
        # Paso 6: Unir los tokens procesados en un solo string
        processed_text = ' '.join(stemmed_tokens)
        
        # Paso 7: Agregar la sinopsis procesada a la lista final
        processed_synopsis.append(processed_text)
    else:
        # Manejo de valores no string (agregar un string vacío)
        processed_synopsis.append('')

# Añadir la columna de sinopsis procesadas al DataFrame
data_df['processed_synopsis'] = processed_synopsis

# Vectorización TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data_df['processed_synopsis'])

print("Matriz TF-IDF:")
print(tfidf_matrix)

# Para ver los términos (palabras) correspondientes a las columnas de la matriz
print("Terminos:")
print(vectorizer.get_feature_names_out())

# Para imprimir los pesos de la primera sinopsis
print("Pesos TF-IDF para la primera sinopsis:")
print(tfidf_matrix[0].toarray())  # Convertir a array denso para visualizar

# Guardar el resultado en un CSV
#data_df[['title', 'processed_synopsis']].to_csv(output_csv, index=False)
