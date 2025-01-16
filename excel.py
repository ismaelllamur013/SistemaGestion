import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import messagebox

def exportar_a_excel():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('base_prueba.db')

        # Consultas para obtener los datos de cada tabla
        queries = {
            'Cliente': "SELECT * FROM Cliente",
            'Tecnico': "SELECT * FROM Tecnico",
            'Equipo': "SELECT * FROM Equipo",
            'Accion': "SELECT * FROM Accion"
        }

        # Crear un diccionario de DataFrames con los datos de cada tabla
        dfs = {table: pd.read_sql(query, conn) for table, query in queries.items()}

        # Guardar todos los DataFrames en un archivo Excel
        with pd.ExcelWriter('base_de_datos.xlsx', engine='openpyxl') as writer:
            for table, df in dfs.items():
                df.to_excel(writer, sheet_name=table, index=False)

        # Cerrar la conexión
        conn.close()

        messagebox.showinfo("Éxito", "Datos exportados a 'base_de_datos.xlsx'")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar: {str(e)}")

def importar_desde_excel():
    try:
        # Leer el archivo Excel
        df_cliente = pd.read_excel('base_de_datos.xlsx', sheet_name='Cliente', engine='openpyxl')
        df_tecnico = pd.read_excel('base_de_datos.xlsx', sheet_name='Tecnico', engine='openpyxl')
        df_equipo = pd.read_excel('base_de_datos.xlsx', sheet_name='Equipo', engine='openpyxl')
        df_accion = pd.read_excel('base_de_datos.xlsx', sheet_name='Accion', engine='openpyxl')

        # Imprimir las primeras filas y los encabezados para depurar
        print("Encabezados de las columnas de Accion:")
        print(df_accion.columns)
        print("Primeras filas de Accion:")
        print(df_accion.head())

        # Verificar si hay valores vacíos en la columna OT
        print("Valores de OT:")
        print(df_accion['OT'].isnull().sum())  # Número de valores nulos en OT
        print("Filas con OT vacío o nulo:")
        print(df_accion[df_accion['OT'].isnull()])

        # Convertir la columna OT a tipo adecuado
        df_accion['OT'] = df_accion['OT'].astype('Int64', errors='ignore')

        # Convertir fecha_entrada y fecha_salida al formato adecuado
        df_accion['fecha_entrada'] = pd.to_datetime(df_accion['fecha_entrada'], errors='coerce').dt.strftime('%Y-%m-%d')
        df_accion['fecha_salida'] = pd.to_datetime(df_accion['fecha_salida'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Asignar valores por defecto si hay NaN
        df_accion['fecha_salida'] = df_accion['fecha_salida'].fillna('')  # Fecha por defecto
        df_accion['descripcion'] = df_accion['descripcion'].fillna('')
        df_accion['garantia'] = df_accion['garantia'].fillna('')

        # Convertir NaN en None (para manejar valores NULL en SQLite)
        df_cliente = df_cliente.where(pd.notnull(df_cliente), None)
        df_tecnico = df_tecnico.where(pd.notnull(df_tecnico), None)
        df_equipo = df_equipo.where(pd.notnull(df_equipo), None)
        df_accion = df_accion.where(pd.notnull(df_accion), None)

        # Conectar a la base de datos
        conn = sqlite3.connect('base_prueba.db')

        # Actualizar la tabla Cliente
        for index, row in df_cliente.iterrows():
            if row['CUIT'] is None or pd.isna(row['CUIT']) or row['direccion'] is None or pd.isna(row['direccion']) or row['tipo_cliente'] is None or pd.isna(row['tipo_cliente']):
                continue  # O asigna valores predeterminados si es necesario

            query = """
            UPDATE Cliente
            SET Nombre = ?, CUIT = ?, direccion = ?, tipo_cliente = ?
            WHERE id_cliente = ?
            """
            conn.execute(query, (row['Nombre'], row['CUIT'], row['direccion'], row['tipo_cliente'], row['id_cliente']))

        # Actualizar la tabla Tecnico
        for index, row in df_tecnico.iterrows():
            query = """
            UPDATE Tecnico
            SET Nombre = ?
            WHERE id_tecnico = ?
            """
            conn.execute(query, (row['Nombre'], row['id_tecnico']))

        # Actualizar la tabla Equipo
        for index, row in df_equipo.iterrows():
            query = """
            UPDATE Equipo
            SET id_cliente = ?, Marca = ?, Modelo = ?, SN = ?, Tipo = ?, Categoria = ?
            WHERE id_equipo = ?
            """
            conn.execute(query, (row['id_cliente'], row['Marca'], row['Modelo'], row['SN'], row['Tipo'], row['Categoria'], row['id_equipo']))

        # Actualizar la tabla Accion
        for index, row in df_accion.iterrows():
            # Verificar si los campos obligatorios están vacíos
            if row['fecha_salida'] is None or pd.isna(row['fecha_salida']) or row['descripcion'] is None or pd.isna(row['descripcion']) or row['garantia'] is None or pd.isna(row['garantia']):
                continue  # O asigna valores predeterminados si es necesario

            # Verificar que 'OT' esté presente y no vacío
            if row['OT'] is None or pd.isna(row['OT']):
                continue  # Si no tiene OT, se omite este registro

            print(f"Actualizando Accion con OT: {row['OT']}")

            query = """
            UPDATE Accion
            SET id_equipo = ?, id_tecnico = ?, fecha_entrada = ?, fecha_salida = ?, descripcion = ?, garantia = ?
            WHERE OT = ?
            """
            conn.execute(query, (row['id_equipo'], row['id_tecnico'], row['fecha_entrada'], row['fecha_salida'], row['descripcion'], row['garantia'], row['OT']))

        # Confirmar los cambios
        conn.commit()
        # Cerrar la conexión
        conn.close()

        messagebox.showinfo("Éxito", "Base de datos actualizada desde 'base_de_datos.xlsx'")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al importar: {str(e)}")
