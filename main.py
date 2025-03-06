import streamlit as st
import numpy as np
from skimage.io import imread

st.title('Propiedades de una imagen digital')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png", "tif"])
col1, col2 = st.columns(2)

if uploaded_file is not None:
    image = imread(uploaded_file)

    with col1:
        st.header("Imagen")
        st.image(image, caption='Imagen', width=200)

    with col2:
        st.header("Propiedades")            
        st.write(f"Tipo de imagen: {type(image)}")
        st.write(f"Dimensiones de la imagen: {image.shape}")
        st.write(f"Cantidad de pixeles: {image.size}")
        st.write(f"Tipo de dato: {image.dtype}")
        st.write(f"Capas por pixel: {image.ndim}")
