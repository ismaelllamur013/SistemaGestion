import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import PhotoImage
from models import insertar_cliente, consultar_clientes, modificar_cliente, eliminar_cliente
from models import insertar_tecnico, consultar_tecnicos, modificar_tecnico, eliminar_tecnico
from models import insertar_equipo, consultar_equipos, modificar_equipo, eliminar_equipo, consultar_equipos_intuitiva
from models import insertar_accion, consultar_acciones, modificar_accion, eliminar_accion, consultar_acciones_intuitivo
from models import resultados_registros, modificar_accion_descripcion, get_descripcion_actual, modificar_accion_descripcion_y_fecha_salida
from graficos import crear_grafico_tecnicos, crear_grafico_tipo_cliente, crear_grafico_tipo_equipo
from excel import importar_desde_excel, exportar_a_excel

class VentanaFormulario:
    def __init__(self, master, tipo):
        self.master = master
        self.tipo = tipo
        self.formulario = tk.Toplevel(self.master)  
        self.formulario.title(f"Formulario de {tipo}")
        
        self.formulario.config(bg="#2e2e2e")  
        self.crear_widgets()

    def crear_widgets(self):
        self.formulario.grid_columnconfigure(0, weight=1)
        self.formulario.grid_columnconfigure(1, weight=2)
        self.formulario.grid_rowconfigure(0, weight=1)
        self.formulario.grid_rowconfigure(1, weight=1)
        self.formulario.grid_rowconfigure(2, weight=1)

        estilo = ttk.Style()
        estilo.configure('TButton', background="#555555", foreground="black", padding=10, font=("Arial", 10))
        estilo.configure('TLabel', background="#2e2e2e", foreground="white", font=("Arial", 10))
        estilo.configure('TEntry', fieldbackground="#333333", foreground="black", font=("Arial", 10))
        estilo.configure('TCombobox', fieldbackground="#333333", foreground="black", font=("Arial", 10))

        if self.tipo == "Cliente":
            self.label_nombre = ttk.Label(self.formulario, text="Nombre Cliente(*):")
            self.label_nombre.grid(row=0, column=0, pady=10, sticky="w", padx=20)
            self.entry_nombre = ttk.Entry(self.formulario, width=30)
            self.entry_nombre.grid(row=0, column=1, pady=10, padx=20)

            self.label_cuit = ttk.Label(self.formulario, text="CUIT Cliente:")
            self.label_cuit.grid(row=1, column=0, pady=10, sticky="w", padx=20)
            self.entry_cuit = ttk.Entry(self.formulario, width=30)
            self.entry_cuit.grid(row=1, column=1, pady=10, padx=20)

            self.label_direccion = ttk.Label(self.formulario, text="Dirección Cliente:")
            self.label_direccion.grid(row=2, column=0, pady=10, sticky="w", padx=20)
            self.entry_direccion = ttk.Entry(self.formulario, width=30)
            self.entry_direccion.grid(row=2, column=1, pady=10, padx=20)

            self.label_tipo_cliente = ttk.Label(self.formulario, text="Tipo de Cliente:")
            self.label_tipo_cliente.grid(row=3, column=0, pady=10, sticky="w", padx=20)
            self.combobox_tipo_cliente = ttk.Combobox(self.formulario, values=["Instituciones", "Profesional Particular", "Estética"], width=27)
            self.combobox_tipo_cliente.grid(row=3, column=1, pady=10, padx=20)

            self.label_n_telefonico = ttk.Label(self.formulario, text="Numero telefonico:")
            self.label_n_telefonico.grid(row=4, column=0, pady=10, sticky="w", padx=20)
            self.entry_n_telefonico = ttk.Entry(self.formulario, width=30)
            self.entry_n_telefonico.grid(row=4, column=1, pady=10, padx=20)

            self.boton_guardar = ttk.Button(self.formulario, text="Guardar", command=self.guardar_cliente)
            self.boton_guardar.grid(row=5, column=0, columnspan=2, pady=20, padx=20)

            self.listbox_clientes = tk.Listbox(self.formulario, height=5, width=50, bg="#333333", fg="white", selectbackground="#555555")
            self.listbox_clientes.grid(row=6, column=0, columnspan=2, pady=10)
            self.cargar_clientes()

            self.boton_modificar = ttk.Button(self.formulario, text="Modificar", command=self.modificar_cliente)
            self.boton_modificar.grid(row=7, column=0, padx=20, pady=20)

            self.boton_eliminar = ttk.Button(self.formulario, text="Eliminar", command=self.eliminar_cliente)
            self.boton_eliminar.grid(row=7, column=1, padx=20, pady=20)

        if self.tipo == "Técnico":
            self.label_nombre_tecnico = ttk.Label(self.formulario, text="Nombre Técnico(*):")
            self.label_nombre_tecnico.grid(row=0, column=0, pady=10, sticky="w", padx=20)
            self.entry_nombre_tecnico = ttk.Entry(self.formulario, width=30)
            self.entry_nombre_tecnico.grid(row=0, column=1, pady=10, padx=20)

            self.boton_guardar = ttk.Button(self.formulario, text="Guardar", command=self.guardar_tecnico)
            self.boton_guardar.grid(row=1, column=0, columnspan=2, pady=20, padx=20)

            self.listbox_tecnicos = tk.Listbox(self.formulario, height=5, width=50, bg="#333333", fg="white", selectbackground="#555555")
            self.listbox_tecnicos.grid(row=2, column=0, columnspan=2, pady=10)
            self.cargar_tecnico()

            self.boton_modificar = ttk.Button(self.formulario, text="Modificar", command=self.modificar_tecnico)
            self.boton_modificar.grid(row=3, column=0, padx=20, pady=20)

            self.boton_eliminar = ttk.Button(self.formulario, text="Eliminar", command=self.eliminar_tecnico)
            self.boton_eliminar.grid(row=3, column=1, padx=20, pady=20)

        if self.tipo == "Equipo":
            self.label_cliente_equipo = ttk.Label(self.formulario, text="Cliente Dueño(*):")
            self.label_cliente_equipo.grid(row=0, column=0, pady=10, sticky="w", padx=20)
            self.combobox_cliente_equipo = ttk.Combobox(self.formulario, width=27)
            self.combobox_cliente_equipo.grid(row=0, column=1, pady=10, padx=20)
            self.cargar_clientes_combobox()

            self.label_marca = ttk.Label(self.formulario, text="Marca(*):")
            self.label_marca.grid(row=1, column=0, pady=10, sticky="w", padx=20)
            self.entry_marca = ttk.Entry(self.formulario, width=30)
            self.entry_marca.grid(row=1, column=1, pady=10, padx=20)

            self.label_modelo = ttk.Label(self.formulario, text="Modelo(*):")
            self.label_modelo.grid(row=2, column=0, pady=10, sticky="w", padx=20)
            self.entry_modelo = ttk.Entry(self.formulario, width=30)
            self.entry_modelo.grid(row=2, column=1, pady=10, padx=20)

            self.label_sn = ttk.Label(self.formulario, text="S/N(*):")
            self.label_sn.grid(row=3, column=0, pady=10, sticky="w", padx=20)
            self.entry_sn = ttk.Entry(self.formulario, width=30)
            self.entry_sn.grid(row=3, column=1, pady=10, padx=20)

            self.label_tipo = ttk.Label(self.formulario, text="Tipo del Equipo(*):")
            self.label_tipo.grid(row=4, column=0, pady=10, sticky="w", padx=20)
            self.entry_tipo = ttk.Entry(self.formulario, width=30)
            self.entry_tipo.grid(row=4, column=1, pady=10, padx=20)

            self.label_categoria = ttk.Label(self.formulario, text="Categoria:")
            self.label_categoria.grid(row=5, column=0, pady=10, sticky="w", padx=20)
            self.combobox_categoria = ttk.Combobox(self.formulario, values=["Terapia", "Quirofano", "Cardiologia", "Imagenes", "Oftalmologia", "Esterilizacion", "Estetica", " Rehabilitacion", "Veterinaria", "Accesorios", "Otros"], width=27)
            self.combobox_categoria.grid(row=5, column=1, pady=10, padx=20)

            self.boton_guardar = ttk.Button(self.formulario, text="Guardar", command=self.guardar_equipos)
            self.boton_guardar.grid(row=6, column=0, columnspan=2, pady=20, padx=20)

            self.listbox_equipos = tk.Listbox(self.formulario, height=5, width=50, bg="#333333", fg="white", selectbackground="#555555")
            self.listbox_equipos.grid(row=7, column=0, columnspan=2, pady=10)
            self.cargar_equipo()

            self.boton_modificar = ttk.Button(self.formulario, text="Modificar", command=self.modificar_equipo)
            self.boton_modificar.grid(row=8, column=0, padx=20, pady=20)

            self.boton_eliminar = ttk.Button(self.formulario, text="Eliminar", command=self.eliminar_equipos)
            self.boton_eliminar.grid(row=8, column=1, padx=20, pady=20)

        if self.tipo == "Acción":
            self.label_equipo_accion = ttk.Label(self.formulario, text="Equipo(*):")
            self.label_equipo_accion.grid(row=0, column=0, pady=10, sticky="w", padx=20)
            self.combobox_equipo_accion = ttk.Combobox(self.formulario, width=27)
            self.combobox_equipo_accion.grid(row=0, column=1, pady=10, padx=20)
            self.cargar_equipo_combobox()

            self.label_tecnico_accion = ttk.Label(self.formulario, text="Técnico(*):")
            self.label_tecnico_accion.grid(row=1, column=0, pady=10, sticky="w", padx=20)
            self.combobox_tecnico_accion = ttk.Combobox(self.formulario, width=27)
            self.combobox_tecnico_accion.grid(row=1, column=1, pady=10, padx=20)
            self.cargar_tecnico_combobox()

            self.label_fecha_entrada = ttk.Label(self.formulario, text="Fecha Entrada(*):")
            self.label_fecha_entrada.grid(row=2, column=0, pady=10, sticky="w", padx=20)
            self.entry_fecha_entrada = DateEntry(self.formulario, width=12, background="darkblue", foreground="white", borderwidth=2)
            self.entry_fecha_entrada.grid(row=2, column=1, pady=10, padx=20)

            self.label_fecha_salida = ttk.Label(self.formulario, text="Fecha Salida:")
            self.label_fecha_salida.grid(row=3, column=0, pady=10, sticky="w", padx=20)
            self.entry_fecha_salida = DateEntry(self.formulario, width=12, background="darkblue", foreground="white", borderwidth=2)
            self.entry_fecha_salida.grid(row=3, column=1, pady=10, padx=20)
            self.entry_fecha_salida.config(state="disabled") 

            self.var_check_fecha_salida = tk.IntVar()  # Variable asociada al Checkbutton
            self.checkbutton_fecha_salida = ttk.Checkbutton(self.formulario, text="¿Tiene Fecha de Salida?", variable=self.var_check_fecha_salida, command=self.toggle_fecha_salida)
            self.checkbutton_fecha_salida.grid(row=3, column=2, pady=10)

            self.label_descripcion = ttk.Label(self.formulario, text="Descripción:")
            self.label_descripcion.grid(row=4, column=0, pady=10, sticky="w", padx=20)
            self.entry_descripcion = ttk.Entry(self.formulario, width=30)
            self.entry_descripcion.grid(row=4, column=1, pady=10, padx=20)

            self.label_horas_insumidas = ttk.Label(self.formulario, text="Horas Insumidas:")
            self.label_horas_insumidas.grid(row=5, column=0, pady=10, sticky="w", padx=20)
            self.entry_horas_insumidas = ttk.Entry(self.formulario, width=30)
            self.entry_horas_insumidas.grid(row=5, column=1, pady=10, padx=20)

            self.label_garantia = ttk.Label(self.formulario, text="Garantía:")
            self.label_garantia.grid(row=6, column=0, pady=10, sticky="w", padx=20)
            self.combobox_garantia = ttk.Combobox(self.formulario, values=["Sí", "No"], width=27)
            self.combobox_garantia.grid(row=6, column=1, pady=10, padx=20)

            self.boton_guardar = ttk.Button(self.formulario, text="Guardar", command=self.guardar_acciones)
            self.boton_guardar.grid(row=7, column=0, columnspan=2, pady=20, padx=20)

            self.listbox_acciones = tk.Listbox(self.formulario, height=5, width=50, bg="#333333", fg="white", selectbackground="#555555")
            self.listbox_acciones.grid(row=8, column=0, columnspan=2, pady=10)
            self.cargar_acciones()

            self.boton_modificar = ttk.Button(self.formulario, text="Modificar", command=self.modificar_accion)
            self.boton_modificar.grid(row=9, column=0, padx=20, pady=20)

            self.boton_eliminar = ttk.Button(self.formulario, text="Eliminar", command=self.eliminar_acciones)
            self.boton_eliminar.grid(row=9, column=1, padx=20, pady=20)

            self.boton_guardar = ttk.Button(self.formulario, text="Cambiar descripcion", command=self.modificar_accion_descripcion)
            self.boton_guardar.grid(row=10, column=0, columnspan=2, pady=20, padx=20)



    def toggle_fecha_salida(self):
        if self.var_check_fecha_salida.get() == 1:  
            self.entry_fecha_salida.config(state="normal") 
        else:
            self.entry_fecha_salida.config(state="disabled")  

    def cargar_equipo_combobox(self):
        equipos = consultar_equipos()
        self.combobox_equipo_accion['values'] = [f"{equipo[2]} - {equipo[3]} - {equipo[4]}" for equipo in equipos]
        self.combobox_equipo_accion.set('') 

    def cargar_tecnico_combobox(self):
        tecnicos = consultar_tecnicos()
        self.combobox_tecnico_accion['values'] = [f"{tecnico[0]} - {tecnico[1]}" for tecnico in tecnicos]
        self.combobox_tecnico_accion.set('')  

    def cargar_clientes_combobox(self):
        clientes = consultar_clientes()
        self.combobox_cliente_equipo['values'] = [cliente[1] for cliente in clientes]
        self.combobox_cliente_equipo.set('')  

 
    def mostrar_mensaje(self, titulo, mensaje):
        ventana_mensaje = tk.Toplevel(self.formulario)
        ventana_mensaje.title(titulo)
        label = tk.Label(ventana_mensaje, text=mensaje)
        label.pack(padx=10, pady=10)
        boton_cerrar = tk.Button(ventana_mensaje, text="Cerrar", command=ventana_mensaje.destroy)
        boton_cerrar.pack(pady=5)


#Cliente

    def cargar_clientes(self):
        clientes = consultar_clientes()
        self.listbox_clientes.delete(0, tk.END) 
        for cliente in clientes:
            self.listbox_clientes.insert(tk.END, f"{cliente[0]} - {cliente[1]} - {cliente[2]} - {cliente[3]} - {cliente[4]} - {cliente[5]}") 

    def guardar_cliente(self):
        nombre = self.entry_nombre.get()
        cuit = self.entry_cuit.get()
        direccion = self.entry_direccion.get()
        tipo_cliente = self.combobox_tipo_cliente.get()
        n_telefonico = self.entry_n_telefonico.get()

        if nombre:
            insertar_cliente(nombre, cuit, direccion,tipo_cliente,n_telefonico)
            self.cargar_clientes()  
        else:
            self.mostrar_mensaje("Error", "El nombre es obligatorio.")

    def modificar_cliente(self):
        seleccion = self.listbox_clientes.curselection()
        if seleccion:
            cliente_seleccionado = self.listbox_clientes.get(seleccion)
            cliente_id = int(cliente_seleccionado.split(" - ")[0])  
            nombre = self.entry_nombre.get()
            cuit = self.entry_cuit.get()
            direccion = self.entry_direccion.get()
            tipo_cliente = self.combobox_tipo_cliente.get()
            n_telefonico = self.entry_n_telefonico.get()

            if nombre:
                modificar_cliente(cliente_id, nombre, cuit, direccion,tipo_cliente,n_telefonico)
                self.cargar_clientes() 
            else:
                self.mostrar_mensaje("Error", "El nombre es obligatorio.")
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona un cliente")

    def eliminar_cliente(self):
        seleccion = self.listbox_clientes.curselection()
        if seleccion:
            cliente_seleccionado = self.listbox_clientes.get(seleccion)
            cliente_id = int(cliente_seleccionado.split(" - ")[0])  
            eliminar_cliente(cliente_id)
            self.cargar_clientes()  
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona un cliente")


#Tecnico

    def cargar_tecnico(self):
        tecnicos = consultar_tecnicos()
        self.listbox_tecnicos.delete(0, tk.END)  
        for tecnico in tecnicos:
            self.listbox_tecnicos.insert(tk.END, f"{tecnico[0]} - {tecnico[1]}") 

    def guardar_tecnico(self):
        nombre = self.entry_nombre_tecnico.get()

        if nombre:
            insertar_tecnico(nombre)
            self.cargar_tecnico()  
        else:
            self.mostrar_mensaje("Error", "El nombre es obligatorio.")

    def modificar_tecnico(self):
        seleccion = self.listbox_tecnicos.curselection()
        if seleccion:
            tecnico_seleccionado = self.listbox_tecnicos.get(seleccion)
            tecnico_id = int(tecnico_seleccionado.split(" - ")[0])  
            nombre = self.entry_nombre_tecnico.get()
        
            if nombre:
                modificar_tecnico(tecnico_id, nombre)
                self.cargar_tecnico()  
            else:
                self.mostrar_mensaje("Error", "Por favor ingresa todos los datos")
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona un tecnico")

    def eliminar_tecnico(self):    
        seleccion = self.listbox_tecnicos.curselection()
        if seleccion:
            tecnico_seleccionado = self.listbox_tecnicos.get(seleccion)
            tecnico_id = int(tecnico_seleccionado.split(" - ")[0])  
            eliminar_tecnico(tecnico_id)
            self.cargar_tecnico() 
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona un tecnico")


# Equipo

    def cargar_equipo(self):
        equipos = consultar_equipos_intuitiva()
        self.listbox_equipos.delete(0, tk.END)  
        for equipo in equipos:
            self.listbox_equipos.insert(tk.END, f"{equipo[0]} - {equipo[1]} - {equipo[2]} - {equipo[3]} - {equipo[4]} - {equipo[5]} - {equipo[6]}") 


    def guardar_equipos(self):
        nombre_cliente = self.combobox_cliente_equipo.get()
        clientes = consultar_clientes()
        cliente_id = None
        for cliente in clientes:
            if cliente[1] == nombre_cliente:
                cliente_id = cliente[0]
                break

        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        sn = self.entry_sn.get()
        tipo = self.entry_tipo.get()
        categoria = self.combobox_categoria.get()
        if cliente_id and marca and modelo and modelo and sn and tipo and categoria:
            insertar_equipo(cliente_id, marca, modelo, sn, tipo, categoria)
            self.cargar_equipo()  
        else:
            self.mostrar_mensaje("Error", "Por favor ingresa todos los datos")


    def modificar_equipo(self):
        seleccion = self.listbox_equipos.curselection()
        if seleccion:
            equipo_seleccionado = self.listbox_equipos.get(seleccion)
            equipo_id = int(equipo_seleccionado.split(" - ")[0]) 
            cliente_equipo = self.combobox_cliente_equipo.get() 
            marca = self.entry_marca.get()
            modelo = self.entry_modelo.get()
            sn = self.entry_sn.get()
            tipo = self.entry_tipo.get()
            categoria = self.combobox_categoria.get()
            clientes = consultar_clientes()
            cliente_id = None
            for cliente in clientes:
                if cliente[1] == cliente_equipo:
                    cliente_id = cliente[0]
                    break

            if cliente_id and marca and modelo and sn and tipo and categoria:
                modificar_equipo(equipo_id, cliente_id, marca, modelo, sn, tipo, categoria)
                self.cargar_equipo() 
            else:
                self.mostrar_mensaje("Error", "Todos los campos son obligatorios.")
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona un equipo para modificar.")


    def eliminar_equipos(self):
        seleccion = self.listbox_equipos.curselection()
        if seleccion:
            equipo_seleccionado = self.listbox_equipos.get(seleccion)
            equipo_id = int(equipo_seleccionado.split(" - ")[0])  
            eliminar_equipo(equipo_id)
            self.cargar_equipo()  
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona un equipo")


# Acciones

    def cargar_acciones(self):
        acciones = consultar_acciones_intuitivo()
        self.listbox_acciones.delete(0, tk.END) 
        for accion in acciones:
            self.listbox_acciones.insert(tk.END, f"{accion[0]} - {accion[1]} - {accion[2]} - {accion[3]} - {accion[4]} - {accion[5]} - {accion[6]}  - {accion[7]} - {accion[8]}")  


    def guardar_acciones(self):
        equipo_accion = self.combobox_equipo_accion.get().split(' - ')[0]  
        tecnico_accion = self.combobox_tecnico_accion.get().split(' - ')[0]  
        fecha_entrada = self.entry_fecha_entrada.get()
        if self.var_check_fecha_salida.get() == 1:
            fecha_salida = self.entry_fecha_salida.get()
        else:
            fecha_salida = ""
        horas_insumidas = self.entry_horas_insumidas.get()
        descripcion = self.entry_descripcion.get()
        garantia = self.combobox_garantia.get()

        if equipo_accion and tecnico_accion and fecha_entrada:
            insertar_accion(equipo_accion, tecnico_accion, fecha_entrada, fecha_salida, descripcion, garantia, horas_insumidas)
            self.cargar_acciones()  
        else:
            self.mostrar_mensaje("Error", "Equipo, Técnico y Fecha de Entrada son obligatorios.")

    def modificar_accion(self):

        seleccion = self.listbox_acciones.curselection()
        if seleccion:
            accion_seleccionada = self.listbox_acciones.get(seleccion)
            accion_id = int(accion_seleccionada.split(" - ")[0])  
            equipo_accion = self.combobox_equipo_accion.get().split(' - ')[0] 
            tecnico_accion = self.combobox_tecnico_accion.get().split(' - ')[0] 
            fecha_entrada = self.entry_fecha_entrada.get()
            if self.var_check_fecha_salida.get() == 1:
                fecha_salida = self.entry_fecha_salida.get()
            else:
                fecha_salida = ""
            descripcion = self.entry_descripcion.get()
            garantia = self.combobox_garantia.get()
            horas_insumidas = self.entry_horas_insumidas.get()


            if equipo_accion and tecnico_accion and fecha_entrada:
                modificar_accion(accion_id, equipo_accion, tecnico_accion, fecha_entrada, fecha_salida, descripcion, garantia,horas_insumidas)
                self.cargar_acciones()  
            else:
                self.mostrar_mensaje("Error", "Equipo, Técnico y Fecha de Entrada son obligatorios.")
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona una acción")

    def modificar_accion_descripcion(self):
        seleccion = self.listbox_acciones.curselection()
        if seleccion:
            accion_seleccionada = self.listbox_acciones.get(seleccion)
            accion_id = int(accion_seleccionada.split(" - ")[0])  
            nueva_descripcion = self.entry_descripcion.get()
            descripcion_actual = get_descripcion_actual(accion_id)  
            descripcion_actual = descripcion_actual[0][0]
            print(descripcion_actual)
            if nueva_descripcion: 
                descripcion_actual_concatenada = descripcion_actual + "\n" + nueva_descripcion
                modificar_accion_descripcion(descripcion_actual_concatenada, accion_id)
                self.cargar_acciones()  
            else:
                self.mostrar_mensaje("Error", "La descripción es obligatoria.")
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona una acción.")



    def eliminar_acciones(self):
        seleccion = self.listbox_acciones.curselection()
        if seleccion:
            accion_seleccionada = self.listbox_acciones.get(seleccion)
            accion_id = int(accion_seleccionada.split(" - ")[0]) 
            eliminar_accion(accion_id)
            self.cargar_acciones() 
        else:
            self.mostrar_mensaje("Error", "Por favor selecciona una acción")


class VentanaAcciones:
    def __init__(self, master):
        self.master = master
        self.formulario = tk.Toplevel(self.master)
        self.formulario.title("Ver Todas las Acciones")
        self.crear_widgets()

    def crear_widgets(self):
        self.buscar_label = tk.Label(self.formulario, text="Buscar:")
        self.buscar_label.pack(padx=10, pady=5, anchor="w")

        self.buscar_entry = tk.Entry(self.formulario, width=50)
        self.buscar_entry.pack(padx=10, pady=5)

        self.buscar_button = tk.Button(self.formulario, text="Buscar", command=self.buscar_registros)
        self.buscar_button.pack(padx=10, pady=5)

        self.treeview = ttk.Treeview(self.formulario, columns=("OT", "Marca", "Modelo", "Cliente", "Técnico", "Entrada", "Salida", "Descripción", "Garantía"), show="headings", height=20)

        self.treeview.heading("OT", text="OT")
        self.treeview.heading("Marca", text="Marca")
        self.treeview.heading("Modelo", text="Modelo")
        self.treeview.heading("Cliente", text="Cliente")
        self.treeview.heading("Técnico", text="Técnico")
        self.treeview.heading("Entrada", text="Entrada")
        self.treeview.heading("Salida", text="Salida")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.heading("Garantía", text="Garantía")

        self.treeview.column("OT", width=50)
        self.treeview.column("Marca", width=100, anchor="w")
        self.treeview.column("Modelo", width=100, anchor="w")
        self.treeview.column("Cliente", width=150, anchor="w")
        self.treeview.column("Técnico", width=100, anchor="w")
        self.treeview.column("Entrada", width=100, anchor="w")
        self.treeview.column("Salida", width=100, anchor="w")
        self.treeview.column("Descripción", width=200, anchor="w")
        self.treeview.column("Garantía", width=100, anchor="w")

        self.treeview.pack(padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.formulario, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview.config(yscrollcommand=scrollbar.set)

        self.registros = resultados_registros()  
        self.mostrar_registros(self.registros)

        self.treeview.bind("<Double-1>", self.mostrar_descripcion_completa)

    def mostrar_registros(self, registros):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        if not registros:
            print("No hay registros disponibles")
            return

        for registro in registros:
            item_id = self.treeview.insert("", tk.END, values=registro)

            fecha_salida = registro[6]  
            if fecha_salida:
                self.treeview.item(item_id, tags=("verde",))

        self.treeview.tag_configure("verde", background="lightgreen")

    def mostrar_descripcion_completa(self, event):
        item = self.treeview.selection()
        if not item:
            return

        descripcion = self.treeview.item(item[0], "values")[7]  
        fecha_salida = self.treeview.item(item[0], "values")[6]  

        ventana_descripcion = tk.Toplevel(self.master)
        ventana_descripcion.title("Editar Descripción y Fecha de Salida")

        texto = tk.Text(ventana_descripcion, wrap="word", width=60, height=15)
        texto.insert(tk.END, descripcion)  
        texto.config(state=tk.NORMAL)  
        texto.pack(padx=10, pady=10)

        fecha_salida_label = tk.Label(ventana_descripcion, text="Fecha de Salida (Opcional):")
        fecha_salida_label.pack(padx=10, pady=5)

        entry_fecha_salida = tk.Entry(ventana_descripcion, width=20)
        entry_fecha_salida.insert(tk.END, fecha_salida if fecha_salida else "")
        entry_fecha_salida.pack(padx=10, pady=5)

        def guardar_descripcion_y_salida():
            nueva_descripcion = texto.get("1.0", tk.END).strip()  
            nueva_fecha_salida = entry_fecha_salida.get().strip() 

            if nueva_descripcion:  
                accion_id = int(self.treeview.item(item[0], "values")[0])  
            
                modificar_accion_descripcion_y_fecha_salida(nueva_descripcion, nueva_fecha_salida, accion_id)

                ventana_descripcion.destroy()

                self.registros = resultados_registros()  
                self.mostrar_registros(self.registros)
            else:
                self.mostrar_mensaje("Error", "La descripción no puede estar vacía.")

        guardar_button = tk.Button(ventana_descripcion, text="Guardar", command=guardar_descripcion_y_salida)
        guardar_button.pack(pady=5)

        cerrar_button = tk.Button(ventana_descripcion, text="Cerrar", command=ventana_descripcion.destroy)
        cerrar_button.pack(pady=5)

    
    def buscar_registros(self):
        busqueda = self.buscar_entry.get().lower()

        if busqueda == "":
            self.mostrar_registros(self.registros)
        else:
            registros_filtrados = [
                registro for registro in self.registros
                if any(busqueda in str(campo).lower() for campo in registro)
            ]
            self.mostrar_registros(registros_filtrados)
            
class Interfaz:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Base de Datos")
        self.master.geometry("450x500")
        
        self.master.config(bg="#2e2e2e")

        self.imagen = PhotoImage(file="imagen.png")  
        self.label_imagen = tk.Label(self.master, image=self.imagen, bg="#2e2e2e")
        self.label_imagen.place(x=200, y=100)  


        estilo = ttk.Style()
        estilo.configure('TButton', background="#555555", foreground="black", padding=10, font=("Arial", 10))
        estilo.configure('TLabel', background="#2e2e2e", foreground="white", font=("Arial", 10))
        estilo.configure('TEntry', fieldbackground="#333333", foreground="black", font=("Arial", 10))
        estilo.configure('TCombobox', fieldbackground="#333333", foreground="black", font=("Arial", 10))

        self.crear_widgets()

    def crear_widgets(self):
        self.frame_botones = tk.Frame(self.master, bg="#2e2e2e")
        self.frame_botones.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.button_cliente = ttk.Button(self.frame_botones, text="Cargar Cliente", width=20, command=self.cargar_cliente)
        self.button_cliente.grid(row=0, column=0, pady=10)

        self.button_tecnico = ttk.Button(self.frame_botones, text="Cargar Técnico", width=20, command=self.cargar_tecnico)
        self.button_tecnico.grid(row=1, column=0, pady=10)

        self.button_equipo = ttk.Button(self.frame_botones, text="Cargar Equipo", width=20, command=self.cargar_equipo)
        self.button_equipo.grid(row=2, column=0, pady=10)

        self.button_accion = ttk.Button(self.frame_botones, text="Cargar Acción", width=20, command=self.cargar_accion)
        self.button_accion.grid(row=3, column=0, pady=10)

        self.button_ver_acciones = ttk.Button(self.frame_botones, text="Ver Todas las Acciones", width=20, command=self.ver_acciones)
        self.button_ver_acciones.grid(row=4, column=0, pady=10)

        self.button_estadisticas = ttk.Button(self.frame_botones, text="Mostrar Estadísticas", width=20, command=self.mostrar_estadisticas)
        self.button_estadisticas.grid(row=5, column=0, pady=10)

        self.boton_exportar = tk.Button(self.frame_botones, text="Exportar a Excel", command=self.exportar_a_excel_a)
        self.boton_exportar.grid(row=6, column=0,pady=10)

        self.boton_importar = tk.Button(self.frame_botones, text="Importar desde Excel", command=self.importar_desde_excel_a)
        self.boton_importar.grid(row=7, column=0,pady=10)


    def cargar_cliente(self):
        VentanaFormulario(self.master, "Cliente")  

    def cargar_tecnico(self):
        VentanaFormulario(self.master, "Técnico") 

    def cargar_equipo(self):
        VentanaFormulario(self.master, "Equipo")  

    def cargar_accion(self):
        VentanaFormulario(self.master, "Acción") 

    def ver_acciones(self):
        VentanaAcciones(self.master) 
    
    def exportar_a_excel_a(self):
        exportar_a_excel()
    def importar_desde_excel_a(self):
        importar_desde_excel()

    def mostrar_estadisticas(self):
        
        crear_grafico_tecnicos()
        crear_grafico_tipo_cliente()  
        crear_grafico_tipo_equipo() 


def iniciar_interfaz():
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
