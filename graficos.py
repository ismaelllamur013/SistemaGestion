import matplotlib.pyplot as plt

def crear_grafico_tecnicos(tecnicos):
    # Crear un gráfico de barras para la cantidad de equipos arreglados por cada técnico
    nombres_tecnicos = list(tecnicos.keys())
    cantidades = list(tecnicos.values())

    plt.figure(figsize=(10, 6))
    plt.bar(nombres_tecnicos, cantidades, color='skyblue')
    plt.title('Cantidad de Equipos Arreglados por Técnico')
    plt.xlabel('Técnico')
    plt.ylabel('Cantidad de Equipos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

from datetime import datetime

# Diccionario de nombres de los meses
nombres_meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def crear_grafico_meses(meses):
    # Convertir las fechas a números de meses y extraer los valores
    meses_list = []
    cantidades = []
    
    for fecha, cantidad in meses.items():
        # Convertir la fecha en formato 'MM/DD/YY' a un objeto datetime
        fecha_obj = datetime.strptime(fecha, '%m/%d/%y')
        mes = fecha_obj.month  # Obtener el número del mes
        meses_list.append(nombres_meses[mes])  # Obtener el nombre del mes
        cantidades.append(cantidad)  # Obtener la cantidad asociada

    plt.figure(figsize=(10, 6))
    plt.bar(meses_list, cantidades, color='orange')
    plt.title('Cantidad de Equipos Arreglados por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Equipos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()