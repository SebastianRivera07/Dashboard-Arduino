from flask import Flask, render_template, jsonify
import mysql.connector
app = Flask(__name__)

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="medicionesjsrm"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/datos")
def obtener_datos():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("Select * from tblsensores order by Fecha_Actual desc limit 10")
    datos = cursor.fetchall()
    conn.close()
    return jsonify(datos)

@app.route("/api/registro")
def obtener_registro():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("Select * from tblsensores order by Fecha_Actual desc limit 1")
    registro = cursor.fetchall()
    conn.close()
    return jsonify(registro)

@app.route("/api/datos-importantes")
def obtener_temperatura():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("Select Temperatura from tblsensores order by Temperatura desc limit 1")
    Temperatura = cursor.fetchone()["Temperatura"]

    cursor.execute("Select AVG(Humedad_Rela) as Humedad from tblsensores")
    Humedad_Rela = cursor.fetchone()["Humedad"]

    cursor.execute("Select Ldr from tblsensores order by Ldr desc limit 1")
    Ldr = cursor.fetchone()["Ldr"]
    

    conn.close()
    return jsonify(Temperatura, Humedad_Rela, Ldr)

if __name__ == "__main__":
    app.run(debug=True)