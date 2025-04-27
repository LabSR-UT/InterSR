# Interpretacion SR
# Quiz 4

import streamlit as st

st.title('Quiz 4')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual de estos no es un indice de vegetacion?",
    ["NDBI", "NDMI", "NDPI", "NDVI"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual de las siguientes aplicaciones no usa indices de vegetacion?",
    ["Deteccion de deslizamientos", "Monitoreo de la vegetacion", "Deteccion de incendios","Evaluacion del estres hidrico"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
