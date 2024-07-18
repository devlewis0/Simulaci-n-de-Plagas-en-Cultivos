import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Función para ejecutar la simulación
def ejecutar_simulacion():
    num_dias = int(entry_num_dias.get())
    tamano_campo = int(entry_tamano_campo.get())
    tasa_reproduccion_plagas = float(entry_tasa_reproduccion_plagas.get())
    tasa_mortalidad_plagas = float(entry_tasa_mortalidad_plagas.get())
    num_plagas_iniciales = int(entry_num_plagas_iniciales.get())

    # Inicialización del campo y plagas
    campo = np.zeros((tamano_campo, tamano_campo))
    plagas = np.zeros((tamano_campo, tamano_campo))

    # Función para esparcir plagas iniciales
    def esparcir_plagas(plagas, num_plagas_iniciales):
        for _ in range(num_plagas_iniciales):
            x = np.random.randint(0, tamano_campo)
            y = np.random.randint(0, tamano_campo)
            plagas[x, y] += 1

    # Esparcir plagas iniciales
    esparcir_plagas(plagas, num_plagas_iniciales)

    # Listas para almacenar los resultados
    poblacion_plagas = []

    # Simulación
    for dia in range(num_dias):
        nuevas_plagas = np.zeros((tamano_campo, tamano_campo))

        # Reproducción de plagas
        for i in range(tamano_campo):
            for j in range(tamano_campo):
                if plagas[i, j] > 0:
                    num_nuevas_plagas = np.random.poisson(tasa_reproduccion_plagas * plagas[i, j])
                    nuevas_plagas[i, j] += num_nuevas_plagas

        # Mortalidad de plagas
        for i in range(tamano_campo):
            for j in range(tamano_campo):
                if plagas[i, j] > 0:
                    num_muertas = np.random.binomial(plagas[i, j], tasa_mortalidad_plagas)
                    plagas[i, j] -= num_muertas

        # Actualización de plagas
        plagas += nuevas_plagas

        # Registro de la población de plagas
        poblacion_plagas.append(np.sum(plagas))

    # Crear las figuras de Matplotlib
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    ax[0].imshow(campo, cmap='Greens')
    ax[0].set_title('Campo Inicial')

    ax[1].imshow(plagas, cmap='Reds')
    ax[1].set_title(f'Plagas después de {num_dias} días')

    ax[2].plot(poblacion_plagas, label='Población de Plagas')
    ax[2].set_xlabel('Días')
    ax[2].set_ylabel('Número de Plagas')
    ax[2].set_title('Simulación de Plagas en Cultivos')
    ax[2].legend()
    ax[2].grid(True)

    plt.tight_layout()

    # Mostrar las figuras en el Tkinter canvas
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_resultados)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Simulación de Plagas en Cultivos")

# Crear el frame principal
frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=1)

# Crear el frame para los inputs
frame_inputs = tk.Frame(frame_principal, padx=10, pady=10)
frame_inputs.pack(side=tk.LEFT, fill=tk.Y)

# Crear el frame para los resultados
frame_resultados = tk.Frame(frame_principal, padx=10, pady=10)
frame_resultados.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# Instructivo
instructivo = """Instructivo:
1. Número de días para la simulación: El número total de días que desea simular.
2. Tamaño del campo: El tamaño del campo en unidades (ejemplo: 100 para un campo de 100x100 unidades).
3. Tasa de reproducción diaria de las plagas: Un valor decimal que representa la tasa diaria de reproducción de las plagas (ejemplo: 0.05).
4. Tasa de mortalidad diaria de las plagas: Un valor decimal que representa la tasa diaria de mortalidad de las plagas (ejemplo: 0.01).
5. Número inicial de plagas: La cantidad inicial de plagas presentes en el campo.

Datos recomendados:
- Número de días: Puede basarse en la duración de la temporada de cultivo.
- Tamaño del campo: Puede basarse en el tamaño real del terreno.
- Tasa de reproducción y mortalidad: Puede consultarse con expertos agrónomos o basarse en estudios científicos.
- Número inicial de plagas: Puede estimarse observando el campo o consultando con especialistas en plagas.

Ingrese los datos y presione "Ejecutar Simulación" para ver los resultados.
"""

ttk.Label(frame_inputs, text=instructivo, wraplength=300).pack(pady=10)

# Creación de los campos de entrada
ttk.Label(frame_inputs, text="Número de días para la simulación:").pack(pady=5)
entry_num_dias = ttk.Entry(frame_inputs)
entry_num_dias.pack(pady=5)

ttk.Label(frame_inputs, text="Tamaño del campo (ej. 100 para 100x100):").pack(pady=5)
entry_tamano_campo = ttk.Entry(frame_inputs)
entry_tamano_campo.pack(pady=5)

ttk.Label(frame_inputs, text="Tasa de reproducción diaria de las plagas:").pack(pady=5)
entry_tasa_reproduccion_plagas = ttk.Entry(frame_inputs)
entry_tasa_reproduccion_plagas.pack(pady=5)

ttk.Label(frame_inputs, text="Tasa de mortalidad diaria de las plagas:").pack(pady=5)
entry_tasa_mortalidad_plagas = ttk.Entry(frame_inputs)
entry_tasa_mortalidad_plagas.pack(pady=5)

ttk.Label(frame_inputs, text="Número inicial de plagas:").pack(pady=5)
entry_num_plagas_iniciales = ttk.Entry(frame_inputs)
entry_num_plagas_iniciales.pack(pady=5)

# Botón para ejecutar la simulación
btn_simular = ttk.Button(frame_inputs, text="Ejecutar Simulación", command=ejecutar_simulacion)
btn_simular.pack(pady=10)

root.mainloop()
