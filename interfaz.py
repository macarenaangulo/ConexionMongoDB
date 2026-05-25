import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Importamos todas las funciones desde tu módulo crud.py
from crud import *

campos_cliente = {}
campos_producto = {}

# LISTA EN MEMORIA OCULTA PARA LOGRAR EL MULTI-PRODUCTO DE FORMA SIMPLE
productos_acumulados_memoria = []

# Variables globales para los componentes de la interfaz
txt_resultados = None
ent_buscar_nombre = None
ent_id_control = None
ent_item_eliminar = None
ent_nueva_dir = None
ent_nueva_com = None
ent_nueva_ciu = None
lbl_contador = None  # Etiqueta para avisar cuántos productos van acumulados

def limpiar_formulario_producto():
    """Limpia exclusivamente las cajas de texto de la zona de productos"""
    campos_producto["item"].delete(0, tk.END)
    campos_producto["cantidad"].delete(0, tk.END)
    campos_producto["precio"].delete(0, tk.END)

def limpiar_campos_completo():
    """Limpia todo el formulario, los controles y vacía la lista temporal de memoria"""
    global productos_acumulados_memoria, lbl_contador
    for entry in campos_cliente.values():
        entry.delete(0, tk.END)
    limpiar_formulario_producto()
    ent_id_control.delete(0, tk.END)
    ent_item_eliminar.delete(0, tk.END)
    ent_nueva_dir.delete(0, tk.END)
    ent_nueva_com.delete(0, tk.END)
    ent_nueva_ciu.delete(0, tk.END)
    
    # Reseteamos la memoria temporal
    productos_acumulados_memoria = []
    if lbl_contador:
        lbl_contador.config(text="Productos listos para guardar: 0", fg="black")

def agregar_producto_a_memoria():
    """Acción del nuevo botón: Valida el producto actual y lo suma a la lista temporal"""
    global productos_acumulados_memoria, lbl_contador
    
    item = campos_producto["item"].get().strip()
    try:
        cantidad = int(campos_producto["cantidad"].get().strip() or 0)
        precio = int(campos_producto["precio"].get().strip() or 0)
    except ValueError:
        messagebox.showerror("Error", "Cantidad y Precio deben ser números enteros.")
        return

    if not item or cantidad <= 0 or precio <= 0:
        messagebox.showwarning("Atención", "Escriba el nombre del producto y asigne cantidad/precio válidos.")
        return

    # Añadimos el producto a nuestra lista provisional en Python
    productos_acumulados_memoria.append({
        "item": item,
        "cantidad": cantidad,
        "precio": precio
    })

    # Actualizamos el aviso visual para el usuario
    lbl_contador.config(text=f"Productos listos para guardar: {len(productos_acumulados_memoria)}", fg="#2196F3", font=('Helvetica', 9, 'bold'))
    
    # Limpiamos las casillas de producto para que escriba el siguiente cómodamente
    limpiar_formulario_producto()

def aceptar_datos():
    """Toma los datos del cliente, une el producto que quede en pantalla (si hay) e inserta todo"""
    global productos_acumulados_memoria
    
    datos_cliente = {
        "nombre": campos_cliente["Nombre:"].get().strip(),
        "email": campos_cliente["Email:"].get().strip(),
        "direccion": campos_cliente["Dirección:"].get().strip(),
        "comuna": campos_cliente["Comuna:"].get().strip(),
        "ciudad": campos_cliente["Ciudad:"].get().strip()
    }
    
    if not datos_cliente["nombre"]:
        messagebox.showwarning("Atención", "Debe ingresar al menos el nombre del cliente.")
        return

    # Verificamos si el usuario dejó un último producto escrito en las casillas sin presionar el botón "Agregar más"
    ultimo_item = campos_producto["item"].get().strip()
    if ultimo_item:
        try:
            ultimo_cant = int(campos_producto["cantidad"].get().strip() or 0)
            ultimo_pre = int(campos_producto["precio"].get().strip() or 0)
            if ultimo_cant > 0 and ultimo_pre > 0:
                productos_acumulados_memoria.append({
                    "item": ultimo_item,
                    "cantidad": ultimo_cant,
                    "precio": ultimo_pre
                })
        except ValueError:
            pass

    # Si no hay absolutamente ningún producto acumulado, no procesamos la venta
    if not productos_acumulados_memoria:
        messagebox.showwarning("Atención", "Debe añadir al menos un producto a la venta.")
        return

    # Enviamos el documento estructurado a MongoDB
    id_generado = insertar_venta(datos_cliente, productos_acumulados_memoria)
    if id_generado:
        messagebox.showinfo("Éxito", f"Venta registrada con éxito.\nID: {id_generado}\nTotal de productos: {len(productos_acumulados_memoria)}")
        limpiar_campos_completo()
        buscar_todas()  # Refresca automáticamente el visor inferior
    else:
        messagebox.showerror("Error", "No se pudo conectar o guardar en MongoDB.")

def renderizar_lista_en_pantalla(lista_ventas):
    """Escribe los resultados de MongoDB estructuradamente en el visor de texto"""
    global txt_resultados
    if txt_resultados is None: return

    txt_resultados.config(state="normal")
    txt_resultados.delete("1.0", tk.END)
    
    if not lista_ventas:
        txt_resultados.insert(tk.END, "📭 No se encontraron ventas con los criterios seleccionados.")
        txt_resultados.config(state="disabled")
        return

    texto_final = ""
    for i, venta in enumerate(lista_ventas, 1):
        cliente = venta.get("cliente", {})
        productos = venta.get("producto", [])
        
        texto_final += f"🛒 Venta #{i} | ID único: {venta['_id']}\n"
        texto_final += f"👤 Cliente: {cliente.get('nombre', 'Sin nombre')}\n"
        
        dir_str = cliente.get('direccion', 'No especificada')
        com_str = cliente.get('comuna', 'No especificada')
        ciu_str = cliente.get('ciudad', 'No especificada')
        texto_final += f"📍 Ubicación: {dir_str}, {com_str}, {ciu_str}\n"
        
        texto_final += "📦 Productos en esta venta:\n"
        if isinstance(productos, list):
            for prod in productos:
                if isinstance(prod, dict):
                    texto_final += f"   - [{prod.get('item')}]: {prod.get('cantidad')} un. x ${prod.get('precio'):,}\n"
        elif isinstance(productos, dict):
            texto_final += f"   - [{productos.get('item')}]: {productos.get('cantidad')} un. x ${productos.get('precio'):,}\n"
        
        texto_final += "-" * 50 + "\n"
        
    txt_resultados.insert(tk.END, texto_final)
    txt_resultados.config(state="disabled")

def buscar_todas():
    """Trae absolutamente todas las ventas de la BD"""
    ventas = obtener_todas_ventas()
    renderizar_lista_en_pantalla(ventas)

def buscar_por_nombre_cliente():
    """Filtra las ventas en MongoDB por el nombre escrito arriba"""
    global ent_buscar_nombre
    nombre = ent_buscar_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Atención", "Escriba un nombre en la casilla para poder buscar.")
        return
    ventas_filtradas = buscar_ventas_por_nombre(nombre)
    renderizar_lista_en_pantalla(ventas_filtradas)

def ejecutar_modificacion_cliente():
    """Toma el ID, nueva dirección, comuna y ciudad y los guarda en MongoDB"""
    global ent_id_control, ent_nueva_dir, ent_nueva_com, ent_nueva_ciu
    id_ingresado = ent_id_control.get().strip()
    dir_ingresada = ent_nueva_dir.get().strip()
    com_ingresada = ent_nueva_com.get().strip()
    ciu_ingresada = ent_nueva_ciu.get().strip()

    if not id_ingresado or not dir_ingresada or not com_ingresada or not ciu_ingresada:
        messagebox.showwarning("Atención", "Complete todos los campos de ubicación (ID, Dirección, Comuna y Ciudad).")
        return

    if actualizar_datos_cliente(id_ingresado, dir_ingresada, com_ingresada, ciu_ingresada):
        messagebox.showinfo("Éxito", "Ubicación del cliente (Dirección, Comuna y Ciudad) actualizada en MongoDB.")
        ent_nueva_dir.delete(0, tk.END)
        ent_nueva_com.delete(0, tk.END)
        ent_nueva_ciu.delete(0, tk.END)
        buscar_todas()
    else:
        messagebox.showerror("Error", "No se pudo actualizar. Verifique el ID de la venta.")

def ejecutar_eliminacion_completa():
    """Elimina el documento entero de MongoDB"""
    global ent_id_control
    id_ingresado = ent_id_control.get().strip()

    if not id_ingresado:
        messagebox.showwarning("Atención", "Ingrese el ID de la venta para poder eliminar.")
        return

    if messagebox.askyesno("Confirmar", f"¿Desea eliminar PERMANENTEMENTE toda la venta ID: {id_ingresado}?"):
        if eliminar_venta_por_id(id_ingresado):
            messagebox.showinfo("Éxito", "Venta eliminada por completo.")
            ent_id_control.delete(0, tk.END)
            buscar_todas()
        else:
            messagebox.showerror("Error", "ID no encontrado o inválido.")

def ejecutar_eliminacion_item():
    """Remueve únicamente el producto especificado dentro del arreglo del documento"""
    global ent_id_control, ent_item_eliminar
    id_ingresado = ent_id_control.get().strip()
    producto_ingresado = ent_item_eliminar.get().strip()

    if not id_ingresado or not producto_ingresado:
        messagebox.showwarning("Atención", "Debe completar el 'ID Venta' y el 'Producto' para remover el ítem.")
        return

    if messagebox.askyesno("Confirmar", f"¿Desea sacar el producto [{producto_ingresado}] de la venta {id_ingresado}?"):
        if eliminar_item_de_lista(id_ingresado, producto_ingresado):
            messagebox.showinfo("Éxito", f"Producto '{producto_ingresado}' removido correctamente.")
            ent_item_eliminar.delete(0, tk.END)
            buscar_todas()
        else:
            messagebox.showerror("Error", "No se modificó el registro. Verifique ID y Producto.")


# --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
window = tk.Tk()
window.title("Formulario Cliente y Ventas")
window.geometry("540x900")

# ==========================================
# FRAME 1: PARTE SUPERIOR (CONSULTAS)
# ==========================================
frame_busqueda = tk.LabelFrame(window, text=" Consultas y Filtros ", padx=10, pady=10)
frame_busqueda.pack(padx=20, pady=5, fill="x")

btn_buscar_todos = tk.Button(frame_busqueda, text="📋 Mostrar Todas las Ventas", command=buscar_todas, bg="#607D8B", fg="white")
btn_buscar_todos.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))

tk.Label(frame_busqueda, text="Nombre Cliente:").grid(row=1, column=0, sticky="w")
ent_buscar_nombre = tk.Entry(frame_busqueda, width=22)
ent_buscar_nombre.grid(row=1, column=1, padx=5)

btn_buscar_filtro = tk.Button(frame_busqueda, text="🔍 Filtrar", command=buscar_por_nombre_cliente, bg="#9C27B0", fg="white")
btn_buscar_filtro.grid(row=1, column=2, sticky="ew")
frame_busqueda.columnconfigure(1, weight=1)

# ==========================================
# FRAME 2: PARTE CENTRAL (FORMULARIO DE REGISTRO)
# ==========================================
frame_cliente = tk.LabelFrame(window, text="Datos del Cliente", padx=10, pady=5)
frame_cliente.pack(padx=20, pady=5, fill="x")

labels_cliente = ["Nombre:", "Email:", "Dirección:", "Comuna:", "Ciudad:"]
for i, texto in enumerate(labels_cliente):
    tk.Label(frame_cliente, text=texto).grid(row=i, column=0, sticky="w", pady=2)
    entry = tk.Entry(frame_cliente, width=30)
    entry.grid(row=i, column=1, pady=2)
    campos_cliente[texto] = entry

# SECCIÓN PRODUCTOS REFORMULADA CON EL NUEVO BOTÓN LATERAL
frame_productos = tk.LabelFrame(window, text=" Carga de Productos ", padx=10, pady=5)
frame_productos.pack(padx=20, pady=5, fill="x")

tk.Label(frame_productos, text="Producto:").grid(row=0, column=0, sticky="w")
ent_prod = tk.Entry(frame_productos, width=22)
ent_prod.grid(row=0, column=1, pady=2, sticky="w")
campos_producto["item"] = ent_prod

# NUEVO BOTÓN: Ubicado a la derecha de las casillas de producto
btn_mas_productos = tk.Button(frame_productos, text="➕ Agregar más productos", command=agregar_producto_a_memoria, bg="#2196F3", fg="white", font=('Helvetica', 8, 'bold'))
btn_mas_productos.grid(row=0, column=2, rowspan=2, padx=10, sticky="nsew", pady=2)

tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, sticky="w")
ent_cant = tk.Entry(frame_productos, width=5)
ent_cant.grid(row=1, column=1, pady=2, sticky="w")
campos_producto["cantidad"] = ent_cant

tk.Label(frame_productos, text="Precio:").grid(row=2, column=0, sticky="w")
ent_precio = tk.Entry(frame_productos, width=10)
ent_precio.grid(row=2, column=1, pady=2, sticky="w")
campos_producto["precio"] = ent_precio

# NUEVA ETIQUETA INFORMATIVA: Indica cuántos artículos van acumulados en memoria temporal
lbl_contador = tk.Label(frame_productos, text="Productos listos para guardar: 0", font=('Helvetica', 9, 'italic'))
lbl_contador.grid(row=3, column=0, columnspan=3, pady=4, sticky="w")

frame_botones = tk.Frame(window)
frame_botones.pack(pady=10)
tk.Button(frame_botones, text="Limpiar Todo", width=12, command=limpiar_campos_completo).pack(side="left", padx=10)
tk.Button(frame_botones, text="Aceptar", width=12, command=aceptar_datos, bg="#4CAF50", fg="white", font=('Helvetica', 9, 'bold')).pack(side="left", padx=10)


# ==========================================
# SECCIÓN: ELIMINACION Y MODIFICACIÓN
# ==========================================
frame_modificaciones = tk.LabelFrame(window, text=" Eliminación y Modificación ", padx=10, pady=10)
frame_modificaciones.pack(fill="x", padx=20, pady=5)

tk.Label(frame_modificaciones, text="ID Venta:").grid(row=0, column=0, sticky="w", pady=2)
ent_id_control = tk.Entry(frame_modificaciones, width=22)
ent_id_control.grid(row=0, column=1, padx=5, pady=2, sticky="w")

btn_borrar_doc = tk.Button(frame_modificaciones, text="🗑️ Borrar Venta Completa", command=ejecutar_eliminacion_completa, bg="#b71c1c", fg="white", font=('Helvetica', 8))
btn_borrar_doc.grid(row=0, column=2, sticky="ew", padx=2, pady=2)

tk.Label(frame_modificaciones, text="Producto:").grid(row=1, column=0, sticky="w", pady=2)
ent_item_eliminar = tk.Entry(frame_modificaciones, width=22)
ent_item_eliminar.grid(row=1, column=1, padx=5, pady=2, sticky="w")

btn_borrar_item = tk.Button(frame_modificaciones, text="❌ Sacar Solo este Ítem", command=ejecutar_eliminacion_item, bg="#e65100", fg="white", font=('Helvetica', 8))
btn_borrar_item.grid(row=1, column=2, sticky="ew", padx=2, pady=2)

tk.Label(frame_modificaciones, text="Nueva Dirección:").grid(row=2, column=0, sticky="w", pady=2)
ent_nueva_dir = tk.Entry(frame_modificaciones, width=22)
ent_nueva_dir.grid(row=2, column=1, padx=5, pady=2, sticky="w")

btn_editar_cliente = tk.Button(frame_modificaciones, text="📝 Editar Ubicación\n(Dirección/Comuna/Ciudad)", command=ejecutar_modificacion_cliente, bg="#1e88e5", fg="white", font=('Helvetica', 8, 'bold'))
btn_editar_cliente.grid(row=2, column=2, rowspan=3, sticky="nsew", padx=2, pady=2)

tk.Label(frame_modificaciones, text="Nueva Comuna:").grid(row=3, column=0, sticky="w", pady=2)
ent_nueva_com = tk.Entry(frame_modificaciones, width=22)
ent_nueva_com.grid(row=3, column=1, padx=5, pady=2, sticky="w")

tk.Label(frame_modificaciones, text="Nueva Ciudad:").grid(row=4, column=0, sticky="w", pady=2)
ent_nueva_ciu = tk.Entry(frame_modificaciones, width=22)
ent_nueva_ciu.grid(row=4, column=1, padx=5, pady=2, sticky="w")

frame_modificaciones.columnconfigure(2, weight=1)


# ==========================================
# FRAME 3: PARTE INFERIOR (DESPLIEGUE DE VENTAS)
# ==========================================
frame_resultados = tk.LabelFrame(window, text=" Ventas Encontradas ", padx=10, pady=5)
frame_resultados.pack(padx=20, pady=5, fill="both", expand=True)

scroll_y = tk.Scrollbar(frame_resultados)
scroll_y.pack(side="right", fill="y")

txt_resultados = tk.Text(frame_resultados, height=8, yscrollcommand=scroll_y.set, font=('Consolas', 9))
txt_resultados.pack(fill="both", expand=True)
scroll_y.config(command=txt_resultados.yview)

txt_resultados.config(state="disabled")

window.mainloop()