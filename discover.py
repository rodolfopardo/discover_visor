import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Función para raspar el sitio web
def scrape_website(entidad):
    url = f"https://p.editor80.com.ar/_lab2023/discover/?entidad={entidad}"
    response = requests.get(url, headers={'Accept-Language': 'es-MX'})
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = [element.text for element in soup.find_all(class_=["fawSt oZW33b", "poMUXd tNxQIb a6sqte ScY7ec"])]
    medios = [element.text for element in soup.find_all(class_=["R9bvDb", "TRPjn"])]

    return titles, medios

def main():
    st.title("Raspar títulos y medios")
    
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
        st.bar_chart(df['Medios'].value_counts())

if __name__ == "__main__":
    main()
