# Proyecto: Liga de eSports Canarias

## Descripción de la Aplicación
Es una plataforma multiplataforma desarrollada en Kotlin que permite a los jóvenes en Canarias competir profesionalmente en videojuegos. Los jugadores pueden registrarse individualmente o formar equipos para participar en torneos y ascender en el ranking competitivo.  
Además, se organizan torneos anuales en toda Canarias para potenciar la visibilidad de los jugadores y equipos destacados.

## Tecnologías Utilizadas
- **Backend:** Pycharn
- **Frontend** kotlin  
- **Base de Datos:** PostgreSQL (gestionado con PGAdmin)  
- **IDE:** IntelliJ IDEA y Pycharm   
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

#### Relaciones:
- Un usuario puede pertenecer a un equipo (`id_equipo` FK, opcional).
- Un usuario puede inscribirse en torneos (`id_torneo` FK, relación M:N).
- Un usuario puede ser moderador (gestiona equipos y torneos).

### 2. Equipo
- `id_equipo` (PK)
- `nombre`
- `fundador` (FK → `id_usuario`)
- `fecha_creacion`

#### Relaciones:
- Un equipo tiene varios jugadores (relación 1:N con Usuario).
- Un equipo puede participar en torneos (`id_torneo` FK, relación M:N).

### 3. Torneo
- `id_torneo` (PK)
- `nombre`
- `fecha_inicio`
- `fecha_fin`
- `ubicación`

#### Relaciones:
- Un torneo puede tener varios equipos y jugadores inscritos (relación M:N con Usuario y Equipo).

### 4. Juego
- `id_juego` (PK)
- `nombre`
- `descripción`
- `plataforma` (PC, PS5, Xbox, etc.)

#### Relaciones:
- Un torneo está asociado a un juego (`id_juego` FK).

### 5. Clasificación
- `id_clasificacion` (PK)
- `id_torneo` (FK → Torneo)
- `id_equipo` o `id_usuario` (FK, dependiendo del tipo de torneo)
- `puntos`
- `posición`

## Figma
Un figma basico para ver la aplicación
![Canary Esports](https://github.com/user-attachments/assets/ee808ce1-8067-488d-af83-10744775947b)
