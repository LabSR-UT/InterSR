import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Define Vegetation Index Calculation Functions ---
def calculate_ndvi(nir, red):
    """NDVI = (NIR - Red) / (NIR + Red)"""
    if (nir + red) == 0: return np.nan
    return (nir - red) / (nir + red)

def calculate_evi(nir, red, blue, L=1.0, C1=6.0, C2=7.5, G=2.5):
    """EVI = G * ((NIR - Red) / (NIR + C1 * Red - C2 * Blue + L))"""
    denominator = (nir + C1 * red - C2 * blue + L)
    if denominator == 0: return np.nan
    return G * ((nir - red) / denominator)

def calculate_savi(nir, red, L=0.5):
    """SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)"""
    denominator = (nir + red + L)
    if denominator == 0: return np.nan
    return ((nir - red) / denominator) * (1 + L)

# --- 2. Define Spectral Signatures for Scenarios (Hypothetical) ---
# Values are [Blue, Red, NIR] reflectance (0 to 1)
SPECTRAL_SIGNATURES = {
    "🌱 Planta sana": {
        "color": "g",
        "bands": {"Blue": 0.05, "Red": 0.08, "NIR": 0.55}
    },
    "🍂 Planta estresada": {
        "color": "y",
        "bands": {"Blue": 0.15, "Red": 0.20, "NIR": 0.35}
    },
    "🧱 Suelo desnudo": {
        "color": "brown",
        "bands": {"Blue": 0.10, "Red": 0.15, "NIR": 0.18}
    },
    "💧 Aguas profundas": {
        "color": "b",
        "bands": {"Blue": 0.02, "Red": 0.01, "NIR": 0.01}
    }
}
BAND_NAMES = ["Blue", "Red", "NIR"]
BAND_WAVELENGTHS = [480, 660, 840] # Approximate centers for visualization

# --- 3. Streamlit App Layout ---
def main():
    st.set_page_config(
        page_title="VI interactiva",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🛰️ Índice de vegetación: identifique como la radiacion marca la diferencia")
    st.markdown("Explore cómo diferentes superficies reflejan la radiacion y cómo esta 'firma espectral' influye en los valores de los índices de vegetación.")
    st.markdown("---")
    
    # Create the Interpolation Scenario Slider in the Sidebar
    st.sidebar.header("🔬 Selector de escenarios")
    st.sidebar.markdown("**Mueva el control deslizante** para volar virtualmente sobre un área que cambia de **Planta sana** a **Suelo desnudo**.")

    # Get the key signatures for interpolation
    sig_healthy = SPECTRAL_SIGNATURES["🌱 Planta sana"]["bands"]
    sig_bare = SPECTRAL_SIGNATURES["🧱 Suelo desnudo"]["bands"]
    
    # Interactive Slider for Interpolation
    interpolation_factor = st.sidebar.slider(
        "Transición de Planta Sana (0) a Suelo Desnudo (1)",
        0.0, 1.0, 0.0, 0.01,
        help="Un valor de 0,0 simula un dosel puramente saludable, 1,0 es un suelo puramente desnudo.."
    )
    
    # Interpolate the spectral values
    current_bands = {}
    for band in BAND_NAMES:
        h_val = sig_healthy[band]
        b_val = sig_bare[band]
        # Linear interpolation: current_value = (1 - factor) * healthy_value + factor * bare_value
        current_bands[band] = (1 - interpolation_factor) * h_val + interpolation_factor * b_val

    # Display current surface type
    if interpolation_factor < 0.25:
        st.sidebar.success("Superficie actual: **Dosel de alto vigor**")
    elif interpolation_factor < 0.75:
        st.sidebar.warning("Superficie actual: **Vegetación escasa/estresada**")
    else:
        st.sidebar.error("Superficie actual: **Suelo desnudo predominante**")


    # --- 4. Spectral Signature Visualization ---
    col_vis, col_calc = st.columns([1, 1])

    with col_vis:
        st.header("1. Firma espectral")
        st.markdown("Esta línea muestra cuánta luz se refleja en cada banda para el escenario elegido.")
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Plot the interpolated signature
        current_reflectance = [current_bands[band] for band in BAND_NAMES]
        
        ax.plot(BAND_WAVELENGTHS, current_reflectance, 'o-', color='green' if interpolation_factor < 0.5 else 'orange', linewidth=2, markersize=8)
        
        # Highlight the key VI bands
        ax.axvspan(620, 700, alpha=0.1, color='red', label='Red (Absorcion)')
        ax.axvspan(760, 900, alpha=0.1, color='green', label='NIR (Reflexion)')

        ax.set_xticks(BAND_WAVELENGTHS)
        ax.set_xticklabels(BAND_NAMES)
        ax.set_ylim(0, 1.0)
        ax.set_title("Curva de reflectancia espectral actual")
        ax.set_ylabel("Valor de reflectancia (0-1)")
        ax.set_xlabel("Banda espectral")
        
        # Add labels to the points
        for i, (band, ref) in enumerate(current_bands.items()):
             ax.text(BAND_WAVELENGTHS[i], ref + 0.05, f"{ref:.2f}", fontsize=9, ha='center')
        
        # Add the 'Vegetation Index Principle' description
        if current_bands["NIR"] > current_bands["Red"]:
            ax.annotate('Gran reflexión NIR, baja absorción del rojo → Alto valor VI', 
                        xy=(BAND_WAVELENGTHS[2], current_bands["NIR"]), xytext=(BAND_WAVELENGTHS[2] - 100, current_bands["NIR"] + 0.3),
                        arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                        fontsize=10, color='darkgreen', ha='center')
        
        st.pyplot(fig)

    # --- 5. Index Calculation and Comparison ---
    with col_calc:
        st.header("2. Cálculo del índice")
        st.markdown("Los índices se calculan utilizando los valores de reflectancia del gráfico..")

        # Calculate results
        nir = current_bands["NIR"]
        red = current_bands["Red"]
        blue = current_bands["Blue"] # Used for EVI
        L_savi = 0.5 # Constant L factor for simplicity in this section

        ndvi_val = calculate_ndvi(nir, red)
        evi_val = calculate_evi(nir, red, blue)
        savi_val = calculate_savi(nir, red, L_savi)		
 
        results_df = pd.DataFrame({
            "Indice": ["NDVI", "EVI", "SAVI"],
            "Valor": [ndvi_val, evi_val, savi_val],
            "Detalle de la Formula": [
                r"(nir-red / nir+red)",
                r"(2.5 * ((nir-red) / (nir + 6 * red - 7.5 * blue + 1)",
                r"((nir–red) / (nir+red+1)) * (1 + 1)" 
            ]
        }).set_index("Indice")
        
        # Display results table
        st.dataframe(results_df.style.format({'Valor': '{:.4f}'}), use_container_width=True)

        st.subheader("¿Por qué la diferencia? ")
        
        # Detailed comparison logic
        if ndvi_val > savi_val:
            st.info(f"""
            **NDVI vs. SAVI:** El NDVI ({ndvi_val:.3f}) es mayor que el SAVI ({savi_val:.3f}).
            **SAVI** utiliza un factor de suelo ($L={L_savi}$), que generalmente reduce el valor del índice en comparación con el NDVI, especialmente cuando el suelo de fondo tiene una fuerte influencia (es decir, cuando la vegetación es escasa).
            """)

        if ndvi_val > evi_val and evi_val > 0:
            st.info(f"""
            **NDVI vs. EVI:** El NDVI ({ndvi_val:.3f}) es mayor que el EVI ({evi_val:.3f}).
            El **EVI** suele ser menor porque utiliza la **banda azul** para corregir de forma agresiva la **neblina atmosférica y el ruido de fondo**.
            Esta corrección es más beneficiosa en copas muy densas, donde el NDVI tiende a saturarse.
            """)

# --- 6. Run the app ---
if __name__ == "__main__":
    main()