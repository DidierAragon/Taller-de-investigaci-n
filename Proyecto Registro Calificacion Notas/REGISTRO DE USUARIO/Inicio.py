usuarios = {}  # Diccionario para almacenar los datos de los usuarios temporalmente

def registrar_usuarios():
    print("-- REGISTRO DE USUARIOS --")
    
    # Solicita los datos del usuario
    username = input("Ingrese su nombre de usuario: ")
    
    tarjeta_identidad = input("Ingrese su Tarjeta de identidad: ")
    
    password = input("Ingrese su contraseña: ")
    
    email = input("Ingrese su correo electrónico: ")
    
    # Verifica si el usuario ya existe
    if tarjeta_identidad in usuarios:
        print("El usuario ya existe")
        return
    
    # Apartado de roles       
    print("\nSeleccione su rol")
    
    print("1. Usuario  (Estudiante)")
    
    print("2. Profesor")  
    
    option = input("Ingrese una opción (1-2): ")
    
    if option == '1':
        rol = 'Estudiante'
        
    elif option == '2':
        rol = 'Profesor'
        
    else:
        print("Opción inválida. Se asignará el rol de 'Estudiante' por defecto.")
        rol = "Estudiante"
        
    # Guarda los datos del usuario en el diccionario
    usuarios[tarjeta_identidad] = {
        'username': username,
        'password': password,
        'email': email,
        'rol': rol
    }
    
    usuarios.append(usuarios)
    print(f"usuario {username} registrado exitosamente con el rol de {rol}")
    
def iniciar_sesion():
    print("\n-- INICIO DE SESIÓN --")
    
    username = input("Ingrese su nombre de usuario: ")
    
    passsword = input("Ingrese su contraseña: ")
    
    # buscar usuario
    for usuario in usuarios: # Itera sobre las claves del diccionario
        
        if usuario['username'] == username and usuario['password'] == passsword:
            print(f"Bienvenido {usuario['username']}! Has iniciado sesión exitosamente.")
            return usuario
        
    print("Nombre de usuario o contraseña incorrectos.")
    return None

def menu_principal():
    
    
        
    
        
        
    
    
        




