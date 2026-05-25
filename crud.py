from conexion import obtener_db
from bson.objectid import ObjectId

db = obtener_db()

def insertar_venta(datos_cliente, lista_productos):
    """C: CREATE - Inserta una nueva venta con su lista acumulada de productos"""
    if db is None: return None
    try:
        documento = {
            "cliente": datos_cliente,
            "producto": lista_productos
        }
        resultado = db.ventas.insert_one(documento)
        return resultado.inserted_id
    except Exception as e:
        print(f"❌ Error al insertar: {e}")
        return None

def obtener_todas_ventas():
    """R: READ - Trae todos los registros"""
    if db is None: return []
    try:
        return list(db.ventas.find())
    except Exception as e:
        print(f"❌ Error al leer la base de datos: {e}")
        return []

def buscar_ventas_por_nombre(nombre_buscado):
    """R: READ con Filtro - Filtra por nombre"""
    if db is None: return []
    try:
        filtro = {"cliente.nombre": {"$regex": nombre_buscado, "$options": "i"}}
        return list(db.ventas.find(filtro))
    except Exception as e:
        print(f"❌ Error al filtrar por nombre: {e}")
        return []

def eliminar_venta_por_id(id_venta):
    """D: DELETE - Elimina un documento completo"""
    if db is None: return False
    try:
        resultado = db.ventas.delete_one({"_id": ObjectId(id_venta)})
        return resultado.deleted_count > 0
    except Exception as e:
        print(f"❌ Error al intentar eliminar: {e}")
        return False

def eliminar_item_de_lista(id_venta, nombre_producto):
    """U: UPDATE ($pull) - Saca un producto del arreglo"""
    if db is None: return False
    try:
        resultado = db.ventas.update_one(
            {"_id": ObjectId(id_venta)},
            {"$pull": {"producto": {"item": nombre_producto}}}
        )
        return resultado.modified_count > 0
    except Exception as e:
        print(f"❌ Error al modificar el arreglo: {e}")
        return False

def actualizar_datos_cliente(id_venta, nueva_direccion, nueva_comuna, nueva_ciudad):
    """U: UPDATE ($set) - Modifica Dirección, Comuna y Ciudad"""
    if db is None: return False
    try:
        resultado = db.ventas.update_one(
            {"_id": ObjectId(id_venta)},
            {
                "$set": {
                    "cliente.direccion": nueva_direccion,
                    "cliente.comuna": nueva_comuna,
                    "cliente.ciudad": nueva_ciudad
                }
            }
        )
        return resultado.matched_count > 0
    except Exception as e:
        print(f"❌ Error al actualizar los datos del cliente: {e}")
        return False