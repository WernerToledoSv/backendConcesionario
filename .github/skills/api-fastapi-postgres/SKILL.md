---
name: api-fastapi-postgres
description: Implementa y depura cambios en la API FastAPI de AutoMarket siguiendo sus capas, contratos, acceso a PostgreSQL y pruebas existentes.
---

# API FastAPI y PostgreSQL

## Patrones del proyecto

- Sigue la separación existente: esquemas Pydantic y endpoints en `app/presentation`, casos de uso en `app/application`, contratos en `app/domain` e implementación SQLAlchemy en `app/infrastructure`.
- Reutiliza los `APIRouter`, dependencias, envoltorios de respuesta y excepciones ya usados por endpoints similares.
- Mantén las rutas administrativas protegidas mediante las dependencias de autenticación existentes.
- Convierte excepciones conocidas en respuestas HTTP explícitas; no ocultes errores con respuestas exitosas ni valores por defecto.

## Persistencia y estados

- Para cambios que escriben en varias tablas, conserva la atomicidad: actualiza todo en una transacción y revierte si una parte falla.
- Si dos solicitudes pueden competir por el mismo vehículo, comprueba el estado al escribir y responde con conflicto cuando ya no sea válido.
- Antes de cambiar el modelo, verifica el esquema SQL o las migraciones existentes; no ejecutes DDL contra la base configurada en `.env` sin autorización explícita.
- No expongas credenciales, URLs completas de conexión ni datos privados en mensajes o logs.

## Pruebas

- Añade pruebas enfocadas a las respuestas HTTP, transiciones válidas e inválidas, persistencia y rollback del comportamiento nuevo.
- Usa las fixtures y el `TestClient` del proyecto; contempla las diferencias de PostgreSQL y SQLite cuando afecten a la prueba.
- En Windows, ejecuta las pruebas con `.venv\Scripts\python.exe -m pytest <ruta-de-prueba> -q`.
- Informa advertencias o limitaciones relevantes sin atribuirles fallos que no causaron.
