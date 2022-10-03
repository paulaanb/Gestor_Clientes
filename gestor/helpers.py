import os
import re #para comrobar si lo que hemos hecho está bien
import platform #detecta el sistema operativo que queremos y lo adapta para poder trabajar con él

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

#para poder leer un texto fácilmente
def leer_texto(longitud_min = 0, longitud_max = 100, mnsj = None):
    print(mnsj) if mnsj else None
    while True:
        texto = input("> ")
        if longitud_min <= len(texto) <= longitud_max:
            return texto

#comprobamos dni
def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, no cumple el formato establecido")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI ya en uso por otro cliente")
            return False
    return True

    