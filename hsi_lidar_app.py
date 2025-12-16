import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- Configuration and Setup ---

# Set the page configuration
st.set_page_config(
    page_title="Explorador de datos HSI y LiDAR",
    layout="wide",
    initial_sidebar_state="expanded"
)

def simulate_hsi_data(rows=50, cols=50, bands=100):
    """Simulates a simple Hyperspectral Image cube."""
    # Create a dummy HSI cube with some spatial pattern
    hsi_data = np.random.rand(rows, cols, bands) * 1000
    # Add a simple gradient to make it look less random
    for i in range(rows):
        for j in range(cols):
            hsi_data[i, j, :] = hsi_data[i, j, :] * (1 + (i+j)/(rows+cols))
    return hsi_data.astype(np.float32)

def simulate_lidar_data(rows=50, cols=50):
    """Simulates a simple 2D LiDAR Elevation Map (Digital Surface Model - DSM)."""
    # Create a dummy DSM with a peak in the center
    x = np.linspace(-2, 2, rows)
    y = np.linspace(-2, 2, cols)
    X, Y = np.meshgrid(x, y)
    # Z is elevation: a mountain-like structure
    Z = 100 * np.exp(-(X**2 + Y**2) / 1.5) + np.random.rand(rows, cols) * 5
    return Z.astype(np.float32)

# Load/Simulate Data
@st.cache_data # Cache the data loading/simulation for performance
def load_data():
    """Load and return simulated HSI and LiDAR data."""
    hsi = simulate_hsi_data()
    lidar = simulate_lidar_data()
    # Create a wavelength list for the HSI
    wavelengths = np.linspace(400, 2500, hsi.shape[2]) # 400nm to 2500nm
    return hsi, lidar, wavelengths

HSI_DATA, LIDAR_DATA, WAVELENGTHS = load_data()


# --- Main App Functions ---

def display_hsi_dashboard():
    """Creates the HSI visualization and interaction section."""
    st.header("🛰️ Análisis de imágenes hiperespectrales (HSI)")

    # Use a three-band composite (e.g., RGB) for visual display
    # We'll use band indices 20, 40, and 60 as R, G, B for a simulated "False Color"
    R_band, G_band, B_band = 20, 40, 60
    hsi_composite = HSI_DATA[:, :, [R_band, G_band, B_band]]
    # Normalize the composite for display
    composite_normalized = (hsi_composite - hsi_composite.min()) / (hsi_composite.max() - hsi_composite.min())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagen compuesta en color")
        # Display the image
        st.image(composite_normalized, caption=f"R: Banda {R_band}, G: Banda {G_band}, B: Banda {B_band}",
                 use_column_width=True)

    with col2:
        st.subheader("Selector de perfil espectral de píxeles")
        # Interactive sliders for selecting a pixel
        max_row, max_col, _ = HSI_DATA.shape
        row = st.slider("Seleccionar fila de píxeles (Y)", 0, max_row - 1, int(max_row / 2))
        col = st.slider("Seleccionar columna de píxeles (X)", 0, max_col - 1, int(max_col / 2))

        # Extract the spectral curve for the selected pixel
        spectral_curve = HSI_DATA[row, col, :]

        # Plot the spectral curve
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(WAVELENGTHS, spectral_curve, label=f"Pixel ({row}, {col})", color='green')
        ax.set_title("Perfil de reflectancia espectral")
        ax.set_xlabel("Longitud de onda (nm)")
        ax.set_ylabel("Número digital (DN) / Reflectancia")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        st.pyplot(fig) # Display the plot in Streamlit

    # Optional: Display HSI Metadata
    st.markdown("---")
    st.subheader("Descripcion")
    user_name = st.text_input(
    "Interprete la figura: ",
    placeholder="ej. dimensiones, valor mínimo y maximo en la coordenada (25,25)")



def display_lidar_dashboard():
    """Creates the LiDAR visualization and interaction section."""
    st.header("🌲 Análisis de datos LiDAR (DSM)")

     # Plot the LiDAR DSM as a heat map
    fig, ax = plt.subplots(figsize=(10, 8))
    # Use imshow for 2D visualization of the elevation data
    cax = ax.imshow(LIDAR_DATA, cmap='viridis', origin='lower')
    fig.colorbar(cax, label='Elevacion (m)') # Add a color bar for scale
    ax.set_title("LiDAR DSM")
    ax.set_xlabel("Coordenada X  (Columna)")
    ax.set_ylabel("Coordenada Y (Fila)")
    st.pyplot(fig)

    # Optional: Simple LiDAR statistics
    st.markdown("---")
    st.subheader("Descripcion")
    user_name = st.text_input(
    "Interprete la figura: ",
    placeholder="ej. dimensiones, elevacion minima, maxima, promedio")


# --- Streamlit Main Loop ---

def main():
    st.sidebar.title("Seleccion de datos")
    st.sidebar.markdown("Use el boton para cambiar entre datos.")

    # Create radio buttons in the sidebar for navigation
    selected_view = st.sidebar.radio(
        "Escoja un conjunto de datos:",
        ("Datos Hiperespectrales", "Datos LiDAR")
    )

    if selected_view == "Datos Hiperespectrales":
        display_hsi_dashboard()
    elif selected_view == "Datos LiDAR":
        display_lidar_dashboard()

if __name__ == "__main__":
    main()