import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Para mostrar alertas de éxito o error

# Importamos la función de inserción desde nuestro módulo crud.py
from crud_varios_productos import insertar_venta 

# Diccionarios globales para almacenar las referencias a los Entry
campos_cliente = {}
campos_producto = {}

def limpiar_campos():
    """Borra el contenido de todos los Entry usando las referencias guardadas"""
    for entry in campos_cliente.values():
        entry.delete(0, tk.END)
    for entry in campos_producto.values():
        entry.delete(0, tk.END)

def aceptar_datos():
    """Recupera los datos de la interfaz, los estructura e invoca al CRUD"""
    # 1. Extraer los datos del cliente desde la interfaz
    datos_cliente = {
        "nombre": campos_cliente["Nombre:"].get().strip(),
        "email": campos_cliente["Email:"].get().strip(),
        "direccion": campos_cliente["Dirección:"].get().strip(),
        "comuna": campos_cliente["Comuna:"].get().strip(),
        "ciudad": campos_cliente["Ciudad:"].get().strip()
    }
    
    # 2. Extraer y validar los datos del producto
    try:
        cantidad_str = campos_producto["cantidad"].get().strip()
        precio_str = campos_producto["precio"].get().strip()
        
        # Convertimos a enteros para que en MongoDB se guarden como números y no como texto
        cantidad = int(cantidad_str) if cantidad_str else 0
        precio = int(precio_str) if precio_str else 0
    except ValueError:
        messagebox.showerror("Error de validación", "Cantidad y Precio deben ser valores numéricos enteros.")
        return

    datos_producto = {
        "item": campos_producto["item"].get().strip(),
        "cantidad": cantidad,
        "precio": precio
    }
    
    # Validar que al menos los campos obligatorios no estén vacíos
    if not datos_cliente["nombre"] or not datos_producto["item"]:
        messagebox.showwarning("Campos vacíos", "Por favor, complete al menos el Nombre del cliente y el Producto.")
        return

    # 3. Llamar al módulo CRUD para insertar el documento en MongoDB
    id_generado = insertar_venta(datos_cliente, datos_producto)
    
    # 4. Mostrar feedback al usuario según el resultado
    if id_generado:
        messagebox.showinfo("Éxito", f"Registro insertado correctamente en MongoDB.\nID generado: {id_generado}")
        limpiar_campos()  # Limpia el formulario tras un registro exitoso
    else:
        messagebox.showerror("Error", "No se pudo guardar el registro. Verifique la conexión en la consola.")

# Configuración de la ventana principal
window = tk.Tk()
window.title("Formulario Cliente - Tienda Online")
window.geometry("400x480")

# --- FRAME: DATOS DEL CLIENTE ---
frame_cliente = tk.LabelFrame(window, text="Datos del Cliente", padx=10, pady=10)
frame_cliente.pack(padx=20, pady=10, fill="x")

# Campos Cliente (Guardando la referencia en el diccionario 'campos_cliente')
labels_cliente = ["Nombre:", "Email:", "Dirección:", "Comuna:", "Ciudad:"]
for i, texto in enumerate(labels_cliente):
    tk.Label(frame_cliente, text=texto).grid(row=i, column=0, sticky="w", pady=2)
    entry = tk.Entry(frame_cliente, width=30)
    entry.grid(row=i, column=1, pady=2)
    campos_cliente[texto] = entry # El label sirve de clave para recuperar el widget después

# --- FRAME: PRODUCTOS ---
frame_productos = tk.LabelFrame(window, text="Productos", padx=10, pady=10)
frame_productos.pack(padx=20, pady=10, fill="x")

# Producto
tk.Label(frame_productos, text="Producto:").grid(row=0, column=0, sticky="w")
ent_prod = tk.Entry(frame_productos, width=30)
ent_prod.grid(row=0, column=1, pady=2, columnspan=3)
campos_producto["item"] = ent_prod

# Cantidad
tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, sticky="w")
ent_cant = tk.Entry(frame_productos, width=5)
ent_cant.grid(row=1, column=1, sticky="w", pady=2)
campos_producto["cantidad"] = ent_cant

# Precio (en la misma fila que cantidad)
tk.Label(frame_productos, text="Precio:").grid(row=1, column=2, sticky="w", padx=5)
ent_precio = tk.Entry(frame_productos, width=10)
ent_precio.grid(row=1, column=3, sticky="w", pady=2)
campos_producto["precio"] = ent_precio

# --- FRAME: BOTONES DE ACCIÓN ---
frame_botones = tk.Frame(window)
frame_botones.pack(padx=20, pady=15, fill="x")

btn_limpiar = tk.Button(frame_botones, text="Limpiar Campos", command=limpiar_campos, width=15)
btn_limpiar.pack(side="left", padx=5)

# Asociamos el botón Aceptar con la lógica de inserción
btn_aceptar = tk.Button(frame_botones, text="Aceptar", command=aceptar_datos, width=15, bg="#4CAF50", fg="white")
btn_aceptar.pack(side="right", padx=5)

# Iniciar la aplicación
window.mainloop()