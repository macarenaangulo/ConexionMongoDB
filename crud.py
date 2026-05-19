from conexion import obtener_db

# Inicializar la conexión a la base de datos (dinámica según tu archivo .env)
db = obtener_db()

def insertar_venta(datos_cliente, lista_productos):
    """
    C: CREATE - Inserta una venta con múltiples productos en la colección 'ventas'.
    Recibe un diccionario (cliente) y una lista de diccionarios (productos).
    """
    if db is None:
        print(f"No se puede insertar: No hay conexión a la base de datos.")
        return None
        
    try:
        # Estructuramos el documento final para MongoDB
        documento_venta = {
            "cliente": {
                "nombre": datos_cliente.get("nombre"),
                "email": datos_cliente.get("email"),
                "direccion": datos_cliente.get("direccion"),
                "comuna": datos_cliente.get("comuna"),
                "ciudad": datos_cliente.get("ciudad")
            },
            # Pasamos la lista completa de productos directamente. 
            # MongoDB la almacena de forma nativa como un arreglo (Array).
            "producto": lista_productos 
        }
        
        # Insertar en la colección 'ventas'
        resultado = db.ventas.insert_one(documento_venta)
        
        print(f"Venta multiproducto insertada con éxito. ID: {resultado.inserted_id}")
        return resultado.inserted_id

    except Exception as e:
        print(f"Error al intentar insertar el documento en MongoDB: {e}")
        return None