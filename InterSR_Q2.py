# Interpretacion SR
# Quiz 2

import streamlit as st

st.title('Quiz 1')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual es la principal diferencia entre correccion y mejoramiento?",
    ["La correccion se aplica primero", "El mejoramiento cambia los valores originales", "El mejoramiento requiere modelos"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual considera que puede ser la mejor definicion de histograma?",
    ["Representa la distribución de un conjunto de datos", "Muestra cómo se ha comportado una muestra basada en una variable numérica o cuantitativa", 
"Sirve para obtener una primera vista general de la distribución de la población"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
