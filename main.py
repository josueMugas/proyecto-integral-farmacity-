import mysql.connector
from mysql.connector import errorcode
import hashlib
import datetime

cursor = None
cnx = None

def ConectarBase():
    global cnx, cursor
    try:
        cnx = mysql.connector.connect(user="root", password="", host="Localhost", database="farmacity")
        cursor = cnx.cursor(dictionary=True)
        print('Conexión establecida')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Usuario o contraseña incorrectos!')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('La base de datos no existe!')
        else:
            print(err)
ConectarBase()

def ConsultaSelect(tabla):
    Consulta = f"SELECT * FROM {tabla};"
    cursor.execute(Consulta)
    return cursor.fetchall()

medicamentos=ConsultaSelect("medicamentos")
def agregarCB():
    for medicamento in medicamentos:
        m = hashlib.sha256()
        id = medicamento["id"]
        id_bytes = str(medicamento["id"]).encode('UTF-8')
        m = hashlib.sha256()
        m.update(id_bytes)
        codigo_sha256 = m.hexdigest()
        consulta = (f"update medicamentos set codigo_barras='{codigo_sha256}' where id={id}")
        cursor.execute(consulta)
        cnx.commit()
        print(consulta)

clientes=ConsultaSelect("clientes")
def ordernarXcb():
    lista = medicamentos
    n = len(lista)
    for i in range(n - 1):
        Hay_Cambio = False
        for j in range(0, n - i - 1):
            if lista[j]["codigo_barras"] > lista[j + 1]["codigo_barras"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                Hay_Cambio = True
        if not Hay_Cambio:
            break
    return lista

def ordernarXdni():
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
    return lista

def busquedaXcb():
    arreglo = ordernarXcb()
    valor = int(input("escanee el codigo de barras: "))
    izquierda = 0
    derecha = len(arreglo) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arreglo[medio]["codigo_barras"] == valor:
            return arreglo[medio]
        elif arreglo[medio]["codigo_barras"] < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

def busquedaXdni():
    arreglo = ordernarXdni()
    valor = int(input("ingrese el dni: "))
    izquierda = 0
    derecha = len(arreglo) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arreglo[medio]["DNI"] == valor:
            return arreglo[medio]
        elif arreglo[medio]["DNI"] < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

def Agregarprioridadd():
    ID=int(input("ingrese el id del producto al que quiere ponerle prioridad: "))
    print(f"El medicamento es {medicamentos[ID-1]['nombre']}")
    prioridad=input("que prioridad desea agregarle: ")
    medicamentos[ID-1]["prioridad"]=prioridad
    for medicamento in medicamentos:
        print(medicamento)

def updateCompras(dni):
    Consulta = (f"update clientes set cantidad_compras=cantidad_compras+1 where DNI={dni}")
    cursor.execute(Consulta)
    cnx.commit()
    return cursor.lastrowid
def comprar():
    cliente=busquedaXdni()
    dni=cliente["DNI"]
    clienteID = cliente["id"]
    producto=busquedaXcb()
    productoID=producto["id"]
    cantidad=int(input("ingrese la cantidad del producto: "))
    fecha=datetime.date(int(input("ingrese el año: ")),int(input("ingrese el mes: ")),int(input("ingrese el dia: ")))
    if dni==clientes:
        updateCompras(dni)
    else:
        nombre=input("inserte su nombre: ").strip().lower()
        sql = f"INSERT INTO clientes (dni, nombre, cantidad_compras)VALUES( %s, %s,%s)"
        cursor.execute(sql, (dni, nombre ,1))
        cnx.commit()
    sql = f"INSERT INTO ventas (clientes_id, medicamentos_id, fecha,cantidad)VALUES( %s, %s,%s,%s)"
    cursor.execute(sql, (clienteID, productoID,fecha, cantidad))
    cnx.commit()
    return cursor.lastrowid

agregarCB()