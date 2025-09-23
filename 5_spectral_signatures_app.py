import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Set the page title and a brief introduction
st.set_page_config(page_title="Firmas espectrales", layout="wide")

st.title("🌱 Firmas espectrales")
st.markdown("""
Esta aplicación está diseñada para comprender cómo los diferentes materiales de la Tierra interactúan con la luz a lo largo del espectro electromagnético, un concepto fundamental en la **teledetección**.

Una firma espectral es un patrón único de reflectancia, transmitancia o absorbancia de la radiación electromagnética de un material en diferentes longitudes de onda.
""")
st.markdown("---")

# --- Sample Spectral Data ---
# This is a simplified representation of spectral signatures for common materials.
# Wavelengths are in nanometers (nm).
# Reflectance values are unitless (0 to 1).
wavelengths = np.arange(400, 2500, 20)
spectral_data = {
    'Vegetacion': {
        'reflectance': [
            0.05, 0.05, 0.06, 0.07, 0.1, 0.12, 0.15, 0.25, 0.35, 0.45, 0.5, 0.5, 0.45,
            0.4, 0.35, 0.3, 0.25, 0.2, 0.18, 0.16, 0.14, 0.12, 0.11, 0.1, 0.09, 0.08,
            0.08, 0.07, 0.06, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02,
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
        ][:len(wavelengths)] # Truncate to match wavelengths length
    },
    'Agua': {
        'reflectance': [
            0.05, 0.04, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        ][:len(wavelengths)]
    },
    'Suelo seco': {
        'reflectance': [
            0.15, 0.16, 0.17, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36,
            0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62,
            0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86,
            0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 1.0, 1.02, 1.04, 1.06, 1.08, 1.1,
            1.12, 1.14, 1.16, 1.18, 1.2, 1.22, 1.24, 1.26, 1.28, 1.3, 1.32, 1.34,
            1.36, 1.38, 1.4, 1.42, 1.44, 1.46, 1.48, 1.5, 1.52, 1.54, 1.56, 1.58,
            1.6, 1.62, 1.64, 1.66, 1.68, 1.7, 1.72, 1.74, 1.76, 1.78, 1.8, 1.82,
            1.84, 1.86, 1.88, 1.9, 1.92, 1.94, 1.96, 1.98, 2.0, 2.02, 2.04, 2.06,
            2.08, 2.1, 2.12, 2.14, 2.16, 2.18, 2.2, 2.22, 2.24, 2.26, 2.28, 2.3,
        ][:len(wavelengths)]
    },
    'Nieve/hielo': {
        'reflectance': [
            0.9, 0.9, 0.89, 0.88, 0.87, 0.85, 0.82, 0.79, 0.75, 0.7, 0.65, 0.6, 0.55,
            0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.18, 0.16, 0.14, 0.12, 0.1, 0.08,
            0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
        ][:len(wavelengths)]
    }
}

# --- Sidebar for user input ---
st.sidebar.header("Seleccione los materiales a comparar:")
selected_materials = st.sidebar.multiselect(
    "Seleccione uno o mas materiales:",
    list(spectral_data.keys()),
    default=["Vegetacion", "Agua", "Suelo seco"]
)

# --- Main plot ---
st.header("Comparacion de firmas espectrales")
if not selected_materials:
    st.warning("Seleccione como minimo un material para ilustrar su firma espectral.")
else:
    fig = go.Figure()
    for material in selected_materials:
        reflectance = spectral_data[material]['reflectance']
        fig.add_trace(go.Scatter(
            x=wavelengths,
            y=reflectance,
            mode='lines',
            name=material,
            line=dict(width=3)
        ))

    # Add background shading for different spectral regions
    fig.add_vrect(x0=400, x1=700, fillcolor="rgba(255, 0, 0, 0.1)", layer="below", line_width=0, annotation_text="Visible", annotation_position="top left")
    fig.add_vrect(x0=700, x1=1100, fillcolor="rgba(0, 255, 0, 0.1)", layer="below", line_width=0, annotation_text="NIR", annotation_position="top left")
    fig.add_vrect(x0=1100, x1=2500, fillcolor="rgba(0, 0, 255, 0.1)", layer="below", line_width=0, annotation_text="SWIR", annotation_position="top left")

    fig.update_layout(
        title="Reflectancia vs. longitud de onda para los materiales seleccionados",
        xaxis_title="Longitud de onda (nm)",
        yaxis_title="Reflectancia",
        yaxis_range=[0, 1],
        legend_title="Materiales",
        font=dict(size=14),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.header("Descripcion de los materiales y caracteristicas claves")
    for material in selected_materials:
        st.subheader(f"__{material}__")
        if material == 'Vegetacion':
            title1 = st.text_input("Ingrese su interpretacion para vegetacion:")
            st.write("Usted ingreso: ", title1)
        elif material == 'Agua':
            title2 = st.text_input("Ingrese su interpretacion para agua:")
            st.write("Usted ingreso: ", title2)
        elif material == 'Suelo seco':
            title3 = st.text_input("Ingrese su interpretacion para suelo seco:")
            st.write("Usted ingreso: ", title3)
			
st.markdown("---")

autor = st.text_input("Ingrese su nombre y apellido:")
st.write(f"Realizado por: {autor}")

st.markdown("### Actividad")
st.markdown("""
1. Hacer las consultas requeridas.
2. Ingresar los resultados en la tabla.
3. Enviar por email el resultado.
""")