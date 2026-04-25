# app.py
import streamlit as st
import numpy as np
import xarray as xr
import rioxarray as rxr
import plotly.express as px
import plotly.graph_objects as go

from skimage.feature import graycomatrix, graycoprops
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.util import img_as_ubyte

import pandas as pd

st.set_page_config(layout="wide")

st.title("🛰️ Textura de Imagenes")

# -----------------------------
# Upload raster
# -----------------------------
uploaded_file = st.file_uploader("Cargue una imagen (GeoTIFF)", type=["tif", "tiff"])

if uploaded_file:
    da = rxr.open_rasterio(uploaded_file, masked=True).squeeze()
    x,y = da.shape
    x, y = x//2, y//2
    
    col1, col2 = st.columns(2)
    
    with col1:  
        st.subheader("Imagen Original")
        fig = px.imshow(da.values, color_continuous_scale="gray")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Fraccion analizada")
        fig = px.imshow(da.values[x-50:x+50,y-50:y+50], color_continuous_scale="gray")
        st.plotly_chart(fig, use_container_width=True)

    # Normalize for texture methods
    img = da.values
    img = np.nan_to_num(img)

    # Convert to 8-bit
    img_norm = (img - img.min()) / (img.max() - img.min())
    img_ubyte = img_as_ubyte(img_norm)
    x,y = img_ubyte.shape
    x, y = x//2, y//2
    img_ubyte = img_ubyte[x-50:x+50,y-50:y+50]

    window_size = st.slider("Tamaño de ventana", 3, 15, 5, step=2)

    # -----------------------------
    # Texture functions
    # -----------------------------
    def GLCM_atribs(image, feature):
        grayscale = image
        x,y = image.shape
        PATCH_SIZE=3
        
        VAL = []
        for i in range(x-PATCH_SIZE+1):
            for j in range(y-PATCH_SIZE+1):
                patch = grayscale[i:i+PATCH_SIZE, j: j+PATCH_SIZE]
                glcm = graycomatrix(patch, distances=[1], angles = [0], levels=256, symmetric=True, normed= True)
                VAL.append(graycoprops(glcm, feature)[0,0])
        img = np.pad(np.resize(np.array(VAL), (int(np.sqrt(len(VAL))), int(np.sqrt(len(VAL))))), pad_width= 1, mode='edge')
        return img

    def compute_entropy(image, size):
        return entropy(image, disk(size))

    def compute_local_variance(image, size):
        mean = np.mean(image)
        return (image - mean) ** 2

    # -----------------------------
    # Comparison mode
    # -----------------------------
    st.subheader("🔍 Comparacion de metodos")

    methods_compare = st.multiselect(
        "Seleccione los metodos a comparar",
        ["GLCM Contraste", "GLCM Homogeneidad", "Entropia", "Varianza Local"]
    )

    results = {}

    for m in methods_compare:
        if m == "GLCM Contraste":
            results[m] = GLCM_atribs(img_ubyte, "contrast")

        elif m == "GLCM Homogeneidad":
            results[m] = GLCM_atribs(img_ubyte, "homogeneity")

        elif m == "Entropia":
            results[m] = compute_entropy(img_ubyte, window_size)

        elif m == "Varianza Local":
            results[m] = compute_local_variance(img_norm, window_size)

    if results:
        cols = st.columns(len(results))

        for i, (name, res) in enumerate(results.items()):
            with cols[i]:
                st.write(name)
                fig = px.imshow(res, color_continuous_scale="viridis")
                st.plotly_chart(fig, use_container_width=True)
                
                fig_hist = px.histogram(res.flatten(), nbins=50)
                fig_hist.update_layout(
                    xaxis_title="Valores",
                    yaxis_title="Frecuencia",
                    title="Histograma"
)
                st.plotly_chart(fig_hist, use_container_width=True)

        # Comparison statistics
        comp_stats = {
            name: [
                np.mean(res),
                np.std(res),
                np.min(res),
                np.max(res)
            ]
            for name, res in results.items()
        }

        df_comp = pd.DataFrame(
            comp_stats,
            index=["Media", "Desv.Est", "Min", "Max"]
        )

        st.dataframe(df_comp)
        
    # -----------------------------
    # User Comments on Comparison
    # -----------------------------
    st.subheader("📝 Analisis")

    if "comments" not in st.session_state:
        st.session_state.comments = []

    comment_text = st.text_area(
        "Escriba un analisis personal sobre su interpretacion de la comparacion:",
        placeholder="..."
    )

else:
    st.info("Escoja una imagen para empezar.")