import streamlit as st
import Backend

st.title("Planificador SJF")

opcion = st.selectbox("¿Cómo deseas ingresar los datos?", ("Manual", "Automático"))

if opcion == "Manual":
    procesos_manual = []
    for i in range(5):
        id_proceso = i + 1
        tiempo_llegada = st.number_input(f"Tiempo de llegada del Proceso {id_proceso}:", min_value=0)
        tiempo_ejecucion = st.number_input(f"Tiempo de ejecución del Proceso {id_proceso}:", min_value=1)
        procesos_manual.append(Backend.Proceso(id_proceso, tiempo_llegada, tiempo_ejecucion))

    if st.button("Ejecutar"):
        resultados_manual = Backend.planificar_sjf(procesos_manual)
        Backend.mostrar_resultados(resultados_manual)

elif opcion == "Automático":
    if st.button("Generar y Ejecutar"):
        procesos_auto = Backend.generar_procesos(5)
        resultados_auto = Backend.planificar_sjf(procesos_auto)
        Backend.mostrar_resultados(resultados_auto)