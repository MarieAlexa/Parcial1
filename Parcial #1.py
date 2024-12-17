import sqlite3


conexion = sqlite3.connect("presupuesto.db")

# Crear tabla si no existe
conexion.execute("""
CREATE TABLE IF NOT EXISTS articulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    cantidad REAL NOT NULL,
    precio_unitario REAL NOT NULL
)
""")
conexion.commit()


def menu():
    print("\nSistema de Registro de Presupuesto")
    print("1. Registro de artículo")
    print("2. Búsqueda de artículos")
    print("3. Edición de artículo")
    print("4. Eliminación de artículo")
    print("5. Salir")


def registrar_articulo():
    nombre = input("Nombre del artículo: ")
    categoria = input("Categoría: ")
    cantidad = float(input("Cantidad: "))
    precio_unitario = float(input("Precio unitario: "))

    conexion.execute("""
    INSERT INTO articulos (nombre, categoria, cantidad, precio_unitario)
    VALUES (?, ?, ?, ?)
    """, (nombre, categoria, cantidad, precio_unitario))
    conexion.commit()
    print("Artículo registrado con éxito.")


def buscar_articulos():
    termino = input("Ingrese el término de búsqueda: ")
    cursor = conexion.execute("""
    SELECT * FROM articulos
    WHERE nombre LIKE ? OR categoria LIKE ?
    """, (f"%{termino}%", f"%{termino}%"))
    resultados = cursor.fetchall()

    if resultados:
        print("\nResultados:")
        for articulo in resultados:
            print(f"ID: {articulo[0]}, Nombre: {articulo[1]}, Categoría: {articulo[2]}, Cantidad: {articulo[3]}, Precio Unitario: {articulo[4]}")
    else:
        print("No se encontraron artículos.")


def editar_articulo():
    id_articulo = input("Ingrese el ID del artículo a editar: ")
    cursor = conexion.execute("SELECT * FROM articulos WHERE id = ?", (id_articulo,))
    articulo = cursor.fetchone()

    if articulo:
        print(f"Editando el artículo: {articulo[1]}")
        nuevo_nombre = input(f"Nuevo nombre ({articulo[1]}): ") or articulo[1]
        nueva_categoria = input(f"Nueva categoría ({articulo[2]}): ") or articulo[2]
        nueva_cantidad = input(f"Nueva cantidad ({articulo[3]}): ") or articulo[3]
        nuevo_precio = input(f"Nuevo precio unitario ({articulo[4]}): ") or articulo[4]

        conexion.execute("""
        UPDATE articulos
        SET nombre = ?, categoria = ?, cantidad = ?, precio_unitario = ?
        WHERE id = ?
        """, (nuevo_nombre, nueva_categoria, nueva_cantidad, nuevo_precio, id_articulo))
        conexion.commit()
        print("Artículo actualizado con éxito.")
    else:
        print("No se encontró el artículo con ese ID.")


def eliminar_articulo():
    id_articulo = input("Ingrese el ID del artículo a eliminar: ")
    cursor = conexion.execute("SELECT * FROM articulos WHERE id = ?", (id_articulo,))
    articulo = cursor.fetchone()

    if articulo:
        conexion.execute("DELETE FROM articulos WHERE id = ?", (id_articulo,))
        conexion.commit()
        print("Artículo eliminado con éxito.")
    else:
        print("No se encontró el artículo con ese ID.")


# Bucle principal
while True:
    menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_articulo()
    elif opcion == "2":
        buscar_articulos()
    elif opcion == "3":
        editar_articulo()
    elif opcion == "4":
        eliminar_articulo()
    elif opcion == "5":
        print("Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
