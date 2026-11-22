# Sistema de Gestión de Taller y Equipamiento Médico (MATS GROUP) 🛠️🏥

Aplicación de escritorio desarrollada íntegramente en **Python** con interfaz gráfica en **Tkinter** y persistencia relacional en **SQLite**, diseñada para gestionar clientes, técnicos, equipamiento médico y órdenes de trabajo (`OT`) de un taller de servicio técnico. Incluye formularios dinámicos adaptativos, buscador en tiempo real, indicadores visuales de estado, generación de estadísticas con **Matplotlib** y sincronización bidireccional con **Excel**.

## 📋 Descripción General y Arquitectura

El proyecto implementa una **arquitectura modular en capas** donde cada archivo cumple una responsabilidad bien definida:

* **`main.py`**: Interfaz gráfica de usuario (GUI) en tema oscuro (`#2e2e2e`), formularios dinámicos adaptativos y panel de seguimiento de órdenes de trabajo.
* **`models.py`**: Capa de lógica de negocio y consultas SQL parametrizadas (CRUD completo y consultas relacionales con `JOIN`).
* **`db.py`**: Capa de conexión, transacciones y ejecución segura sobre la base de datos SQLite (`base_prueba.db`).
* **`tablas.sql`**: Script DDL con la definición del esquema relacional, claves primarias y claves foráneas.
* **`excel.py`**: Módulo de exportación e importación bidireccional entre SQLite y Microsoft Excel (`base_de_datos.xlsx`).
* **`gráficos.py`**: Módulo de analítica visual que genera reportes estadísticos de productividad y distribución de reparaciones.
* **`imagen.png`**: Logotipo institucional (**MATS GROUP**) integrado en la pantalla principal.
* **`base_prueba.db`**: Base de datos SQLite preconfigurada con la estructura de tablas y datos de prueba listos para usar.
* **`base_de_datos.xlsx`**: Libro Excel multi-hoja de respaldo y sincronización vinculado al módulo `excel.py`.

## 🗄️ Modelo de Datos Relacional (`tablas.sql`)

La base de datos `base_prueba.db` está compuesta por **4 tablas interrelacionadas**:

1. **`Cliente`**:
   * `id_cliente` (PK), `Nombre` (`NOT NULL`), `CUIT`, `direccion`, `tipo_cliente` (*Instituciones, Profesional Particular, Estética*), `n_telefonico`.
2. **`Tecnico`**:
   * `id_tecnico` (PK), `Nombre` (`NOT NULL`).
3. **`Equipo`**:
   * `id_equipo` (PK), `id_cliente` (FK → `Cliente`), `Marca`, `Modelo`, `SN` (Número de Serie), `Tipo`, `Categoria` (*Terapia, Quirófano, Cardiología, Imágenes, Oftalmología, Esterilización, Estética, Rehabilitación, Veterinaria, Accesorios, Otros*).
4. **`Accion` (Órdenes de Trabajo)**:
   * `OT` (PK autoincremental), `id_equipo` (FK → `Equipo`), `id_tecnico` (FK → `Tecnico`), `fecha_entrada`, `fecha_salida`, `descripcion`, `horas_insumidas`, `garantia`.

## ⚙️ Funcionamiento Detallado por Módulo

### 1. `main.py` — Interfaz Gráfica y Flujo de Usuario
Construido con `tkinter`, `ttk` y `tkcalendar` (`DateEntry`), organiza la experiencia en tres clases principales:

* **`Interfaz` (Ventana Principal):** Presenta el logotipo corporativo (`imagen.png`) y 8 accesos directos: *Cargar Cliente*, *Cargar Técnico*, *Cargar Equipo*, *Cargar Acción*, *Ver Todas las Acciones*, *Mostrar Estadísticas*, *Exportar a Excel* e *Importar desde Excel*.
* **`VentanaFormulario` (Formularios Dinámicos):** Ventana modal reutilizable que adapta dinámicamente sus campos, desplegables (`Combobox`) y listados inferiores (`Treeview`) según el módulo abierto (`Cliente`, `Técnico`, `Equipo` o `Acción`):
  * En **Equipos**, vincula cada dispositivo a un cliente existente y permite clasificarlo por categoría médica.
  * En **Acciones (`OT`)**, permite seleccionar equipo y técnico, registrar `fecha_entrada` mediante calendario, habilitar condicionalmente `fecha_salida` mediante casilla de verificación, indicar horas insumidas y estado de garantía, y agregar nuevas notas de avance sin sobrescribir el historial previo (`modificar_accion_descripcion`).
  * Incluye búsqueda rápida en tiempo real y edición/eliminación directa sobre los registros listados.
* **`VentanaAcciones` (Panel de Seguimiento de Órdenes de Trabajo):**
  * Muestra una tabla completa (`Treeview`) cruzando datos de `OT`, `Equipo`, `Cliente`, `Técnico`, fechas, descripción, horas y garantía.
  * **Indicador visual de estado:** Resalta automáticamente en **verde claro (`lightgreen`)** todas las filas que ya poseen `fecha_salida` registrada (equipos entregados/finalizados).
  * **Filtro instantáneo:** Permite buscar dinámicamente por cualquier columna mientras se escribe.
  * **Actualización rápida con doble clic:** Al hacer doble clic sobre cualquier `OT`, abre una ventana emergente para añadir texto a la descripción técnica y asignar la fecha de salida.

### 2. `models.py` — Lógica de Negocio y Consultas
Encapsula todas las operaciones sobre la base de datos utilizando consultas parametrizadas (`?`) para prevenir inyección SQL:
* Implementa funciones CRUD completas para `Cliente`, `Técnico`, `Equipo` y `Accion`.
* Provee consultas relacionales con `INNER JOIN` (`consultar_equipos_intuitiva`, `consultar_acciones_intuitivo`, `resultados_registros`) para transformar identificadores numéricos (`id_cliente`, `id_equipo`, `id_tecnico`) en nombres legibles para el usuario.
* Gestiona la concatenación incremental de diagnósticos y reparaciones mediante `get_descripcion_actual` y `modificar_accion_descripcion_y_fecha_salida`.

### 3. `db.py` — Capa de Acceso a Datos (SQLite)
Centraliza la conexión con `base_prueba.db` mediante tres funciones base con manejo de excepciones (`sqlite3.Error`) y cierre garantizado (`finally: conn.close()`):
* `conectar_db()`: Establece la conexión con el archivo SQLite.
* `ejecutar_consulta(query, params)`: Ejecuta sentencias de escritura (`INSERT`, `UPDATE`, `DELETE`) y confirma la transacción (`conn.commit()`).
* `obtener_datos(query, params)`: Ejecuta consultas de lectura (`SELECT`) y retorna los resultados mediante `fetchall()`.

### 4. `gráficos.py` — Estadísticas y Visualización (`Matplotlib`)
Genera tres gráficos de barras independientes consultando conteos agrupados (`COUNT(Accion.OT)`) directamente desde SQLite:
* `crear_grafico_tecnicos()`: Volumen de equipos reparados por cada técnico.
* `crear_grafico_tipo_cliente()`: Distribución de órdenes de trabajo según el tipo de cliente (*Instituciones, Profesional Particular, Estética*).
* `crear_grafico_tipo_equipo()`: Cantidad de reparaciones agrupadas por tipo de equipamiento médico.

### 5. `excel.py` — Interoperabilidad con Excel (`Pandas` + `OpenPyXL`)
Permite respaldar, auditar o editar masivamente la información fuera del sistema mediante el archivo `base_de_datos.xlsx`:
* **`exportar_a_excel()`**: Lee las 4 tablas (`Cliente`, `Tecnico`, `Equipo`, `Accion`) con `pandas.read_sql` y las exporta en hojas separadas dentro de `base_de_datos.xlsx`.
* **`importar_desde_excel()`**: Lee las 4 hojas del libro Excel, normaliza formatos de fecha (`%m/%d/%y`), limpia valores nulos (`fillna`) y sincroniza los registros en SQLite (realizando *upsert* en `Cliente` y `Tecnico`, y actualización por clave primaria en `Equipo` y `Accion`).

## 🛠️ Tecnologías Utilizadas

* **Python 3**
* **Tkinter / ttk / tkcalendar** *(interfaz gráfica de escritorio y selectores de fecha)*
* **SQLite3** *(motor de base de datos relacional local)*
* **Pandas & OpenPyXL** *(lectura, escritura y sincronización de archivos `.xlsx`)*
* **Matplotlib** *(generación de gráficos estadísticos)*
* **Pillow (`PIL`)** *(carga y renderizado del logotipo en la interfaz)*

## 🚀 Cómo Ejecutar el Proyecto

1. **Clonar el repositorio:**
   `git clone https://github.com/ismaelllamur013/SistemaGestion.git`
2. **Entrar al directorio del proyecto:**
   `cd SistemaGestion`
3. **Instalar las dependencias:**
   `pip install pandas openpyxl matplotlib pillow tkcalendar`
4. **Iniciar la aplicación:**
   `python main.py`
   *(El sistema incluye `base_prueba.db` y `base_de_datos.xlsx` con datos de ejemplo listos para probar. Si deseas iniciar una base vacía desde cero, ejecuta el script `tablas.sql` en SQLite3).*

## 👤 Autor

* **Ismael Llamur** - [@ismaelllamur013](https://github.com/ismaelllamur013)
