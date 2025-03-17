import streamlit as st
import skimage as ski
from skimage import exposure, io
from skimage import transform
import numpy as np
from skimage.color import rgb2gray
import cv2

st.title('Mejoramiento')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"])
img = io.imread(uploaded_file)

option = st.selectbox(
    "Tipo de mejoramiento",
    ("Contraste", "Ecualizacion", "Paso Alto", "Paso Bajo", "Color"),
)

if option=="Contraste":
	brightness = st.number_input("Ingrese valor de brillo: (0, +Inf)", value=10.0, placeholder="Ingrese un numero...")
	# Adjusts the contrast by scaling the pixel values by 2.3 
	contrast = st.number_input("Ingrese valor de contraste: (0, +Inf)", value=2.3, placeholder="Ingrese un numero...")
	image2 = cv2.addWeighted(img, contrast, np.zeros(img.shape, img.dtype), 0, brightness) 

if option=="Paso Alto":
	# Create the sharpening kernel 
	kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
	  
	# Sharpen the image 
	image2 = cv2.filter2D(img, -1, kernel) 

if option=="Paso Bajo":
	valor = st.number_input("Ingrese tamaño del filtro impar: (3, +Inf)", value=11, placeholder="Ingrese un numero...")
	# Sharpen the image using the Laplacian operator 
	image2 = cv2.medianBlur(img, valor) 
	
if option=="Color":
	# Convert the image from BGR to HSV color space 
	img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV) 
	  
	# Adjust the hue, saturation, and value of the image 
	# Adjusts the hue by multiplying it by 0.7 
	img[:, :, 0] = img[:, :, 0] * 0.7
	# Adjusts the saturation by multiplying it by 1.5 
	img[:, :, 1] = img[:, :, 1] * 1.5
	# Adjusts the value by multiplying it by 0.5 
	img[:, :, 2] = img[:, :, 2] * 0.5
	  
	# Convert the image back to BGR color space 
	img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR) 
	image2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

if option=="Ecualizacion":	
	# Convert the image to grayscale 
	gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
	  
	# Equalize the histogram 
	image2 = cv2.equalizeHist(gray_image) 
	
	
col1, col2 = st.columns(2)
if uploaded_file is not None:	

	with col1:
		st.header("Imagen original:")
		st.image(img, caption='huella', width=200)

	with col2:
		st.header("Imagen mejorada: ")
		st.image(image2, caption='huella', width=200)

