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
        print("Leyendo el archivo Excel...")
        df_cliente = pd.read_excel('base_de_datos.xlsx', sheet_name='Cliente', engine='openpyxl')
        df_tecnico = pd.read_excel('base_de_datos.xlsx', sheet_name='Tecnico', engine='openpyxl')
        df_equipo = pd.read_excel('base_de_datos.xlsx', sheet_name='Equipo', engine='openpyxl')
        df_accion = pd.read_excel('base_de_datos.xlsx', sheet_name='Accion', engine='openpyxl')

        # Convertir las fechas al formato MM/DD/YY en la columna 'fecha_entrada' y 'fecha_salida'
        df_accion['fecha_entrada'] = pd.to_datetime(df_accion['fecha_entrada'], errors='coerce').dt.strftime('%m/%d/%y')
        df_accion['fecha_salida'] = pd.to_datetime(df_accion['fecha_salida'], errors='coerce').dt.strftime('%m/%d/%y')

        # Asignar un valor predeterminado para fechas vacías
        df_accion['fecha_salida'] = df_accion['fecha_salida'].fillna('')  # Valor por defecto en formato MM/DD/YY

        # Asignar valores predeterminados para las columnas 'descripcion' y 'garantia' si son nulas
        df_accion['descripcion'] = df_accion['descripcion'].fillna('')
        df_accion['garantia'] = df_accion['garantia'].fillna('')

        # Conectar a la base de datos SQLite
        print("Conectando a la base de datos...")
        conn = sqlite3.connect('base_prueba.db')
        cursor = conn.cursor()

        # Actualizar o insertar en la tabla Cliente
        print("Actualizando o insertando en la tabla Cliente...")
        for index, row in df_cliente.iterrows():
            # Verificar si el cliente existe en la base de datos
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_cliente = ?", (row['id_cliente'],))
            result = cursor.fetchone()

            if result:
                # Si el cliente existe, actualizamos
                query = """
                UPDATE Cliente
                SET Nombre = ?, CUIT = ?, direccion = ?, tipo_cliente = ?
                WHERE id_cliente = ?
                """
                cursor.execute(query, (row['Nombre'], row['CUIT'], row['direccion'], row['tipo_cliente'], row['id_cliente']))
                print(f"Actualizado Cliente: {row['id_cliente']}")
            else:
                # Si no existe, insertamos
                query = """
                INSERT INTO Cliente (id_cliente, Nombre, CUIT, direccion, tipo_cliente)
                VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, (row['id_cliente'], row['Nombre'], row['CUIT'], row['direccion'], row['tipo_cliente']))
                print(f"Insertado Cliente: {row['id_cliente']}")

        # Actualizar o insertar en la tabla Tecnico
        print("Actualizando o insertando en la tabla Tecnico...")
        for index, row in df_tecnico.iterrows():
            # Verificar si el tecnico existe en la base de datos
            cursor.execute("SELECT id_tecnico FROM Tecnico WHERE id_tecnico = ?", (row['id_tecnico'],))
            result = cursor.fetchone()

            if result:
                # Si el técnico existe, actualizamos
                query = """
                UPDATE Tecnico
                SET Nombre = ?
                WHERE id_tecnico = ?
                """
                cursor.execute(query, (row['Nombre'], row['id_tecnico']))
                print(f"Actualizado Tecnico: {row['id_tecnico']}")
            else:
                # Si no existe, insertamos
                query = """
                INSERT INTO Tecnico (id_tecnico, Nombre)
                VALUES (?, ?)
                """
                cursor.execute(query, (row['id_tecnico'], row['Nombre']))
                print(f"Insertado Tecnico: {row['id_tecnico']}")

        # Actualizar la tabla Equipo
        print("Actualizando la tabla Equipo...")
        for index, row in df_equipo.iterrows():
            query = """
            UPDATE Equipo
            SET id_cliente = ?, Marca = ?, Modelo = ?, SN = ?, Tipo = ?, Categoria = ?
            WHERE id_equipo = ?
            """
            cursor.execute(query, (row['id_cliente'], row['Marca'], row['Modelo'], row['SN'], row['Tipo'], row['Categoria'], row['id_equipo']))
            print(f"Actualizado Equipo: {row['id_equipo']}")

        # Actualizar la tabla Accion
        print("Actualizando la tabla Accion...")
        for index, row in df_accion.iterrows():
            query = """
            UPDATE Accion
            SET id_equipo = ?, id_tecnico = ?, fecha_entrada = ?, fecha_salida = ?, descripcion = ?, garantia = ?
            WHERE OT = ?
            """
            cursor.execute(query, (row['id_equipo'], row['id_tecnico'], row['fecha_entrada'], row['fecha_salida'], row['descripcion'], row['garantia'], row['OT']))
            print(f"Actualizado Accion: {row['OT']}")

        # Confirmar los cambios en la base de datos
        conn.commit()

        # Verificar los datos actualizados
        print("Verificando los datos actualizados...")
        cursor.execute("SELECT * FROM Accion")
        result = cursor.fetchall()
        for row in result:
            print(row)

        # Cerrar la conexión
        conn.close()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Base de datos actualizada desde 'base_de_datos.xlsx'")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al importar: {str(e)}")
