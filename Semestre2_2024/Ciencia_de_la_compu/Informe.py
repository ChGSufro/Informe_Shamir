"""
Manual codigo

El programa se ejecutara simplemente ejecutando el archivo .py con el codigo fuente donde se desplegara el respectivo menu. 
Todo este archivo esta escrito en python por lo solo debe copiar, pegar y ejecutarlo con python.

Generar claves: 
• Selecciona esta opcion para generar claves RSA y fragmentar una clave usando el esquema de comparticion de secretos de Shamir. 
• Se te pedira que introduzcas el numero total de partes y el numero minimo de partes necesarias para reconstruir la clave.

Cifrar mensaje: 
• Elige esta opcion para cifrar un mensaje. • Introduce el mensaje que deseas cifrar. 
• Proporciona la clave publica en forma de tupla (n, e).

Descifrar mensaje: 
• Selecciona esta opcion para descifrar un mensaje previamente cifrado. 
• Proporciona el mensaje cifrado y el valor de n de la clave. 
• Introduce las partes (x, y) necesarias para reconstruir la clave privada.

Salir: 
• Elige esta opcion para salir del programa.

Ejemplo de Uso

Generar Claves: 
• Opcion: 1 
• Introduce el numero de partes: 5 
• Introduce el numero minimo de partes para reconstruir la clave: 3

Cifrar Mensaje: 
• Opcion: 2 
• Introduce el mensaje a cifrar: Hola Mundo 
• Introduce la clave publica como tupla (n, e): (n, e) (reemplaza n y e con los valores generados)

Descifrar Mensaje: 
• Opcion: 3 
• Introduce el mensaje cifrado: [mensaje cifrado] (reemplaza con el mensaje cifrado) 
• Introduce n de la clave: n (reemplaza con el valor de n) 
• Introduce las partes necesarias: (1, y1), (2, y2), ... (donde y1, y2, etc., son los valores y asociados a los x)
"""

from random import randint
import random
import os #Solo es para imprimir el PID del programa


#########################
#   FUNCIONES VARIAS    #
#########################
def modulo(num, div):
    div_entera = num // div
    return num - (div_entera*div)

def numero_es_par(numero):
    return numero % 2 == 0

def euclides(a, b):
    if b == 0:
        return a
    return euclides(b, a % b)

def euclides_extendido(a, b):
    #Devuelve el MCD de a y b, y los coeficientes "x" y "y" tales que ax + by = MCD(a, b).
    if a == 0:
        return b, 0, 1
    mcd, x1, y1 = euclides_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return mcd, x, y

def inverso_modular(a, b):
    mcd, x, _ = euclides_extendido(a, b)
    if mcd != 1:
        raise ValueError("El inverso modular no existe")
    return x % b


def cambio_de_base(numero, base_origen, base_destino):
    decimal = int(numero, base_origen)
    nuevo_numero = ""
    
    while decimal > 0:
        residuo = decimal % base_destino 
        nuevo_numero = str(residuo) + nuevo_numero 
        decimal = decimal // base_destino 
    
    return nuevo_numero

def square_and_multiply(base, exponente, modulo):
    binario = cambio_de_base(str(exponente), 10, 2)
    binario = binario[::-1]

    resultado = 1

    for i in binario:
        if i == "1":
            resultado = (resultado * base) % modulo
        base = base**2 % modulo

    return resultado


#Unicode es un esquema de codificación de caracteres que asigna un número único a cada carácter en la mayoría de los idiomas escritos.
def convertir_a_unicode(mensaje):
    #ord() es una función que toma un carácter y devuelve su valor Unicode
    return [ord(caracter) for caracter in mensaje]


def convertir_a_caracteres(unicode):
    #chr() es una función que toma un valor Unicode y devuelve el carácter correspondiente
    return "".join([chr(caracter) for caracter in unicode])


################################
#    MILLER-RABIN PRIMALIDAD   #
################################
def test_primalidad_Miller_Rabin(numero, repeticiones):
    #Escribimos n-1 como 2^s * d
    s = 0 #s es el exponente de 2
    d = numero - 1 #d es el numero impar
    while d % 2 == 0:
        d //= 2
        s += 1


    for _ in range(repeticiones):

        #Elegimos un numero aleatorio a tal que 2 <= a <= n-2
        a = randint(2, numero-1)

        #Calculamos x = a^d mod n
        x = square_and_multiply(a, d, numero)

        #Si x == 1 o x == n-1, entonces n es probablemente primo
        if x == 1 or x == numero - 1:
            continue

        #Repetimos s-1 veces
        for _ in range(s-1):
            # x = x^2 mod n
            x = square_and_multiply(x, 2, numero)

            #Si x == 1, entonces n no es primo
            if x == 1:
                return False
            
            #Si x == n-1, entonces n es probablemente primo
            if x == numero - 1:
                break
        else:
            return False
        
    return True


def generar_primo(bits, intentos, presicion):
    intento = 0
    while intento < intentos:
        #Generamos un numero aleatorio entre 2^(bits-1) y 2^bits - 1
        numero = randint(2**(bits-1), 2**bits - 1)

        #Si el numero es par, no es primo
        if numero_es_par(numero):
            intento += 1
            continue

        #Si el numero es primo, lo devolvemos
        if test_primalidad_Miller_Rabin(numero, presicion):
            print(f"Numero primo encontrado en {intento + 1} intentos")
            return numero
        
        #Seguro para evitar bucles largos
        intento += 1
    raise Exception(f"No se pudo generar un numero primo en {intentos} intentos")


################################
#   GENERACION DE CLAVES RSA   #
################################
def generar_claves_RSA():
    print("Generando claves RSA")

    #Generamos dos numeros primos aleatorios
    #10 y 11 bits, 1000 intentos de busqueda y
    #10 repeticiones del test de Miller-Rabin
    p = generar_primo(10, 1000, 10)
    q = generar_primo(11, 1000, 10)
    n = p*q

    #Calculamos el totiente de Euler
    totiente = (p-1)*(q-1)

    print("Buscando un copirimo de totiente")
    #Elegimos un numero e tal que 1 < e < totiente - 1, y sea coprimo con totiente
    e = randint(1, totiente-1)

    #Mientras e y totiente no sean coprimos, elegimos otro e
    while euclides(e, totiente) != 1:
        e = randint(1, totiente-1)

    print("Calculando inverso multiplicativo de e mod totiente")

    #Calculamos d, el inverso multiplicativo de e mod totiente
    d = inverso_modular(e, totiente)
    return (n, e), (n, d) #Clave publica y clave privada



################################
#      CIFRADO DE MENSAJE      #
################################
def cifrado_RSA(mensaje, clave_publica):
    print("Comenzando cifrado")
    n, e = clave_publica
    mensaje_cifrado = []

    mensaje_ucode = convertir_a_unicode(mensaje)

    #Ciframos cada bloque del mensaje
    for bloque in mensaje_ucode:
        #Ciframos el bloque elevando a la potencia e y tomando el modulo n
        nbloque = square_and_multiply(bloque, e, n)
        mensaje_cifrado.append(nbloque)

    print("Cifrado completado")
    return mensaje_cifrado



################################
#     DESCIFRADO DE MENSAJE    #
################################
def descifrado_RSA(mensaje_cifrado, clave_privada):
    print("Comenzando descifrado")
    n, d = clave_privada
    mensaje_descifrado = []

    #Desciframos cada bloque del mensaje cifrado
    for bloque in mensaje_cifrado:
        #Desciframos el bloque elevando a la potencia d y tomando el modulo n
        nbloque = square_and_multiply(bloque, d, n)
        mensaje_descifrado.append(nbloque)

    print("Descifrado completado")
    return convertir_a_caracteres(mensaje_descifrado)


################################
#          Shamir              #
################################
# Generar un polinomio aleatorio de grado k-1
def generate_polynomial(secret: int, k: int):
    coefficients = [random.randint(1, 100) for _ in range(k - 1)]
    coefficients.insert(0, secret)  # El secreto es el término independiente (a_0)
    return coefficients

# Evaluar el polinomio en x
def evaluate_polynomial(coefficients, x):
    result = 0
    for i, coeff in enumerate(coefficients):
        result += coeff * (x ** i)
    return result

# Generar las partes (x, y) evaluando el polinomio en x = 1, 2, ..., n
def generate_shares(n, k, secret):
    polynomial = generate_polynomial(secret, k)
    shares = [(i, evaluate_polynomial(polynomial, i)) for i in range(1, n + 1)]
    return shares

# Interpolación de Lagrange para reconstruir el secreto
def lagrange_interpolation(x_values, y_values, x=0):
    total = 0
    for i in range(len(x_values)):
        xi, yi = x_values[i], y_values[i]
        li = 1
        for j in range(len(x_values)):
            if i != j:
                li *= (x - x_values[j]) / (xi - x_values[j])
        total += yi * li
    return int(total)

# Función para reconstruir el secreto a partir de k partes
def reconstruct_secret(shares):
    x_values, y_values = zip(*shares)
    return lagrange_interpolation(x_values, y_values)


################################
#     INTERFAZ INTERACTIVA     #
################################
def fragmentacion(clave, partes, minimas_partes):
    print("Fragmentando clave")
    shares = generate_shares(partes, minimas_partes, clave)
    for i in range(len(shares)):
        print(f"\nGenerando parte {i+1}")
        print(f"Parte {i+1}: {shares[i]}")

def solicitar_partes():
    partes = int(input("Introduce el número de partes: "))
    minimas_partes = int(input("Introduce el número mínimo de partes para reconstruir la clave: "))
    if minimas_partes > partes:
        raise ValueError("El número mínimo de partes no puede ser mayor al número de partes")

    return partes, minimas_partes

def ingresar_partes():
    partes = []
    while True:
        parte = input("Introduce una parte (x, y) o escribe 'q' para salir: ")
        if parte == "q":
            break
        partes.append(eval(parte))
    return partes


def menu():
    print("Bienvenido. \nPID del programa: ", os.getpid(), "\n")

    while True:
        print("\n1. Generar claves")
        print("2. Cifrar mensaje")
        print("3. Descifrar mensaje")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")



        match opcion:
            case "1":
                try:
                    partes, minimas_partes = solicitar_partes()
                    clave_publica, clave_privada = generar_claves_RSA()
                    print(f"\nClave publica: {clave_publica}")
                    print (f"n: {clave_publica[0]}")
                    fragmentacion(clave_privada[1], partes, minimas_partes)
                except ValueError as e:
                    print(f"\nError: {e}\n")


            case "2":
                try:
                    mensaje = input("Introduce el mensaje a cifrar: ")
                    clave = eval(input("Introduce la clave publica como tupla (n, e): "))
                    mensaje_cifrado = cifrado_RSA(mensaje, clave)
                    print(f"\nMensaje cifrado: {mensaje_cifrado}\n")

                except NameError:
                    print("\nError: Clave publica no válida\n")
                except ValueError as e:
                    print(f"\nError: {e}\n")
                except Exception as e:
                    print(f"\nError: {e}\n")

            case "3":
                try:
                    mensaje_cifrado = eval(input("Introduce el mensaje cifrado: "))
                    n = int(input("Introduce n de la clave: "))
                    partes = ingresar_partes()
                    mensaje_descifrado = descifrado_RSA(mensaje_cifrado, (n, reconstruct_secret(partes)))
                    print(f"\nMensaje descifrado: {mensaje_descifrado}\n")

                except NameError:
                    print("\nError: Clave privada no válida\n")
                except ValueError as e:
                    print(f"\nError: {e}\n")
                except Exception as e:
                    print(f"\nError: {e}\n")


            case "4":
                break
            case _:
                print("\nOpción no válida\n")


menu()