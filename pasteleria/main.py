import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ========= Config DB (sirve local y en Render) =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # carpeta /pasteleria
DB_DIR = os.environ.get("DB_DIR", os.path.join(BASE_DIR, "data"))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "pasteleria.db")
print("USANDO DB:", DB_PATH, flush=True)

def get_conn():
    # row_factory para acceder por nombre de columna si quisieras
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            cedula         VARCHAR(9)  PRIMARY KEY,
            nombre         VARCHAR(25),
            primerApellido VARCHAR(25),
            email          VARCHAR,
            contrasena     VARCHAR(8)
        )
        """)
        conn.commit()

# ========= Rutas =========
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
                        "INSERT INTO clientes (cedula, nombre, contrasena, email, primerApellido) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (cedula, nombre, contrasena, email, primerApellido),
                    )
                    conn.commit()
            except Exception as e:
                print("ERROR insertando en clientes:", e, flush=True)

        return redirect(url_for("contactos"))

    # GET: mostrar lista
    filas = []
    try:
        with get_conn() as conn:
            filas = conn.execute(
                "SELECT rowid AS id, cedula, nombre, contrasena, email, primerApellido "
                "FROM clientes ORDER BY rowid DESC"
            ).fetchall()
    except Exception as e:
        print("ERROR leyendo clientes:", e, flush=True)
        filas = []

    return render_template("contactos.html", info=filas)

@app.route("/clientes")
def clientes():
    try:
        with get_conn() as conn:
            datos = conn.execute(
                "SELECT rowid AS id, cedula, nombre, primerApellido, email, contrasena "
                "FROM clientes ORDER BY rowid DESC"
            ).fetchall()
    except Exception as e:
        print("ERROR leyendo clientes:", e, flush=True)
        datos = []
    return render_template("clientes.html", datos=datos)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)


