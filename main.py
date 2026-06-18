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
def validar_existencia(archivo, num):
    while True:
        try:
            with open(archivo, "r", encoding="utf-8") as ar:
                lector_dict = csv.DictReader(ar)
                #Creamos un diccionario auxiliar
                dict_empelado = {}
                for diccionario in lector_dict:
                    if num == int(diccionario['id_empleado']):
                        #Si encuentra el id, guarda la info del empleado en el diccionario
                        dict_empelado = diccionario
                        return dict_empelado
                raise ValueError(f"El id {num} no está en la lista.")
        except FileNotFoundError:
            print(f"Error: el archivo '{archivo}' no existe.")
            return None
        except ValueError as e:
            print("Error:", e)
            num = input("Bot: Ingrese un id válido: ").strip()
            num = validar_entero_positivo(num)
        else:
            return num
    
#Creamos una función para validar el formato de las fechas ingresadas
def validar_fecha(texto):
    while True:
        try:
            texto = datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            print("Bot: Lo siento, no reconozco ese formato. Por favor, ingresa la fecha como DD/MM/AAAA.")
            texto = input(f"Bot: ingresá una fecha válida: ").strip()
        else:
            return texto

#creamos una función para validar que 
# el inicio no sea anterior a hoy --> regla del diccionario de datos
def validar_inicio_vacaciones(texto):
    while True:
        try:
            if texto.date() < datetime.now().date():
                raise ValueError("La fecha ingresada ya pasó!")
        except ValueError as e:
            print("Error:", e)
            texto = input(f"Bot: Ingresá una fecha válida: ").strip()
            texto = validar_fecha(texto)
        else:
            return texto

#creamos una función para validar que 
# el final no sea anterior al inicio --> regla del diccionario de datos
def validar_final_vacaciones(inicio, final):
    while True:
        try:
            if inicio.date() > final.date():
                raise ValueError("La fecha ingresada es anterior a la inicial!")
        except ValueError as e:
            print("Error:", e)
            final = input(f"Bot: Ingresá una fecha válida: ").strip()
            final = validar_fecha(final)
        else:
            return final




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
            info_empleado = validar_existencia(archivo1, id)
            print(f"Bot: Hola {info_empleado['nombre_empleado']}!")
            print(f"Bot: Te quedan {info_empleado['saldo_dias']} días de vacaciones disponibles.")
            fecha_inicio = input(f"Bot: {info_empleado['nombre_empleado']}, ingresá la fecha de inicio para tus vacaciones: ").strip()
            fecha_inicio = validar_fecha(fecha_inicio)
            fecha_inicio = validar_inicio_vacaciones(fecha_inicio)
            fecha_fin = input(f"Bot: {info_empleado['nombre_empleado']}, ingresá la fecha de fin para tus vacaciones: ").strip()
            fecha_fin = validar_fecha(fecha_fin)
            fecha_fin = validar_final_vacaciones(fecha_inicio, fecha_fin)
            
            bot.fecha_inicio = fecha_inicio
            bot.fecha_fin = fecha_fin
            bot.estado = Validando_saldo()
            bot.estado.procesar(bot, None)

        else:

            print("Bot: No entendí lo que escribiste!")
            print("Bot: Si querés iniciar una conversación, ingresá 'hola' o 'vacaciones'.")
            print("Bot: Escribí 'fin' cuando quieras terminar la conversación.")

class Validando_saldo:

    def procesar(self, bot, mensaje):

        pass
        
        


class Esperando_aprobacion:
    
    def procesar(self, bot, mensaje):
        pass

class Finalizado:
    def procesar(self, bot, mensaje):
        print("Bot: Adiós!")
        bot.ejecutando = False
        return

class Bot:

    def __init__(self):

        self.estado = Inicio()
        self.ejecutando = True

    def recibir_mensaje(self, mensaje):

        self.estado.procesar(self, mensaje)

##########################################
################## MAIN ##################
##########################################
import csv
from datetime import datetime

archivo1 = "temp1.csv"
archivo2 = "temp2.csv"

bot = Bot()

while bot.ejecutando:
        texto = input("Usuario: ").strip().lower()
        bot.recibir_mensaje(texto)