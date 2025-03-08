import streamlit as st
import numpy as np
from skimage.io import imread

st.title('Valores de pixeles de una imagen')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"])
image = imread(uploaded_file)
st.subheader("Imagen original")
st.image(image, caption='imagen completa', width=200)
st.write(f"Dimensiones de la imagen: {image.shape}")

values = st.slider("Select a range of values", 0, 10, (2, 4))
st.write("Values:", values)

x1 = image.shape[0]//2 - values[0]
x2 = image.shape[0]//2 + values[1]
y1 = image.shape[1]//2 - values[0]
y2 = image.shape[1]//2 + values[1]

st.write("Las coordenadas son: (",x1,",",x2,":",y1,",",y2,")")

col1, col2 = st.columns(2)

if uploaded_file is not None:	
	frac = image[int(x1):int(x2), int(y1):int(y2),0]

	with col1:
		st.header("Area seleccionada")
		st.image(frac, caption='area', width=200)

	with col2:
		st.write(frac)
        
