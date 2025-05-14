from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def ejecutar_sql(sql_text, params=None, fetch=True):
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="EsportsCanarias",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(sql_text, params)

    if not fetch:
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"msg": "Operación exitosa"})

    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(filas)

# -----------------------
# AUTENTICACIÓN
# -----------------------

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

# -----------------------
# USUARIOS
# -----------------------

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return ejecutar_sql('SELECT * FROM "Usuario" ORDER BY id_usuario ASC')

@app.route('/usuario', methods=['POST'])
def nuevo_usuario():
    data = request.json
    return ejecutar_sql("""
        INSERT INTO "Usuario" (nombre, email, contraseña, rol)
        VALUES (%s, %s, %s, %s)
    """, (data['nombre'], data['email'], data['contraseña'], data['rol']), fetch=False)

# -----------------------
# EQUIPOS
# -----------------------

@app.route('/equipos', methods=['GET'])
def obtener_equipos():
    return ejecutar_sql('SELECT * FROM "Equipo" ORDER BY id_equipo ASC')

@app.route('/equipo', methods=['POST'])
def nuevo_equipo():
    data = request.json
    return ejecutar_sql("""
        INSERT INTO "Equipo" (nombre, fundador, fecha_creacion)
        VALUES (%s, %s, %s)
    """, (data['nombre'], data['fundador'], data['fecha_creacion']), fetch=False)

# -----------------------
# TORNEOS
# -----------------------

@app.route('/torneos', methods=['GET'])
def obtener_torneos():
    return ejecutar_sql("""
        SELECT t.*, j.nombre AS nombre_juego, e.nombre AS nombre_evento
        FROM "Torneo" t
        JOIN "Juego" j ON t.id_juego = j.id_juego
        JOIN "Evento" e ON t.id_evento = e.id_evento
        ORDER BY t.id_torneo ASC
    """)

# -----------------------
# CLASIFICACIÓN
# -----------------------

@app.route('/clasificacion/<int:id_torneo>', methods=['GET'])
def clasificacion_torneo(id_torneo):
    return ejecutar_sql("""
        SELECT c.*, u.nombre AS nombre_usuario, eq.nombre AS nombre_equipo
        FROM "Clasificacion" c
        LEFT JOIN "Usuario" u ON c.id_usuario = u.id_usuario
        LEFT JOIN "Equipo" eq ON c.id_equipo = eq.id_equipo
        WHERE c.id_torneo = %s
        ORDER BY c.posicion ASC
    """, (id_torneo,))

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

# -----------------------
# EVENTOS y JUEGOS
# -----------------------

@app.route('/eventos', methods=['GET'])
def obtener_eventos():
    return ejecutar_sql('SELECT * FROM "Evento" ORDER BY año DESC, tipo ASC')

@app.route('/juegos', methods=['GET'])
def obtener_juegos():
    return ejecutar_sql('SELECT * FROM "Juego" ORDER BY id_juego ASC')

@app.route('/juego', methods=['POST'])
def nuevo_juego():
    data = request.json
    return ejecutar_sql("""
        INSERT INTO "Juego" (nombre, descripcion, plataforma, es_individual)
        VALUES (%s, %s, %s, %s)
    """, (data['nombre'], data['descripcion'], data['plataforma'], data['es_individual']), fetch=False)

# -----------------------
# INICIALIZACIÓN
# -----------------------

if __name__ == '__main__':
    app.run(debug=True)
