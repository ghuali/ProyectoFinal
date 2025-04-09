from flask import Flask, request, jsonify
import psycopg2


app = Flask(__name__)

def ejecutar_sql(sql_text, params=None, fetch=True):
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="EsportsCanarias",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()

    cursor.execute(sql_text, params)

    if not fetch:
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"msg": "Operación exitosa"})

    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    resultado = [dict(zip(columnas, fila)) for fila in filas]

    cursor.close()
    conn.close()
    return jsonify(resultado)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('contraseña')

    resultado = ejecutar_sql("""
        SELECT * FROM "Usuario"
        WHERE email = %s AND contraseña = %s
    """, (email, password))

    if resultado.json:
        return resultado
    else:
        return jsonify({"msg": "Login incorrecto"}), 401


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return ejecutar_sql('SELECT * FROM "Usuario" ORDER BY id_usuario ASC')


@app.route('/equipos', methods=['GET'])
def obtener_equipos():
    return ejecutar_sql('SELECT * FROM "Equipo" ORDER BY id_equipo ASC')


@app.route('/torneos', methods=['GET'])
def obtener_torneos():
    return ejecutar_sql('SELECT * FROM "Torneo" ORDER BY id_torneo ASC')


@app.route('/clasificacion/<int:id_torneo>', methods=['GET'])
def clasificacion_torneo(id_torneo):
    return ejecutar_sql("""
        SELECT * FROM "Clasificacion"
        WHERE id_torneo = %s
        ORDER BY posicion ASC
    """, (id_torneo,))


@app.route('/usuario', methods=['POST'])
def nuevo_usuario():
    data = request.json
    return ejecutar_sql("""
        INSERT INTO "Usuario" (nombre, email, contraseña, rol)
        VALUES (%s, %s, %s, %s)
    """, (data['nombre'], data['email'], data['contraseña'], data['rol']), fetch=False)


@app.route('/equipo', methods=['POST'])
def nuevo_equipo():
    data = request.json
    return ejecutar_sql("""
        INSERT INTO "Equipo" (nombre, fundador, fecha_creacion)
        VALUES (%s, %s, %s)
    """, (data['nombre'], data['fundador'], data['fecha_creacion']), fetch=False)


@app.route('/clasificacion', methods=['POST'])
def nueva_clasificacion():
    data = request.json
    return ejecutar_sql("""
        INSERT INTO "Clasificacion" (id_torneo, id_equipo, id_usuario, puntos, posicion)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['id_torneo'],
        data.get('id_equipo'),
        data.get('id_usuario'),
        data['puntos'],
        data['posicion']
    ), fetch=False)

if __name__ == '__main__':
    app.run(debug=True)
