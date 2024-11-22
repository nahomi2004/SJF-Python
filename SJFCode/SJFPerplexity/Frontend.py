import streamlit as st
import Backend as bk

st.title("Simulador de Planificación de Procesos")

# Selección de planificador y forma de ingreso de datos
opcion_planificador = st.selectbox("Selecciona el planificador:", ["FIFO", "SJF"])
opcion_ingreso_datos = st.selectbox("¿Cómo deseas ingresar los datos?", ["Manual", "Automático"])

if opcion_ingreso_datos == "Manual":
    st.write("### Ingreso Manual de Procesos")
    num_procesos = st.number_input("Número de procesos:", min_value=1, value=5)
    procesos_manual = []

    for i in range(num_procesos):
        with st.container():
            st.write(f"#### Proceso {i + 1}")
            tiempo_llegada = st.number_input(f"Tiempo de llegada del Proceso {i + 1}:", min_value=0)
            tiempo_ejecucion = st.number_input(f"Tiempo de ejecución del Proceso {i + 1}:", min_value=1)
            procesos_manual.append(bk.Proceso(i + 1, tiempo_llegada, tiempo_ejecucion))

    if st.button("Ejecutar"):
        if opcion_planificador == "FIFO":
            resultados = bk.planificar_fifo(procesos_manual)
        else:
            resultados = bk.planificar_sjf(procesos_manual)

        df_resultados, promedio_espera, promedio_tiempo_sistema = bk.mostrar_resultados(resultados)
        st.dataframe(df_resultados)
        st.write(f"**Tiempo de Espera Promedio:** {promedio_espera:.2f}")
        st.write(f"**Tiempo Promedio en el Sistema:** {promedio_tiempo_sistema:.2f}")

elif opcion_ingreso_datos == "Automático":
    st.write("### Generación Automática de Procesos")
    num_procesos = st.number_input("Número de procesos a generar:", min_value=1, value=5)

    if st.button("Generar y Ejecutar"):
        procesos_auto = bk.generar_procesos(num_procesos)
        if opcion_planificador == "FIFO":
            resultados = bk.planificar_fifo(procesos_auto)
        else:
            resultados = bk.planificar_sjf(procesos_auto)

        df_resultados, promedio_espera, promedio_tiempo_sistema = bk.mostrar_resultados(resultados)
        st.dataframe(df_resultados)
        st.write(f"**Tiempo de Espera Promedio:** {promedio_espera:.2f}")
        st.write(f"**Tiempo Promedio en el Sistema:** {promedio_tiempo_sistema:.2f}")
