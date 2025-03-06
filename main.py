import streamlit as st
import numpy as np

from skimage.io import imread

st.title('Propiedades de una imagen digital')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    #image = cv2.imread(uploaded_file)
    image = imread(uploaded_file)    
 
    st.image(image, caption='Imagen', width=400)
    st.write(f"Tipo de imagen: {type(image)}")
    st.write(f"Dimensiones de la imagen: {image.shape}")
    st.write(f"Cantidad de pixeles: {image.size}")
    st.write(f"Tipo de dato: {image.dtype}")
    st.write(f"Capas por pixel: {image.ndim}")

st.write("Nota: usar imagenes en formato jpg")
