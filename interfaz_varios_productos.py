import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Importamos la función de inserción desde nuestro módulo crud.py
from crud_varios_productos import insertar_venta 

# Diccionarios globales para almacenar las referencias a los Entry de datos
campos_cliente = {}
campos_producto = {}

# Lista en memoria para almacenar los productos agregados temporalmente
lista_productos_memoria = []

def limpiar_campos_completos():
    """Borra absolutamente todo el formulario y vacía la tabla de productos"""
    global lista_productos_memoria
    for entry in campos_cliente.values():
        entry.delete(0, tk.END)
    limpiar_formulario_producto()
    
    # Vaciar lista en memoria y limpiar el Treeview
    lista_productos_memoria = []
    for item in tabla_productos.get_children():
        tabla_productos.delete(item)

def limpiar_formulario_producto():
    """Limpia sólo los campos del bloque Producto para poder escribir uno nuevo"""
    campos_producto["item"].delete(0, tk.END)
    campos_producto["cantidad"].delete(0, tk.END)
    campos_producto["precio"].delete(0, tk.END)

def agregar_producto_a_lista():
    """Valida el producto actual y lo añade a la tabla visual y a la memoria"""
    item = campos_producto["item"].get().strip()
    cantidad_str = campos_producto["cantidad"].get().strip()
    precio_str = campos_producto["precio"].get().strip()
    
    if not item or not cantidad_str or not precio_str:
        messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos del producto.")
        return
        
    try:
        cantidad = int(cantidad_str)
        precio = int(precio_str)
    except ValueError:
        messagebox.showerror("Error de tipo", "Cantidad y Precio deben ser números enteros.")
        return

    # Calcular subtotal para mostrarlo en la tabla
    subtotal = cantidad * precio
    
    # 1. Agregar a la lista interna en memoria
    lista_productos_memoria.append({
        "item": item,
        "cantidad": cantidad,
        "precio": precio
    })
    
    # 2. Insertar visualmente en el Treeview (tabla en pantalla)
    tabla_productos.insert("", tk.END, values=(item, cantidad, f"${precio:,}", f"${subtotal:,}"))
    
    # Limpiar solo el bloque de producto para que ingresen el siguiente de forma cómoda
    limpiar_formulario_producto()

def enviar_venta_final():
    """Recupera los datos del cliente y el arreglo de productos para enviarlo al CRUD"""
    datos_cliente = {
        "nombre": campos_cliente["Nombre:"].get().strip(),
        "email": campos_cliente["Email:"].get().strip(),
        "direccion": campos_cliente["Dirección:"].get().strip(),
        "comuna": campos_cliente["Comuna:"].get().strip(),
        "ciudad": campos_cliente["Ciudad:"].get().strip()
    }
    
    # Validaciones fundamentales
    if not datos_cliente["nombre"]:
        messagebox.showwarning("Campos vacíos", "El Nombre del cliente es obligatorio.")
        return
        
    if not lista_productos_memoria:
        messagebox.showwarning("Sin productos", "Debe agregar al menos un producto a la lista antes de guardar.")
        return

    # Llamar al módulo CRUD enviando la lista (array) de productos directamente
    id_generado = insertar_venta(datos_cliente, lista_productos_memoria)
    
    if id_generado:
        messagebox.showinfo("Éxito", f"Venta registrada exitosamente con {len(lista_productos_memoria)} productos.\nID: {id_generado}")
        limpiar_campos_completos()
    else:
        messagebox.showerror("Error", "No se pudo guardar la venta. Revise la consola del sistema.")


# --- CONFIGURACIÓN VENTANA PRINCIPAL ---
window = tk.Tk()
window.title("Formulario de Ventas Multi-Producto")
window.geometry("460x650") # Ampliado para dar espacio a la tabla

# --- FRAME: DATOS DEL CLIENTE ---
frame_cliente = tk.LabelFrame(window, text="Datos del Cliente", padx=10, pady=10)
frame_cliente.pack(padx=20, pady=10, fill="x")

labels_cliente = ["Nombre:", "Email:", "Dirección:", "Comuna:", "Ciudad:"]
for i, texto in enumerate(labels_cliente):
    tk.Label(frame_cliente, text=texto).grid(row=i, column=0, sticky="w", pady=2)
    entry = tk.Entry(frame_cliente, width=35)
    entry.grid(row=i, column=1, pady=2)
    campos_cliente[texto] = entry

# --- FRAME: ENTRADA DE PRODUCTOS ---
frame_productos = tk.LabelFrame(window, text="Ingreso de Productos", padx=10, pady=10)
frame_productos.pack(padx=20, pady=5, fill="x")

tk.Label(frame_productos, text="Producto:").grid(row=0, column=0, sticky="w")
ent_prod = tk.Entry(frame_productos, width=35)
ent_prod.grid(row=0, column=1, pady=2, columnspan=3)
campos_producto["item"] = ent_prod

tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, sticky="w")
ent_cant = tk.Entry(frame_productos, width=5)
ent_cant.grid(row=1, column=1, sticky="w", pady=2)
campos_producto["cantidad"] = ent_cant

tk.Label(frame_productos, text="Precio:").grid(row=1, column=2, sticky="w", padx=5)
ent_precio = tk.Entry(frame_productos, width=12)
ent_precio.grid(row=1, column=3, sticky="w", pady=2)
campos_producto["precio"] = ent_precio

# Botón intermedio para añadir ítems a la tabla
btn_add_prod = tk.Button(frame_productos, text="➕ Agregar Producto a Lista", command=agregar_producto_a_lista, bg="#2196F3", fg="white")
btn_add_prod.grid(row=2, column=0, columnspan=4, pady=8, sticky="ew")

# --- FRAME: LISTA / DETALLE DE LA VENTA ---
frame_tabla = tk.LabelFrame(window, text="Detalle de Productos Agregados", padx=10, pady=10)
frame_tabla.pack(padx=20, pady=5, fill="both", expand=True)

# Configurar columnas de la tabla visual
columnas = ("producto", "cantidad", "precio", "subtotal")
tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=5)

tabla_productos.heading("producto", text="Producto")
tabla_productos.heading("cantidad", text="Cant.")
tabla_productos.heading("precio", text="Precio Unit.")
tabla_productos.heading("subtotal", text="Subtotal")

tabla_productos.column("producto", width=160, anchor="w")
tabla_productos.column("cantidad", width=50, anchor="center")
tabla_productos.column("precio", width=80, anchor="e")
tabla_productos.column("subtotal", width=80, anchor="e")
tabla_productos.pack(fill="both", expand=True)

# --- FRAME: ACCIONES FINALES ---
frame_botones = tk.Frame(window)
frame_botones.pack(padx=20, pady=15, fill="x")

btn_limpiar = tk.Button(frame_botones, text="Limpiar Todo", command=limpiar_campos_completos, width=15)
btn_limpiar.pack(side="left", padx=5)

btn_aceptar = tk.Button(frame_botones, text="Registrar Venta", command=enviar_venta_final, width=18, bg="#4CAF50", fg="white")
btn_aceptar.pack(side="right", padx=5)

window.mainloop()