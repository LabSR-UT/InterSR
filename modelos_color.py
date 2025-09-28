import streamlit as st
from skimage import io
import numpy as np
from skimage import color

st.title('Modelos de Color')

img = None # Initialize to None

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png", "jfif"])
	

if uploaded_file is not None:	

    img = io.imread(uploaded_file)
    option = st.selectbox("Tipo de conversion",("RGB -> HSV","RGB -> Lab","RGB -> XYZ"))
    option2 = int((st.selectbox("Canal",("0","1","2"))))

    if option=="RGB -> HSV":
	    img2 = color.rgb2hsv(img) 
    if option=="RGB -> Lab":
        img2 = color.rgb2lab(img) 
    if option=="RGB -> XYZ":
        img2 = color.rgb2lab(img) 
		
		
		
    col1, col2 = st.columns(2)
    with col1:
        st.header("Modelo RGB:")
        st.image(img, width=200)
    with col2:
        st.header("Modelo {}".format(option[-3:]))
        if option=="RGB -> HSV":
            st.image(img2[:,:,option2], width=200, clamp=True)
            st.write("Canal {} Min: {:.2f}".format(str(option2),img2[:,:,option2].min()), "Max: {:.2f}".format(img2[:,:,option2].max()))
        if option=="RGB -> Lab":            
            st.image(img2[:,:,option2], width=200, clamp=True)
            st.write("Canal {} Min: {:.2f}".format(str(option2),img2[:,:,option2].min()), "Max: {:.2f}".format(img2[:,:,option2].max()))
        if option=="RGB -> XYZ":
            st.image(img2[:,:,option2], width=200, clamp=True)
            st.write("Canal {} Min: {:.2f}".format(str(option2),img2[:,:,option2].min()), "Max: {:.2f}".format(img2[:,:,option2].max()))
		
    col3 = st.columns(1)
    st.title("Actividad")

    # 1. Ask the question using st.text_area
    # The result (user's answer) is stored in the 'user_answer' variable
    user_answer = st.text_area(
        label="**Consulta:** Comparar los valores obtenidos para canal de luminosidad entre los modelos de color usados",
        height=200,  # Sets the height of the input box
        placeholder="Escriba su respuesta aca..."
    )


