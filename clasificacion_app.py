import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from sklearn.cluster import KMeans

# --- Configuration MUST BE HERE ---
st.set_page_config(
    page_title="Image Analysis App",
    layout="wide",
    initial_sidebar_state="expanded"
)
# -----------------------------------

# --- Model Loading and Setup (Cached for Performance) ---

@st.cache_resource
def load_supervised_model():
    """Load a pre-trained VGG16 model for supervised classification features."""
    # Load VGG16 pre-trained on ImageNet
    model = tf.keras.applications.VGG16(
        weights='imagenet', 
        include_top=True  # Include the classification layer for a prediction
    )
    # The actual VGG16 prediction is for 1000 classes, 
    # but for simplicity, we'll use the feature extractor for both parts.
    return model

@st.cache_resource
def load_feature_extractor():
    """Load a pre-trained VGG16 model without the top layer for feature extraction."""
    # Use VGG16 to extract features (no final classification layer)
    model = tf.keras.applications.VGG16(
        weights='imagenet', 
        include_top=False, 
        pooling='avg'  # Global Average Pooling to get a single vector per image
    )
    return model

# Load the models
SUPERVISED_MODEL = load_supervised_model()
FEATURE_EXTRACTOR = load_feature_extractor()

# Get the ImageNet class labels for supervised mode (optional, for richer output)
# You might need to install 'requests' if you don't have it
# You can skip this part if you don't want to show the class name
try:
    import json
    import requests
    response = requests.get("https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json")
    IMAGENET_CLASSES = {int(k): v[1] for k, v in json.loads(response.text).items()}
except Exception as e:
    st.warning(f"Could not load ImageNet class index: {e}. Supervised mode will show class ID.")
    IMAGENET_CLASSES = None
    
# --- Image Processing Functions ---

def preprocess_image(image: Image.Image, target_size=(224, 224), include_top=True) -> np.ndarray:
    """Preprocesses a PIL image for VGG16 model."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize and convert to numpy array
    image = image.resize(target_size)
    img_array = tf.keras.utils.img_to_array(image)
    
    # Expand dimensions to create a batch of 1
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess input (normalize)
    if include_top:
        # Preprocessing for a full classification model
        return tf.keras.applications.vgg16.preprocess_input(img_array)
    else:
        # Preprocessing for feature extraction
        return tf.keras.applications.vgg16.preprocess_input(img_array)

# --- Supervised Classification ---

def supervised_classification(uploaded_file):
    """Handles the supervised image classification process."""
    st.subheader("🚀 Clasificacion Supervisada (VGG16)")
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Subir imagen', use_column_width=True)
            st.write("")
            st.write("Clasificando...")
            
            # Preprocess the image
            processed_image = preprocess_image(image, include_top=True)
            
            # Predict
            predictions = SUPERVISED_MODEL.predict(processed_image)
            
            # Decode the predictions
            decoded_predictions = tf.keras.applications.vgg16.decode_predictions(predictions, top=3)[0]

            st.success("Clasificacion completada!")
            st.markdown("### Mejores 3 Predicciones:")
            
            # Display results
            results_data = []
            for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
                results_data.append([
                    f"**{label}**", 
                    f"{score*100:.2f}%"
                ])
            
            st.table(results_data)

        except Exception as e:
            st.error(f"An error occurred during classification: {e}")
    else:
        st.info("Por favor, suba una imagen para iniciar la clasificación supervisada.")

# --- Main Streamlit App Layout ---

def main():
    """Defines the main layout and logic of the Streamlit app."""
    st.title("🖼️ Aplicación interactiva de análisis de imágenes")
    st.markdown("Seleccione un método para analizar sus imágenes: Clasificación supervisada.")

    st.sidebar.header("App Configuration")
    analysis_mode = st.sidebar.radio(
        "Selecciones Modo de Analisis:",
        ("Clasificacion Supervisada")
    )

    st.divider()

    if analysis_mode == "Clasificacion Supervisada":
        st.sidebar.subheader("Supervised Input")
        uploaded_file = st.sidebar.file_uploader(
            "Subir una sola imagen (JPG, PNG)", 
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=False
        )
        supervised_classification(uploaded_file)


if __name__ == "__main__":
    main()
