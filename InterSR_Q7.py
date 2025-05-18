# Interpretacion SR
# Quiz 6

import streamlit as st

st.title('Quiz 7')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual es la principal diferencia entre el metodo supervisado vs no supervisado:",
    ["Numero de clases debe indicarse", "Uso de conjunto de entrenamiento", "Numero de iteraciones", "Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Que metrica es la mas utilizada?",
    ["AUC", "Exactitud", "Recall", "Indice Kappa","Puntaje F1","Precision", "Ninguna"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
