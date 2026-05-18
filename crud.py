from conexion import obtener_db

# Inicializar la conexión a la base de datos (dinámica según tu archivo .env)
db = obtener_db()

def insertar_venta(datos_cliente, datos_producto):
    """
    C: CREATE - Inserta un nuevo documento de venta en la colección 'ventas'.
    Recibe dos diccionarios y los guarda de forma estructurada.
    """
    # Validar que la conexión a MongoDB esté activa
    if db is None:
        print("No se puede insertar: No hay conexión a la base de datos.")
        return None
        
    try:
        # Estructuramos el documento final de MongoDB (Modelo Embebido)
        documento_venta = {
            "cliente": {
                "nombre": datos_cliente.get("nombre"),
                "email": datos_cliente.get("email"),
                "direccion": datos_cliente.get("direccion"),
                "comuna": datos_cliente.get("comuna"),
                "ciudad": datos_cliente.get("ciudad")
            },
            "producto": {
                "item": datos_producto.get("item"),
                "cantidad": datos_producto.get("cantidad"),
                "precio": datos_producto.get("precio")
            }
        }
        
        # Insertar el documento en la colección llamada 'ventas'
        # Si la colección no existe, MongoDB la crea automáticamente en este momento
        resultado = db.ventas.insert_one(documento_venta)
        
        # Imprimir confirmación en la consola del servidor
        print(f"Documento insertado con éxito. ID asignado por MongoDB: {resultado.inserted_id}")
        
        # Retornamos el _id autogenerado para que la interfaz pueda mostrarlo
        return resultado.inserted_id

    except Exception as e:
        print(f"Error al intentar insertar el documento en MongoDB: {e}")
        return None