import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote
import matplotlib.pyplot as plt

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

# ... [resto del código sin cambios]

def main():
    st.title("🔍 Scrapeando Google Discover")
    
    entidad = st.text_input("Introduce una entidad (ejemplo: liga mx para ver noticias relacionadas a Liga MX ;)):")
    
    if st.button("Raspar para ver noticias"):
        titles, medios = scrape_website(entidad)
        
        # Mostrar en formato tabla
        df = pd.DataFrame({
            'Títulos': titles,
            'Medios': medios
        })
        st.table(df)

        # Mostrar en gráfico de barras horizontal
        st.subheader("Medios que más están impactando en la entidad")
        medios_counts = df['Medios'].value_counts().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        medios_counts.plot(kind='barh', ax=ax)
        ax.set_xlabel('Cantidad')
        ax.set_title('Medios que más impactan en la entidad')
        st.pyplot(fig)

        # Gráfico de torta usando matplotlib
        st.subheader("Impacto en proporción")
        fig, ax = plt.subplots()
        df['Medios'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
        ax.set_ylabel('')
        st.pyplot(fig)

    st.write("© Alivia Media")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
