# Interpretacion SR
# Quiz 6

import streamlit as st

st.title('Quiz 6')
st.subheader('Cual es el objetivo de la aplicacion CTrees:')

valor1 = st.radio("Cual de estos no es un indice de vegetacion?",
    ["Sirve para inventariar el volumen de madera en cada arbol y bosque del planeta", "Sirve para cuantificar la cantidad de arboles del planeta", "Sirve para rastrear el carbono almacenado por cada arbol y bosque del planeta", "Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Que aplicacion no pertenece a la iniciativa GenomeEarth?",
    ["Global Plastics", "WindMap", "TheMargin", "CTrees","Global Energy","Groundwater Recharge Assesment", "Ninguna"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
