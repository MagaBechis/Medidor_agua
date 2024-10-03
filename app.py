from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configura la conexión a la base de datos
db_config = {
    "host": "b1f1nbspgfusdyux6aaw-mysql.services.clever-cloud.com",
    "user": "u9pgityls4no2yc8",
    "password": "kxmHZm4i0a5LtbGMwAEd",
    "database": "b1f1nbspgfusdyux6aaw",
}


# Ruta principal
@app.route("/")
def home():
    return "Bienvenido a la aplicación de Medidor de Agua"


# Ruta para insertar datos en la tabla 'datos'
@app.route("/data", methods=["POST"])
def insert_data():
    print(
        "Solicitud recibida en /data"
    )  # Debug: imprimir cuando se recibe la solicitud
    if request.is_json:
        data = request.get_json()
        mensaje = data.get("mensaje")
        print(f"Mensaje recibido: {mensaje}")  # Debug: imprimir el mensaje recibido

        if mensaje is None:
            return (
                jsonify(
                    {"status": "error", "message": "El campo 'mensaje' es obligatorio"}
                ),
                400,
            )

        try:
            # Establecer conexión a la base de datos
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Consulta SQL para insertar el mensaje
            sql_query = "INSERT INTO datos (mensaje) VALUES (%s)"
            cursor.execute(sql_query, (mensaje,))

            # Confirmar los cambios
            connection.commit()

            # Retornar respuesta de éxito
            return (
                jsonify(
                    {"status": "success", "message": "Datos insertados correctamente"}
                ),
                201,
            )

        except mysql.connector.Error as err:
            print(
                f"Error de base de datos: {str(err)}"
            )  # Debug: imprimir errores de base de datos
            return jsonify({"status": "error", "message": str(err)}), 500

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print(
                    "Conexión a la base de datos cerrada."
                )  # Debug: confirmar cierre de conexión
    else:
        print(
            "Se esperaba JSON en la solicitud"
        )  # Debug: imprimir si no se recibe JSON
        return jsonify({"status": "error", "message": "Se esperaba JSON"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
