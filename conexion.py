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

@app.route('/login', methods=['GET', 'POST'])  # Página de inicio de sesión de usuarios
def login():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contraseña = request.form.get('contraseña', '')

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Obtener contraseña y rol del usuario
            cur.execute("SELECT contrasena, id_rol FROM usuarios WHERE correo = %s", (correo,))
            row = cur.fetchone()
            cur.close()
            close_db_connection(conn)

            if not row:
                print("Usuario no encontrado")
                return redirect(url_for('login'))

            stored = row[0]
            id_rol = row[1]

            # Verificar contraseña (hash) o texto plano como fallback
            if (stored and check_password_hash(stored, contraseña)) or (stored == contraseña):
                # Redirigir según rol
                if id_rol == 1:
                    return redirect(url_for('estudiante'))#Redirige a la página de estudiante si el rol es 1
                elif id_rol == 2:
                    return redirect(url_for('profesor'))#Redirige a la página de profesor si el rol es 2
                elif id_rol == 3:
                    return redirect(url_for('administrador'))#Redirige a la página de administrador si el rol es 3
                else:
                    return redirect(url_for('home'))#Redirige a la página de inicio por defecto
            else:
                print("Credenciales incorrectas")#Mensaje de error por credenciales incorrectas
                return redirect(url_for('login'))#Redirige de nuevo a la página de inicio de sesión
        except Exception:#Manejo de excepciones durante el proceso de inicio de sesión
            print("Error en login:")#Mensaje de error en el inicio de sesión
            traceback.print_exc()#Imprime la traza del error para depuración
            return redirect(url_for('login'))#Redirige de nuevo a la página de inicio de sesión en caso de error

    return render_template('login.html')


@app.route('/home')#Página de inicio después del login exitoso
def home():
    return render_template('home.html')

# Rutas por rol
@app.route('/estudiante')#Página específica para estudiantes
def estudiante():
    return render_template('estudiante.html')#Renderiza la plantilla HTML para la página de estudiantes

@app.route('/profesor')#Página específica para profesores
def profesor():
    return render_template('profesor.html')#Renderiza la plantilla HTML para la página de profesores

@app.route('/administrador')#Página específica para administradores
def administrador():
    return render_template('administrador.html')#Renderiza la plantilla HTML para la página de administradores

if __name__ == "__main__":#Punto de entrada principal de la aplicación
    app.run(debug=True)#Ejecuta la aplicación Flask en modo de depuración.
