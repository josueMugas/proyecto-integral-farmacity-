import mysql.connector  # librería para conectar con MySQL
from mysql.connector import errorcode  # códigos de error de mysql.connector
import hashlib  # para generar hashes (SHA-256)
import datetime  # para manejar fechas
import json  # para volcar datos a JSON

cursor = None  # cursor de la base de datos (se inicializa en conectarBase)
cnx = None  # conexión a la base de datos (se inicializa en conectarBase)

# Conección a la base de datos
def conectarBase():
    global cnx, cursor
    # Se intenta conectar la base de datos
    try:
        cnx = mysql.connector.connect(user="root", password="", host="Localhost", database="farmacity")
        cursor = cnx.cursor(dictionary=True)  # cursor que devuelve filas como diccionarios
        print('Conexión establecida')
    # Si no se puede, se identifica el error
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Usuario o contraseña incorrectos!')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('La base de datos no existe!')
        else:
            print(err)
conectarBase()  # conexión inicial al ejecutar la conexión

# Establecemos la consulta select dependiendo de la variable "Tabla"
def consultaSelect(tabla):
    Consulta = f"SELECT * FROM {tabla};"  # consulta dinámica(por depender de la tabla que se le ingrese)
    cursor.execute(Consulta)  # ejecuta la consulta con el cursor global
    return cursor.fetchall()  # retorna todas las filas como lista de diccionarios

# Se agregá un código de barras(a modo de hash SHA-256) a cada medicamento en la base de datos
def agregar_Codigo_Barras():
    medicamentos = consultaSelect("medicamentos")  # obtiene todos los medicamentos de la BD
    for medicamento in medicamentos:
        id = medicamento["id"]  # id del registro
        id_bytes = str(id).encode('UTF-8')  # convertir id a bytes para hashear
        # Se hashea el ID para tener el código de barras
        m = hashlib.sha256()
        m.update(id_bytes)
        codigo_sha256 = m.hexdigest()  # hash en formato hexadecimal
        # Se actualiza el código de barras en el id recorrido por el for
        consulta = (f"update medicamentos set codigo_barras='{codigo_sha256}' where id={id}")
        cursor.execute(consulta)
        cnx.commit()  # confirma la transacción en la base de datos

#=========================================================================================================================#
#-------------------------------------------FUNCIONES DE ORDENAMIENTO-----------------------------------------------------#
#=========================================================================================================================#

# Se ordena de forma binaria por código de barras los productos
def ordernarProductos():
    medicamentos = consultaSelect("medicamentos")  # carga actualizada desde BD
    lista = medicamentos  # alias local para manipular la lista
    n = len(lista)
    for i in range(n - 1):
        Hay_Cambio = False  # indicador para detectar si hubo intercambios en esta pasada
        for j in range(0, n - i - 1):  # no comparar los últimos i elementos ya ordenados
            if lista[j]["codigo_barras"] > lista[j + 1]["codigo_barras"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]  # intercambio
                Hay_Cambio = True
        if not Hay_Cambio:
            break  # si no hubo cambios, la lista ya está ordenada
    return lista  # retorna la lista ordenada

# Se ordena de forma binaria por DNI los clientes
def ordernarclientes():
    clientes = consultaSelect("clientes")  # carga clientes desde BD
    lista=clientes
    n = len(lista)
    for i in range(n - 1):
        Hay_Cambio = False
        for j in range(0, n - i - 1):
            if lista[j]["DNI"] > lista[j + 1]["DNI"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                Hay_Cambio = True
        if not Hay_Cambio:
            break
    return lista  # retorna lista de clientes ordenada por DNI

#=========================================================================================================================#
#------------------------------------------------  FUNCIONES DE BUSQUEDA  ------------------------------------------------#
#=========================================================================================================================#

# Búsqueda binaria de un producto por código de barras
def busquedaProducto(codigo_barras):
    arreglo = ordernarProductos()  # trabajar sobre lista ordenada por código
    valor = codigo_barras
    izquierda = 0
    derecha = len(arreglo) - 1
    # búsqueda binaria clásica
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arreglo[medio]["codigo_barras"] == valor:
            return arreglo[medio]  # retorna el diccionario del producto encontrado
        elif arreglo[medio]["codigo_barras"] < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1  # no encontrado

# Búsqueda binaria de un cliente por DNI
def busquedaCliente(dni):
    arreglo = ordernarclientes()  # lista de clientes ordenada por DNI
    valor = dni
    izquierda = 0
    derecha = len(arreglo) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arreglo[medio]["DNI"] == valor:
            return arreglo[medio]  # retorna el cliente encontrado
        elif arreglo[medio]["DNI"] < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1  # no encontrado

# Búsqueda secuencial de empleados por rol o nombre 
def busquedaEmpleados(opc):
    empleados=consultaSelect("empleados")  # obtiene empleados desde BD
    if opc == 1:
        Rol = input("ingrese el Rol a buscar")
        for empleado in empleados:
            if empleado["rol"] == Rol:
                return empleado  # retorna el primer empleado que coincida con el rol
    elif opc == 2:
        Nombre = input("ingrese el nombre a buscar")
        for empleado in empleados:
            if empleado["nombre"] == Nombre:
                return empleado  # retorna el primer empleado que coincida con el nombre
    else:
      print("sos un poco mogo down :D?")  # mensaje por opción inválida

#=========================================================================================================================#
#------------------------------------------------  FUNCIONES DE PRIORIDAD  ------------------------------------------------#
#=========================================================================================================================#

# Agrega prioridad a un producto específico
def agregarprioridad(prioridad,id_producto):
    Consulta = (f"update prioridad set prioridad='{prioridad}' where id={id_producto}")  # actualiza prioridad para un producto específico
    cursor.execute(Consulta)
    cnx.commit()
    print("Prioridad Aplicada correctamente") # confirma la operación
    return cursor.lastrowid  # retorna id del cursor

#=========================================================================================================================#
#------------------------------------------------  FUNCIONES DE COMPRA  --------------------------------------------------# 
#=========================================================================================================================#

def updateCompras(dni):
    Consulta = (f"update clientes set cantidad_compras=cantidad_compras+1 where DNI={dni}")  # incrementa contador de compras del cliente según DNI
    cursor.execute(Consulta) # ejecuta la consulta SQL
    cnx.commit() # confirma la transacción de datos a la base de datos
    return cursor.lastrowid


def comprar(DNI,cantidad,fecha,empleado_id):
    cliente = busquedaCliente(DNI)  # busca cliente por DNI
    if cliente != -1: # si el cliente existe
        dni = cliente["DNI"] # obtiene DNI del cliente encontrado
        clienteID = cliente["id"] # obtiene ID del cliente
        producto = busquedaProducto(input("ingrese el codigo de barras: "))  # pide código de barras del producto
        productoID = producto["id"] # obtiene ID del producto
        cantidad = cantidad  # mantiene la cantidad de productos comprados pasada
        empleado = empleado_id  # asigna el id del empleado que   realizó la venta 
        fecha = fecha # asigna la fecha de la compra
        updateCompras(dni)  # incrementa contador de compras del cliente
        sql = f"INSERT INTO ventas (clientes_id, medicamentos_id, fecha,cantidad,empleado_id)VALUES( %s,%s, %s,%s,%s)" # consulta para registrar la venta
        cursor.execute(sql, (clienteID, productoID, fecha, cantidad, empleado)) # ejecuta la inserción de la venta
        cnx.commit() # confirma la transacción en la base de datos
        return cursor.lastrowid
    else: # si el cliente no existe, se crea uno nuevo
        nombre=input("inserte su nombre: ").strip().lower()  # solicita nombre y lo normaliza
        sql = f"INSERT INTO clientes (dni, nombre, cantidad_compras)VALUES( %s, %s,%s)" # consulta para crear nuevo cliente
        cursor.execute(sql, (DNI, nombre ,1))  # crea nuevo cliente con 1 compra
        cnx.commit() # confirma la transacción en la base de datos
        cliente = busquedaCliente(DNI)  # recupera el cliente creado
        clienteID = cliente["id"]   # obtiene ID del nuevo cliente
        producto = busquedaProducto(input("ingrese el codigo de barras: "))  # pide código de barras
        productoID = producto["id"]  # obtiene ID del producto
        cantidad = cantidad  # mantiene la cantidad de productos comprados pasada
        empleado = empleado_id  # asigna el id del empleado que  realizó la venta 
        fecha = fecha # asigna la fecha de la compra
        sql = f"INSERT INTO ventas (clientes_id, medicamentos_id, fecha,cantidad,empleado_id)VALUES( %s,%s, %s,%s,%s)" # consulta para registrar la venta
        cursor.execute(sql, (clienteID, productoID,fecha, cantidad,empleado)) # ejecuta la inserción de la venta
        cnx.commit() # confirma la transacción en la base de datos
        return cursor.lastrowid

#=========================================================================================================================#
#------------------------------------------------  MENÚ PRINCIPAL  -------------------------------------------------------#
#=========================================================================================================================#

def menu():
    while True:
        opcion=int(input("""
    |=======================|
    |    Farmacity Menu     |
    |=======================|
    | 1) Mostrar Stock      |
    | 2) Mostrar Empleados  |
    | 3) Mostrar Clientes   |
    | 4) Mostrar Ventas     |
    | 5) Realizar pedido    |
    | 6) Buscar Producto    |
    | 7) Buscar Empleado    |
    | 8) Buscar Cliente     |
    | 9) Agregar Prioridad  |
    | 10) salir             |
    |=======================|
    | ingrese una opcion: """))
        if opcion == 1: 
            
            medicamentos = consultaSelect("medicamentos")  # carga actualizada y la muestra
            for medicamento in medicamentos: # muestra cada medicamento
                print(medicamento)
                
        elif opcion == 2:
            
            empleados = consultaSelect("empleados")  # carga empleados y los muestra
            for empleado in empleados: # muestra cada empleado
                print(empleado)
                
        elif opcion == 3:
            
            clientes = consultaSelect("clientes")  # carga clientes y los muestra
            for cliente in clientes: # muestra cada cliente
                print(cliente)
                
        elif opcion == 4:
            
            ventas = consultaSelect("ventas")  # carga ventas y las muestra
            for venta in ventas: # muestra cada venta
                print(venta)
                
        elif opcion == 5:
            
            DNI=int(input("ingrese del cliente dni")) # pide DNI del cliente
            cantidad = int(input("ingrese la cantidad del producto: ")) # pide cantidad de productos
            empleado = int(input("ingrese su ID: ")) # pide ID del empleado que realiza la venta
            fecha=datetime.date(int(input("ingrese el año: ")),int(input("ingrese el mes: ")),int(input("ingrese el dia: "))) # pide fecha de la compra
            comprar(DNI,cantidad,fecha,empleado)  # registra la compra
            ParaJson = str(ventas)  # convierte ventas a string (nota: ventas no se actualiza aquí)
            with open("ventas.json", 'w', encoding='utf-8') as archivo: # abre archivo JSON para escritura y mantener un registro de ventas
                json.dump(ParaJson, archivo, indent=4, ensure_ascii=False)  # guarda en JSON el string de ventas
                
        elif opcion == 6:
            
            codigo_barras=input("escanee el codigo de barras: ") # pide código de barras
            print(busquedaProducto(codigo_barras))  # muestra resultado de la búsqueda
            
        elif opcion == 7:
            
            opc = int(input("""
               |===========|
               | 1)Rol     |
               | 2)Nombre  |
               |===========|
                               """))
            
            print(busquedaEmpleados(opc))  # búsqueda por rol o nombre
            
        elif opcion == 8:
            
           dni = int(input("ingrese el dni: ")) # pide DNI del cliente
           print(busquedaCliente(dni))  # búsqueda de cliente por DNI
           
        elif opcion==9:
            
            prioridad = int(input("ingrese el id del producto al que quiere ponerle prioridad: ")) # pide ID del producto al que agregar prioridad    
            agregarprioridad(prioridad)  # aplica prioridad (sin WHERE, afecta todos los registros)
            
        elif opcion ==10:
            
            print("saliendo...")
            break  # sale del menú
        
        else:
            
            print("opcion incorrecta, intente de nuevo")
            
agregar_Codigo_Barras()  # genera códigos los de barras en la BD al iniciar
menu()  # inicia el menú interactivo