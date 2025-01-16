from db import ejecutar_consulta, obtener_datos

# Funciones para manejar Clientes
def insertar_cliente(nombre, cuit="", direccion="", tipo_cliente=""):
    query = "INSERT INTO Cliente (Nombre, CUIT, direccion,tipo_cliente) VALUES (?, ?, ?, ?)"
    ejecutar_consulta(query, (nombre, cuit, direccion,tipo_cliente))

def consultar_clientes(nombre=""):
    query = "SELECT * FROM Cliente WHERE Nombre LIKE ?"
    return obtener_datos(query, ('%' + nombre + '%',))

def modificar_cliente(id_cliente, nombre, cuit="", direccion="",tipo_cliente=""):
    query = "UPDATE Cliente SET Nombre = ?, CUIT = ?, direccion = ?, tipo_cliente = ? WHERE id_cliente = ?"
    ejecutar_consulta(query, (nombre, cuit, direccion,tipo_cliente,id_cliente))

def eliminar_cliente(id_cliente):
    query = "DELETE FROM Cliente WHERE id_cliente = ?"
    ejecutar_consulta(query, (id_cliente,))

# Funciones para manejar Tecnicos
def insertar_tecnico(nombre):
    query = "INSERT INTO Tecnico (Nombre) VALUES (?)"
    ejecutar_consulta(query, (nombre,))

def consultar_tecnicos(nombre=""):
    query = "SELECT * FROM Tecnico WHERE Nombre LIKE ?"
    return obtener_datos(query, ('%' + nombre + '%',))

def modificar_tecnico(id_tecnico, nombre):
    query = "UPDATE Tecnico SET Nombre = ? WHERE id_tecnico = ?"
    ejecutar_consulta(query, (nombre, id_tecnico))

def eliminar_tecnico(id_tecnico):
    query = "DELETE FROM Tecnico WHERE id_tecnico = ?"
    ejecutar_consulta(query, (id_tecnico,))

# Funciones para manejar Equipos
def insertar_equipo(id_cliente, marca, modelo, sn, tipo, categoria):
    query = "INSERT INTO Equipo (id_cliente, Marca, Modelo, SN, Tipo, Categoria) VALUES (?, ?, ?, ?, ?, ?)"
    ejecutar_consulta(query, (id_cliente, marca, modelo, sn, tipo, categoria))

def consultar_equipos(marca="", modelo=""):
    query = "SELECT * FROM Equipo WHERE Marca LIKE ? AND Modelo LIKE ?"
    return obtener_datos(query, ('%' + marca + '%', '%' + modelo + '%',))

def consultar_equipos_intuitiva(marca="", modelo=""):
    query = """
    SELECT 
        e.id_equipo,
        c.Nombre AS Nombre_Cliente,
        e.Marca,
        e.Modelo,
        e.SN,
        e.Tipo,
        e.Categoria
    FROM 
        Equipo e
    JOIN 
        Cliente c ON e.id_cliente = c.id_cliente
    WHERE 
        e.Marca LIKE ? AND e.Modelo LIKE ?
    """
    return obtener_datos(query, ('%' + marca + '%', '%' + modelo + '%'))

def consultar_acciones_intuitivo(id_equipo="", id_tecnico=""):
    query = """
    SELECT 
        A.OT,
        E.Marca AS Equipo_Marca,
        E.Modelo AS Equipo_Modelo,
        T.Nombre AS Tecnico_Nombre,
        A.fecha_entrada, 
        A.fecha_salida, 
        A.descripcion, 
        A.garantia 
    FROM 
        Accion A 
    JOIN  
        Equipo E ON A.id_equipo = E.id_equipo 
    JOIN  
        Tecnico T ON A.id_tecnico = T.id_tecnico
    WHERE 
        A.id_equipo LIKE ? AND A.id_tecnico LIKE ?
    """
    return obtener_datos(query, ('%' + id_equipo + '%', '%' + id_tecnico + '%'))

def modificar_equipo(id_equipo, id_cliente, marca, modelo, sn, tipo, categoria):
    query = "UPDATE Equipo SET id_cliente = ?, Marca = ?, Modelo = ?, SN = ?, Tipo = ?, Categoria = ? WHERE id_equipo = ?"
    ejecutar_consulta(query, (id_cliente, marca, modelo, sn, tipo, categoria, id_equipo))

def eliminar_equipo(id_equipo):
    query = "DELETE FROM Equipo WHERE id_equipo = ?"
    ejecutar_consulta(query, (id_equipo,))

# Funciones para manejar Acciones
def insertar_accion(id_equipo, id_tecnico, fecha_entrada, fecha_salida="", descripcion="", garantia=""):
    query = "INSERT INTO Accion (id_equipo, id_tecnico, fecha_entrada, fecha_salida, descripcion, garantia) VALUES (?, ?, ?, ?, ?, ?)"
    ejecutar_consulta(query, (id_equipo, id_tecnico, fecha_entrada, fecha_salida, descripcion, garantia))

def consultar_acciones(id_equipo="", id_tecnico=""):
    query = "SELECT * FROM Accion WHERE id_equipo LIKE ? AND id_tecnico LIKE ?"
    return obtener_datos(query, ('%' + id_equipo + '%', '%' + id_tecnico + '%',))

def modificar_accion(ot, id_equipo, id_tecnico, fecha_entrada, fecha_salida="", descripcion="", garantia=""):
    query = "UPDATE Accion SET id_equipo = ?, id_tecnico = ?, fecha_entrada = ?, fecha_salida = ?, descripcion = ?, garantia = ? WHERE OT = ?"
    ejecutar_consulta(query, (id_equipo, id_tecnico, fecha_entrada, fecha_salida, descripcion, garantia, ot))

def eliminar_accion(ot):
    query = "DELETE FROM Accion WHERE OT = ?"
    ejecutar_consulta(query, (ot,))

def resultados_registros():
    query = " SELECT A.OT, E.Marca AS Equipo_Marca, E.Modelo AS Equipo_Modelo, C.Nombre AS Cliente_Nombre, " \
            "T.Nombre AS Tecnico_Nombre, A.fecha_entrada, A.fecha_salida, A.descripcion, A.garantia " \
            "FROM Accion A " \
            "JOIN  Equipo E ON A.id_equipo = E.id_equipo " \
            "JOIN  Cliente C ON E.id_cliente = C.id_cliente " \
            "JOIN  Tecnico T ON A.id_tecnico = T.id_tecnico;"
    return obtener_datos(query)

def modificar_accion_descripcion(nueva_descripcion, accion_id):
    # Realizar la actualización solo de la descripción de la acción
    query = "UPDATE Accion SET descripcion = ? WHERE OT = ?"
    ejecutar_consulta(query, (nueva_descripcion, accion_id))

def get_descripcion_actual(accion_id):
    # Suponiendo que tienes acceso a una base de datos
    query = "SELECT descripcion FROM Accion WHERE OT = ?"
    return obtener_datos(query, (str(accion_id)))