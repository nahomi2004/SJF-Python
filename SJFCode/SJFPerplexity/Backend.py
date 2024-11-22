import random
import pandas as pd

# Crear clase Proceso
class Proceso:
    def __init__(self, id_proceso, tiempo_llegada, tiempo_ejecucion):
        self.id_proceso = id_proceso
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.inicio_ejecucion = 0
        self.fin_ejecucion = 0
        self.tiempo_espera = 0

def generar_procesos(num_procesos):
    # Genera una lista de procesos con tiempos aleatorios de llegada y ejecución
    procesos = []
    for i in range(num_procesos):
        tiempo_llegada = random.randint(0, 10)
        tiempo_ejecucion = random.randint(1, 10)
        procesos.append(Proceso(i + 1, tiempo_llegada, tiempo_ejecucion))
    return procesos

def planificar_fifo(procesos):
    # Planifica los procesos utilizando la política FIFO
    tiempo_actual = 0
    for proceso in procesos:
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada
        proceso.inicio_ejecucion = tiempo_actual
        proceso.fin_ejecucion = tiempo_actual + proceso.tiempo_ejecucion
        proceso.tiempo_espera = proceso.inicio_ejecucion - proceso.tiempo_llegada
        tiempo_actual += proceso.tiempo_ejecucion
    return procesos

def planificar_sjf(procesos):
    # Planifica los procesos utilizando la política SJF con desempate FIFO
    tiempo_actual = 0
    procesos_ordenados = sorted(procesos, key=lambda x: (x.tiempo_llegada, x.tiempo_ejecucion))
    procesos_planificados = []

    while procesos_ordenados:
        disponibles = [p for p in procesos_ordenados if p.tiempo_llegada <= tiempo_actual]
        if not disponibles:
            tiempo_actual += 1
            continue
        proceso_a_ejecutar = min(disponibles, key=lambda x: (x.tiempo_ejecucion, x.tiempo_llegada))
        procesos_ordenados.remove(proceso_a_ejecutar)

        proceso_a_ejecutar.inicio_ejecucion = max(tiempo_actual, proceso_a_ejecutar.tiempo_llegada)
        proceso_a_ejecutar.fin_ejecucion = proceso_a_ejecutar.inicio_ejecucion + proceso_a_ejecutar.tiempo_ejecucion
        proceso_a_ejecutar.tiempo_espera = proceso_a_ejecutar.inicio_ejecucion - proceso_a_ejecutar.tiempo_llegada
        tiempo_actual = proceso_a_ejecutar.fin_ejecucion

        procesos_planificados.append(proceso_a_ejecutar)

    return procesos_planificados

def mostrar_resultados(procesos):
    # Genera un DataFrame con los resultados y calcula métricas promedio.
    resultados = []
    for p in procesos:
        resultados.append({
            "ID Proceso": p.id_proceso,
            "Tiempo de Llegada": p.tiempo_llegada,
            "Tiempo de Ejecución": p.tiempo_ejecucion,
            "Inicio de Ejecución": p.inicio_ejecucion,
            "Finalización": p.fin_ejecucion,
            "Tiempo de Espera": p.tiempo_espera,
            "Tiempo en el Sistema": p.fin_ejecucion - p.tiempo_llegada,
        })

    df_resultados = pd.DataFrame(resultados)
    promedio_espera = df_resultados["Tiempo de Espera"].mean()
    promedio_tiempo_sistema = df_resultados["Tiempo en el Sistema"].mean()

    return df_resultados, promedio_espera, promedio_tiempo_sistema
