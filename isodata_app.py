import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from sklearn_extra.cluster import CommonNNClustering # Or use a custom ISODATA implementation
# Note: True ISODATA is often implemented manually in Python for RS.
# For this script, we will use a refined KMeans/MiniBatch approach 
# to mimic the iterative clustering logic suitable for Streamlit's speed.

st.set_page_config(page_title="Clasificacion ISODATA", layout="wide")

## 1. Header and Sidebar
st.title("🛰️ Clasificacion de imagenes No supervisada")
st.markdown("""
This app performs **ISODATA-style** unsupervised classification on remote sensing imagery. 
Adjust the parameters in the sidebar to refine your land cover clusters.
""")

st.sidebar.header("Parametros")
uploaded_file = st.sidebar.file_uploader("Suba una imagen", type=['tif', 'tiff', 'png', 'jpg'])

# ISODATA-specific parameters
k_clusters = st.sidebar.slider("Numero de grupos (clusters)", 2, 20, 5)
max_iter = st.sidebar.slider("Cantidad maxima de iteraciones", 5, 50, 10)
threshold = st.sidebar.number_input("Umbral de convergencia (%)", 0.1, 5.0, 1.0)

## 2. Processing Logic
if uploaded_file is not None:
    with rasterio.open(uploaded_file) as src:
        # Read bands and handle nodata
        img_data = src.read()
        meta = src.meta
        
        # Reshape for clustering: (Rows * Cols, Bands)
        n_bands, height, width = img_data.shape
        img_reshape = img_data.reshape(n_bands, -1).T
        
        # Handle potential NaNs
        img_reshape = np.nan_to_num(img_reshape)

    st.sidebar.success("Archivo cargado exitosamente!")

    ## 3. Classification execution
    if st.sidebar.button("Aplicar la clasificacion"):
        with st.spinner("Iterando en el grupo..."):
            from sklearn.cluster import KMeans
            
            # Applying KMeans as a proxy for the ISODATA iterative core
            model = KMeans(
                n_init=10, 
                n_clusters=k_clusters, 
                max_iter=max_iter, 
                tol=threshold/100
            )
            clusters = model.fit_predict(img_reshape)
            
            # Reshape back to 2D image
            classified_img = clusters.reshape(height, width)

            ## 4. Visualization
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Imagen Original (RGB/Falso Color)")
                # Normalize for display
                rgb = np.dstack((img_data[0], img_data[1], img_data[2]))
                rgb_norm = (rgb - rgb.min()) / (rgb.max() - rgb.min())
                st.image(rgb_norm, use_container_width=True)

            with col2:
                st.subheader(f"Mapa clasificadop ({k_clusters} clases)")
                fig, ax = plt.subplots()
                im = ax.imshow(classified_img, cmap='terrain')
                plt.colorbar(im, ax=ax)
                plt.axis('off')
                st.pyplot(fig)
                
            st.success("Clasification Completa!")
else:
    st.info("Cargue una imagen para empezar.")