import random
import datetime

def crear_bitacora():
    nombre_archivo = "bitacora_partida_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    return open(nombre_archivo, "a")

baraja_cartas = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'As'] * 4
cartas_salidas = []
jugador1_puntos_acumulados = 0
jugador2_puntos_acumulados = 0

def generador_cartas():
    if len(baraja_cartas) < 2:
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

def valor_carta(carta, acumulado, mano):
    if carta == 'As':
        if acumulado + 11 <= 21 and len(mano) > 0:
            print(f"Tienes un As y otra carta en la mano: {mano[0]}.")
            while True:
                valor = input("¿Deseas que el As valga 1 u 11? ")
                if valor == '1' or valor == '11':
                    return int(valor)
                else:
                    print("Opción inválida. Por favor, ingresa '1' o '11'.")
        else:
            return 1
    elif type(carta) == int:
        return carta
    else:
        return 10

def suma_puntaje(mano):
    suma = sum([valor_carta(carta, sum([valor_carta(c, 0, mano[:i]) for c in mano[:i]]), mano[:i]) for i, carta in enumerate(mano)])
    return suma

def jugador_virtual(acumulado, adversario_acumulado, primera_vez):
    if primera_vez:
        return True
    elif acumulado <= 9:
        return True
    elif 9 < acumulado <= 14:
        return adversario_acumulado > 14
    elif 14 < acumulado < 21:
        return random.choice([True, False])
    else:
        return False

def actualizar_bitacora(bitacora, texto):
    now = datetime.datetime.now().strftime('%I:%M:%S %p')
    bitacora.write(f"{now}, {texto}\n")

def pedir_carta(jugador, mano, acumulado, bitacora):
    if acumulado >= 21:
        print(f"{jugador} ya tiene 21 o más puntos. No se puede pedir más cartas.")
        return acumulado
    carta = baraja_cartas.pop(random.randint(0, len(baraja_cartas) - 1))
    cartas_salidas.append(carta)
    mano.append(carta)
    nuevo_puntaje = suma_puntaje(mano)
    print(f"{jugador} solicito carta.")
    print(f"{jugador} recibio: {carta} (valor: {valor_carta(carta, acumulado, mano)})")
    print(f"{jugador} tiene:", mano)
    print(f"El total de la mano de {jugador}: {nuevo_puntaje}\n")
    actualizar_bitacora(bitacora, f"{jugador} solicito una carta, es un {carta} y representa un valor {valor_carta(carta, acumulado, mano)}")
    if nuevo_puntaje >= 21:
        print(f"{jugador} ha alcanzado 21 o más puntos. Su turno ha terminado.")
        actualizar_bitacora(bitacora, f"{jugador} ha alcanzado 21 o más puntos. Su turno ha terminado.")
    return nuevo_puntaje

def imprimir_mano(jugador, mano):
    if jugador == "Jugador 2":
        mano_oculta = ["*"] * len(mano)
        print(f"{jugador} tiene:", mano_oculta)
    else:
        print(f"{jugador} tiene:", mano)

def turno_jugador(jugador, mano, puntaje, bitacora):
    while True:
        respuesta = input(f"{jugador}, ¿Desea solicitar otra carta? (s/n): ").lower()
        actualizar_bitacora(bitacora, f"{jugador} tomo la decision de {'solicitar otra carta' if respuesta == 's' else 'no solicitar otra carta'}")
        if respuesta == "n":
            break
        elif respuesta == "s":
            puntaje = pedir_carta(jugador, mano, puntaje, bitacora)
            if puntaje >= 21:
                print(f"{jugador} se ha pasado de 21 puntos. Su turno ha terminado.")
                actualizar_bitacora(bitacora, f"{jugador} se ha pasado de 21 puntos. Su turno ha terminado.")
                break
        else:
            print("Respuesta inválida. Por favor, ingrese 's' para sí o 'n' para no.")
    return puntaje

def calcular_puntos(puntos):
    if puntos == 21:
        return 6
    elif puntos < 21 and puntos >= 17:
        return 2
    elif puntos < 17:
        return 1
    else:
        return 0

def imprimir_resultados(jugador, mano, puntaje, puntos, acumulado, resultado):
    print(f"Resultados {jugador}:")
    imprimir_mano(jugador, mano)
    print(f"Puntos {jugador}: {puntaje}")
    print(f"Puntos: {puntos}")
    print(f"Total acumulado de {jugador}: {acumulado}")
    print(f"Resultado: {resultado}\n")

def main():
    global jugador1_puntos_acumulados, jugador2_puntos_acumulados
    while True:
        print("Bienvenido al juego de Blackjack.")
        print("Seleccione una opción:")
        print("1. Jugar")
        print("2. Ver baraja restante")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            jugador1_puntos_acumulados = 0
            jugador2_puntos_acumulados = 0
            mano_1 = generador_cartas()
            if mano_1 is None:
                print("¡El juego se ha terminado! No quedan cartas disponibles.")
                break
            mano_2 = generador_cartas()
            if mano_2 is None:
                print("¡El juego se ha terminado! No quedan cartas disponibles.")
                break
            jugador1_puntos = suma_puntaje(mano_1)
            jugador2_puntos = suma_puntaje(mano_2)
            imprimir_mano("Jugador 1", mano_1)
            imprimir_mano("Jugador 2", mano_2)
            bitacora = crear_bitacora()
            actualizar_bitacora(bitacora, f"USUARIO solicito cartas. Tiene: {mano_1}")
            actualizar_bitacora(bitacora, f"IA solicito cartas. Tiene: {mano_2}")
            turno_jugador1 = True
            primera_vez_jugador2 = True
            while True:
                if turno_jugador1:
                    jugador1_puntos = turno_jugador("Jugador 1", mano_1, jugador1_puntos, bitacora)
                    jugador1_puntos_acumulados += jugador1_puntos
                    if jugador1_puntos >= 21:
                        break
                else:
                    if jugador_virtual(jugador2_puntos, jugador1_puntos, primera_vez_jugador2):
                        jugador2_puntos = pedir_carta("Jugador 2", mano_2, jugador2_puntos, bitacora)
                        jugador2_puntos_acumulados += jugador2_puntos
                        if jugador2_puntos >= 21:
                            break
                        else:
                            actualizar_bitacora(bitacora, f"Jugador 2 solicitó una carta. Mano actual: {mano_2}. Puntos: {jugador2_puntos}")
                    else:
                        turno_jugador1 = True
                primera_vez_jugador2 = False
                turno_jugador1 = not turno_jugador1
            puntos_jugador1 = calcular_puntos(jugador1_puntos)
            puntos_jugador2 = calcular_puntos(jugador2_puntos)
            if puntos_jugador1 == puntos_jugador2:
                resultado = "Empate"
                bitacora.write("Resultado: Empate\n")
            else:
                if puntos_jugador1 > puntos_jugador2:
                    resultado = "Jugador 1"
                    bitacora.write("Ganador: Jugador 1\n")
                else:
                    resultado = "Jugador 2"
                    bitacora.write("Ganador: Jugador 2\n")
            imprimir_resultados("Jugador 1", mano_1, jugador1_puntos, puntos_jugador1, jugador1_puntos_acumulados, resultado)
            imprimir_resultados("Jugador 2", mano_2, jugador2_puntos, puntos_jugador2, jugador2_puntos_acumulados, resultado)
            bitacora.write(f"Puntos finales - Jugador 1: {jugador1_puntos_acumulados}\n")
            bitacora.write(f"Puntos finales - Jugador 2: {jugador2_puntos_acumulados}\n")
            actualizar_bitacora(bitacora, f"Estado final de la partida:\nJugador 1 - Mano: {mano_1}, Puntos: {jugador1_puntos_acumulados}\nJugador 2 - Mano: {mano_2}, Puntos: {jugador2_puntos_acumulados}")
            bitacora.close()
        elif opcion == "2":
            contador_cartas = contar_cartas_restantes()
            print("Cartas restantes en la baraja:")
            for carta, cantidad in contador_cartas.items():
                print(f"{carta}: {cantidad} carta(s)")
        elif opcion == "3":
            print("Juego terminado.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida (1, 2 o 3).")

if __name__ == "__main__":
    main()