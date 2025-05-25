# Interpretacion SR
# Quiz 8

import streamlit as st

st.title('Quiz 8')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual es la principal diferencia entre seleccion y extraccion de atributos:",
    ["Transforma atributos originales", "Crea atributos nuevos", "Elimina atributos del conjunto", "Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Tipos de metodos de seleccion de atributos?",
    ["Filtrado/Embutidos/Envolventes", "Filtrado/Embebidos/Envolventes", "Filtrado/Embebidos/Envueltos", "Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
