CREATE TABLE Cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    CUIT TEXT,
    direccion TEXT,
    tipo_cliente TEXT,
    n_telefonico TEXT 
);

CREATE TABLE Tecnico (
    id_tecnico INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL
);

CREATE TABLE Equipo (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    Marca TEXT NOT NULL,
    Modelo TEXT NOT NULL,
    SN TEXT NOT NULL,
    Tipo TEXT NOT NULL,
    Categoria TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

CREATE TABLE Accion (
    OT INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipo INTEGER,
    id_tecnico INTEGER,
    fecha_entrada TEXT NOT NULL,
    fecha_salida TEXT ,
    descripcion TEXT ,
    horas_insumidas TEXT ,
    garantia TEXT NOT NULL,
    FOREIGN KEY (id_equipo) REFERENCES Equipo(id_equipo),
    FOREIGN KEY (id_tecnico) REFERENCES Tecnico(id_tecnico)
);
