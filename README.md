# Trabajo Práctico Integrador: Gestor de pedido de vacaciones de la empresa 'ElectroFast'
## Alumnos: Juan Manuel Reyes Lima y Carolina Rodríguez
Trabajo Práctico Integrador de la materia Organización Empresarial, Universidad Tecnológica Nacional

### Descripción

Este proyecto implementa un chatbot para la gestión automática de solicitudes de vacaciones de empleados. El sistema valida la identidad del empleado, verifica la disponibilidad de días de vacaciones, controla posibles superposiciones dentro del sector y registra las solicitudes aprobadas.

### Requisitos

* Python 3.10 o superior
* Módulos estándar de Python:
    * csv
    * datetime

### Instalación

Clonar el repositorio:

git clone https://github.com/rodricar186/TP_Integrador_OE.git

cd TP_Integrador_OE

### Ejecución

Ejecutar el programa principal:
python main.py

### Archivo de Datos

El sistema utiliza archivos CSV para simular las bases de datos de la empresa. Estos archivos deben encontrarse en el mismo directorio que el programa.

* datos_empleados.csv: información de empleados y saldo de vacaciones
* datos_calendario.csv: registro de solicitudes aprobadas

### Manual de Uso
#### Inicio del trámite

Luego de una interacción del usuario, el bot saluda y presenta las opciones disponibles. El usuario debe ingresar la palabra: "Vacaciones" u "Hola".

#### Identificación del empleado

El bot solicita el ID de empleado y lo valida en la base de datos.

Una vez validado:

* Recupera el nombre del empleado
* Muestra el saldo de días disponibles
* Solicita fecha de inicio y fecha de fin

Las fechas deben ingresarse con el formato: DD/MM/AAAA

El sistema valida:

* Formato correcto
* Coherencia cronológica

#### Validación de la solicitud

El bot verifica:

* Que el empleado posea días suficientes
* Que no existan superposiciones con más de dos empleados del mismo sector

Si el empleado solicita más días de los disponibles, puede optar por:

* Cancelar la solicitud
* Solicitar únicamente los días disponibles

Si la solicitud es cancelada o rechazada por superposición, el proceso finaliza.

#### Aprobación

La solicitud se envía al responsable de RRHH.

Si la solicitud es aprobada:

* Se actualiza el saldo de vacaciones del empleado
* Se actualiza el calendario de vacaciones

#### Finalización

Tanto para solicitudes aprobadas como rechazadas, el bot informa el resultado, se despide y finaliza la conversación.

### Ejemplo de uso
```text
C:\Users\sasha\OneDrive\Escritorio\GitHub\TP_Integrador_OE>C:\Users\sasha\AppData\Local\Programs\Python\Python314\python.exe c:/Users/sasha/OneDrive/Escritorio/GitHub/TP_Integrador_OE/main.py
Usuario: 
Bot: Bienvenido al gestor de vacaciones de la empresa.
Bot: Si querés iniciar una conversación, ingresá 'hola' o 'vacaciones'.
Bot: Escribí 'fin' cuando quieras terminar la conversación.
Usuario: hola
Bot: Decime tu número de identificación de empleado: 101
Bot: Hola Carolina Rodríguez!
Bot: Te quedan 27 días de vacaciones disponibles.
Bot: Carolina Rodríguez, ingresá la fecha de inicio para tus vacaciones: 13/08/2026
Bot: Carolina Rodríguez, ingresá la fecha de fin para tus vacaciones: 26/08/2026
Bot: Esperando aprobación del supervisor...

Bot: Solicitud APROBADA!
Bot: Adiós!
```