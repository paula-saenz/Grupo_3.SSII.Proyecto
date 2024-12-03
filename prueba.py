import streamlit as st
import pandas as pd

 
df = pd.read_csv("peliculas.csv")
 
st.write("""
# My first app
Hello *world!*
""", df)
