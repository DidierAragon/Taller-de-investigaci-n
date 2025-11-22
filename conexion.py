# conexion.py
# Archivo para gestionar la conexión a la base de datos PostgreSQL y manejar el registro e inicio de sesión de usuarios.
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

#Inicialización de la aplicación Flask
app = Flask(__name__)

#Función para establecer la conexión a la base de datos PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="plataforma_nota",
        user="postgres",
        password="123456",
        port="5432"
    )
    return conn
#Función para cerrar la conexión a la base de datos
def close_db_connection(conn):
    conn.close()

@app.route('/')
def index():#Página principal de la aplicación
    return render_template('register.html')#Página de registro de usuarios

@app.route('/register', methods=['GET', 'POST'])#en esta parte se realiza el registro del usuario para que pueda acceder a la plataforma
def register():
    if request.method == 'POST':
        # Obtener datos del formulario de registro
        primernombre = request.form.get('primernombre', '').strip()#Obtiene el primer nombre del formulario y elimina espacios en blanco.
        segundonombre = request.form.get('segundonombre', '').strip()#Obtiene el segundo nombre del formulario y elimina espacios en blanco.
        primerapellido = request.form.get('primerapellido', '').strip()#Obtiene el primer apellido del formulario y elimina espacios en blanco.
        segundopellido = request.form.get('segundopellido', '').strip()#Obtiene el segundo apellido del formulario y elimina espacios en blanco.
        correo = request.form.get('correo', '').strip()#Obtiene el correo electrónico del formulario y elimina espacios en blanco.
        contraseña = request.form.get('contraseña', '')#Obtiene la contraseña del formulario.
        confirma_contraseña = request.form.get('confirma_contraseña', '')#Obtiene la confirmación de la contraseña del formulario.
        fecha_nacimiento = request.form.get('fecha_nacimiento') or None#Obtiene la fecha de nacimiento del formulario.
        rol_nombre = request.form.get('rol', '')#Obtiene el rol del usuario del formulario.
        estado = True  # Por defecto, el usuario está activo

        # Mapeo de roles a sus IDs correspondientes
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

            # Encriptar la contraseña
            hash_password = generate_password_hash(contraseña)

            conn = get_db_connection()
            cur = conn.cursor()

            # Insertar en la informacion a la base de datos en la tabla de usuarios
            cur.execute(
                "INSERT INTO usuarios (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, correo, contrasena, fecha_nacimiento, id_rol, estado) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (primernombre, segundonombre, primerapellido, segundopellido, correo, hash_password, fecha_nacimiento, id_rol, estado)
            )

            conn.commit()
            cur.close()
            close_db_connection(conn)

#Mensaje de éxito y redirección al login
            print("Usuario registrado exitosamente")
            return redirect(url_for('login'))
        except Exception:
            print("Error al registrar:")
            traceback.print_exc()
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])#Página de inicio de sesión de usuarios
#

#en esta parte se realiza el login del usuario para que pueda acceder a la plataforma
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')

        try:
            conn = get_db_connection()
#Establece conexión con la base de datos PostgreSQL.

            cur = conn.cursor()
#Ejecuta una consulta SQL para obtener la contraseña almacenada del usuario con el correo proporcionado.

            cur.execute("SELECT contrasena FROM usuarios WHERE correo = %s", (correo,))
#Obtiene el resultado de la consulta.

            row = cur.fetchone()
#Cierra el cursor y la conexión a la base de datos.
            cur.close()
            close_db_connection(conn)

            if not row:
#Si no se encuentra el usuario, redirige al login con un mensaje de error.
                print("Usuario no encontrado")
                return redirect(url_for('login'))

            stored = row[0]

#valida las credenciales del usuario con la informacion almacenada en la base de datos            
            if (stored and check_password_hash(stored, contraseña)) or (stored == contraseña):
                return redirect(url_for('home'))
            else:
                print("Credenciales incorrectas")
                return redirect(url_for('login'))
        except Exception:
            print("Error en login:")
            traceback.print_exc()#Redirige al login en caso de error.
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/home')#Página de inicio después del login exitoso
def home():
    return render_template('home.html')

if __name__ == "__main__":#Punto de entrada principal de la aplicación
    app.run(debug=True)#Ejecuta la aplicación Flask en modo de depuración.
