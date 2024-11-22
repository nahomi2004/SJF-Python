import random
import pandas as pd

class Proceso:
    def __init__(self, id_proceso, tiempo_llegada, tiempo_ejecucion):
        self.id_proceso = id_proceso
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.inicio_ejecucion = 0
        self.fin_ejecucion = 0
        self.tiempo_espera = 0

def generar_procesos(num_procesos):
    procesos = []
    for i in range(num_procesos):
        tiempo_llegada = random.randint(0, 10)
        tiempo_ejecucion = random.randint(1, 10)
        procesos.append(Proceso(i + 1, tiempo_llegada, tiempo_ejecucion))
    return procesos

def planificar_sjf(procesos):
    tiempo_actual = 0
    procesos.sort(key=lambda x: (x.tiempo_llegada, x.tiempo_ejecucion))

    for proceso in procesos:
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada

        proceso.inicio_ejecucion = tiempo_actual
        proceso.fin_ejecucion = tiempo_actual + proceso.tiempo_ejecucion
        proceso.tiempo_espera = proceso.inicio_ejecucion - proceso.tiempo_llegada

        tiempo_actual += proceso.tiempo_ejecucion

    return procesos

def mostrar_resultados(procesos):
    resultados = []
    for p in procesos:
        resultados.append({
            "ID": p.id_proceso,
            "Tiempo de Llegada": p.tiempo_llegada,
            "Tiempo de Ejecución": p.tiempo_ejecucion,
            "Inicio de Ejecución": p.inicio_ejecucion,
            "Fin de Ejecución": p.fin_ejecucion,
            "Tiempo de Espera": p.tiempo_espera,
        })

    df_resultados = pd.DataFrame(resultados)
    print(df_resultados)
    print(f"Tiempo de Espera Promedio: {df_resultados['Tiempo de Espera'].mean()}")

# Ejemplo de uso
num_procesos = 5
procesos_generados = generar_procesos(num_procesos)
procesos_planificados = planificar_sjf(procesos_generados)
mostrar_resultados(procesos_planificados)