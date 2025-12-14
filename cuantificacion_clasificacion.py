import streamlit as st
import numpy as np
import pandas as pd
import rasterio as rio
from io import BytesIO

# --- Configuration ---
HECTARE_CONVERSION = 0.0001  # 1 square meter = 0.0001 hectares

def calculate_area(uploaded_file, class_mapping):
    """
    Reads a classified image, counts pixels per class, and calculates
    area and percentage in hectares.
    """
    try:
        # Read the file-like object using rasterio
        with rio.open(uploaded_file) as src:
            # 1. Read the Classified Image Data
            image_data = src.read(1)  # Read the first band (assuming single-band classification)

            # 2. Get Pixel Resolution (Ground Sampling Distance)
            # Assuming square pixels for simplicity. `src.res[0]` is the width resolution.
            # Area of one pixel in square meters (m²).
            pixel_area_sqm = src.res[0] * src.res[1]

            # 3. Count Pixels per Class
            # np.unique returns unique values and their counts
            unique_classes, counts = np.unique(image_data, return_counts=True)
            
            # Remove class 0 (often NoData or background, if present)
            if 0 in unique_classes:
                idx_zero = np.where(unique_classes == 0)[0][0]
                unique_classes = np.delete(unique_classes, idx_zero)
                counts = np.delete(counts, idx_zero)

            total_pixels = counts.sum()
            total_area_sqm = total_pixels * pixel_area_sqm
            total_area_ha = total_area_sqm * HECTARE_CONVERSION

            # 4. Calculate Area and Percentage for each class
            results = []
            for class_value, pixel_count in zip(unique_classes, counts):
                class_name = class_mapping.get(int(class_value), f"Class {int(class_value)}")
                
                # Pixel count
                pixels = int(pixel_count)

                # Area calculation
                area_sqm = pixel_count * pixel_area_sqm
                area_ha = area_sqm * HECTARE_CONVERSION
                
                # Percentage calculation
                percentage = (pixel_count / total_pixels) * 100

                results.append({
                    "Valor Clase": int(class_value),
                    "Nombre Clase": class_name,
                    "Pixeles": pixels,
                    "Area (metros2)": area_sqm,
                    "Area (Hectareas)": area_ha,
                    "Porcentaje (%)": percentage
                })

            df = pd.DataFrame(results)
            return df, total_area_ha

    except rio.RasterioIOError:
        st.error("Error: El archivo cargado no es un archivo GeoTIFF o raster válido.")
        return None, None
    except Exception as e:
        st.error(f"Se produjo un error inesperado: {e}")
        return None, None

# --- Streamlit App Interface ---
def main():
    st.set_page_config(layout="wide", page_title="Classified Image Area Quantifier")
    st.title("🛰️ Cuantificador de área de imágenes clasificadas")
    st.markdown("Cargue un archivo GeoTIFF de banda única (donde los valores de los píxeles son identificadores de clase) para calcular el recuento de píxeles, el área (en hectáreas) y el porcentaje de cobertura para cada clase.")
    

    st.sidebar.header("Configuración de clase")
    
    # User-defined class mapping (e.g., 1=Forest, 2=Water)
    st.sidebar.info("Define la asignación de valores de píxeles (ID de clase) a un nombre legible para humanos.")
    
    class_id_str = st.sidebar.text_area(
        "Introduzca pares ID de clase:Nombre de clase (uno por línea)",
        value="1:Agricultura\n2:Bosque\n3:Agua",
        height=150
    )
    
    # Parse the class mapping input
    class_mapping = {}
    try:
        for line in class_id_str.split('\n'):
            if line.strip():
                class_id, class_name = line.split(':')
                class_mapping[int(class_id.strip())] = class_name.strip()
    except Exception:
        st.sidebar.error("Formato no válido para la asignación de clases. Usar'ID:Name' format.")
        return

    st.sidebar.json(class_mapping)

    # File Uploader
    uploaded_file = st.file_uploader(
        "Subir un archivo ráster GeoTIFF clasificado (.tif)", 
        type=["tif", "tiff"]
    )

    if uploaded_file is not None:
        # Pass the file content to the calculation function
        # We need to use BytesIO to let rasterio read the uploaded file from memory
        file_content = BytesIO(uploaded_file.read())
        
        # Calculate results
        results_df, total_area_ha = calculate_area(file_content, class_mapping)

        if results_df is not None:
            st.success("Análisis completo!")
            
            # --- Display Total Area ---
            st.metric(
                label="Área total analizada", 
                value=f"{total_area_ha:,.2f} ha"
            )
            
            st.subheader("Resultados por clase")
            
            # --- Display Table ---
            # Format the output columns for better readability
            formatted_df = results_df.copy()
            formatted_df["Pixeles"] = formatted_df["Pixeles"].apply(lambda x: f"{x:,.0f}")
            formatted_df["Area (Hectareas)"] = formatted_df["Area (Hectareas)"].apply(lambda x: f"{x:,.2f}")
            formatted_df["Porcentaje (%)"] = formatted_df["Porcentaje (%)"].apply(lambda x: f"{x:.2f}%")
            formatted_df.drop(columns=["Area (metros2)"], inplace=True)
            
            st.dataframe(formatted_df.set_index("Valor Clase"), use_container_width=True)
            
            # --- Display Chart ---
            st.subheader("Gráfico de porcentaje de área")
            st.bar_chart(results_df.set_index("Nombre Clase")["Porcentaje (%)"])
            
            # --- Download Link ---
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar datos de análisis como CSV",
                data=csv,
                file_name='análisis_de_imágenes_clasificadas.csv',
                mime='text/csv',
            )

if __name__ == "__main__":
    main()