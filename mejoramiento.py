import streamlit as st
import skimage as ski
from skimage import exposure, io
from skimage import transform
import numpy as np
from skimage.color import rgb2gray
from skimage.filters import gaussian, unsharp_mask

st.title('Mejoramiento')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"])
img = io.imread(uploaded_file)	

option = st.selectbox(
	"Tipo de mejoramiento",
	("Contraste", "Ecualizacion", "Ecualizacion adaptativa", "Suavizado", "Refinado"),
)

if option=="Contraste":
	image2 = exposure.rescale_intensity(img)

if option=="Suavizado":	
    image2 = gaussian(img, sigma=5)

if option=="Refinado":
	image2 = unsharp_mask(img, radius=10, amount=1)
	
if option=="Ecualizacion adaptativa":
	valor = st.number_input("Ingrese el limite de corte: (0.0,1.0)", value=0.33, placeholder="Ingrese un numero...")
	gray_image = rgb2gray(img)
	image2 = exposure.equalize_adapthist(img, clip_limit=valor)	

if option=="Ecualizacion":	
    gray_image = rgb2gray(img)
    image2 = exposure.equalize_hist(gray_image)
		
if uploaded_file is not None:
    col1, col2 = st.columns(2)	
    with col1:
        st.header("Imagen original:")
        st.image(img, caption='1', width=200)
    with col2:
        st.header("Imagen mejorada: ")
        st.image(image2, caption='2', width=200)

user_feedback = st.text_area("Describa su eleccion:")
if user_feedback:
    st.write(f"Comentario: {user_feedback}")

