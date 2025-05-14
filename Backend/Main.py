from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Conexión a PostgreSQL
def conectar():
    return psycopg2.connect(
        host="localhost",
        database="alexsoft",
        user="postgres",
        password="1234"
    )

# Ejecutar SQL y devolver JSON
def ejecutar_sql(sql):
    try:
        conn = conectar()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)

        if sql.strip().lower().startswith("select"):
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify(rows)
        else:
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"msg": "Operación exitosa"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login
@app.route('/usuario/login', methods=['POST'])
def login_usuario():
    data = request.json
    email = data['email']
    contrasena = data['contraseña']
    sql = f'''SELECT * FROM "Usuario" WHERE email = '{email}' AND contraseña = '{contrasena}' '''
    result = ejecutar_sql(sql)
    if result.status_code != 200 or not result.json:
        return jsonify({"msg": "Credenciales inválidas"}), 401
    usuario = result.json[0]
    return jsonify({
        "id": usuario["id_usuario"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"],
        "email": usuario["email"]
    })

# Registro
@app.route('/usuario/registro', methods=['POST'])
def registro_usuario():
    data = request.json
    nombre = data['nombre']
    email = data['email']
    contraseña = data['contraseña']
    rol = data['rol']
    sql = f'''
        INSERT INTO "Usuario" (nombre, email, contraseña, rol)
        VALUES ('{nombre}', '{email}', '{contraseña}', '{rol}')
    '''
    return ejecutar_sql(sql)

# Juegos por equipos
@app.route('/juegos/equipos', methods=['GET'])
def juegos_por_equipos():
    return ejecutar_sql('''SELECT * FROM "Juego" WHERE es_individual = FALSE''')

# Torneos activos
@app.route('/torneos/activos', methods=['GET'])
def torneos_activos():
    return ejecutar_sql('''
        SELECT t.id_torneo, t.nombre AS torneo, t.fecha_inicio, t.fecha_fin,
               j.nombre AS juego, e.nombre AS evento, e.tipo, e.año
        FROM "Torneo" t
        INNER JOIN "Juego" j ON t.id_juego = j.id_juego
        INNER JOIN "Evento" e ON t.id_evento = e.id_evento
        WHERE t.fecha_fin >= CURRENT_DATE
        ORDER BY t.fecha_inicio ASC
    ''')

# Clasificación de torneo
@app.route('/torneo/clasificacion', methods=['GET'])
def clasificacion_torneo():
    torneo_id = request.args.get('id')
    return ejecutar_sql(f'''
        SELECT c.id_clasificacion, c.puntos, c.posicion,
               u.nombre AS usuario, eq.nombre AS equipo
        FROM "Clasificacion" c
        LEFT JOIN "Usuario" u ON c.id_usuario = u.id_usuario
        LEFT JOIN "Equipo" eq ON c.id_equipo = eq.id_equipo
        WHERE c.id_torneo = {torneo_id}
        ORDER BY c.posicion ASC
    ''')

# Crear equipo
@app.route('/equipo/crear', methods=['POST'])
def crear_equipo():
    data = request.json
    nombre = data['nombre']
    fundador = data['fundador']  # ID del usuario
    fecha = data['fecha_creacion']
    return ejecutar_sql(f'''
        INSERT INTO "Equipo" (nombre, fundador, fecha_creacion)
        VALUES ('{nombre}', {fundador}, '{fecha}')
    ''')

# Añadir usuario a equipo
@app.route('/equipo/unir', methods=['POST'])
def unir_equipo():
    data = request.json
    usuario_id = data['usuario_id']
    equipo_id = data['equipo_id']
    return ejecutar_sql(f'''
        INSERT INTO "UsuarioEquipo" (usuario_id, equipo_id)
        VALUES ({usuario_id}, {equipo_id})
    ''')

# Crear torneo
@app.route('/torneo/crear', methods=['POST'])
def crear_torneo():
    d = request.json
    return ejecutar_sql(f'''
        INSERT INTO "Torneo" (nombre, fecha_inicio, fecha_fin, ubicacion, id_juego, id_evento)
        VALUES ('{d['nombre']}', '{d['fecha_inicio']}', '{d['fecha_fin']}', '{d['ubicacion']}', {d['id_juego']}, {d['id_evento']})
    ''')

# Participar en torneo
@app.route('/torneo/unir', methods=['POST'])
def unir_torneo():
    d = request.json
    if d['tipo'] == 'equipo':
        return ejecutar_sql(f'''
            INSERT INTO "EquipoTorneo" (equipo_id, torneo_id)
            VALUES ({d['id']}, {d['torneo_id']})
        ''')
    else:
        return ejecutar_sql(f'''
            INSERT INTO "UsuarioTorneo" (usuario_id, torneo_id)
            VALUES ({d['id']}, {d['torneo_id']})
        ''')

# Añadir clasificación
@app.route('/torneo/clasificacion', methods=['POST'])
def crear_clasificacion():
    d = request.json
    campos = "id_torneo, puntos, posicion"
    valores = f"{d['id_torneo']}, {d['puntos']}, {d['posicion']}"
    if d['tipo'] == 'equipo':
        campos += ", id_equipo"
        valores += f", {d['id']}"
    else:
        campos += ", id_usuario"
        valores += f", {d['id']}"
    return ejecutar_sql(f'''
        INSERT INTO "Clasificacion" ({campos})
        VALUES ({valores})
    ''')

if __name__ == '__main__':
    app.run(debug=True)