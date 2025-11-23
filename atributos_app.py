import streamlit as st
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression, chi2
from sklearn.preprocessing import LabelEncoder
import numpy as np
import io

# --- Configuration & Initialization (Mandatory for Canvas, safe to ignore for local run) ---
# Global variables are provided by the canvas environment for persistent storage,
# but they are not used for this purely computational script.
# const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
# const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
# const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : '';
# ------------------------------------------------------------------------------------------


def feature_selection_app():
    """Main function to run the Streamlit feature selection application."""
    st.set_page_config(
        page_title="Seleccion de Atributos",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Seleccion de Atributos 📊")
    st.markdown("Cargar un conjunto de datos y usar metodos estadisticos para identificar los mejores predictores para su variable objetivo.")

    # --- File Uploader ---
    uploaded_file = st.file_uploader(
        "Cargue un archivo CSV (recomendado) o Excel",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            # Load the data
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else: # Assuming .xlsx
                data = pd.read_excel(uploaded_file)

            st.success("Archivo cargado con exito!")
            st.subheader("Previsualizacion de datos (Primeras 5 filas)")
            st.dataframe(data.head())

            # --- Data Cleaning and Preprocessing ---
            # Drop rows with any missing values for simplicity in this demo
            original_rows = len(data)
            data_cleaned = data.dropna()
            rows_after_drop = len(data_cleaned)

            if original_rows != rows_after_drop:
                st.warning(f"Note: Dropped {original_rows - rows_after_drop} rows with missing values for analysis.")
            
            if data_cleaned.empty:
                st.error("El conjunto de datos esta vacio despues de eliminar los valores faltantes. Favor verificar sus datos.")
                return

            # --- Sidebar Controls ---
            st.sidebar.header("Configuracion")

            # 1. Target Variable Selection
            all_cols = data_cleaned.columns.tolist()
            target_column = st.sidebar.selectbox(
                "1. Seleccione la variable objetivo (Y):",
                all_cols
            )

            # Separate features (X) from the target (Y)
            features = data_cleaned.drop(columns=[target_column])
            target = data_cleaned[target_column]

            # Convert non-numeric target to numeric if needed (e.g., binary classification labels)
            le = LabelEncoder()
            if target.dtype == 'object' or target.dtype == 'category':
                target_encoded = le.fit_transform(target)
                st.info(f"Target column '{target_column}' was label encoded for analysis.")
            else:
                target_encoded = target.values


            # Select only numeric features for SelectKBest, as it requires numerical input
            numeric_features = features.select_dtypes(include=np.number)
            
            if numeric_features.empty:
                st.error("No se encontraron atributos numericos en el conjunto de datos para realizar la seleccion estadistica. Favor preprocesar sus datos.")
                return

            feature_names = numeric_features.columns.tolist()
            X = numeric_features.values
            Y = target_encoded

            # Determine task type and suitable scoring function
            unique_target_values = len(np.unique(Y))
            is_classification = unique_target_values <= 20 and Y.dtype in (np.int64, np.int32) and target.dtype != 'float'

            if is_classification:
                # Chi-squared test is suitable for non-negative numerical data and categorical target
                score_func = chi2 
                method_name = "Chi-cuadrado (Clasificacion)"
                st.sidebar.info("Modelo detectado: **Clasificacion** (usando la prueba Chi-cuadrado).")
                
                # Check for non-negative values required by chi2
                if (X < 0).any():
                    st.warning("La prueba Chi-cuadrado requiere valores del atributos no negativos. Se usara la regresion F por seguridad.")
                    score_func = f_regression
                    method_name = "Regresion F (General)"
                    is_classification = False
            else:
                # F-regression for regression tasks or if chi2 requirements aren't met
                score_func = f_regression
                method_name = "Regresion F (Regresion)"
                st.sidebar.info("Modelo detectado: **Regresion** (usando la regresion F).")
            
            # 2. Select Number of Features (K)
            max_k = len(feature_names)
            k_features = st.sidebar.slider(
                f"2. Seleccione el numero de mejores atributos (K, Max: {max_k}):",
                min_value=1,
                max_value=max_k,
                value=min(10, max_k)
            )

            st.sidebar.markdown(f"**Metodo Seleccionado:** `{method_name}`")
            st.sidebar.write(f"Buscando los mejores **{k_features}** atributos entre los **{max_k}**.")

            st.subheader("Resultados")

            # --- Feature Selection Implementation ---
            with st.spinner(f'Calculando los mejores atributos usando el {method_name}...'):
                # Initialize SelectKBest
                selector = SelectKBest(score_func=score_func, k=k_features)

                # Fit and transform the data
                selector.fit(X, Y)

                # Get the scores and p-values
                scores = selector.scores_
                p_values = selector.pvalues_

                # Create a DataFrame for results
                feature_results = pd.DataFrame({
                    'Atributo': feature_names,
                    'Puntaje': scores,
                    'P-valor': p_values
                })

                # Rank the features by score (higher score is better)
                feature_results = feature_results.sort_values(by='Puntaje', ascending=False).reset_index(drop=True)
                feature_results.index += 1 # Start index at 1

                # Get the indices of the selected features (based on the original, unsorted array)
                selected_indices = selector.get_support(indices=True)
                selected_features_mask = [i in selected_indices for i in range(len(feature_names))]
                
                # Identify the selected features by checking the selector mask
                selected_features = [feature_names[i] for i in selected_indices]


            # --- Display Results ---

            st.markdown(f"### Top {k_features} Selected Features")
            st.dataframe(pd.DataFrame({"Atributos seleccionados": selected_features}), use_container_width=True)

            st.markdown(f"### Ranking de Atributos totales (basado en el puntaje {method_name})")
            
            # Highlight the top K features in the full list
            def highlight_top_k(s):
                """Highlight the top K rows in the results."""
                return ['background-color: #d1e7dd' if i < k_features else '' for i in s.index]

            st.dataframe(
                feature_results.style.apply(highlight_top_k, axis=0),
                use_container_width=True,
                height=500
            )
            
            st.caption("Atributos rankeados por puntaje. Los P-valores mas bajos generalmente indican una relacion estadistica mas fuerte con la variable objetivo.")


            # --- Download Button for Selected Data ---
            @st.cache_data
            def convert_df_to_csv(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv(index=False).encode('utf-8')
            
            # Create a DataFrame containing only the selected features + the target
            selected_data = data_cleaned[selected_features + [target_column]]
            csv = convert_df_to_csv(selected_data)

            st.download_button(
                label=f"Descargar el conjunto de datos con los mejores {k_features} atributos",
                data=csv,
                file_name=f'dataset_mejores_{k_features}.csv',
                mime='text/csv',
                key='download_csv'
            )


        except Exception as e:
            st.error(f"An error occurred during data processing: {e}")
            st.exception(e)

    else:
        st.info("Esperando la carga del archivo. Favor cargar un archivo CSV o Excel para empezar el proceso de seleccion de atributos.")

if __name__ == '__main__':
    feature_selection_app()