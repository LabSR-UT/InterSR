# Interpretacion SR
# Quiz 2

import streamlit as st

st.title('Actividad 1: Analisis de video')
st.subheader('Pregunta 1:')

# Código corregido
valor1 = st.radio("Según el video, ¿qué rol puede desempeñar la inteligencia artificial en el trabajo diario de un docente?",
    ["a. Un dispositivo para la retroalimentación automática que no requiere la intervención del maestro.","b. Un reemplazo completo para la búsqueda de información y la planificación de clases.","c. Un colega para la toma de decisiones definitivas y sin supervisión humana.","d. Una herramienta para la automatización de tareas operativas y repetitivas."],
	index=None,
)
st.write("Usted seleccionó:", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("¿Cuál es la postura principal que defiende el texto sobre la inteligencia artificial y su impacto en la labor del docente?",
    ["a. La IA es una oportunidad de transformación que complementa las capacidades del maestro.","b. El impacto de la IA depende completamente del tipo de institución educativa que la implemente.", "c. La IA no tiene un impacto significativo en la educación y su implementación es innecesaria.","d. La IA es una amenaza que inevitablemente reemplazará a los maestros, haciéndolos obsoletos."],
	index=None,
)
st.write("Usted selecciono: ", valor2)

st.subheader('Pregunta 3:')

valor3 = st.radio("De acuerdo con el video, ¿qué universidad utiliza la inteligencia artificial para detectar alumnos con riesgo de deserción escolar?",
    ["a. Universidad de Helsinki.",	"b. Tecnológico de Monterrey.","c. Universidad de La Sabana.","d. Stanford."],
	index=None,
)
st.write("Usted selecciono: ", valor3)

st.subheader('Pregunta 4:')

valor4 = st.radio("¿Cuál es uno de los mayores riesgos de la inteligencia artificial en la educación, según el video?",
    ["a. Que los maestros no desarrollen habilidades para usarla.","b. El costo económico de la implementación de la IA en las escuelas.", "c. La falta de herramientas de IA adecuadas para la retroalimentación.","d. La delegación excesiva de decisiones y permitir que la IA actúe como 'jefe'."],
	index=None,
)
st.write("Usted selecciono: ", valor4)

st.subheader('Pregunta 5:')

valor5 = st.radio("¿Según el video, ¿qué habilidades deben desarrollar tanto docentes como estudiantes para la era de la IA?",
    ["a. La capacidad de memorizar grandes cantidades de información.", "b. Alfabetización digital avanzada y programación.", "c. Habilidades de comunicación y oratoria.",	"d. Pensamiento crítico y ética."],
	index=None,
)
st.write("Usted selecciono: ", valor5)

#Respuestas
# P1 d
# P2 a
# P3 b
# P4 d
# P5 d
