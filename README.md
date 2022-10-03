# Gestor de clientes en Python para Ingeniería


El grupo está formado por Paula Naranjo, Ana López y Andrea Manuel. 

Nuestra dirección de GitHub para este repositorio es la siguiente: [GitHub](https://github.com/paulaanb/Gestor_Clientes.git)
https://github.com/paulaanb/Gestor_Clientes.git

Hemos realizado un proyecto de gestor de clientes donde incluye:
·Listar los clientes del gestor.

·Consultar un cliente a partir del dni.

·Agregar un cliente con campos nombre, apellido, dni.

·Modificar el nombre y apellido de un cliente a partir del dni.

·Borrar un cliente a partir del dni.

·Salir del programa.

Al igual que no guarda los datos en el disco duro, siempre partirá de unos clientes de prueba iniciales y no podrá haber dos clientes con el mismo dni.

## Instalar las dependencias

_Nota: Sólo incluye pytest para realizar pruebas unitarias._

```bash
pip install -r requirements.txt
```

## Para probar el programa en modo gráfico

```bash
python run.py
```

## Para probar el programa en modo terminal

```bash
python run.py -t
```

## Para ejecutar las pruebas unitarias

```bash
pytest -v
```
El código es el siguiente:
# Carpeta gestor
# config
```
import sys

DATABASE_PATH = 'gestor/clientes.csv'
#lo ponemos aquí pq antes nos daba problemas
#pq antes las pruebaS nos modificaban el fichero csv, por eso lo hacemos constante
if 'pytest' in sys.argv[0]:
    DATABASE_PATH = 'tests/clientes_test.csv' #con esto las pruebas irán a bucar el nuevo fichero

```
# Database
```

import csv 
import config

class Cliente: #coge los datos y los devuelve
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
    
    def __str__(self): #Nos devuelve una cadena de caracteres, como si fuese el getter
        return f"({self.dni}) {self.nombre} {self.apellido}"
    
    def to_dict(self):
        return {'dni': self.dni, 'nombre': self.nombre, 'apellido' : self.apellido}
class Clientes: #Se encargará de uscar, crear, actualizar y borrar clientes
    #lista de clientes
    #Recogerá todos los datos dni, nombre y apellidos
    lista = []
    # Creamos la lista y cargamos los clientes en memoria
    with open(config.DATABASE_PATH, newline="\n") as fichero:
        reader = csv.reader(fichero, delimiter=";")
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)
            
    @staticmethod #Se le pone a los métodos q llamamos mucho, donde solo nos guarda lo último
    def buscar(dni):
        for cliente in Clientes.lista: #busca en la lista que hemos creado antes
            if cliente.dni == dni:
                return cliente
            
    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido) #llamamos a la clase Cliente
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni: #cliente nos recorre la lita, pero esta se compone de objetos de las clases, por eso podemos poner el .dni. Pq va asociado a la clase Clientes
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido =apellido
                Clientes.guardar()
                return Clientes.lista[indice]
    
    @staticmethod
    def borrar(dni):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(indice)
                Clientes.guardar()
                return cliente
            
    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, "w", newline="\n") as fichero:
            writer = csv.writer(fichero, delimiter=";")
            for c in Clientes.lista:
                writer.writerow((c.dni, c.nombre, c.apellido))
```
# helpers

```

import os
import re #para comprobar si lo que nos dan está bien
import platform #detecta el sistema operativo que queremos y lo adapta para poder trabajar con él.

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

#Es para poder leer un texto cómodamente
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        
#comprobamos dni
def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente.")
            return False
    return True
```
# menu
```

import os #para poder interactuar con la base
import helpers
import database as db

def iniciar():
     while True:
        helpers.limpiar_pantalla()
        
        print("========================")
        print(" BIENVENIDO AL Manager ")
        print("========================")
        print("[1] Listar clientes ")
        print("[2] Buscar cliente ")
        print("[3] Añadir cliente ")
        print("[4] Modificar cliente ")
        print("[5] Borrar cliente ")
        print("[6] Cerrar el Manager ")
        print("========================")
        
        opcion = input("> ")
        helpers.limpiar_pantalla()

        if opcion == '1':
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
                
        if opcion == '2':
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado.")
        
        if opcion == '3':
            print("Añadiendo un cliente...\n")
            # Comprobación de DNI válido
            dni = None
            while 1:
                dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break
            nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 chars)").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 chars)").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente.")
        
        if opcion == '4':
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"Nombre (de 2 a 30 chars) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido (de 2 a 30 chars) [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado.")
                
        if opcion == '5':
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
            print("Cliente borrado correctamente.") if db.Clientes.borrar(dni) else print("Cliente no encontrado.")
            
        if opcion == '6':
            print("Saliendo...\n")
            break
       
        input("\nPresiona ENTER para continuar...")


```

# run

```
import menu

if __name__=='__main__':
    menu.iniciar()

```

# Carpeta tests en gestor
# __init__

# test_database

```
import copy
import unittest
import helpers
import config
import csv
import database as db

# el unittest.TestCase es para que pase todos los datos de los test a esta clase
class TestDatabase(unittest.TestCase):
    
    def setUp(self): #Es un método de Python
        #se ejecuta antes de cada prueba
        db.Clientes.lista = [
            db.Cliente('15J', 'Marta', 'Pérez'), 
            db.Cliente('48H', 'Manolo', 'López'),
            db.Cliente('28Z', 'Ana', 'Garcia') ]
        
    #miramos cada método de la clase Clientes, siempre con la palabra test delante
    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15J')
        cliente_no_existente = db.Clientes.buscar('99X')
        self.assertIsNotNone(cliente_existente) #assert es como el print de los tests
        self.assertIsNone(cliente_no_existente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('39X', 'Héctor', 'Costa')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '39X')
        self.assertEqual(nuevo_cliente.nombre, 'Héctor')
        self.assertEqual(nuevo_cliente.apellido, 'Costa')
        
    
    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('28Z'))
        cliente_modificado = db.Clientes.modificar('28Z', 'Mariana', 'Pérez')
        self.assertEqual(cliente_a_modificar.nombre, 'Ana')
        self.assertEqual(cliente_modificado.nombre, 'Mariana')
 
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('48H')
        cliente_rebuscado = db.Clientes.buscar('48H')
        self.assertEqual(cliente_borrado.dni, '48H')
        self.assertNotEqual(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('23223S', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('48H', db.Clientes.lista))
    
    
    def test_escritura_csv(self):
        db.Clientes.borrar('48H')
        db.Clientes.borrar('15J')
        db.Clientes.modificar('28Z', 'Mariana', 'García')
        
        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline="\n") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            dni, nombre, apellido = next(reader) # Primera línea del iterador
        self.assertEqual(dni, '28Z')
        self.assertEqual(nombre, 'Mariana')
        self.assertEqual(apellido, 'García')

if __name__== '__main__':
    unittest.main()

```
