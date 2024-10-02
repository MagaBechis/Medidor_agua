from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    "host": "b1f1nbspgfusdyux6aaw-mysql.services.clever-cloud.com",
    "user": "u9pgityls4no2yc8",
    "password": "kxmHZm4i0a5LtbGMwAEd",
    "database": "b1f1nbspgfusdyux6aaw",
}


# Ruta para insertar datos en la tabla
@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()
        mensaje = data.get("mensaje")

        if mensaje is None:
            return (
                jsonify(
                    {"status": "error", "message": "El campo 'mensaje' es requerido"}
                ),
                400,
            )

        # Lógica para insertar en la base de datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO datos (mensaje) VALUES (%s)", (mensaje,))
            conn.commit()
            cursor.close()
            conn.close()
            return (
                jsonify(
                    {"status": "success", "message": "Datos insertados correctamente"}
                ),
                201,
            )
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return (
            jsonify(
                {"status": "error", "message": "La solicitud debe ser en formato JSON"}
            ),
            400,
        )


# Ruta para obtener los datos de la tabla
@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM datos")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "data": rows}), 200
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
