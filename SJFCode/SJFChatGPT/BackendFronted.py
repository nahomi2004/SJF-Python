import tkinter as tk 
#biblioteca estándar de Python para crear interfaces gráficas

from tkinter import ttk, messagebox
# submódulo que muestra cuadros de diálogo (ventanas emergentes) con mensajes.
# ttk: conjunto de widgets (componentes visuales) mejorados

import random
# simular tiempos de llegada y duración

import time
# simular una pausa durante la ejecución de procesos

# Trabajo con diccionario que representa a un proceso
def fifo_scheduling(processes):
    # Organiza los procesos por tiempo de llegada (FIFO)
    processes.sort(key=lambda x: x['arrival']) 
    # Reloj del sistema, comienza en 0
    current_time = 0
    # Lista para almacenar los procesos ejecutados con sus tiempos calculados
    result = []
    # Simula la ejecución en orden de llegada
    # Recorre todos los procesos
    for process in processes:
        # Calcular tiempos del proceso
        # Inicio de ejecución
        process['start'] = max(current_time, process['arrival'])
        #Fin de ejecución
        process['finish'] = process['start'] + process['burst']
        # Tiempo de espera
        process['wait'] = process['start'] - process['arrival']
        # Tiempo en el sistema
        process['turnaround'] = process['finish'] - process['arrival']
        result.append(process)
        # Actualiza el reloj del sistema
        current_time = process['finish']
    return result


def sjf_scheduling(processes):
    # organiza los procesos por tiempo de llegada y selecciona el de menor duración para ejecutar primero
    processes.sort(key=lambda x: (x['arrival'], x['burst']))
    # Reloj del sistema, comienza en 0
    current_time = 0 
    # Lista para almacenar los procesos ejecutados con sus tiempos calculados
    result = []
    # Mientras haya procesos pendientes
    while processes:
        # Elige a los procesos disponibles (tiempo de llegada menor o igual al tiempo actual)
        available = [p for p in processes if p['arrival'] <= current_time]
        if available:
            # Elegir el proceso con menor tiempo de ejecución, en caso de empate usa 'arrival'como criterio secundario
            process = min(available, key=lambda x: x['burst'])
            # Elimina el proceso que se acaba de seleccionar de la lista de procesos pendientes
            processes.remove(process)
            # Calcular tiempos del proceso seleccionado
            # Inicio
            process['start'] = max(current_time, process['arrival'])
            # Fin
            process['finish'] = process['start'] + process['burst']
            # Espera
            process['wait'] = process['start'] - process['arrival']
            # Tiempo de sistema
            process['turnaround'] = process['finish'] - process['arrival']
            result.append(process)
            # Actualiza el reloj del sistema
            current_time = process['finish']
        else:   
            # Avanzar el tiempo si no hay procesos disponibles
            current_time += 1
    return result


def simulate_execution(processes):
    # Simula la ejecución de los procesos uno por uno
    for process in processes:
        time.sleep(1)
        # Muestra en el log cómo se ejecuta cada proceso y actualiza la ventana
        log.insert(tk.END, f"Ejecutando {process['id']} desde {process['start']} hasta {process['finish']}\n")
        log.see(tk.END)
        root.update()


def calculate():
    # Obtiene el algoritmo seleccionado (FIFO o SJF) y los procesos de la tabla
    selected_algorithm = algorithm_var.get()
    # Validacion
    if not selected_algorithm:
        messagebox.showerror("Error", "Seleccione un algoritmo de planificación.")
        return

    # Crea una lista vacía
    processes = []
    # Recorre todas las filas (nodos) de un control tree
    for row in tree.get_children():
        # Devuelve un diccionario con información de la fila específica del arbol
        data = tree.item(row)['values']
        # Crea un diccionario para cada proceso
        # Y agrega este diccionario a la lista processes
        processes.append({
            'id': data[0],
            'arrival': int(data[1]),
            'burst': int(data[2])
        })

    # Llama a la función correspondiente
    if selected_algorithm == "FIFO":
        scheduled = fifo_scheduling(processes)
    elif selected_algorithm == "SJF":
        scheduled = sjf_scheduling(processes)

    # Simula la ejecución y muestra los resultados en otra tabla
    simulate_execution(scheduled)

    tree_result.delete(*tree_result.get_children())
    total_wait = 0
    total_turnaround = 0
    for process in scheduled:
        total_wait += process['wait']
        total_turnaround += process['turnaround']
        tree_result.insert("", "end", values=(
            process['id'], process['arrival'], process['burst'],
            process['start'], process['finish'], process['wait'], process['turnaround']
        ))
    avg_wait = total_wait / len(scheduled)
    avg_turnaround = total_turnaround / len(scheduled)
    messagebox.showinfo("Resultados", f"Tiempo de espera promedio: {avg_wait:.2f}\n"
                                       f"Tiempo en el sistema promedio: {avg_turnaround:.2f}")

# Crea una ventana emergente para ingresar un nuevo proceso.
def add_process():
    def save_process():
        arrival = int(entry_arrival.get())
        burst = int(entry_burst.get())
        process_id = f"P{len(tree.get_children()) + 1}"
        tree.insert("", "end", values=(process_id, arrival, burst))
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Agregar Proceso")
    popup.geometry("300x200")

    # Muestra automáticamente el ID del proceso
    tk.Label(popup, text="ID del Proceso:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(popup, text=f"P{len(tree.get_children()) + 1}").grid(row=0, column=1, padx=10, pady=10)

    # Permite ingresar:
    # Tiempo de llegada
    tk.Label(popup, text="Tiempo de Llegada:").grid(row=1, column=0, padx=10, pady=10)
    entry_arrival = tk.Entry(popup)
    entry_arrival.grid(row=1, column=1, padx=10, pady=10)

    # Duración del proceso
    tk.Label(popup, text="Duración:").grid(row=2, column=0, padx=10, pady=10)
    entry_burst = tk.Entry(popup)
    entry_burst.grid(row=2, column=1, padx=10, pady=10)

    # Al guardar, el proceso se agrega a la tabla principal
    btn_save = tk.Button(popup, text="Guardar", command=save_process)
    btn_save.grid(row=3, columnspan=2, pady=10)


# Genera automáticamente 5 procesos con tiempos de llegada y duración aleatorios
def generate_processes():
    tree.delete(*tree.get_children())
    for i in range(5):
        arrival = random.randint(0, 10)
        burst = random.randint(1, 10)
        tree.insert("", "end", values=(f"P{i + 1}", arrival, burst))


# Crea la ventana principal de la aplicación
root = tk.Tk()
# Define el título y el tamaño de la ventana
root.title("Simulador de Planificación")
root.geometry("900x700")

# Variable para almacenar el algoritmo seleccionado
algorithm_var = tk.StringVar()

frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, pady=10)

# Menú desplegable para elegir entre FIFO y SJF
tk.Label(frame_top, text="Seleccione el Algoritmo:").pack(side=tk.LEFT, padx=10)
algorithm_menu = ttk.Combobox(frame_top, textvariable=algorithm_var, state="readonly")
algorithm_menu['values'] = ["FIFO", "SJF"]
algorithm_menu.pack(side=tk.LEFT, padx=10)

btn_calculate = tk.Button(frame_top, text="Calcular", command=calculate)
btn_calculate.pack(side=tk.LEFT, padx=10)

frame_middle = tk.Frame(root)
frame_middle.pack(fill=tk.BOTH, expand=True, pady=10)

# Crea una tabla para mostrar los procesos
columns = ("ID", "Llegada", "Duración")
tree = ttk.Treeview(frame_middle, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_y = ttk.Scrollbar(frame_middle, orient="vertical", command=tree.yview)
tree.configure(yscroll=scroll_y.set)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Botones
frame_buttons = tk.Frame(root)
frame_buttons.pack(fill=tk.X, pady=10)

# Abre una ventana para ingresar manualmente un proceso
btn_add = tk.Button(frame_buttons, text="Agregar Proceso", command=add_process)
btn_add.pack(side=tk.LEFT, padx=5)

# Genera procesos aleatorios
btn_generate = tk.Button(frame_buttons, text="Generar Automáticamente", command=generate_processes)
btn_generate.pack(side=tk.LEFT, padx=5)

# Muestra un registro en tiempo real de cómo se ejecutan los procesos
log = tk.Text(root, height=10, bg="black", fg="white")
log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

frame_bottom = tk.Frame(root)
frame_bottom.pack(fill=tk.BOTH, expand=True)

# Tabla para mostrar los resultados después de ejecutar todos los procesos
columns_result = ("ID", "Llegada", "Duración", "Inicio", "Fin", "Espera", "Sistema")
tree_result = ttk.Treeview(frame_bottom, columns=columns_result, show='headings')
for col in columns_result:
    tree_result.heading(col, text=col)
tree_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_result_y = ttk.Scrollbar(frame_bottom, orient="vertical", command=tree_result.yview)
tree_result.configure(yscroll=scroll_result_y.set)
scroll_result_y.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
