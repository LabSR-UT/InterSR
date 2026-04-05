import streamlit as st
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("🌿 Indices de Vegetacion")

# --- User Info Section ---
st.sidebar.header("Informacion del usuario:")

user_name = st.sidebar.text_input("Nombre")
user_response = st.sidebar.text_area("Que valor le asigna cada indice a la clase bosque?")

# --- Sidebar ---
st.sidebar.header("Options")

index_option = st.sidebar.selectbox(
    "Seleccione un indice",
    ["NDVI", "GNDVI", "SAVI"]
)

uploaded_file = st.file_uploader("Cargar una imagen multiespectral (GeoTIFF preferred)", type=["tif", "tiff", "png"])

# --- Functions ---
def calculate_index(index_name, bands):
    # Expecting bands as dict: {"red":..., "green":..., "nir":...}
    red = bands.get("red")
    green = bands.get("green")
    nir = bands.get("nir")

    if index_name == "NDVI":
        return (nir - red) / (nir + red + 1e-10)

    elif index_name == "GNDVI":
        return (nir - green) / (nir + green + 1e-10)

    elif index_name == "SAVI":
        L = 0.5
        return ((nir - red) / (nir + red + L)) * (1 + L)

    else:
        return None


def get_stats(array):
    flat = array.flatten()
    flat = flat[~np.isnan(flat)]

    stats = {
        "Media": np.mean(flat),
        "Mediana": np.median(flat),
        "Minimo": np.min(flat),
        "Maximo": np.max(flat),
        "Desv. Est.": np.std(flat)
    }

    return pd.DataFrame(stats.items(), columns=["Metrica", "Valor"])


# --- Main Logic ---
if uploaded_file:
    with rasterio.open(uploaded_file) as src:
        st.write("### Informacion de la imagen")
        st.write(f"Bandas: {src.count}")
        st.write(f"Dimensiones (cols, filas): {src.width} x {src.height}")

        # Basic assumption: band order
        # You may adjust depending on your dataset
        bands = {}

        if src.count >= 3:
            bands["red"] = src.read(4).astype(float)
            bands["green"] = src.read(3).astype(float)
            bands["nir"] = src.read(8).astype(float)
        else:
            st.error("La imagen debe tener  bandas (R, G, NIR)")
            st.stop()

        index = calculate_index(index_option, bands)

        col1, col2 = st.columns(2)

        # --- Display Index Map ---
        with col1:
            st.subheader(f"{index_option}")
            fig, ax = plt.subplots()
            im = ax.imshow(index, cmap="RdYlGn")
            plt.colorbar(im, ax=ax)
            ax.axis("off")
            st.pyplot(fig)

        # --- Histogram ---
        with col2:
            st.subheader("Histograma")
            fig2, ax2 = plt.subplots()
            ax2.hist(index.flatten(), bins=50)
            ax2.set_title("Distribucion")
            st.pyplot(fig2)

        # --- Statistics ---
        st.subheader("Estadisticas descriptivas")
        stats_df = get_stats(index)
        st.dataframe(stats_df)
		
		# --- Display User Info ---
        if user_name or user_response:
            st.markdown("### 👤 Contexto")
            st.write(f"**Nombre:** {user_name if user_name else 'Sin respuesta'}")
            st.write(f"**Respuesta:** {user_response if user_response else 'Sin respuesta'}")

else:
    st.info("Cargue una imagen para empezar.")