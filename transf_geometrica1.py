import streamlit as st
import skimage as ski
from skimage import exposure, io
from skimage import transform
import numpy as np
import scipy.spatial.distance as dist
from skimage.color import rgb2gray

st.title('Correccion geometrica')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
img = io.imread(uploaded_file[0])
#uploaded_file2 = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"], key=2)
#img_final = io.imread(uploaded_file[1])

st.write(f"Dimensiones: ",img.shape)

col1, col2 = st.columns(2)
if uploaded_file is not None:	

	with col1:
		rotacion = st.number_input("Ingrese un valor de rotacion: (0.0-360.0)", value=0.0, placeholder="Ingrese un numero...")
		escalado = st.number_input("Ingrese un valor de escalado: (-0.9,1.9)", value=0.0, placeholder="Ingrese un numero...")

	with col2:
		traslacionX = st.number_input("Ingrese un valor de traslacion en el eje X: (-Inf, +Inf)", value=0.0, placeholder="Ingrese un numero...")
		traslacionY = st.number_input("Ingrese un valor de traslacion en el eje Y: (-Inf, +Inf)", value=0.0, placeholder="Ingrese un numero...")

rotacion = np.deg2rad(rotacion)
tform = transform.SimilarityTransform(scale=escalado, rotation= rotacion, translation=(traslacionX, traslacionY))
st.write("Parametros de la correccion geometrica: ",tform.params)

tf_img = ski.transform.warp(img, tform)
#data = 255 * tf_img # Now scale by 255
#img2 = data.astype(np.uint8)

#st.write(f"Dimensiones: ",img2.shape)
#st.write(f"Bit: ",img2.dtype)


col3, col4 = st.columns(2)
if uploaded_file is not None:	

	with col3:
		st.header("Imagen original:")
		st.image(img, caption='gato original', width=200)

	with col4:
		st.header("Imagen corregida:")
		st.image(tf_img, caption='gato_corregido (rotado, trasladado, escalado)', width=200)
