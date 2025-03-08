import streamlit as st
import numpy as np
from skimage.io import imread

st.title('Resoluciones de una imagen')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"])
image = imread(uploaded_file)

value1 = st.number_input("Ingrese la distancia: ", value=None, placeholder="Escriba un numero...")
value2 = st.number_input("Ingrese numero de pixeles: ", value=None, placeholder="Escriba un numero...")

#value = 105.0/image.shape[1]
res = value1 / value2
formatted_string = "{:.2f}".format(res)
float_value = float(formatted_string)

col1, col2 = st.columns(2)

if uploaded_file is not None:	

	with col1:
		st.header("Imagen")
		st.image(image, caption='imagen', width=200)

	with col2:
		st.header("Resoluciones")
		st.write(f"Resolucion espacial: ",float_value," metros/pixel")
		st.write(f"Resolucion temporal: {1}")
		st.write(f"Resolucion espectral: {image.shape[2]} capas")
		st.write(f"Resolucion radiometrica: {image.dtype}")
