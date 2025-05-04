# Interpretacion SR
# Quiz 4

import streamlit as st

st.title('Quiz 4')
st.subheader('Cuales son los componentes de la transformada KT:')

valor1 = st.radio("Cual de estos no es un indice de vegetacion?",
    ["Brillo, verdosidad, humedad", "Brillo, amarillez, humedad", "Brillo, verdosidad, ninguna", "Brillo, ninguna, humedad"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Que otros nombres recibe la transformada KL",
    ["Karhunen-Love", "PCA", "Hotelling","Todas"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
