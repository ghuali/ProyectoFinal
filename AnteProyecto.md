# Proyecto: Liga de eSports Canarias

## Descripción de la Aplicación
Es una plataforma multiplataforma desarrollada en Kotlin que permite a los jóvenes en Canarias competir profesionalmente en videojuegos. Los jugadores pueden registrarse individualmente o formar equipos para participar en torneos y ascender en el ranking competitivo.  
Además, se organizan torneos anuales en toda Canarias para potenciar la visibilidad de los jugadores y equipos destacados.

## Tecnologías Utilizadas
- **Backend:** Kotlin  
- **Base de Datos:** PostgreSQL (gestionado con PGAdmin)  
- **IDE:** IntelliJ IDEA  
- **Servicios y API:** Desarrollados en PyCharm  

## Roles de Usuario

### 1. Usuario No Registrado
- Puede ver las tablas de clasificación de equipos y jugadores.
- Puede explorar información sobre torneos y eventos.

### 2. Usuario Registrado (Jugador)
- Puede inscribirse en la liga.
- Puede unirse a equipos o crear uno propio.
- Puede inscribirse en torneos y competiciones.
- Puede consultar su progreso en la clasificación.

### 3. Moderador
- Acceso a un CRUD completo de:
  - Equipos
  - Jugadores
  - Juegos
  - Eventos y torneos anuales
- Puede aprobar o eliminar equipos/jugadores que no cumplan las reglas.
- Puede gestionar las inscripciones en torneos.

## Requisitos Funcionales

### Autenticación de Usuarios
- Login y opción de continuar sin cuenta (modo espectador).
- Registro de nuevos usuarios con validación.

### Gestión de Equipos y Jugadores
- Creación de equipos por parte de los usuarios registrados.
- Posibilidad de unirse a un equipo existente.
- Visualización del perfil de jugadores y equipos.

### Participación en Torneos
- Inscripción a torneos individuales o en equipo.
- Sistema de clasificación basado en resultados.

### Panel de Moderación
- CRUD de equipos, jugadores, juegos y torneos.
- Sistema de aprobación y eliminación de contenido.

## Entidades y Relaciones

### 1. Usuario
- `id_usuario` (PK)
- `nombre`
- `email`
- `contraseña`
- `rol` (Jugador / Moderador)
