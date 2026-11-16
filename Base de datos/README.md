# Base de datos AutoMarket

Esta carpeta contiene el esquema PostgreSQL y la configuración para levantarlo con Docker Compose.
El `Dockerfile` copia `bdConcesionario.sql` a `/docker-entrypoint-initdb.d/`; PostgreSQL ejecuta ese
script al inicializar por primera vez un volumen de datos vacío.

## Requisitos

- Docker Desktop con Docker Compose.
- Un archivo `.env` en esta carpeta. No lo subas a Git.

Configura en ese `.env` las credenciales de PostgreSQL que correspondan al `DATABASE_URL` del
backend. Por ejemplo:

```env
POSTGRES_DB=bdconcesionario
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
POSTGRES_PORT=5432
TZ=America/El_Salvador
```

`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_PORT` deben coincidir con los datos
de conexión configurados en `DATABASE_URL` en el `.env` del backend. Si la contraseña contiene
caracteres especiales, codifícalos correctamente en la URL de conexión.

## Crear e iniciar el contenedor

Desde PowerShell, abre esta carpeta y construye/inicia el servicio:

```powershell
Set-Location "Base de datos"
docker compose up --build -d
```

Verifica el estado y revisa los logs de inicialización:

```powershell
docker compose ps
docker compose logs -f db
```

El puerto local por defecto es `5432`; se puede cambiar con `POSTGRES_PORT` en `.env`. Al terminar,
detén el servicio sin eliminar los datos:

```powershell
docker compose down
```

Los scripts de `/docker-entrypoint-initdb.d` solo se ejecutan cuando PostgreSQL crea un volumen
vacío. Si `postgres_data` ya existe, cambiar el esquema en el SQL no vuelve a ejecutarlo
automáticamente. `docker compose down -v` elimina el volumen y todos sus datos; úsalo solo si
realmente quieres reiniciar la base desde cero.
