import csv
from xml.dom.pulldom import END_DOCUMENT
import config


class Cliente: #Coge los datos y los devuelve
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"

    def to_dict(self):
        return {'dni': self.dni, 'nombre': self.nombre, 'apellido': self.apellido}


class Clientes:

    lista = [] #creamos la lista y cargamos los clientes en memoria
    with open(config.DATABASE_PATH, newline='\n') as fichero:
        reader = csv.reader(fichero, delimiter=';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    @staticmethod#a las funciones que llamemos mucho, para que solo nos guarde lo ultimo
    def busca(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente #nos lo devuelve si el dni aparece en la lista de registrados
        

    @staticmethod
    def crear(dni, nombre, apellido): 
        cliente = Cliente(dni, nombre, apellido)#llamamos a la clase cliente
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente

    @staticmethod
    def modificar(dni, nombre, apellido):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni: #cliente nos recorre la lsta, pero esta se compone de objetos de las clases, por eso ponemos el .dni
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[indice]

    @staticmethod
    def borrador(dni):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(indice)
                cliente.guardar()
                return cliente
        

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.dni, cliente.nombre, cliente.apellido))
