import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

# Función para raspar el sitio web
def scrape_website(entidad):
    # Codifica la entidad para que sea segura para usar en una URL
    entidad_encoded = quote(entidad)
    url = f"https://p.editor80.com.ar/_lab2023/discover/?entidad={entidad_encoded}"
    response = requests.get(url, headers={'Accept-Language': 'es-MX'})
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = [element.text for element in soup.find_all(class_=["fawSt oZW33b", "poMUXd tNxQIb a6sqte ScY7ec"])]
    medios = [element.text for element in soup.find_all(class_=["R9bvDb", "TRPjn"])]

    return titles, medios

def main():
    st.title("🔍 Scrapeando Discover")
    
    entidad = st.text_input("Introduce una entidad (ejemplo: chivas):")
    
    if st.button("Raspar"):
        titles, medios = scrape_website(entidad)
        
        # Mostrar en formato tabla
        df = pd.DataFrame({
            'Títulos': titles,
            'Medios': medios
        })
        st.table(df)

        # Mostrar en gráfico de barras
        st.subheader("Medios que más impactan en la entidad")
        st.bar_chart(df['Medios'].value_counts().sort_values(ascending=False))

        # Gráfico de torta
        st.subheader("Proporción de medios")
        st.pie_chart(df['Medios'].value_counts())

    st.write("© Alivia Media")

if __name__ == "__main__":
    main()
