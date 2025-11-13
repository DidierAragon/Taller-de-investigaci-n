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
        # Procesar datos del formulario
        return redirect(url_for('index'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)

