import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import (
    SelectKBest,
    mutual_info_classif,
    f_classif,
    RFE
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Seleccion de atributos",
                   layout="wide")

st.title("Seleccion de Atributos")

st.markdown("""
Esta aplicación simula un conjunto de datos de teledetección multiespectral,
aplica selección de características y evalúa el rendimiento de la clasificación.
""")

# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------
st.sidebar.header("Configuracion")

n_samples = st.sidebar.slider(
    "Numero de Pixeles",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=1000
)

n_bands = st.sidebar.slider(
    "Numero de bandas espectrales",
    min_value=5,
    max_value=50,
    value=20
)

n_classes = st.sidebar.slider(
    "Numero de clases",
    min_value=2,
    max_value=6,
    value=4
)

selection_method = st.sidebar.selectbox(
    "Metodo de Seleccion de Atributos",
    [
        "Informacion Mutua",
        "ANOVA F-Test",
        "RFE (Recursive Feature Elimination)",
        "RFI (Random Forest Importance)"
    ]
)

k_features = st.sidebar.slider(
    "Numero de Atributos a seleccionar",
    min_value=2,
    max_value=n_bands,
    value=min(10, n_bands)
)

# --------------------------------------------------
# Generate Simulated Remote Sensing Data
# --------------------------------------------------
@st.cache_data
def generate_data(n_samples, n_bands, n_classes):
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_bands,
        n_informative=max(3, int(n_bands * 0.4)),
        n_redundant=max(1, int(n_bands * 0.2)),
        n_classes=n_classes,
        random_state=42
    )

    band_names = [f"Band_{i+1}" for i in range(n_bands)]

    return pd.DataFrame(X, columns=band_names), y


X, y = generate_data(
    n_samples,
    n_bands,
    n_classes
)

st.subheader("Datos")
st.write(X.head())

# --------------------------------------------------
# Simulated Remote Sensing Image
# --------------------------------------------------
st.subheader("Imagen simulada")

image_size = 100

sim_image = np.random.rand(
    image_size,
    image_size,
    min(3, n_bands)
)

fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(sim_image)
ax.set_title("Imagen RGB simulada")
ax.axis("off")

st.pyplot(fig)

# --------------------------------------------------
# Train/Test Split
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

selected_features = None
scores = None

# --------------------------------------------------
# Feature Selection
# --------------------------------------------------
if selection_method == "Informacion Mutua":

    selector = SelectKBest(
        score_func=mutual_info_classif,
        k=k_features
    )

    selector.fit(X_train, y_train)

    selected_features = X.columns[
        selector.get_support()
    ]

    scores = selector.scores_

elif selection_method == "ANOVA F-Test":

    selector = SelectKBest(
        score_func=f_classif,
        k=k_features
    )

    selector.fit(X_train, y_train)

    selected_features = X.columns[
        selector.get_support()
    ]

    scores = selector.scores_

elif selection_method == "RFE (Recursive Feature Elimination)":

    estimator = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    selector = RFE(
        estimator=estimator,
        n_features_to_select=k_features
    )

    selector.fit(X_train, y_train)

    selected_features = X.columns[
        selector.support_
    ]

    scores = selector.ranking_

elif selection_method == "RFI (Random Forest Importance)":

    rf = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    rf.fit(X_train, y_train)

    importance = rf.feature_importances_

    indices = np.argsort(importance)[::-1]

    selected_features = X.columns[
        indices[:k_features]
    ]

    scores = importance

# --------------------------------------------------
# Selected Features
# --------------------------------------------------
st.subheader("Bandas Espectrales seleccionadas")

st.write(list(selected_features))

# --------------------------------------------------
# Feature Importance Plot
# --------------------------------------------------
st.subheader("Puntaje de Atributos")

score_df = pd.DataFrame({
    "Feature": X.columns,
    "Score": scores
})

score_df = score_df.sort_values(
    "Score",
    ascending=False
)

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=score_df.head(15),
    x="Feature",
    y="Score",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)

# --------------------------------------------------
# Classification
# --------------------------------------------------
X_train_sel = X_train[selected_features]
X_test_sel = X_test[selected_features]

clf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

clf.fit(X_train_sel, y_train)

y_pred = clf.predict(X_test_sel)

acc = accuracy_score(y_test, y_pred)

st.subheader("Imagen Clasificada")

st.metric(
    label="Exactitud",
    value=f"{acc:.3f}"
)

report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)

report_df = pd.DataFrame(report).transpose()

st.dataframe(report_df)

# --------------------------------------------------
# Compare Full vs Selected Features
# --------------------------------------------------
st.subheader("Comparacion de Rendimiento")

full_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

full_model.fit(X_train, y_train)

full_pred = full_model.predict(X_test)

full_acc = accuracy_score(
    y_test,
    full_pred
)

comparison = pd.DataFrame({
    "Model": [
        "Todas las Bandas",
        "Bandas Seleccionadas"
    ],
    "Accuracy": [
        full_acc,
        acc
    ]
})

fig, ax = plt.subplots(figsize=(6, 4))

sns.barplot(
    data=comparison,
    x="Model",
    y="Accuracy",
    ax=ax
)

ax.set_ylim(0, 1)

st.pyplot(fig)

st.dataframe(comparison)