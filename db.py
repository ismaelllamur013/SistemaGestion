import sqlite3

def conectar_db():
    try:
        conn = sqlite3.connect('base_prueba.db')  # Cambia esto si usas otro DB
        return conn
    except sqlite3.Error as e:
        print(f"Error de conexión: {e}")
        return None

def ejecutar_consulta(query, params=()):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error ejecutando consulta: {e}")
        finally:
            conn.close()

def obtener_datos(query, params=()):
    conn = conectar_db()
    datos = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            datos = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo datos: {e}")
        finally:
            conn.close()
    return datos
