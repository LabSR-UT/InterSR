import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import rasterio
from rasterio.plot import reshape_as_image
import geopandas as gpd

st.set_page_config(layout="wide", page_title="Intro SR")

st.title("🎯 Visualizacion Imagenes SR")
st.markdown("Esta aplicacion permite visualizar imagenes de varias plataformas de SR.")

sat = st.sidebar.selectbox("Seleccione una imagen", ('Landsat', 'Sentinel', 'Planet', 'UAV' ))

if sat == 'Landsat':
    url = "https://github.com/LabSR-UT/InterSR/RGB.tif"
elif sat == 'Sentinel':
    url = "https://github.com/LabSR-UT/InterSR/TCI.tif"
elif sat == 'Planet':
    url = "https://github.com/LabSR-UT/InterSR/20201214_144239_07_222b_3B_Visual_clip.tif"
else:
    url = "https://github.com/LabSR-UT/InterSR/logo_campus_modified.tif"

run = st.sidebar.button('Aplicar')
    
# 1. Load Image and its Metadata (CRS/Transform)
@st.cache_data
def get_raster_and_meta(url):
    with rasterio.open(url) as src:
        img = src.read([1, 2, 3])
        transform = src.transform  # The 'key' to converting GPS to Pixels
        crs = src.crs              # The coordinate system (e.g., WGS84)
        
        img_display = reshape_as_image(img)
        img_display = (img_display - img_display.min()) / (img_display.max() - img_display.min())
        return img_display, transform, crs

# 2. File Uploader
uploaded_file = gpd.read_file("https://github.com/LabSR-UT/InterSR/campusUT.gpkg")

# 4. Alignment Logic
if run:
    try:
        img, transform, img_crs = get_raster_and_meta(url)
    
        # 3. Base Plotly Figure        
        fig = px.imshow(img)
        
        gdf = uploaded_file
        
        # Ensure GeoJSON matches the Image's Coordinate System
        gdf = gdf.to_crs(img_crs)

        for _, row in gdf.iterrows():
            if row.geometry.geom_type in ['Polygon', 'MultiPolygon']:
                # Get the 'exterior' of the polygon
                # We use ~transform to turn (Lon, Lat) -> (Row, Col)
                for poly in (row.geometry.geoms if row.geometry.geom_type == 'MultiPolygon' else [row.geometry]):
                    lon_coords, lat_coords = poly.exterior.coords.xy
                    
                    # THE MAGIC STEP: Convert GPS to Pixels
                    cols, rows = rasterio.transform.rowcol(transform, lon_coords, lat_coords)
                    
                    fig.add_trace(go.Scatter(
                        x=rows, y=cols, 
                        mode='lines', 
                        fill="toself",
                        fillcolor="rgba(255, 255, 0, 0.0)",  # Yellow with 30% opacity
                        line=dict(color='yellow', width=3),                        
                        name="Capas alineadas"
                    ))
        st.sidebar.success("Hecho!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

    fig.update_layout(width=900, height=700)

    st.plotly_chart(fig, use_container_width=True)

