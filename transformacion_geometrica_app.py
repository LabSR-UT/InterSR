import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Correcciones geometricas", layout="wide")

st.title("🖼️ Transformaciones geometricas de imagenes")
st.write("Cargue una imagen y ajuste los deslizadores para aplicar las transformaciones.")

# --- Sidebar Controls ---
st.sidebar.header("Parametros de transformacion")

uploaded_file = st.sidebar.file_uploader("Seleccione una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]

    # 1. Rotation & Scale
    st.sidebar.subheader("Rotacion & Escalamiento")
    angle = st.sidebar.slider("Rotation Angle", -180, 180, 0)
    scale = st.sidebar.slider("Scale", 0.1, 3.0, 1.0)

    # 2. Translation
    st.sidebar.subheader("Translacion")
    tx = st.sidebar.slider("Translacien en X (pixeles)", -w, w, 0)
    ty = st.sidebar.slider("Translacion en Y (pixeles)", -h, h, 0)

    # 3. Perspective Warp (Simulated by shifting corners)
    st.sidebar.subheader("Distorsion en Perspectiva")
    p_strength = st.sidebar.slider("Intensidad de la Perspectiva", 0.0, 0.5, 0.0)

    # --- Apply Transformations ---

    # A. Rotation and Scale Matrix
    # center, angle, scale
    M_rot = cv2.getRotationMatrix2D((w/2, h/2), angle, scale)
    
    # B. Translation Matrix (add to rotation matrix or apply separately)
    M_rot[0, 2] += tx
    M_rot[1, 2] += ty
    
    # Apply Affine (Rotation + Scale + Translation)
    transformed = cv2.warpAffine(img, M_rot, (w, h))

    # C. Perspective Transformation
    if p_strength > 0:
        pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        # Define 4 points to move for perspective
        offset = p_strength * w
        pts2 = np.float32([
            [offset, offset], 
            [w - offset, 0], 
            [0, h], 
            [w, h - offset]
        ])
        M_persp = cv2.getPerspectiveTransform(pts1, pts2)
        transformed = cv2.warpPerspective(transformed, M_persp, (w, h))

    # --- Display Results ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Imagen original")
        st.image(img, use_container_width=True)

    with col2:
        st.subheader("Imagen transformada")
        st.image(transformed, use_container_width=True)

else:
    st.info("Suba una imagen para iniciar.")