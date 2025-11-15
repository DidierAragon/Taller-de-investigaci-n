from flask import Flask, render_template, request, redirect, url_for
import psycopg2

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
        primernombre = request.form['primernombre']
        segundonombre = request.form['segundonombre']
        primerapellido = request.form['primerapellido']
        segundopellido = request.form['segundopellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        confirma_contraseña = request.form['confirma_contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']
        rol_nombre = request.form['rol']
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
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Insertar en la BD
            cur.execute(
                "INSERT INTO usuarios (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, correo, contrasena, fecha_nacimiento, id_rol, estado, confirma_contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (primernombre, segundonombre, primerapellido, segundopellido, correo, contraseña, fecha_nacimiento, id_rol, estado, confirma_contraseña)
            )
            
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            print("Usuario registrado exitosamente")
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error al registrar: {e}")
            return redirect(url_for('register'))
    
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)

