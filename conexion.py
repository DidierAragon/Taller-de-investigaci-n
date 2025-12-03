# conexion.py
# Archivo para gestionar la conexión a la base de datos PostgreSQL y manejar el registro e inicio de sesión de usuarios.
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Función para establecer la conexión a la base de datos PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="plataforma_nota",
        user="postgres",
        password="123456",
        port="5432"
    )
    return conn

# Función para cerrar la conexión a la base de datos
def close_db_connection(conn):
    conn.close()

@app.route('/')
def index():  # Página principal de la aplicación
    return render_template('register.html')  # Página de registro de usuarios

@app.route('/register', methods=['GET', 'POST'])  # Registro de usuario
def register():
    if request.method == 'POST':
        primernombre = request.form.get('primernombre', '').strip()
        segundonombre = request.form.get('segundonombre', '').strip()
        primerapellido = request.form.get('primerapellido', '').strip()
        segundopellido = request.form.get('segundopellido', '').strip()
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')
        confirma_contraseña = request.form.get('confirma_contraseña', '')
        fecha_nacimiento = request.form.get('fecha_nacimiento') or None
        rol_nombre = request.form.get('rol', '')
        estado = True

        roles = {
            'estudiante': 1,
            'profesor': 2,
            'administrador': 3
        }

        id_rol = roles.get(rol_nombre)

        try:
            if contraseña != confirma_contraseña:
                print("Las contraseñas no coinciden")
                return redirect(url_for('register'))

            if not id_rol:
                print("Rol inválido")
                return redirect(url_for('register'))

            hash_password = generate_password_hash(contraseña)

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO usuarios (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, correo, contrasena, fecha_nacimiento, id_rol, estado) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (primernombre, segundonombre, primerapellido, segundopellido, correo, hash_password, fecha_nacimiento, id_rol, estado)
            )

            conn.commit()
            cur.close()
            close_db_connection(conn)

            print("Usuario registrado exitosamente")
            return redirect(url_for('login'))

        except Exception:
            print("Error al registrar:")
            traceback.print_exc()
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])  # Página de inicio de sesión
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT contrasena, id_rol FROM usuarios WHERE correo = %s", (correo,))
            row = cur.fetchone()
            cur.close()
            close_db_connection(conn)

            if not row:
                print("Usuario no encontrado")
                return redirect(url_for('login'))

            stored = row[0]
            id_rol = row[1]

            if (stored and check_password_hash(stored, contraseña)) or (stored == contraseña):
                if id_rol == 1:
                    return redirect(url_for('estudiante'))
                elif id_rol == 2:
                    return redirect(url_for('profesor'))
                elif id_rol == 3:
                    return redirect(url_for('administrador'))
                else:
                    return redirect(url_for('home'))
            else:
                print("Credenciales incorrectas")
                return redirect(url_for('login'))

        except Exception:
            print("Error en login:")
            traceback.print_exc()
            return redirect(url_for('login'))

    return render_template('login.html')

# 🔹 RUTA AGREGADA: recuperar contraseña
@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/home')  # Página de inicio después del login exitoso
def home():
    return render_template('home.html')

# Rutas por rol
@app.route('/estudiante')
def estudiante():
    return render_template('estudiante.html')

@app.route('/profesor')
def profesor():
    return render_template('profesor.html')

@app.route('/administrador')
def administrador():
    return render_template('administrador.html')

if __name__ == "__main__":
    app.run(debug=True)
