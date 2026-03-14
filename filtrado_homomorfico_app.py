import streamlit as st
import cv2
import numpy as np

def homomorphic_filter(image, low_gain, high_gain, cutoff, slope=1.0):
    # Convert image to floating point and take log to separate illumination/reflectance
    img_log = np.log1p(np.array(image, dtype="float") / 255.0)
    
    # Frequency domain transformation (DFT)
    rows, cols = image.shape
    img_fft = np.fft.fft2(img_log)
    img_fft_shift = np.fft.fftshift(img_fft)
    
    # Create the filter mask
    u, v = np.meshgrid(np.arange(cols), np.arange(rows))
    d_squared = (u - cols/2)**2 + (v - rows/2)**2
    
    # The Transfer Function
    rh, rl = high_gain, low_gain
    d0_squared = cutoff**2
    h_mask = (rh - rl) * (1 - np.exp(-slope * (d_squared / d0_squared))) + rl
    
    # Apply filter and inverse DFT
    result_filter = img_fft_shift * h_mask
    result_interm = np.real(np.fft.ifft2(np.fft.ifftshift(result_filter)))
    
    # Exponentiate to return to spatial domain
    result = np.expm1(result_interm)
    return np.clip(result * 255, 0, 255).astype(np.uint8)

# --- Streamlit UI ---
st.title("✨ Filtrado Homomorfico")
st.write("Mejorar la visualizacion de la imagen balanceando la iluminacion y reflectancia.")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load image
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    col1, col2 = st.columns(2)
    
    with st.sidebar:
        st.header("Parametros")
        # 'a' and 'b' are often represented as Low Gain (rl) and High Gain (rh)
        rl = st.slider("Ganancia de Baja Frecuencia (rl / a)", 0.0, 1.0, 0.5)
        rh = st.slider("Ganancia de Alta Frecuencia  (rh / b)", 1.0, 3.0, 2.0)
        cutoff = st.slider("Frecuencia de corte (D0)", 1, 100, 30)
        slope = st.slider("Pendiente (c)", 0.1, 2.0, 1.0)

    # Process
    filtered_image = homomorphic_filter(image, rl, rh, cutoff, slope)
    
    with col1:
        st.subheader("Imagen Original (gris)")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Imagen Resultante")
        st.image(filtered_image, use_container_width=True)