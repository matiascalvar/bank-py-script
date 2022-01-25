# Matias Calvar
import os
import random
import numpy as np
from pyrecord import Record as Record
###############################################
# Vector-registro CUENTAS
Rcuentas = Record.create_type("Rcuentas", "nro_cuenta", "apellido", "nombre", "dni", "tipo_cuenta", "saldo", "sw",
                              nro_cuenta=0, apellido=' ', nombre=' ', dni=' ', tipo_cuenta=0, saldo=0.0, sw=True)
# Segun documentation, se pueden setear defaults pero no tipos de datos.

CUENTAS = np.array([Rcuentas]*650)
i_cuentas = 0
# Vector-registro CAJEROS
Rcajeros = Record.create_type("Rcajeros", "nro_cajero", "ubicacion", "cant_mov",
                              nro_cajero=0, ubicacion=' ', cant_mov=0)
CAJEROS = np.array([Rcajeros]*120)

###############################################


def carga_cajeros():
    i = 0
    cajeros = open('cajeros.txt', 'r')
    linea_cajero = cajeros.readline().strip()
    while linea_cajero != "" and i < len(CAJEROS):
        s = linea_cajero.split(",")
        nro_caj = int(s[0])
        ubic = s[1]
        mov = int(s[2])

        CAJEROS[i] = Rcajeros()
        CAJEROS[i].nro_cajero = nro_caj
        CAJEROS[i].ubicacion = ubic
        CAJEROS[i].cant_mov = mov
        linea_cajero = cajeros.readline().strip()
        i = i + 1


def carga_vec_cuentas():
    global i_cuentas
    i_cuentas = 0
    cuentas = open('cuentas.txt', 'r')
    linea_cuentas = cuentas.readline().strip()
    while linea_cuentas != "":
        s = linea_cuentas.split(",")
        nro_cuenta = int(s[0])
        apellido = s[1]
        nombre = s[2]
        dni = int(s[3])
        tip_cuenta = int(s[4])
        saldo = float(s[5])
        sw = bool(s[6])

        CUENTAS[i_cuentas] = Rcuentas()
        CUENTAS[i_cuentas].nro_cuenta = nro_cuenta
        CUENTAS[i_cuentas].apellido = apellido
        CUENTAS[i_cuentas].nombre = nombre
        CUENTAS[i_cuentas].dni = dni
        CUENTAS[i_cuentas].tipo_cuenta = tip_cuenta
        CUENTAS[i_cuentas].saldo = saldo
        CUENTAS[i_cuentas].sw = sw
        i_cuentas = i_cuentas + 1
        linea_cuentas = cuentas.readline().strip()
    # Carga de cuenta extra indicada en el aula virtual para evitar errores
    CUENTAS[i_cuentas] = Rcuentas()
    CUENTAS[i_cuentas].nro_cuenta = 1600
    CUENTAS[i_cuentas].apellido = 'MUSSO'
    CUENTAS[i_cuentas].nombre = 'LUCCA'
    CUENTAS[i_cuentas].dni = '35897451'
    CUENTAS[i_cuentas].tipo_cuenta = '6'
    CUENTAS[i_cuentas].saldo = 4500.56
    CUENTAS[i_cuentas].sw = 'TRUE'

###############################################

# Carga de archivos desde operaciones.txt


def procesar_archivo():
    operaciones = open('operaciones.txt', 'r')
    linea = operaciones.readline().strip()
    arr_mov_cajeros = np.array([0]*120)
    while linea != "":
        s = linea.split(",")
        cuenta_ant = s[0]

        sum_saldo = 0
        while linea != "" and cuenta_ant == s[0]:
            # Guardo nro de cuenta, tipo de movimiento, dinero y nro cajero
            nro_cuenta_op = int(s[0])
            tipo_mov = int(s[5])
            mov_dinero = float(s[6])
            nro_cajero = int(s[4])
            # Actualizar saldo en CUENTAS
            if tipo_mov == 1:
                sum_saldo += mov_dinero
            elif tipo_mov == 2:
                sum_saldo -= mov_dinero

            # Actualizo cantidad de movimiento de cajeros en array temporal
            arr_mov_cajeros[nro_cajero-1] += 1

            linea = operaciones.readline().strip()
            s = linea.split(",")
            #-------------FIN DEL 2º WHILE---------------------#
        # Actualizo el saldo de cada cuenta con el total acumulado dentro del while
        CUENTAS[nro_cuenta_op -
                1000].saldo = CUENTAS[nro_cuenta_op - 1000].saldo + sum_saldo

        linea = operaciones.readline().strip()
        # Informo total anual en pesos de los movimientos de cada cuenta
        print(
            f"El movimiento anual de la cuenta número: {CUENTAS[nro_cuenta_op - 1000].nro_cuenta} es ${CUENTAS[nro_cuenta_op - 1000].saldo}")
    #-------------FIN DEL 1º WHILE---------------------#

    # Paso al archivo CAJEROS desde array temporal y determino el cajero con mayor movimiento
    cant_mov_may = 0
    nro_caj_may = -1
    for i in range(len(CAJEROS)):
        CAJEROS[i].cant_mov += arr_mov_cajeros[0]
        if CAJEROS[i].cant_mov > cant_mov_may:
            cant_mov_may = CAJEROS[i].cant_mov
            nro_caj_may = CAJEROS[i].nro_cajero

    # Informo que cajero registró mayor cantidad de movimientos durante el año.
    print(
        f"\nEl cajero que mas movimientos realizó fue el cajero número {nro_caj_may} de {CAJEROS[nro_caj_may-1].ubicacion} con {cant_mov_may} realizados.\n")

    operaciones.close()


###############################################

# Consulta de saldo
def consulta_cuenta(nro_cuenta):
    if (nro_cuenta - 1000) <= i_cuentas and (nro_cuenta - 1000) >= 0:
        print("Apellido: ", CUENTAS[nro_cuenta-1000].apellido)
        print("Nombre: ", CUENTAS[nro_cuenta-1000].nombre)
        print("DNI: ", CUENTAS[nro_cuenta-1000].dni)
        print("El saldo de la cuenta es: ", CUENTAS[nro_cuenta-1000].saldo)
        if CUENTAS[nro_cuenta-1000].sw == False:
            print("La cuenta está inactiva\n")
    else:
        print("El número de cuenta ingresado no es correcto")

###############################################

# Alta de cuentas


def alta_cuenta(dni_ingresado):
    # Verificamos si la cuenta ya existe
    global i_cuentas
    existe = False
    de_baja = False

    for i in range(i_cuentas):
        if dni_ingresado == CUENTAS[i].dni:
            existe = True
            index = i
            if CUENTAS[i].sw == True:
                de_baja = True
    if existe == True:
        print("Esa persona ya es cliente del banco. Sus datos son: ")
        print("Apellido: ", CUENTAS[index].apellido)
        print("Nombre: ", CUENTAS[index].nombre)
        print("Número de cuenta: ", CUENTAS[index].nro_cuenta)

    elif de_baja == True:
        print("La cuenta fue dada de baja anteriormente")
    elif existe == False:
        # Cargamos la cuenta
        i_cuentas = i_cuentas + 1
        CUENTAS[i_cuentas] = Rcuentas()
        CUENTAS[i_cuentas].nro_cuenta = i_cuentas + 1000
        CUENTAS[i_cuentas].apellido = input("Ingrese su Apellido\n")
        CUENTAS[i_cuentas].nombre = input("Ingrese su Nombre\n")
        CUENTAS[i_cuentas].dni = dni_ingresado
        CUENTAS[i_cuentas].tipo_cuenta = input("Ingrese tipo de Cuenta\n")
        CUENTAS[i_cuentas].saldo = input("Ingrese el saldo\n")
        CUENTAS[i_cuentas].sw = True
        print("Cuenta agregada!")


# Borrado de cuentas


def del_cuenta(nro_cuenta):
    if (nro_cuenta - 1000) <= i_cuentas and (nro_cuenta - 1000) >= 0:
        if CUENTAS[nro_cuenta-1000].sw == True:
            CUENTAS[nro_cuenta-1000].sw = False
            print("La cuenta ha sido dada de baja")
        elif CUENTAS[nro_cuenta-1000].sw == False:
            print("No es posible realizar la acción.")
            print("La cuenta ya había sido dado de baja anteriormente.")
            print("¿Desea reactivarla? Ingrese 1 para reactivarla o 0 para salir.")
            optn = int(input("Ingrese una opcion: \n"))
            if optn == 1:
                CUENTAS[nro_cuenta-1000].sw = True
                print("La cuenta ha sido reactivada con éxito.")
    else:
        print("El número de cuenta ingresado no es correcto")


# Modificacion de cuentas CORREGIR


def mod_cuenta(nro_cuenta):
    if (nro_cuenta - 1000) <= i_cuentas and (nro_cuenta - 1000) >= 0:
        op = -1
        while op != 0:
            limpiar_pantalla()
            print("Datos actuales de la cuenta:")
            print("Apellido: ", CUENTAS[nro_cuenta - 1000].apellido)
            print("Nombre: ", CUENTAS[nro_cuenta - 1000].nombre)
            print("Tipo de cuenta: ", CUENTAS[nro_cuenta - 1000].tipo_cuenta)
            print(" ")
            print("¿Que dato desea modificar?")
            print("-Apellido 1")
            print("-Nombre 2")
            print("-Tipo de Cuenta 3")
            print("-Para volver al menu anterior ingrese 0\n")
            op = int(input("Ingrese una opcion: \n"))

            if op == 1:
                CUENTAS[nro_cuenta -
                        1000].apellido = input("Ingrese nuevo apellido:")
                print("Información actualizada")
            if op == 2:
                CUENTAS[nro_cuenta -
                        1000].nombre = input("Ingrese nuevo nombre:")
                print("Información actualizada")
            if op == 3:
                CUENTAS[nro_cuenta -
                        1000].tipo_cuenta = input("Ingrese nuevo tipo de cuenta:")
                print("Información actualizada")
            if op == 0:
                limpiar_pantalla()
    else:
        print("El número de cuenta ingresado no es correcto")


###############################################


def limpiar_pantalla():
    if (os.name) == 'posix':
        os.system('clear')
    if (os.name) == 'nt':
        os.system('cls')
    return None

###############################################

# Menu principal


def menu():
    option = -1
    while option != 0:
        print("\n")
        print("Menu:")
        print("---------------------------------")
        print("-1- Cargar vectores")
        print("-2- Procesar movimientos")
        print("-3- Consultar saldo")
        print("-4- Alta de cuenta")
        print("-5- Borrado de cuenta")
        print("-6- Modificacion de cuenta")
        print("--Para salir ingrese 0--\n")
        print("---------------------------------")
        option = int(input("Ingrese una opcion: \n"))
        if option == 1:
            carga_cajeros()
            carga_vec_cuentas()
            print("Vectores CUENTAS y CAJEROS cargados correctamente.")
        elif option == 2:
            procesar_archivo()
        elif option == 3:
            nro_cuenta = int(input("Ingrese número de cuenta \n"))
            consulta_cuenta(nro_cuenta)
        elif option == 4:
            dni_ingresado = int(input("Ingrese DNI \n"))
            alta_cuenta(dni_ingresado)
        elif option == 5:
            nro_cuenta = int(input("Ingrese número de cuenta \n"))
            del_cuenta(nro_cuenta)
        elif option == 6:
            nro_cuenta = int(input("Ingrese número de cuenta \n"))
            mod_cuenta(nro_cuenta)
        input("Presione Enter para continuar...")
        limpiar_pantalla()


menu()
