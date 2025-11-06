import psycopg2


def conectar_bd():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="PlataformaNotas",
            user="PlataformaNotas",
            password="123456"
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
if __name__ == "__main__":
    conectar_bd()
    print("Conexión exitosa.")
