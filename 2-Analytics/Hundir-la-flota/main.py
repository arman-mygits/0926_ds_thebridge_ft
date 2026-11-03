"""Hundir la flota: jugador contra máquina. Ejecutar con: python main.py"""
from utils import (
    crear_tablero, colocar_barcos, disparar, quedan_barcos,
    mostrar_tableros, leer_coordenada, disparo_maquina,
)

TAMAÑO = 10


def jugar():
    mi_tablero = colocar_barcos(crear_tablero(TAMAÑO))
    tablero_maquina = colocar_barcos(crear_tablero(TAMAÑO))
    disparos_maquina = set()

    print("¡Bienvenido a Hundir la flota!")
    print("O = barco, X = tocado, A = agua, _ = sin explorar")

    while True:
        mostrar_tableros(mi_tablero, tablero_maquina)

        # Turno del jugador (repite si acierta)
        turno_jugador = True
        while turno_jugador:
            casilla = leer_coordenada(TAMAÑO)
            if casilla is None:
                print("Has abandonado la partida. ¡Hasta pronto!")
                return
            resultado = disparar(casilla, tablero_maquina)
            if resultado == "repetido":
                print("Ya disparaste ahí, elige otra casilla.")
            elif resultado == "tocado":
                print("¡Tocado!")
                if not quedan_barcos(tablero_maquina):
                    mostrar_tableros(mi_tablero, tablero_maquina)
                    print("¡¡Has ganado!! Hundiste toda la flota enemiga.")
                    return
                mostrar_tableros(mi_tablero, tablero_maquina)
            else:
                print("Agua.")
                turno_jugador = False

        # Turno de la máquina (repite si acierta)
        turno_maquina = True
        while turno_maquina:
            casilla, resultado = disparo_maquina(mi_tablero, disparos_maquina)
            print(f"La máquina dispara a {casilla}: {resultado}")
            if resultado == "tocado":
                if not quedan_barcos(mi_tablero):
                    mostrar_tableros(mi_tablero, tablero_maquina)
                    print("Has perdido. La máquina hundió toda tu flota.")
                    return
            else:
                turno_maquina = False


if __name__ == "__main__":
    jugar()
