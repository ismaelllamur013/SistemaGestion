import matplotlib.pyplot as plt
from db import obtener_datos

def crear_grafico_tecnicos():
    query = """
    SELECT Tecnico.Nombre, COUNT(Accion.OT) AS reparaciones
    FROM Accion
    JOIN Tecnico ON Accion.id_tecnico = Tecnico.id_tecnico
    GROUP BY Tecnico.Nombre;
    """
    datos = obtener_datos(query)

    nombres_tecnicos = [dato[0] for dato in datos]
    cantidades = [dato[1] for dato in datos]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres_tecnicos, cantidades, color='skyblue')
    plt.title('Cantidad de Equipos Arreglados por Técnico')
    plt.xlabel('Técnico')
    plt.ylabel('Cantidad de Equipos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()

def crear_grafico_tipo_cliente():
    query = """
    SELECT Cliente.tipo_cliente, COUNT(Accion.OT) AS reparaciones
    FROM Accion
    JOIN Equipo ON Accion.id_equipo = Equipo.id_equipo
    JOIN Cliente ON Equipo.id_cliente = Cliente.id_cliente
    GROUP BY Cliente.tipo_cliente;
    """
    datos = obtener_datos(query)

    tipos_cliente = [dato[0] for dato in datos]
    reparaciones = [dato[1] for dato in datos]

    plt.figure(figsize=(10, 6))
    plt.bar(tipos_cliente, reparaciones, color='lightblue')
    plt.title('Cantidad de Reparaciones por Tipo de Cliente')
    plt.xlabel('Tipo de Cliente')
    plt.ylabel('Cantidad de Reparaciones')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()

def crear_grafico_tipo_equipo():
    query = """
    SELECT Equipo.Tipo, COUNT(Accion.OT) AS reparaciones
    FROM Accion
    JOIN Equipo ON Accion.id_equipo = Equipo.id_equipo
    GROUP BY Equipo.Tipo;
    """
    datos = obtener_datos(query)

    tipos_equipo = [dato[0] for dato in datos]
    reparaciones = [dato[1] for dato in datos]

    plt.figure(figsize=(10, 6))
    plt.bar(tipos_equipo, reparaciones, color='lightgreen')
    plt.title('Cantidad de Reparaciones por Tipo de Equipo')
    plt.xlabel('Tipo de Equipo')
    plt.ylabel('Cantidad de Reparaciones')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()
