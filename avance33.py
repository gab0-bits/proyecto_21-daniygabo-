import random
import datetime

bitacora = open("bitacoravance.txt", "a")

baraja_cartas = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'As'] * 4
cartas_salidas = []
jugador1_puntos = 0
jugador2_puntos = 0

def generador_cartas():
    if len(baraja_cartas) == 0:
        return None

    cartas_generadas = random.sample(baraja_cartas, 2)
    for carta in cartas_generadas:
        baraja_cartas.remove(carta)
        cartas_salidas.append(carta)

    return cartas_generadas

def contar_cartas_restantes():
    contador_cartas = {}
    for carta in baraja_cartas:
        if carta in contador_cartas:
            contador_cartas[carta] += 1
        else:
            contador_cartas[carta] = 1
    return contador_cartas

def valor_carta(carta, acumulado):
    if carta == 'As':
        if acumulado + 11 <= 21:
            while True:
                valor = input("¿Desea que el As valga 1 u 11? ")
                if valor == '1' or valor == '11':
                    return int(valor)
                else:
                    print("Opción inválida. Por favor, ingrese '1' o '11'.")
        else:
            return 1
    elif type(carta) == int:
        return carta
    else:
        return 10

def suma_puntaje(mano):
    suma = sum([valor_carta(carta, sum([valor_carta(c, 0) for c in mano[:i]])) for i, carta in enumerate(mano)])
    return suma

def jugador_virtual(acumulado):
    if acumulado == 0:
        return True
    elif acumulado <= 9:
        return True
    elif acumulado <= 14:
        return False
    elif acumulado < 21:
        return random.choice([True, False])
    else:
        return False

def actualizar_bitacora(texto):
    with open("bitacoravance.txt", "a") as bitacora_file:
        bitacora_file.write(texto + "\n")

def imprimir_baraja():
    contador_cartas = contar_cartas_restantes()
    print("Cartas restantes en la baraja:")
    for carta, cantidad in contador_cartas.items():
        print(f"{carta}: {cantidad} carta(s)")

def imprimir_mano(jugador, mano):
    print(f"{jugador} tiene:", mano)

def calcular_puntos(puntos):
    if puntos == 21:
        return 6
    elif puntos < 21 and puntos >= 17:
        return 2
    elif puntos < 17:
        return 1
    else:
        return 0

def pedir_carta(jugador, mano, acumulado):
    carta = baraja_cartas.pop(random.randint(0, len(baraja_cartas) - 1))
    cartas_salidas.append(carta)
    mano.append(carta)
    nuevo_puntaje = suma_puntaje(mano)
    print(f"{jugador} solicitó carta.")
    print(f"{jugador} recibió: {carta} (valor: {valor_carta(carta, acumulado)})")
    print(f"{jugador} tiene:", mano)
    print(f"El total de la mano de {jugador}: {nuevo_puntaje}\n")
    return nuevo_puntaje

def turno_jugador(jugador, mano, puntaje):
    while True:
        respuesta = input(f"{jugador}, ¿Desea solicitar otra carta? (s/n): ").lower()
        if respuesta == "n":
            break
        elif respuesta == "s":
            puntaje = pedir_carta(jugador, mano, puntaje)
        else:
            print("Respuesta inválida. Por favor, ingrese 's' para sí o 'n' para no.")
    return puntaje

def jugar():
    global jugador1_puntos, jugador2_puntos

    mano_1 = generador_cartas()
    if mano_1 is None:
        print("¡El juego se ha terminado! No quedan cartas disponibles.")
        return

    mano_2 = generador_cartas()
    if mano_2 is None:
        print("¡El juego se ha terminado! No quedan cartas disponibles.")
        return

    jugador1_puntos = suma_puntaje(mano_1)
    jugador2_puntos = suma_puntaje(mano_2)

    imprimir_mano("Jugador 1", mano_1)
    imprimir_mano("Jugador 2", mano_2)

    actualizar_bitacora(f"{datetime.datetime.now().strftime('%H:%M:%S')} | JUGADOR 1 solicitó cartas.")
    actualizar_bitacora(f"{datetime.datetime.now().strftime('%H:%M:%S')} | JUGADOR 1 tiene: {mano_1}")
    actualizar_bitacora(f"{datetime.datetime.now().strftime('%H:%M:%S')} | JUGADOR 1 total de la mano: {jugador1_puntos}\n")

    turno_jugador1 = True
    while True:
        if turno_jugador1:
            jugador1_puntos = turno_jugador("Jugador 1", mano_1, jugador1_puntos)
            if jugador1_puntos >= 21:
                break
        else:
            if jugador_virtual(jugador2_puntos):
                jugador2_puntos = pedir_carta("Jugador 2", mano_2, jugador2_puntos)
                if jugador2_puntos >= 21:
                    break
            else:
                turno_jugador1 = True

        turno_jugador1 = not turno_jugador1

    puntos_jugador1 = calcular_puntos(jugador1_puntos)
    puntos_jugador2 = calcular_puntos(jugador2_puntos)
    print("Puntos Jugador 1:", puntos_jugador1)
    print("Puntos Jugador 2:", puntos_jugador2)

    if puntos_jugador1 > puntos_jugador2:
        print("¡Jugador 1 gana!")
        actualizar_bitacora(f"{datetime.datetime.now().strftime('%H:%M:%S')} | GANADOR: JUGADOR 1\n")
    elif puntos_jugador1 < puntos_jugador2:
        print("¡Jugador 2 gana!")
        actualizar_bitacora(f"{datetime.datetime.now().strftime('%H:%M:%S')} | GANADOR: JUGADOR 2\n")
    else:
        print("¡Empate!")
        actualizar_bitacora(f"{datetime.datetime.now().strftime('%H:%M:%S')} | ¡EMPATE!\n")

def menu_bienvenida():
    print("Bienvenido al juego de Blackjack.")
    print("Seleccione una opción:")
    print("1. Jugar")
    print("2. Ver baraja restante")
    print("3. Salir")

def main():
    while True:
        menu_bienvenida()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            jugar()
        elif opcion == "2":
            imprimir_baraja()
        elif opcion == "3":
            print("Juego terminado.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida (1, 2 o 3).")

if __name__ == "__main__":
    main()

bitacora.close()
