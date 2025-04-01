# Imagenes SR
# Quiz 1

import streamlit as st

st.title('Quiz 3')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cuales es la principal diferencia entre patron y frima espectral?",
    ["Numero de parametros", "numero de objetos", "numero de factores"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual es la diferencia entre ventana y persiana?",
    ["Cantidad de radiacion que dejan pasar", "Presencia de moleculas en la atmosfera", "Ancho del rango de longitud de onda"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
