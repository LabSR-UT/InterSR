import streamlit as st
import numpy as np
from PIL import Image
from sklearn.metrics import cohen_kappa_score

# --- Configuration and Title ---
st.set_page_config(page_title="Calculo del Coeficiente Kappa", layout="centered")
st.title("🗺️ Calculadora del coeficiente Kappa de imágenes clasificadas")
st.markdown("Sube dos imágenes clasificadas (Ground Truth y Prediction) para calcular el coeficiente Kappa de Cohen, una medida de acuerdo entre evaluadores que corrige el acuerdo aleatorio..")

# --- Helper Function to Calculate Kappa ---
def calculate_kappa(ground_truth_img, predicted_img):
    """
    Calculates the Cohen's Kappa Coefficient between two classified images.
    
    The images are flattened into 1D arrays of pixel values for the calculation.
    """
    try:
        # Convert images to NumPy arrays
        gt_array = np.array(ground_truth_img)
        pred_array = np.array(predicted_img)

        # 1. Check if dimensions match
        if gt_array.shape != pred_array.shape:
            st.error("Las dimensiones de la imagen no coinciden. Sube imágenes del mismo tamaño..")
            return None, None

        # 2. Flatten the arrays for pixel-wise comparison
        # This assumes a single-band (grayscale/indexed) image for classification
        # If RGB, we'd need to decide how to handle the three bands (e.g., convert to single-band class image first)
        gt_flat = gt_array.flatten()
        pred_flat = pred_array.flatten()

        # 3. Calculate Kappa
        kappa = cohen_kappa_score(gt_flat, pred_flat)
        
        # 4. Calculate simple Observed Agreement (Accuracy)
        observed_agreement = np.mean(gt_flat == pred_flat)
        
        return kappa, observed_agreement

    except Exception as e:
        st.error(f"Se produjo un error durante el cálculo: {e}")
        return None, None

# --- Streamlit UI: File Uploads ---
st.header("Subir imágenes clasificadas")
col1, col2 = st.columns(2)

with col1:
    gt_file = st.file_uploader(
        "**Ground Truth Image** (ej. clasificacion manual )",
        type=["png", "jpg", "jpeg"]
    )

with col2:
    pred_file = st.file_uploader(
        "**Imagen predicha** (ej. resultado del modelo)",
        type=["png", "jpg", "jpeg"]
    )

# --- Process and Display Results ---
if gt_file and pred_file:
    # Load images using PIL
    ground_truth_image = Image.open(gt_file)
    predicted_image = Image.open(pred_file)

    st.subheader("Imágenes cargadas")
    
    # Display images side-by-side
    st.image([ground_truth_image, predicted_image], 
             caption=["Ground Truth", "Prediccion"], 
             use_column_width=True)

    st.subheader("Resultado del coeficiente Kappa")
    
    # Calculate and display results
    kappa, accuracy = calculate_kappa(ground_truth_image, predicted_image)

    if kappa is not None:
        st.metric(
            label="Cohen's Kappa ($\kappa$)", 
            value=f"{kappa:.4f}"
        )
        st.info(f"El acuerdo observado (precisión simple de píxel por píxel) es:**{accuracy:.4f}**")
        
        st.markdown("---")
        
        # Interpret the Kappa score (using Landis & Koch 1977 guidelines)
        if kappa < 0:
            interpretation = "Mal acuerdo (peor que el azar)"
        elif kappa <= 0.20:
            interpretation = "Ligero acuerdo"
        elif kappa <= 0.40:
            interpretation = "Acuerdo justo"
        elif kappa <= 0.60:
            interpretation = "Acuerdo moderado"
        elif kappa <= 0.80:
            interpretation = "Acuerdo sustancial"
        else: # kappa <= 1.0
            interpretation = "Acuerdo casi perfecto"

        st.success(f"**Interpretacion:** {interpretation}")

st.markdown("---")
