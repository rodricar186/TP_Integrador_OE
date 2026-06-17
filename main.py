##########################################
############ VALIDACIONES ################
##########################################

#Creamos una función para validar enteros positivos     
def validar_entero_positivo(num):
    while True:
        try:
            #Intentamos convertir el número a entero
            num = int(num)
            #Analizamos que el usuario haya ingresado un número válido
            if num < 0:
                raise Exception("La cantidad ingresada debe ser positiva.")
        except ValueError:
            #Si el valor ingresado no es un dígito
            print("Debe ingresar un número válido.")
            num = input("Intente nuevamente: ").strip()
        except Exception as e:
            #si el número ingresado no cumple con lo requerido por el sistema
            print("Error: ", e)
            num = input("Intente nuevamente: ").strip()
        else:
            return num

#Creamos una función para validar la existencia del id ingresado
def validar_existencia(archivo, texto):
    try:
        with open(archivo, "r", encoding="utf-8") as ar:
            lector_dict = csv.DictReader(ar)
            for diccionario in lector_dict:
                if texto == diccionario['nombre']:
                    return texto
            raise ValueError(f"El país {texto} no está en la lista.")
    except FileNotFoundError:
        print(f"Error: el archivo '{archivo}' no existe.")
        return None
    except ValueError as e:
        print("Error:", e)
        print()
        return None




##########################################
###### Inicialización del chatbot ########
##########################################

class Inicio:

    def procesar(self, bot, mensaje):

        print("Bot: Bienvenido al gestor de vacaciones de la empresa.")
        print("Bot: Si querés iniciar una conversación, ingresá 'hola' o 'vacaciones'.")
        print("Bot: Escribí 'fin' cuando quieras terminar la conversación.")

        bot.estado = Esperando_fechas()

class Esperando_fechas:

    def procesar(self, bot, mensaje):

        if mensaje == "fin":

            print("Bot: Adiós!")
        
        elif mensaje in ["hola","vacaciones"]:

            id = input("Bot: Decime tu número de identificación de empleado: ").strip()
            id = validar_entero_positivo(id)

        else:

            print("Bot: No entendí lo que escribiste!")
            print("Bot: Si querés iniciar una conversación, ingresá 'hola' o 'vacaciones'.")
            print("Bot: Escribí 'fin' cuando quieras terminar la conversación.")

class Bot:

    def __init__(self):

        self.estado = Inicio()

    def recibir_mensaje(self, mensaje):

        self.estado.procesar(self, mensaje)

##########################################
################## MAIN ##################
##########################################
import csv

bot = Bot()

ejecutando = True

while ejecutando:

    texto = input("Usuario: ").strip().lower()

    if texto.strip().lower() == "fin":
        ejecutando = False

    bot.recibir_mensaje(texto)

