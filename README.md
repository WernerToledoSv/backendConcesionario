# AutoMarket - Backend

Backend del sistema **AutoMarket**, una tienda virtual para la venta de vehículos. Desarrollado con Python y FastAPI, utilizando PostgreSQL como sistema de gestión de base de datos.

El backend se encarga de gestionar la información de los vehículos, administradores y solicitudes de compra, mediante una API REST que permitirá la comunicación con el frontend.

## Tecnologías utilizadas

| Tecnología  | Descripción                             |
| ----------- | --------------------------------------- |
| Python 3.12 | Lenguaje de programación.               |
| FastAPI     | Framework para desarrollar la API REST. |
| PostgreSQL  | Sistema de base de datos.               |
| SQLAlchemy  | ORM para interactuar con PostgreSQL.    |
| Pydantic    | Validación y estructura de datos.       |
| Alembic     | Administración de migraciones.          |
|             |                                         |
| Uvicorn     | Servidor ASGI.                          |
| Docker      | Contenerización de la aplicación.       |



## Arquitectura del proyecto

El backend utiliza una arquitectura modular basada en Clean Architecture y los principios SOLID, separando las responsabilidades en diferentes capas.

### Estructura de carpetas

```text
backendConcesionario/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── security.py
│   │
│   ├── domain/
│   │   ├── entities/
│   │   └── repositories/
│   │
│   ├── application/
│   │   ├── dto/
│   │   └── use_cases/
│   │       ├── administradores/
│   │       ├── solicitudes/
│   │       └── vehiculos/
│   │
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── security/
│   │
│   ├── presentation/
│   │   └── api/
│   │       └── v1/
│   │           ├── endpoints/
│   │           ├── schemas/
│   │           ├── dependencies.py
│   │           └── router.py
│   │
│   └── main.py
│
├── migrations/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

### Responsabilidad de las capas

- **Core:** configuración general y manejo de excepciones.
- **Domain:** entidades del negocio y contratos de repositorios.
- **Application:** casos de uso y objetos de transferencia de datos (DTO).
- **Infrastructure:** conexión a PostgreSQL, modelos SQLAlchemy, repositorios y componentes de seguridad.
- **Presentation:** endpoints, esquemas y dependencias de la API.

## Base de datos

El proyecto utiliza PostgreSQL para almacenar la información del sistema.

Las principales entidades contempladas son:

| Tabla              | Descripción                                        |
| ------------------ | -------------------------------------------------- |
| administradores    | Información de los administradores.                |
| vehiculos          | Inventario de vehículos y fotografías.             |
| solicitudes_compra | Solicitudes de compra realizadas por los clientes. |
| detalle_solicitud  | Vehículos asociados a cada solicitud.              |

La conexión se configura mediante la variable de entorno `DATABASE_URL`, permitiendo utilizar una instancia local o un servicio en la nube como Neon.

## Instalación y configuración

### Requisitos

- Python 3.12.
- PostgreSQL local o una instancia en la nube.
- Git.

### 1. Clonar el repositorio

```bash
git clone https://github.com/WernerToledoSv/backendConcesionario.git

cd backendConcesionario
```

### 2. Crear el entorno virtual

**Windows:**

```powershell
python -m venv .venv

.venv\\Scripts\\activate
```

**Linux:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear el archivo `.env` a partir del archivo de ejemplo.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux:**

```bash
cp .env.example .env
```

Configurar la conexión a PostgreSQL en el archivo `.env`:

```env
DATABASE_URL=postgresql+psycopg2://usuario:contraseña@host:5432/base_datos?sslmode=require
```

Reemplazar los valores de ejemplo por las credenciales correspondientes a la base de datos.

`JWT_SECRET_KEY` es obligatorio y debe ser una clave aleatoria de al menos 32 caracteres. Puede
generarse con:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

`JWT_ACCESS_TOKEN_EXPIRE_MINUTES` controla la vida del token (por defecto 15 minutos; máximo 60) y
`JWT_ISSUER` identifica al emisor (por defecto `automarket-api`). En despliegues con varias
instancias, todas deben compartir la misma clave.

### 5. Ejecutar el backend

Desde la raíz del proyecto ejecutar:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

## Documentación de la API

FastAPI genera automáticamente documentación interactiva para consultar y ejecutar los endpoints.

| Recurso              | URL                                                                |
| -------------------- | ------------------------------------------------------------------ |
| Swagger UI           | [http://localhost:8000/docs](http://localhost:8000/docs)           |
| ReDoc                | [http://localhost:8000/redoc](http://localhost:8000/redoc)         |
| Estado de la API     | [http://localhost:8000/health](http://localhost:8000/health)       |
| Estado de PostgreSQL | [http://localhost:8000/health/db](http://localhost:8000/health/db) |

## Endpoints disponibles

La API incluye administración protegida, catálogo público de vehículos y el flujo de solicitudes de compra.

| Método | Endpoint                                               | Función                   |
| ------ | ------------------------------------------------------ | ------------------------- |
| POST   | `/api/v1/administradores/IniciarSesion` | Validar credenciales y emitir token JWT. |
| POST   | `/api/v1/administradores/CrearAdministrador` | Crear administrador (JWT requerido). |
| GET    | `/api/v1/administradores/ListarAdministradores` | Listar administradores (JWT requerido). |
| GET    | `/api/v1/administradores/ObtenerAdministrador/{id}` | Consultar administrador (JWT requerido). |
| PUT    | `/api/v1/administradores/ActualizarAdministrador/{id}` | Actualizar administrador (JWT requerido). |
| DELETE | `/api/v1/administradores/EliminarAdministrador/{id}` | Eliminar administrador (JWT requerido). |
| POST   | `/api/v1/solicitudes/CrearSolicitud` | Crear solicitud pública; precios calculados por el servidor. |
| GET    | `/api/v1/solicitudes/ListarSolicitudes` | Listar solicitudes con detalle (JWT requerido). |
| PATCH  | `/api/v1/solicitudes/ActualizarNotas/{id}` | Actualizar notas administrativas (JWT requerido). |
| PATCH  | `/api/v1/solicitudes/ActualizarEstado/{id}` | Cambiar estado con transiciones validadas (JWT requerido). |
| GET    | `/api/v1/estadisticas/Resumen` | Resumen de inventario y solicitudes (JWT requerido). |
| POST   | `/api/v1/vehiculos/CrearVehiculo` | Crear vehículo (JWT requerido). |
| PUT    | `/api/v1/vehiculos/ActualizarVehiculo/{id}` | Actualizar vehículo (JWT requerido). |
| DELETE | `/api/v1/vehiculos/EliminarVehiculo/{id}` | Eliminar vehículo (JWT requerido). |
| GET    | `/api/v1/catalogosgenerales/Marcas`                     | Marcas registradas sin duplicados. |
| GET    | `/api/v1/catalogosgenerales/Transmisiones`              | Transmisiones registradas sin duplicados. |
| GET    | `/api/v1/catalogosgenerales/Combustibles`               | Combustibles registrados sin duplicados. |
| GET    | `/api/v1/catalogosgenerales/RangoPrecios`               | Precio mínimo y máximo. |
| GET    | `/api/v1/catalogosgenerales/Anios`                      | Años de fabricación sin duplicados. |
| GET    | `/api/v1/catalogosgenerales/Condiciones`                | Condiciones registradas sin duplicados. |
| GET    | `/api/v1/catalogosgenerales/RangoKilometraje`           | Kilometraje mínimo y máximo. |
| GET    | `/api/v1/filtros/Vehiculos`                             | Vehículos filtrados por parámetros opcionales. |

El inicio de sesión recibe `{"correo": "admin@automarket.com", "password": "..."}`. Si las
credenciales son correctas, devuelve el administrador sin la contraseña y un token JWT de acceso
con vigencia corta. En las rutas protegidas se debe enviar
`Authorization: Bearer <access_token>`. Los tokens se firman y validan únicamente con HS256;
la API comprueba su expiración, emisor y que el administrador siga activo. No hay refresh token:
con la vigencia corta y sin almacenamiento de sesiones no se mantiene un mecanismo de revocación.

Las contraseñas nuevas se almacenan con Argon2id y una sal única. Si la base de datos contiene las
contraseñas en texto plano de la versión anterior, ejecutar una vez
`python -m app.scripts.rehash_legacy_admin_passwords` antes de desplegar esta versión. El script
actualiza el contenido de `password_hash` sin cambiar el esquema.

El endpoint público `POST /api/v1/solicitudes/CrearSolicitud` recibe datos del cliente,
`vehiculos_ids` y un mensaje opcional. No acepta precios ni total: ambos se calculan con los precios
actuales de los vehículos en una transacción junto con los detalles. La solicitud debe incluir al
menos un vehículo existente y no puede repetir identificadores.

El cambio de estado permite únicamente estas transiciones:

| Estado actual | Estados permitidos |
| ------------- | ------------------ |
| `pendiente` | `contactado`, `rechazada`, `cancelada` |
| `contactado` | `confirmada`, `rechazada`, `cancelada` |
| `confirmada` | `completada`, `cancelada` |
| `rechazada`, `cancelada`, `completada` | Ninguno (finales) |

Cada cambio de estado o de notas administrativas actualiza `actualizado_en`.

`GET /api/v1/solicitudes/ListarSolicitudes` devuelve cada solicitud con sus datos de cliente y un
arreglo `detalles` con los vehículos asociados (`vehiculo_id`, `marca`, `modelo`, `anio`,
`fotoauto` y `precio_unitario`).

`GET /api/v1/estadisticas/Resumen` devuelve el inventario por estado, las solicitudes por estado,
los totales estimados de las solicitudes y el conteo mensual de solicitudes de los últimos seis
meses calendario. El esquema actual no registra fechas de venta, transacciones, costos ni tipos de
carrocería; por ello no permite calcular ingresos brutos, margen, unidades vendidas en un mes ni mix
por carrocería. `vehiculos_vendidos` representa el inventario actualmente marcado como vendido,
no ventas efectuadas en un período.

El endpoint `GET /api/v1/filtros/Vehiculos` acepta `marca`, `transmision`,
`combustible`, `precioMinimo`, `precioMaximo`, `anio`, `condicion`,
`kilometrajeMinimo` y `kilometrajeMaximo`. Todos son opcionales y se pueden combinar;
los límites mínimo y máximo se aplican de forma independiente.

## Formato de respuestas

Las respuestas de la API utilizan una estructura estándar:

**Respuesta con un objeto:**

```json
{
    "code": 1,
    "message": "Registro obtenido exitosamente.",
    "item": {}
}
```

**Respuesta con varios objetos:**

```json
{
    "code": 1,
    "message": "Registros obtenidos exitosamente.",
    "items": []
}
```

**Respuesta sin objetos:**

```json
{
    "code": 1,
    "message": "Registro actualizado exitosamente."
}
```

El campo `code` representa el resultado de la operación:

- `1`: operación exitosa.
- `0`: operación fallida.

El campo `message` describe el resultado de la operación.

## Preparación de administradores

La creación de administradores por API requiere un JWT. Para el primer administrador, ejecutar
`python -m app.scripts.create_initial_admin` desde la raíz con las variables de entorno y la base de
datos configuradas. El comando solicita la contraseña de forma interactiva y solo funciona si aún
no hay administradores.

## Pruebas

Instalar las dependencias de desarrollo y ejecutar la suite:

```bash
pip install -r requirements-dev.txt
pytest
```

Las pruebas usan SQLite en memoria; no requieren una base PostgreSQL ni credenciales reales.

## Consideraciones

- Mantener las credenciales de conexión en el archivo `.env`.
- No subir archivos con información sensible al repositorio.
- Mantener la separación de responsabilidades entre las capas.
- Documentar los nuevos endpoints conforme se implementen.

## Repositorio

[GitHub - WernerToledoSv/backendConcesionario](https://github.com/WernerToledoSv/backendConcesionario)
