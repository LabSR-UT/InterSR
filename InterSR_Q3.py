# Interpretacion SR
# Quiz 2

import streamlit as st

st.title('Quiz 3')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual es la principal diferencia entre los modelos de color RGB & HSV?",
    ["Forma geometrica", "Numero de componentes", "Definicion de un color particular"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual es el objetivo de las combinaciones de bandas?",
    ["Distinguir objetos en una imagen", "Facilitar el procesamiento","Visualizacion mas llamativa"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
