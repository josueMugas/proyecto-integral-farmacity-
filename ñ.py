mult=1
arreglo=[4,5,5,6,1,3,345,4]
def factorial(numero):
    global mult
    if numero==1:
        mult*= numero
        print(mult)
        return mult
    mult*= numero
    factorial(numero-1)

pocicion=0
suma=0
def suma(pocicion):
    global suma
    if pocicion==len(arreglo)-1:
        suma+= arreglo[pocicion]
        print(suma)
        return suma
    suma+=arreglo[pocicion]
    suma(pocicion+1)

class medicamentos:
    def __init__(self,nombre,stock,precio,categoria,codigoBarras):
        self.nombre=nombre
        self.stock = stock
        self.precio = precio
        self.categoria = categoria
        self.codigoBarras = codigoBarras

    def sumarStock(self,cantidad):
        self.stock += cantidad
        print(f"el stock actual es de {self.stock}")

    def comprar(self,cantidad):
        if cantidad <= self.stock:
            self.stock = cantidad
            print(f"el stock actual es de {self.stock}")
        else:
            print("no hay suficiente stock")