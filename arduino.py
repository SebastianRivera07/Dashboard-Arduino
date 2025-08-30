
import serial
import mysql.connector
import time

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="medicionesjsrm"
    )

# Conexión a la base de datos y puerto serie
try:
    conexion = conectar_db()
    cursor = conexion.cursor()
    ser = serial.Serial("COM8",9600) # Tener en cuenta el puerto
    time.sleep(2) # Espera a que Arduino inicie
except Exception as e:
    print(f"Error al conectar: {e}")
    exit()

def insertar_datos(Temperatura, Humedad_Rela, Potenciometro1, Potenciometro2, Ldr):
    try:
        query = """
        insert into tblsensores (Temperatura, Humedad_Rela, Potenciometro1, Potenciometro2, Ldr, Fecha_Actual)
        Values (%s, %s, %s, %s, %s, Now())
        """
        valores = (Temperatura, Humedad_Rela, Potenciometro1, Potenciometro2, Ldr)
        cursor.execute(query, valores)
        conexion.commit()
        print("Insertado en BD", valores)
    except mysql.connector.Error as err:
        print(f"Error al insertar en la base de datos: {err}")

# Bucle de lectura desde el puerto serie
try:
    while True:
        try:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            print("Transmisión de datos:", repr(linea)) # Muestra texto completo

            datos = linea.split(',')
            print("Mediciones:", datos)

            if len(datos) != 5:
                print(f"Formato incorrecto (esperados 5, recibidos {len(datos)}):", datos)
                continue 

            try:
                Temperatura, Humedad_Rela, Potenciometro1, Potenciometro2, Ldr = map(float, datos)
            except ValueError as e: 
                print("Error al convertir a float:", e, "Datos:", datos)
                continue
            insertar_datos(Temperatura, Humedad_Rela, Potenciometro1, Potenciometro2, Ldr)
        except serial.SerialException as e:
            print(f"Error de lectura del puerto serie: {e}")
            break

except KeyboardInterrupt: 
    print("Interrupción del usuario. Cerrando conexiones...")
finally:
    ser.close()
    cursor.close()
    conexion.close()
    print("Conexiones cerradas.")