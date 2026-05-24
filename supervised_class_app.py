import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Set page layout to wide
st.set_page_config(layout="wide")

st.title("🛰️ Classificacion supervisada")
st.write("Clasificar una imagen usando varios metodos de aprendizaje de maquinas para clasificar sus pixeles.")

# -------------------------------------------------------------------------
# 1. SIDEBAR - CONTROLS & HYPERPARAMETERS
# -------------------------------------------------------------------------
st.sidebar.header("1. Configuracion del Modelo")

# Dropdown to select the classifier
method = st.sidebar.selectbox(
    "Seleccione un metodo de clasificacion",
    ("Bosque aleatorio (RF)", "Maquina de Soporte de Vectores (SVM)", "K-Vecinos mas Cercanos (kNN)")
)

# Dynamic hyperparameter tuning based on the selected method
if method == "Bosque aleatorio (RF)":
    n_estimators = st.sidebar.slider("Numero de arboles (n_estimators)", 10, 200, 100, step=10)
    max_depth = st.sidebar.slider("Maxima profundidad", 2, 20, 10)
elif method == "Maquina de Soporte de Vectores (SVM)":
    C_val = st.sidebar.slider("Parametro de Regularizacion (C)", 0.1, 10.0, 1.0, step=0.5)
    kernel = st.sidebar.selectbox("Kernel", ("rbf", "linear", "poly"))
elif method == "K-Vecinos mas Cercanos (kNN)":
    n_neighbors = st.sidebar.slider("Numero de vecinos (k)", 1, 15, 5, step=1)

# -------------------------------------------------------------------------
# 2. DATA GENERATION (Toy Remote Sensing Image)
# -------------------------------------------------------------------------
@st.cache_data
def generate_toy_image():
    """Generates a synthetic 3-band image (100x100 pixels) with 3 distinct ground classes."""
    np.random.seed(42)
    width, height = 100, 100
    bands = 3
    
    # Create an empty image array
    img = np.zeros((width, height, bands))
    
    # Define class masks (Simulating Water, Vegetation, and Urban)
    # Class 0: Water (Bottom-left)
    # Class 1: Vegetation (Middle diagonal)
    # Class 2: Urban (Top-right)
    X, Y = np.meshgrid(np.arange(width), np.arange(height))
    
    # Ground Truth Map
    ground_truth = np.zeros((width, height), dtype=int)
    ground_truth[(X + Y) < 80] = 0        # Water
    ground_truth[((X + Y) >= 80) & ((X + Y) < 130)] = 1  # Vegetation
    ground_truth[(X + Y) >= 130] = 2     # Urban

    # Inject signature spectral features with some noise
    # Water: Low values across all bands, slightly higher in blue/green
    img[ground_truth == 0] = [0.1, 0.2, 0.4] + np.random.normal(0, 0.15, (np.sum(ground_truth == 0), 3))
    # Vegetation: High Green/NIR signature (Simulated via high Middle Band)
    img[ground_truth == 1] = [0.2, 0.6, 0.2] + np.random.normal(0, 0.25, (np.sum(ground_truth == 1), 3))
    # Urban: High reflectance across all bands (Greyish/Bright)
    img[ground_truth == 2] = [0.7, 0.7, 0.7] + np.random.normal(0, 0.5, (np.sum(ground_truth == 2), 3))
    
    # Clip values between 0 and 1 for safe plotting
    img = np.clip(img, 0, 1)
    
    return img, ground_truth

img, ground_truth = generate_toy_image()

# -------------------------------------------------------------------------
# 3. PREPARE TRAINING DATA & TRAIN MODEL
# -------------------------------------------------------------------------
# Flatten image to shape (N_pixels, N_bands) for scikit-learn
X_pixels = img.reshape(-1, 3)
y_pixels = ground_truth.flatten()

# Sample a small percentage of pixels to act as labeled "training ground truth"
X_train, X_test, y_train, y_test = train_test_split(
    X_pixels, y_pixels, train_size=0.05, random_state=42, stratify=y_pixels
)

# Initialize chosen model
if method == "Bosque aleatorio (RF)":
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
elif method == "Maquina de Soporte de Vectores (SVM)":
    model = SVC(C=C_val, kernel=kernel, random_state=42)
elif method == "K-Vecinos mas Cercanos (kNN)":
    model = KNeighborsClassifier(n_neighbors=n_neighbors)

# Train the model
model.fit(X_train, y_train)

# Predict on test split to show metrics
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Predict across the ENTIRE image to get the final classification map
full_prediction = model.predict(X_pixels)
classified_img = full_prediction.reshape(ground_truth.shape)

# -------------------------------------------------------------------------
# 4. VISUALIZATION
# -------------------------------------------------------------------------
# Custom colormap for classes: 0 = Blue (Water), 1 = Green (Veg), 2 = Red/Grey (Urban)
from matplotlib.colors import ListedColormap
cmap_classes = ListedColormap(['#1f77b4', '#2ca02c', '#7f7f7f'])
class_names = ['Agua', 'Vegetacion', 'Urbano']

# Display summary metrics
st.subheader("📊 Rendimiento del Modelo")
col1, col2, col3 = st.columns(3)
col1.metric("Metodo seleccionado", method)
col2.metric("Pixeles de entrenamiento usados (muestra 5%)", len(X_train))
col3.metric("Punta de Exactitud de la prueba", f"{accuracy * 100:.2f}%")

st.markdown("---")
st.subheader("🖼️ Visualizacion de Resultados")

# Plot side-by-side maps
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Subplot 1: Original True Color / False Color Composite
ax[0].imshow(img)
ax[0].set_title("Imagen original (RGB)")
ax[0].axis('off')

# Subplot 2: Ground Truth
im2 = ax[1].imshow(ground_truth, cmap=cmap_classes)
ax[1].set_title("Clases Verdaderas")
ax[1].axis('off')

# Subplot 3: Classified Image
im3 = ax[2].imshow(classified_img, cmap=cmap_classes)
ax[2].set_title(f"Mapa clasificado ({method})")
ax[2].axis('off')

# Add a shared legend for classes
cbar = fig.colorbar(im3, ax=ax.ravel().tolist(), ticks=[0.33, 1.0, 1.66], shrink=0.6, location='bottom')
cbar.ax.set_xticklabels(class_names)

st.pyplot(fig)

# -------------------------------------------------------------------------
# 5. DATA INSIGHTS
# -------------------------------------------------------------------------
st.markdown("---")
with st.expander("🔍 Valores espectrales de los pixeles"):
    st.write("Aquí se muestra un vistazo rápido a los datos espectrales de píxeles sin procesar (características) que se introducen en su metodo de aprendizaje automático.:")
    import pandas as pd
    df_sample = pd.DataFrame(X_train, columns=["Banda 1 (Red)", "Banda 2 (Green)", "Banda 3 (Blue)"])
    df_sample["ID clase"] = y_train
    df_sample["Nombre de Clase"] = df_sample["ID clase"].map({0: "Agua", 1: "Vegetacion", 2: "Urbano"})
    st.dataframe(df_sample.head(15), use_container_width=True)