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

def crear_grafico_meses(meses):
    # Crear un gráfico de barras para la cantidad de equipos arreglados por mes
    meses_list = list(meses.keys())
    cantidades = list(meses.values())

    plt.figure(figsize=(10, 6))
    plt.bar(meses_list, cantidades, color='orange')
    plt.title('Cantidad de Equipos Arreglados por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Equipos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()