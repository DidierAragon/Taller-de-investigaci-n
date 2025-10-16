from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirige a login por defecto

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aquí podrías validar usuario y contraseña
        return f"Bienvenido {username}!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Aquí podrías guardar los datos del usuario
        return f"Usuario {username} registrado!"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)


