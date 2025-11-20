from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="plataforma_nota",
        user="postgres",
        password="123456",
        port="5432"
    )
    return conn

def close_db_connection(conn):
    conn.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        primernombre = request.form.get('primernombre', '').strip()
        segundonombre = request.form.get('segundonombre', '').strip()
        primerapellido = request.form.get('primerapellido', '').strip()
        segundopellido = request.form.get('segundopellido', '').strip()
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')
        confirma_contraseña = request.form.get('confirma_contraseña', '')
        fecha_nacimiento = request.form.get('fecha_nacimiento') or None
        rol_nombre = request.form.get('rol', '')
        estado = True  # Por defecto activo

        # Mapear nombres de rol a IDs
        roles = {
            'estudiante': 1,
            'profesor': 2,
            'administrador': 3
        }

        id_rol = roles.get(rol_nombre)

        try:
            # Validar que las contraseñas coincidan
            if contraseña != confirma_contraseña:
                print("Las contraseñas no coinciden")
                return redirect(url_for('register'))

            if not id_rol:
                print("Rol inválido")
                return redirect(url_for('register'))

            # Hashear la contraseña antes de guardar
            hash_password = generate_password_hash(contraseña)

            conn = get_db_connection()
            cur = conn.cursor()

            # Insertar en la BD (sin columna de confirmación)
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT contrasena FROM usuarios WHERE correo = %s", (correo,))
            row = cur.fetchone()
            cur.close()
            close_db_connection(conn)

            if not row:
                print("Usuario no encontrado")
                return redirect(url_for('login'))

            stored = row[0]

            # Intentar verificación con hash; si no coincide, comprobar texto plano (fallback)
            if (stored and check_password_hash(stored, contraseña)) or (stored == contraseña):
                return redirect(url_for('home'))
            else:
                print("Credenciales incorrectas")
                return redirect(url_for('login'))
        except Exception:
            print("Error en login:")
            traceback.print_exc()
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
