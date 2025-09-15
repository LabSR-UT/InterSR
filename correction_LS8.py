import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from Py6S import *
import datetime

# --- App Title and Description ---
st.title("Corrección atmosférica OLI del Landsat 8 con Py6S")
st.markdown("Esta aplicación realiza una **prueba de concepto** de corrección atmosférica en una imagen OLI del Landsat 8 utilizando el modelo de transferencia radiativa Py6S. Está diseñada para demostrar el flujo de trabajo para un solo píxel o un área pequeña sobre Armero-Guayabal, Colombia.")

# --- File Upload Section ---
st.header("1. Cargar los datos Landsat 8")
with st.expander("Cargue su imagen Landsat 8 (.TIF) y su correspondiente metadata (.MTL)"):
    uploaded_image = st.file_uploader("Escoja el archivo TIF de la imagen Landsat 8", type="TIF")
    uploaded_metadata = st.file_uploader("Escoja el archivo MTL correspondiente al metadato", type="TXT")

    if uploaded_image and uploaded_metadata:
        st.success("Archivos cargados correctamente! ✅")

# --- Atmospheric Parameters Section ---
st.header("2. Configuracion de parametros atmosfericos")
st.info("Establezca las condiciones atmosféricas para la corrección. Los valores predeterminados corresponden a un clima tropical cerca de Armero-Guayabal.")

# --- Correction Button and Main Logic ---
st.header("3. Ejecutar la correccion atmosferica")
if st.button("Run Atmospheric Correction"):
    if not uploaded_image or not uploaded_metadata:
        st.error("Por favor cargue ambos archivos TIF y MTL para continuar.")
    else:
        # Save uploaded files to a temporary location
        with open("uploaded_image.TIF", "wb") as f:
            f.write(uploaded_image.getbuffer())
        with open("uploaded_metadata.TXT", "wb") as f:
            f.write(uploaded_metadata.getbuffer())
        
        # --- Pre-processing: Extract Metadata ---
        st.subheader("Procesando los datos...")
        with open("uploaded_metadata.TXT", "r") as f:
            metadata_lines = f.readlines()

        def get_metadata_value(key):
            for line in metadata_lines:
                if key in line:
                    return float(line.split("=")[1].strip())
            return None

        # Extract radiometric scaling factors and other parameters
        rad_mult_band4 = get_metadata_value("RADIANCE_MULT_BAND_4")
        rad_add_band4 = get_metadata_value("RADIANCE_ADD_BAND_4")
        
        solar_zenith = get_metadata_value("SUN_ELEVATION")
        if solar_zenith is not None:
            solar_zenith = 90.0 - solar_zenith
            
        acquisition_date_str = None
        for line in metadata_lines:
            if "DATE_ACQUIRED" in line:
                acquisition_date_str = line.split("=")[1].strip().replace("'", "")
                break
        
        # --- `Py6S` Configuration ---
        st.subheader("Configuracion del Modelo Py6S")
        s = SixS()
        
        # Set geometry
        s.geometry = Geometry.User()
        s.geometry.solar_z = solar_zenith
        s.geometry.view_z = 0  # Assuming nadir view
        s.geometry.month = datetime.datetime.strptime(acquisition_date_str, '%Y-%m-%d').month
        s.geometry.day = datetime.datetime.strptime(acquisition_date_str, '%Y-%m-%d').day
        
        # Set atmospheric conditions
        #s.aero_profile = AeroProfile.PredefinedType(AeroProfile.types[aero_profile])
        s.aero_profile = AeroProfile.PredefinedType(1)
        s.aot550 = 0.1 #aot_550
        #s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.types[atmos_profile])
        s.atmos_profile = AtmosProfile.UserWaterAndOzone(0.22, 1.97)
        
        # Set altitudes
        s.altitudes.set_target_sea_level()
        s.altitudes.set_sensor_satellite_level()

        # Set atmospheric correction mode
        s.atmos_corr = AtmosCorr.AtmosCorrLambertianFromRadiance(1) # Radiance value is a placeholder

        # --- Process and Visualize a Single Band (e.g., Band 4 - Red) ---
        st.subheader("Ejecutando la correccion de la Banda 4 (Red)...")
        
        with rasterio.open("uploaded_image.TIF") as src:
            band4_data = src.read(1) # Assuming Band 4 is the red band
        
        # Get a single pixel for demonstration (e.g., center of the image)
        pixel_row, pixel_col = band4_data.shape[0] // 2, band4_data.shape[1] // 2
        dn_value = band4_data[pixel_row, pixel_col]
        
        # Convert DN to TOA Radiance
        radiance = dn_value * rad_mult_band4 + rad_add_band4
        st.write(f"Raw DN value for a sample pixel: {dn_value}")
        st.write(f"TOA Radiance for this pixel: {radiance:.4f} W/(m² sr µm)")
        
        # Run Py6S for the specific pixel's radiance
        s.atmos_corr = AtmosCorr.AtmosCorrLambertianFromRadiance(radiance)
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B4)
        s.run()
        
        surface_reflectance = s.outputs.atmos_corrected_reflectance_lambertian
        
        st.write(f"**Calculated Surface Reflectance for this pixel:** **{surface_reflectance:.4f}**")
        st.success("Correction completed! ✨")
        
        # --- Visualization Section ---
        st.header("4. Visualizacion")
        
        # Display the raw image
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(band4_data, cmap='Reds', vmin=band4_data.min(), vmax=band4_data.max())
        ax.set_title("Imagen de la Banda 4 Image (DNs)")
        ax.set_xlabel("Columna")
        ax.set_ylabel("Fila")
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown(f"Los DN sin procesar no representan las propiedades reales de la superficie. El valor del píxel central es {dn_value}, y este fue el que se corrigio.")