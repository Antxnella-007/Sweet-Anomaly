# Importamos librerías
from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = r"c:\Users\evaan\OneDrive\Desktop\pasteleria\data\pasteleria.db"

app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    with get_conn() as conn:
       
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT NOT NULL,
                nombre TEXT NOT NULL,
                contrasena TEXT NOT NULL,
                email TEXT NOT NULL,
                primerApellido TEXT NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

# Las rutas 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/postres")
def postres():
    return render_template("postres.html")

@app.route("/acercadenosotros")
def acercadenosotros():
    return render_template("acercadenosotros.html")


@app.route("/contactos", methods=["GET", "POST"])
def contactos():
    if request.method == "POST":
        
        cedula         = request.form.get("cedula", "").strip()
        nombre         = request.form.get("nombre", "").strip()
        contrasena     = request.form.get("contrasena", "").strip()
        email          = request.form.get("correo", "").strip()
        primerApellido = request.form.get("apellido", "").strip()

        
        if all([cedula, nombre, contrasena, email, primerApellido]):
            try:
                with get_conn() as conn:
                    conn.execute(
                        "INSERT INTO clientes (cedula, nombre, contrasena, email, primerApellido) VALUES (?, ?, ?, ?, ?)",
                        (cedula, nombre, contrasena, email, primerApellido),
                    )
            except Exception as e:
                
                print("ERROR insertando en clientes:", e)

       
        return redirect(url_for("contactos"))

  
    filas = []
    try:
        with get_conn() as conn:
            filas = conn.execute(
        "SELECT rowid AS id, cedula, nombre, contrasena, email, primerApellido "
        "FROM clientes ORDER BY rowid DESC"
    ).fetchall()

    except Exception as e:
        print("ERROR leyendo clientes:", e)
        filas = []

    return render_template("contactos.html", info=filas)

    return render_template("contactos.html", info=filas)


@app.route("/clientes")
def clientes():
    """Muestra solo la lista de clientes registrados"""
    try:
        with get_conn() as conn:
            datos = conn.execute(
        "SELECT rowid AS id, cedula, nombre, primerApellido, email, contrasena "
        "FROM clientes ORDER BY rowid DESC"
    ).fetchall()

    except Exception as e:
        print("ERROR leyendo clientes:", e)
        datos = []
    return render_template("clientes.html", datos=datos)


if __name__ == "__main__":
    init_db()
   
    app.run(host="0.0.0.0", port=5000, debug=True)

