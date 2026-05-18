import tkinter as tk
from tkinter import ttk

def limpiar_campos():
    # Borra el contenido de todos los Entry en la ventana
    for widget in window.winfo_children():
        if isinstance(widget, tk.LabelFrame):
            for child in widget.winfo_children():
                if isinstance(child, tk.Entry):
                    child.delete(0, tk.END)

def aceptar_datos():
    # Aquí podrías agregar la lógica para procesar la información
    print("Datos guardados correctamente.")

# Configuración de la ventana principal
window = tk.Tk()
window.title("Formulario Cliente")
window.geometry("400x450")

# --- FRAME: DATOS DEL CLIENTE ---
frame_cliente = tk.LabelFrame(window, text="Datos del Cliente", padx=10, pady=10)
frame_cliente.pack(padx=20, pady=10, fill="x")

# Campos Cliente
labels_cliente = ["Nombre:", "Email:", "Dirección:", "Comuna:", "Ciudad:"]
for i, texto in enumerate(labels_cliente):
    tk.Label(frame_cliente, text=texto).grid(row=i, column=0, sticky="w", pady=2)
    tk.Entry(frame_cliente, width=30).grid(row=i, column=1, pady=2)

# --- FRAME: PRODUCTOS ---
frame_productos = tk.LabelFrame(window, text="Productos", padx=10, pady=10)
frame_productos.pack(padx=20, pady=10, fill="x")

# Producto
tk.Label(frame_productos, text="Producto:").grid(row=0, column=0, sticky="w")
ent_prod = tk.Entry(frame_productos, width=30)
ent_prod.grid(row=0, column=1, pady=2, columnspan=3)

# Cantidad
tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, sticky="w")
ent_cant = tk.Entry(frame_productos, width=3)
ent_cant.grid(row=1, column=1, sticky="w", pady=2)

# Precio (en la misma fila que cantidad para optimizar espacio)
tk.Label(frame_productos, text="Precio:").grid(row=1, column=2, sticky="w", padx=(10, 0))
ent_precio = tk.Entry(frame_productos, width=6)
ent_precio.grid(row=1, column=3, sticky="w", pady=2)

# --- BOTONES ---
frame_botones = tk.Frame(window)
frame_botones.pack(pady=20)

btn_aceptar = tk.Button(frame_botones, text="Aceptar", width=10, command=aceptar_datos)
btn_aceptar.pack(side="left", padx=10)

btn_limpiar = tk.Button(frame_botones, text="Limpiar", width=10, command=limpiar_campos)
btn_limpiar.pack(side="left", padx=10)

window.mainloop()