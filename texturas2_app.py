import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from skimage.feature import graycomatrix, graycoprops
from skimage.color import rgb2gray
import io

# --- Configuration ---
st.set_page_config(
    page_title="Comparación de imágenes de textura",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Feature Extraction Function ---
@st.cache_data
def extract_glcm_features(image_file):
    """Processes an uploaded image to extract GLCM texture features."""
    try:
        # Open and convert to grayscale
        img = Image.open(image_file).convert('RGB')
        img_array = np.array(img)
        gray_img = rgb2gray(img_array)
        
        # Scale to 8-bit integer (0-255) for GLCM
        # Ensure the image is correctly scaled for GLCM calculation
        image_int = (gray_img * 255).astype(np.uint8)

        # Calculate GLCM. Common parameters: distance=1, angle=0 (horizontal)
        distances = [1]
        angles = [0]
        # We're calculating one GLCM for simplicity, but more can be done.
        glcm = graycomatrix(
            image_int, 
            distances=distances, 
            angles=angles, 
            levels=256, 
            symmetric=True, 
            normed=True
        )

        # Extract features
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]

        return {
            'Contrast': contrast, 
            'Correlation': correlation, 
            'Energy': energy, 
            'Homogeneity': homogeneity
        }, img
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None, None

# --- Main App Logic ---
def main():
    st.title("🖼️ Comparación de características de imágenes texturizadas")
    st.markdown("Sube dos imágenes texturizadas para calcular y comparar sus características de **Matriz de coocurrencia de niveles de grises (GLCM)**.")
    
    st.sidebar.header("Subir imágenes")
    
    # Image Uploaders
    file1 = st.sidebar.file_uploader(
        "Subir imagen 1", 
        type=["png", "jpg", "jpeg", "gif"], 
        key="file1"
    )
    file2 = st.sidebar.file_uploader(
        "Subir imagen 2", 
        type=["png", "jpg", "jpeg", "gif"], 
        key="file2"
    )

    if file1 and file2:
        st.subheader("Vistas previas de imágenes")
        col1, col2 = st.columns(2)
        
        # 1. Process Image 1
        with st.spinner("Procesando imagen 1..."):
            features1, img1 = extract_glcm_features(file1)
        
        # 2. Process Image 2
        with st.spinner("Procesando imagen 2..."):
            features2, img2 = extract_glcm_features(file2)

        # Display Images
        with col1:
            st.image(img1, caption=f"Image 1: {file1.name}", use_column_width=True)
        with col2:
            st.image(img2, caption=f"Image 2: {file2.name}", use_column_width=True)
            
        st.divider()

        if features1 and features2:
            st.subheader("📊 Comparación de características de textura (GLCM)")
            st.markdown("GLCM cuenta con aspectos cuantificadores de la textura: **Contraste** (variación de intensidad local), **Correlación** (linealidad de nivel de gris), **Energía** (uniformidad/suavidad) y **Homogeneidad** (cercanía de los elementos a la diagonal).")

            # Combine features into a DataFrame for easy display
            df_data = {
                "Imagen 1 Valor": list(features1.values()),
                "Imagen 2 Valor": list(features2.values()),
                "Diferencia entre Atributos (Abs)": [
                    abs(features1[key] - features2[key]) 
                    for key in features1.keys()
                ]
            }
            df = pd.DataFrame(df_data, index=list(features1.keys()))
            
            # Highlight the smallest difference for potential similarity
            #def color_diff(val):
            #    """Highlights the row with the minimum absolute difference."""
            #    is_min = val == df['Feature Difference (Abs)'].min()
            #    return ['background-color: #d4edda'] if is_min else ['']
            def color_diff(row):
                # Define a threshold for coloring (e.g., color if the absolute difference is > 0.001)
                threshold = 0.001
    
                # 🚨 FIX: Access the scalar value using row.iloc[0] or row['Feature Difference (Abs)']
                diff_value = row['Diferencia entre Atributos (Abs)'] 
    
                # Now, the conditional check is performed on a single scalar value, not a Series.
                if diff_value > threshold:
                # Return a string with CSS style for the cell
                    return ['background-color: lightcoral'] * len(row)
                else:
                    # Return a list of empty strings to keep the default style
                    return [''] * len(row)

            st.dataframe(
                df.style.apply(
                    color_diff, 
                    subset=['Diferencia entre Atributos (Abs)'], 
                    axis=1
                ).format(
                    {'Imagen 1 Valor': '{:.4f}', 'Imagen 2 Valor': '{:.4f}', 'Diferencia entre Atributos (Abs)': '{:.4f}'}
                ), 
                use_container_width=True
            )
            
            st.divider()

            # --- Similarity Score (Euclidean Distance) ---
            st.subheader("⭐ Puntuación de similitud general")
            
            # Calculate Euclidean Distance between the feature vectors
            features_list1 = np.array(list(features1.values()))
            features_list2 = np.array(list(features2.values()))
            
            # The Euclidean distance is a measure of dissimilarity
            distance = np.linalg.norm(features_list1 - features_list2)
            
            st.metric(
                label="Distancia euclidiana (disimilitud)",
                value=f"{distance:.4f}",
                help="Un valor más bajo indica una mayor similitud de características."
            )
            
            st.info(f"La **distancia euclidiana** de {distance:.4f} es una métrica simple donde un valor más cercano a cero sugiere que las características de textura de las dos imágenes son más similares..")

    elif file1 or file2:
        st.warning("Cargue **ambas** imágenes, la 1 y la 2, para iniciar la comparación..")
    else:
        st.info("Sube dos imágenes en la barra lateral para comenzar a procesarlas y compararlas.")

if __name__ == "__main__":
    main()