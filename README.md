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

Actualmente se encuentra desarrollada una implementación inicial para la gestión de administradores.

| Método | Endpoint                                               | Función                   |
| ------ | ------------------------------------------------------ | ------------------------- |
| POST   | `/api/v1/administradores/CrearAdministrador`           | Crear administrador.      |
| GET    | `/api/v1/administradores/ListarAdministradores`        | Listar administradores.   |
| GET    | `/api/v1/administradores/ObtenerAdministrador/{id}`    | Consultar administrador.  |
| PUT    | `/api/v1/administradores/ActualizarAdministrador/{id}` | Actualizar administrador. |
| DELETE | `/api/v1/administradores/EliminarAdministrador/{id}`   | Eliminar administrador.   |

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

## Estado del desarrollo

El backend se encuentra en desarrollo. Actualmente cuenta con una implementación inicial del módulo de administradores, conexión a PostgreSQL, estructura modular y configuración básica de FastAPI.

Quedan pendientes de completar los módulos de vehículos y solicitudes de compra, así como la autenticación y autorización administrativa y la integración completa de los componentes de seguridad.

## Consideraciones

- Mantener las credenciales de conexión en el archivo `.env`.
- No subir archivos con información sensible al repositorio.
- Mantener la separación de responsabilidades entre las capas.
- Documentar los nuevos endpoints conforme se implementen.

## Repositorio

[GitHub - WernerToledoSv/backendConcesionario](https://github.com/WernerToledoSv/backendConcesionario)
