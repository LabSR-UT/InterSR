import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

import plotly.express as px

from streamlit_plotly_events import plotly_events

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.set_page_config(layout="wide")

st.title("Clasificacion Supervisada")

# -------------------------------------------------------
# Upload image
# -------------------------------------------------------
uploaded = st.file_uploader(
    "Cargue una imagen",
    type=["png", "jpg", "jpeg"]
)

if uploaded is not None:

    image = Image.open(uploaded).convert("RGB")
    img = np.array(image)

    h, w, _ = img.shape

    # -------------------------------------------------------
    # Classes
    # -------------------------------------------------------
    st.sidebar.header("Clases")

    n_classes = st.sidebar.slider(
        "Numero de clases",
        2,
        6,
        3
    )

    class_names = []

    for i in range(n_classes):
        class_names.append(
            st.sidebar.text_input(
                f"Clase {i}",
                f"Clase_{i}"
            )
        )

    selected_class = st.sidebar.radio(
        "Clase actual",
        class_names
    )

    # -------------------------------------------------------
    # Session state
    # -------------------------------------------------------
    if "samples" not in st.session_state:
        st.session_state.samples = []

    if st.sidebar.button("Limpiar muestras"):
        st.session_state.samples = []

    # -------------------------------------------------------
    # Plot image
    # -------------------------------------------------------
    fig = px.imshow(img)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.subheader("Haga click sobre los pixeles para seleccionar las muestras")

    selected_points = plotly_events(
        fig,
        click_event=True,
        hover_event=False,
        select_event=False
    )

    # -------------------------------------------------------
    # Add clicked sample
    # -------------------------------------------------------
    if selected_points:

        point = selected_points[0]

        x = int(point["x"])
        y = int(point["y"])

        rgb = img[y, x]

        sample = {
            "x": x,
            "y": y,
            "r": int(rgb[0]),
            "g": int(rgb[1]),
            "b": int(rgb[2]),
            "class": selected_class
        }

        if sample not in st.session_state.samples:
            st.session_state.samples.append(sample)

    # -------------------------------------------------------
    # Show samples
    # -------------------------------------------------------
    st.subheader("Muestras de entrenamiento")

    df = pd.DataFrame(st.session_state.samples)

    st.dataframe(df)

    # -------------------------------------------------------
    # Train models
    # -------------------------------------------------------
    if len(df) > 10:

        X = df[["r", "g", "b"]].values
        y = df["class"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.3,
            random_state=42,
            stratify=y
        )

        models = {
            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),
            "SVM": SVC(),
            "Naive Bayes": GaussianNB()
        }

        results = []

        flat_pixels = img.reshape(-1, 3)

        tabs = st.tabs(list(models.keys()))

        colors = [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
            [255, 255, 0],
            [255, 0, 255],
            [0, 255, 255]
        ]

        class_colors = {
            class_names[i]: colors[i]
            for i in range(n_classes)
        }

        # -------------------------------------------------------
        # Train and predict
        # -------------------------------------------------------
        for tab, (name, model) in zip(tabs, models.items()):

            with tab:

                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)

                acc = accuracy_score(y_test, y_pred)

                results.append({
                    "Model": name,
                    "Accuracy": acc
                })

                st.write(f"Exactitud: {acc:.4f}")

                # ---------------------------------------------------
                # Full image classification
                # ---------------------------------------------------
                pred_img = model.predict(flat_pixels)

                pred_img = pred_img.reshape(h, w)

                classified = np.zeros((h, w, 3), dtype=np.uint8)

                for cname, color in class_colors.items():
                    classified[pred_img == cname] = color

                c1, c2 = st.columns(2)

                with c1:
                    st.image(img, caption="Original")

                with c2:
                    st.image(classified, caption=f"Clasificacion {name} ")

        # -------------------------------------------------------
        # Metrics summary
        # -------------------------------------------------------
        st.subheader("Comparacion de modelos")

        st.dataframe(pd.DataFrame(results))