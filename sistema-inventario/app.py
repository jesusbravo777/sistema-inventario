from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-antes-de-publicar"
DB_PATH = Path(__file__).with_name("inventario.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                cantidad INTEGER NOT NULL DEFAULT 0 CHECK(cantidad >= 0),
                precio REAL NOT NULL DEFAULT 0 CHECK(precio >= 0)
            )
        """)

@app.route("/")
def index():
    with db() as conn:
        productos = conn.execute("SELECT * FROM productos ORDER BY nombre").fetchall()
        resumen = conn.execute("SELECT COUNT(*) AS tipos, COALESCE(SUM(cantidad),0) AS unidades FROM productos").fetchone()
    return render_template("index.html", productos=productos, resumen=resumen)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form.get("nombre", "").strip()
    cantidad_txt = request.form.get("cantidad", "0").strip()
    precio_txt = request.form.get("precio", "0").strip()
    try:
        cantidad = int(cantidad_txt)
        precio = float(precio_txt)
        if not nombre or cantidad < 0 or precio < 0:
            raise ValueError
        with db() as conn:
            conn.execute("INSERT INTO productos (nombre,cantidad,precio) VALUES (?,?,?)", (nombre,cantidad,precio))
        flash("Producto agregado.", "success")
    except sqlite3.IntegrityError:
        flash("Ya existe un producto con ese nombre.", "error")
    except ValueError:
        flash("Revisa el nombre, la cantidad y el precio.", "error")
    return redirect(url_for("index"))

@app.route("/actualizar/<int:producto_id>", methods=["POST"])
def actualizar(producto_id):
    try:
        cantidad = int(request.form.get("cantidad", "0"))
        if cantidad < 0:
            raise ValueError
        with db() as conn:
            conn.execute("UPDATE productos SET cantidad=? WHERE id=?", (cantidad, producto_id))
        flash("Stock actualizado.", "success")
    except ValueError:
        flash("La cantidad debe ser un número igual o mayor que cero.", "error")
    return redirect(url_for("index"))

@app.route("/eliminar/<int:producto_id>", methods=["POST"])
def eliminar(producto_id):
    with db() as conn:
        conn.execute("DELETE FROM productos WHERE id=?", (producto_id,))
    flash("Producto eliminado.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
