import streamlit as st
from PIL import Image
import PIL.ExifTags

st.title('Propiedades de una imagen')

uploaded_file = st.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png", "ppm"])

if uploaded_file is not None:
	img = Image.open(uploaded_file)

	exif = {
		PIL.ExifTags.TAGS[k]: v
		for k, v in img._getexif().items()
		if k in PIL.ExifTags.TAGS
	  }


#value = 105.0/image.shape[1]
#formatted_string = "{:.2f}".format(value)
#float_value = float(formatted_string)

col1, col2 = st.columns(2)

if uploaded_file is not None:
    with col1:
        st.header("Imagen")
        st.image(img, caption='imagen', width=200)
    with col2:
        try:    
            st.header("Propiedades Imagen:")
            st.write(f"Fecha de captura: ", exif['DateTime'][-20:-8])
            st.write(f"Hora de captura: ", exif['DateTime'][-8:])
            st.write(f"Ancho: ", exif['ImageWidth'])
            st.write(f"Alto: ", exif['ImageLength'])
            st.write(f"Bits por pixel: ", exif['BitsPerSample'])
        except KeyError:
            st.write("Información no disponible")
		
col3, col4 = st.columns(2)		
if uploaded_file is not None:
    with col3:
        try:
            st.header("Propiedades Camara:")	
            st.write(f"Marca: ", exif['Make'])
            st.write(f"Modelo: ", exif['Model'])
        except KeyError:
            st.write("Información no disponible")
    with col4:
        try:
            st.header("Configuracion Visualizacion:")
            st.write(f"Contraste: ",exif['Contrast'])
            st.write(f"Saturacion: ", exif['Saturation'])
            st.write(f"Sharpness: ", exif['Sharpness'])		
        except KeyError:
            st.write("Información no disponible")
