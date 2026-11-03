"""Funciones auxiliares para el juego Hundir la flota."""
import os
import random

import numpy as np

AGUA = "_"
BARCO = "O"
TOCADO = "X"
FALLO = "A"
ESLORAS = [2, 2, 2, 3, 3, 4]  # 3 de eslora 2, 2 de eslora 3 y 1 de eslora 4
ORIENTACIONES = ["N", "S", "E", "O"]

# Colores ANSI (os.system("") activa el soporte de colores en la consola de Windows)
os.system("")
RESET, NEGRITA = "\033[0m", "\033[1m"
AZUL, VERDE, ROJO, BLANCO, AMARILLO, CIAN = (
    "\033[34m", "\033[92m", "\033[91m", "\033[97m", "\033[93m", "\033[96m")
# Cómo se dibuja cada casilla: (símbolo, color)
VISTA = {
    AGUA: ("~", AZUL),
    BARCO: ("■", VERDE),
    TOCADO: ("✖", ROJO),
    FALLO: ("•", BLANCO),
}


def crear_tablero(tamaño=10):
    """Crea un tablero cuadrado relleno de '_'."""
    return np.full((tamaño, tamaño), AGUA)


def colocar_barco(barco, tablero):
    """Coloca un barco (lista de casillas) en el tablero.

    Devuelve True si se ha colocado; False si se sale del tablero
    o se superpone con otro barco (el tablero no se modifica).
    """
    filas, columnas = tablero.shape
    for f, c in barco:
        if not (0 <= f < filas and 0 <= c < columnas):
            return False
        if tablero[f, c] != AGUA:
            return False
    for casilla in barco:
        tablero[casilla] = BARCO
    return True


def disparar(casilla, tablero):
    """Dispara a una casilla. Devuelve 'tocado', 'agua' o 'repetido'.

    Lanza ValueError si la casilla está fuera del tablero.
    """
    f, c = casilla
    if not (0 <= f < tablero.shape[0] and 0 <= c < tablero.shape[1]):
        raise ValueError("Casilla fuera del tablero")
    if tablero[f, c] == BARCO:
        tablero[f, c] = TOCADO
        return "tocado"
    if tablero[f, c] == AGUA:
        tablero[f, c] = FALLO
        return "agua"
    return "repetido"


def crear_barco(eslora, tamaño=10):
    """Genera aleatoriamente las casillas de un barco dentro del tablero."""
    while True:
        f = random.randint(0, tamaño - 1)
        c = random.randint(0, tamaño - 1)
        orientacion = random.choice(ORIENTACIONES)
        df, dc = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}[orientacion]
        barco = [(f + i * df, c + i * dc) for i in range(eslora)]
        if all(0 <= x < tamaño and 0 <= y < tamaño for x, y in barco):
            return barco


def colocar_barcos(tablero, esloras=ESLORAS):
    """Coloca aleatoriamente todos los barcos sin solapamientos."""
    tamaño = tablero.shape[0]
    for eslora in esloras:
        while not colocar_barco(crear_barco(eslora, tamaño), tablero):
            pass
    return tablero


def quedan_barcos(tablero):
    """True si aún queda alguna casilla de barco sin tocar."""
    return bool((tablero == BARCO).any())


def mostrar_tableros(propio, enemigo):
    """Imprime el tablero propio y el del rival (ocultando sus barcos)."""
    visible = np.where(enemigo == BARCO, AGUA, enemigo)
    n = propio.shape[0]

    def fila(tab, i):
        celdas = []
        for v in tab[i]:
            simbolo, color = VISTA[v]
            celdas.append(f"{color}{simbolo}{RESET}")
        return " ".join(celdas)

    ancho = n * 2 + 2  # ancho visible de un tablero (índice + celdas)
    cab = "   " + " ".join(str(i) for i in range(n))
    titulos = "TU FLOTA".center(ancho + 1) + "      " + "FLOTA ENEMIGA".center(ancho + 1)
    borde = "   " + "─" * (n * 2 - 1)
    print()
    print(f"{NEGRITA}{CIAN}{titulos}{RESET}")
    print(f"{AMARILLO}{cab}        {cab}{RESET}")
    print(f"{borde}      {borde}")
    for i in range(n):
        print(f"{AMARILLO}{i:>2}{RESET}│{fila(propio, i)}      {AMARILLO}{i:>2}{RESET}│{fila(visible, i)}")
    print(f"{borde}      {borde}")
    print(f"  {VERDE}■{RESET} barco  {ROJO}✖{RESET} tocado  {BLANCO}•{RESET} agua  {AZUL}~{RESET} sin explorar\n")


def leer_coordenada(tamaño=10):
    """Pide fila y columna al jugador. Devuelve (fila, col) o None si quiere salir."""
    while True:
        texto = input(f"Disparo (fila,columna 0-{tamaño - 1}) o 's' para salir: ").strip().lower()
        if texto == "s":
            return None
        partes = texto.replace(",", " ").split()
        if len(partes) == 2 and all(p.isdigit() for p in partes):
            f, c = int(partes[0]), int(partes[1])
            if 0 <= f < tamaño and 0 <= c < tamaño:
                return (f, c)
        print("Coordenada no válida, prueba de nuevo (ej: 3,4).")


def disparo_maquina(tablero, ya_disparadas):
    """La máquina dispara aleatoriamente a una casilla no disparada antes."""
    tamaño = tablero.shape[0]
    while True:
        casilla = (random.randint(0, tamaño - 1), random.randint(0, tamaño - 1))
        if casilla not in ya_disparadas:
            ya_disparadas.add(casilla)
            return casilla, disparar(casilla, tablero)
