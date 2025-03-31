import streamlit as st
from skimage import io
import numpy as np
from skimage import color

st.title('Modelos de Color')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png", "jfif"])
img = io.imread(uploaded_file)

option = st.selectbox(
    "Tipo de conversion",
    ("RGB -> HSV"),
)

if option=="RGB -> HSV":
	img2 = color.rgb2hsv(img) 

	
col1, col2 = st.columns(2)
if uploaded_file is not None:	

	with col1:
		st.header("Imagen original:")
		st.image(img, width=200)

	with col2:
		st.header("Modelo: ")
		st.image(img2, width=200)
		
col3, col4, col5 = st.columns(3)
if uploaded_file is not None:	

	with col3:
		if option=="RGB -> HSV":
			st.header("Hue")
			st.image(img2[:,:,0], width=200)
			st.write("Min: {:.2f}".format(img2[:,:,0].min()), "Max: {:.2f}".format(img2[:,:,0].max()))

	with col4:
		if option=="RGB -> HSV":
			st.header("Saturacion")
			st.image(img2[:,:,1], width=200)
			st.write("Min: {:.2f}".format(img2[:,:,1].min()), "Max: {:.2f}".format(img2[:,:,1].max()))
	
	with col5:
		if option=="RGB -> HSV":
			st.header("Valor")
			st.image(img2[:,:,2], width=200)
			st.write("Min: {:.2f}".format(img2[:,:,2].min()), "Max: {:.2f}".format(img2[:,:,2].max()))

