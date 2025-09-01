import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Set the page configuration with a wide layout
st.set_page_config(layout="wide", page_title="Procesamiento basico de Imagenes")

st.title("🛰️ Procesamiento interactivo de imagenes de Sensores Remotos")
st.markdown("Cargue una imagen multiespectral o RGB para aplicarle varias tecnicas basicas de procesamiento.")

# Sidebar for controls
with st.sidebar:
    st.header("Opciones de procesamiento")
    
    # File uploader
    uploaded_file = st.file_uploader("Escoja una imagen de sensores remotos", type=["jpg", "jpeg", "png", "tif", "tiff"])
    
    # Select processing mode
    st.markdown("---")
    processing_mode = st.radio(
        "Seleccione una tecnica de procesamiento:",
        ("Imagen original", "Escala de grises", "Canales de color", "Indice NDVI (requiere banda IR)", "Deteccion de bordes", "Ecualizacion de Histograma")
    )
    
    # NDVUI info and input fields
    if processing_mode == "Indice NDVI (requiere banda IR)":
        st.markdown("---")
        st.subheader("Indice de vegetacion de diferencia normalizada (NDVI)")
        st.markdown(r"El NDVI es un índice comúnmente utilizado para evaluar la salud de la vegetación. Se calcula utilizando las bandas de infrarrojo cercano (NIR) y rojo de una imagen multiespectral. Su fórmula es: $$NDVI = \frac{NIR - Red}{NIR + Red}$$")
        st.warning("Esta función requiere una imagen multiespectral con banda de infrarrojo cercano. La aplicación asumirá que el rojo es el primer canal (0) y el infrarrojo cercano es el segundo canal (1) para una imagen de dos canales, o usará los canales 2 y 3 para una imagen de cuatro canales (p. ej., RGBN)..")
        
    st.markdown("---")
    st.info("La aplicación requiere reiniciarse para cargar nuevos archivos o seleccionar el modo de procesamiento.")


def convert_image_to_numpy_array(uploaded_file):
    """
    Reads an uploaded file and converts it to a NumPy array.
    Handles different file types and potential color channels.
    """
    try:
        # Use Pillow to open the image file
        image = Image.open(uploaded_file)
        
        # Convert to RGBA to ensure a consistent number of channels
        image = image.convert("RGBA")
        
        # Convert the Pillow image to a NumPy array
        np_image = np.array(image)
        return np_image
    except Exception as e:
        st.error(f"Error al leer la imagen: {e}")
        return None

def apply_grayscale(image_np):
    """Converts a NumPy image array to grayscale using OpenCV."""
    # Ensure the input is not a single-channel image
    if len(image_np.shape) < 3 or image_np.shape[2] == 1:
        st.warning("La imagen ya está en escala de grises.")
        return image_np
    
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGBA2GRAY)
    return gray_image

def apply_color_channels(image_np):
    """Splits an RGB or RGBA image into its component channels."""
    if len(image_np.shape) < 3 or image_np.shape[2] < 3:
        st.warning("La imagen no tiene suficientes canales de color para dividir.")
        return None
    
    # Separate the channels (R, G, B)
    channels = cv2.split(image_np)
    
    return channels

def apply_ndvi(image_np):
    """
    Calculates the NDVI from a multispectral image.
    Assumes a 4-channel image (RGBN) or a 2-channel image (Red, NIR).
    """
    if len(image_np.shape) < 3:
        st.error("La imagen de entrada debe tener al menos dos canales para el cálculo de NDVI.")
        return None
    
    # Assume channels based on image shape.
    # Remote sensing images can have different band arrangements.
    if image_np.shape[2] >= 4:
        # Assumes a 4-channel image (e.g., RGB and a NIR band)
        red_band = image_np[:, :, 2].astype(float) # Red is often channel 2
        nir_band = image_np[:, :, 3].astype(float) # NIR is often channel 3
        st.write("Usando los canales 3 (Rojo) y 4 (NIR) para el calculo del indice NDVI.")
    elif image_np.shape[2] == 2:
        # Assumes a 2-channel image with Red and NIR bands
        red_band = image_np[:, :, 0].astype(float)
        nir_band = image_np[:, :, 1].astype(float)
        st.write("Uso de los canales 0 (rojo) y 1 (NIR) para el cálculo del NDVI.")
    else:
        st.error("El NDVI requiere al menos una banda roja y una banda infrarroja cercana. Sube una imagen adecuada..")
        return None
        
    # Handle division by zero
    numerator = np.subtract(nir_band, red_band)
    denominator = np.add(nir_band, red_band)
    
    # Using np.errstate to handle invalid values in a safe way
    with np.errstate(invalid='ignore'):
        ndvi = np.divide(numerator, denominator)
        # Handle nan values (where denominator was zero)
        ndvi[denominator == 0] = 0.0

    # Map the NDVI values from -1 to 1 to a grayscale range 0-255 for visualization
    ndvi_scaled = ((ndvi + 1) * 127.5).astype(np.uint8)
    
    return ndvi_scaled

def apply_edge_detection(image_np):
    """
    Applies Canny edge detection to the image.
    Requires a grayscale image as input.
    """
    # Convert to grayscale first if it's not already
    gray_image = apply_grayscale(image_np)
    
    if gray_image is None:
        return None

    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, 100, 200)
    
    return edges

def apply_histogram_equalization(image_np):
    """
    Applies histogram equalization to improve image contrast.
    Works best on grayscale images.
    """
    # Convert to grayscale
    gray_image = apply_grayscale(image_np)
    if gray_image is None:
        return None
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized_image = clahe.apply(gray_image)
    
    return equalized_image


# Main application logic
if uploaded_file is not None:
    # Convert the uploaded file to a NumPy array
    image_np = convert_image_to_numpy_array(uploaded_file)
    
    if image_np is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Imagen original")
            st.image(uploaded_file, caption="Imagen original", use_column_width=True)
            
        with col2:
            st.header(f"Imagen procesada")
            
            processed_image = None
            if processing_mode == "Imagen original":
                st.image(image_np, caption="Imagen original", use_column_width=True)
            
            elif processing_mode == "Escala de grises":
                processed_image = apply_grayscale(image_np)
                st.image(processed_image, caption="Imagen en escala de grises", use_column_width=True)
                
            elif processing_mode == "Canales de color":
                channels = apply_color_channels(image_np)
                if channels:
                    col_r, col_g, col_b = st.columns(3)
                    with col_r: 
                        st.subheader("Canal Red")
                        st.image(channels[0], caption="Rojo", use_column_width=True)
                    with col_g:
                        st.subheader("Canal Green")
                        st.image(channels[1], caption="Verde", use_column_width=True)
                    with col_b:
                        st.subheader("Canal Blue")
                        st.image(channels[2], caption="Azul", use_column_width=True)
                        
            elif processing_mode == "Indice NDVI (requiere banda IR)":
                processed_image = apply_ndvi(image_np)
                if processed_image is not None:
                    st.image(processed_image, caption="Imagen NDVI (Visualizacion)", use_column_width=True)
                    st.markdown(
                        """
                        El resultado del NDVI es una matriz de punto flotante con valores de -1 a 1.
                        Esta imagen es una visualización en escala de grises donde la vegetación se ve más brillante.
                        """
                    )
                    
            elif processing_mode == "Deteccion de bordes":
                processed_image = apply_edge_detection(image_np)
                if processed_image is not None:
                    st.image(processed_image, caption="Imagen con deteccion de bordes", use_column_width=True)
                    
            elif processing_mode == "Ecualizacion de Histograma":
                processed_image = apply_histogram_equalization(image_np)
                if processed_image is not None:
                    st.image(processed_image, caption="Imagen ecualizada", use_column_width=True)

else:
    st.info("Cargue una imagen para empezar.")
    
# Footer
st.markdown("---")
st.markdown("Procesamiento usando Streamlit, Pillow, NumPy, and OpenCV.")	
		
