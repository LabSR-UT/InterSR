import streamlit as st
import numpy as np
import rasterio
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from PIL import Image

st.title("Transformada Karhunen-Loève (KLT)")

# Upload file
uploaded_file = st.file_uploader("Cargue una imagen multiespectral (GeoTIFF o RGB)", type=["tif", "tiff", "png", "jpg"])

def load_image(file):
    try:
        with rasterio.open(file) as src:
            img = src.read()  # shape: (bands, rows, cols)
            img = np.transpose(img, (1, 2, 0))  # -> (rows, cols, bands)
    except:
        img = np.array(Image.open(file))
        if img.ndim == 2:
            img = np.expand_dims(img, axis=-1)
    return img

def normalize_for_display(img):
    img = img.astype(np.float32)
    min_val = np.min(img)
    max_val = np.max(img)

    if max_val - min_val == 0:
        return np.zeros_like(img)

    img = (img - min_val) / (max_val - min_val)
    return img

def percentile_stretch(img, p_low=2, p_high=98):
    low = np.percentile(img, p_low)
    high = np.percentile(img, p_high)

    img = np.clip(img, low, high)
    return (img - low) / (high - low)

def despliegue(display_mode, img, bands, title, k):
    if display_mode == "RGB":
        if bands >= 3:
            r = st.selectbox("Canal R (Red)", list(range(bands)), index=2, key=k+1)
            g = st.selectbox("Canal G (Green)", list(range(bands)), index=1, key=k+2)
            b = st.selectbox("Canal B (Blue)", list(range(bands)), index=0, key=k+3)

            rgb = np.stack([img[:, :, r], img[:, :, g], img[:, :, b]], axis=-1)
            rgb = normalize_for_display(rgb)

            st.image(rgb, caption=f"{title} RGB")
        else:
            st.warning("La imagen seleccionada no tiene suficientes bandas para mostrar la RGB.")

    else:
        band_idx = st.slider("Seleccione la banda", 0, bands - 1, 0, key=k+4)
        band_img = img[:, :, band_idx]
        band_img = normalize_for_display(band_img)

        st.image(band_img, caption=f"{title} Banda {band_idx}")

if uploaded_file is not None:
    img = load_image(uploaded_file)

    # Reshape for PCA
    rows, cols, bands = img.shape
    reshaped = img.reshape(-1, bands)

    # Normalize
    reshaped = reshaped.astype(np.float32)
    reshaped -= np.mean(reshaped, axis=0)

    # Apply PCA (KLT)
    pca = PCA()
    transformed = pca.fit_transform(reshaped)
    
    st.subheader("Opciones para desplegar la imagen")

    display_mode = st.radio("Escoja el modo", ["RGB", "Banda individual"],key=0)

    despliegue(display_mode, img, bands,title='Original', k=0)

    st.subheader("Varianza explicada")
    st.write(pca.explained_variance_ratio_)

    # Reshape back to image
    components = transformed.reshape(rows, cols, bands)

    st.subheader("Componentes KLT")

    component_idx = st.slider("Seleccione el componente", 0, bands - 1, 0)
    comp = percentile_stretch(components[:, :, component_idx])

    st.image(comp, caption=f"Componente KLT {component_idx}")

    # Optional reconstruction
    st.subheader("Reconstruccion usando los componentes seleccionados")

    k = st.slider("Numero de componentes", 1, bands, min(3, bands))

    reduced = transformed[:, :k]

    # Pad with zeros to match original number of components
    padded = np.zeros_like(transformed)
    padded[:, :k] = reduced

    reconstructed = pca.inverse_transform(padded)
    reconstructed = reconstructed.reshape(rows, cols, bands)

    reconstructed = percentile_stretch(reconstructed)

    st.subheader("Opciones para desplegar la imagen")

    display_mode = st.radio("Escoja el modo", ["RGB", "Banda individual"],key=5)

    despliegue(display_mode, reconstructed, bands,title='Reconstruida', k=5)


