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

# Función que verifica superposición de vacaciones en mismo sector
def puede_tomar_vacaciones(id_emp, f_inicio, f_fin):
   
    # Se determina sector del empleado solicitante
    sector_solicitante = str(id_emp)[0]
    # Se inicializa contador para superposición
    contador = 0
   
    with open(archivo2, "r", encoding="utf-8") as ar:
        lector_dict = csv.DictReader(ar)
        for fila in lector_dict:
            id = fila["id_empleado"]
            sector_existente = id[0]
            if sector_existente == sector_solicitante:
                # Si son del mismo sector se verifican las fechas
                
                inicio_existente = validar_fecha(fila["fecha_inicio"])
                fin_existente = validar_fecha(fila["fecha_fin"])
                
                if (f_inicio <= fin_existente and f_fin >= inicio_existente):
                    contador += 1
                
                # Si ya hay dos personas, no se puede
                if contador == 2:
                    return False
    
    # Si se sale del bucle con menos de 2 coincidencias
    return True

def actualizar_calendario(diccionario, f_inicio, f_fin):
    columnas = ["id_empleado","nombre_empleado","fecha_inicio","fecha_fin"]
    datos = {}
    datos["id_empleado"] = diccionario["id_empleado"]
    datos["nombre_empleado"] = diccionario["nombre_empleado"]
    datos["fecha_inicio"] = f_inicio.strftime("%d/%m/%Y")
    datos["fecha_fin"] = f_fin.strftime("%d/%m/%Y")
    with open(archivo2, "a", encoding="utf-8",  newline="") as ar:
        #Creamos el escritor indicando los nombres de columnas
        escritor_dict = csv.DictWriter(ar, fieldnames=columnas)
        #Escribimos los datos
        escritor_dict.writerow(datos)

def actualizar_datos_empleado(datos_empleado, dias_descontar):
    try:
        #Definimos el orden como claves del diccionario
        columnas = ["id_empleado", "nombre_empleado", "saldo_dias"]
        #Definimos una lista auxiliar de diccionarios
        lista =[]
        with open(archivo1, "r", encoding="utf-8",  newline="") as ar:
            lector_dict = csv.DictReader(ar)
            for diccionario in lector_dict:
                if datos_empleado["id_empleado"] == diccionario['id_empleado']:
                    diccionario['saldo_dias'] = int(diccionario['saldo_dias']) - dias_descontar
                #Agregamos todos los diccionarios como estaban + el corregido
                lista.append(diccionario)
        with open(archivo1, "w", encoding="utf-8",  newline="") as ar:
            #Creamos el escritor indicando los nombres de columnas
            escritor_dict = csv.DictWriter(ar, fieldnames=columnas)
            #Escribimos el encabezado
            escritor_dict.writeheader()
            #Actualizamos el archivo
            escritor_dict.writerows(lista)
    except FileNotFoundError:
        print(f"Error: el archivo '{archivo1}' no existe.")
        return None
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

            bot.estado = Finalizado()
            bot.estado.procesar(bot, None)
        
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
            bot.info_empleado = info_empleado
            bot.estado = Validando_saldo()
            bot.estado.procesar(bot, None)

        else:

            print("Bot: No entendí lo que escribiste!")
            print("Bot: Si querés iniciar una conversación, ingresá 'hola' o 'vacaciones'.")
            print("Bot: Escribí 'fin' cuando quieras terminar la conversación.")

class Validando_saldo:

    def procesar(self, bot, mensaje):

        intervalo = (bot.fecha_fin - bot.fecha_inicio).days
        
        # Validar que tenga saldo suficiente
        if intervalo > int(bot.info_empleado["saldo_dias"]):
            print(f"Bot: Sólo tienes {bot.info_empleado['saldo_dias']}")
            print("Bot: No se puede realizar la solicitud")
            respuesta = input("Bot: Queres solicitar solo los dias disponibles? (si/no): ").strip().lower()
            if respuesta == "si":
                intervalo = int(bot.info_empleado["saldo_dias"])

                bot.fecha_fin = bot.fecha_inicio + timedelta(days=intervalo - 1)
                print(f"Bot: Ajustamos a {intervalo} dias")
                print(f"Bot: Hasta el {bot.fecha_fin.strftime('%d/%m/%Y')}")
            
            else:
                print("Bot: Tramite cancelado por falta de saldo.\n")
                bot.estado = Finalizado()
                bot.estado.procesar(bot, None)
                return

        # Validar que no haya superposición de empleados del mismo sector
        id = bot.info_empleado["id_empleado"]
        if puede_tomar_vacaciones(id, bot.fecha_inicio, bot.fecha_fin):
            bot.estado = Esperando_aprobacion()
            bot.estado.procesar(bot, None)
        else:
            print("Bot: No es posible solicitar vacaciones para la fecha solicitada")
            print("Bot: Ya hay dos empleados con los que se superponen fechas.")
            bot.estado = Finalizado()
            bot.estado.procesar(bot, None)
            return

class Esperando_aprobacion:
    
    def procesar(self, bot, mensaje):
        print("Bot: Esperando aprobación del supervisor...")
        input("")
        actualizar_calendario(bot.info_empleado, bot.fecha_inicio, bot.fecha_fin)
        dias_pedidos = (bot.fecha_fin - bot.fecha_inicio).days + 1
        actualizar_datos_empleado(bot.info_empleado, dias_pedidos)
        print("Bot: Solicitud APROBADA!")
        bot.estado = Finalizado()
        bot.estado.procesar(bot, None)

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
from datetime import datetime, timedelta

archivo1 = "datos_empleados"
archivo2 = "datos_calendario.csv"

bot = Bot()

while bot.ejecutando:
    texto = input("Usuario: ").strip().lower()
    bot.recibir_mensaje(texto)
