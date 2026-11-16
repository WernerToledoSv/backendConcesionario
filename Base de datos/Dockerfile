
# Imagen oficial de PostgreSQL
FROM postgres:17

# Información de la imagen
LABEL maintainer="Proyecto Concesionario"
LABEL description="Base de datos PostgreSQL para sistema de venta de vehículos"

# Copiar script de inicialización del esquema
COPY --chown=postgres:postgres bdConcesionario.sql /docker-entrypoint-initdb.d/01-bdConcesionario.sql

# Puerto de PostgreSQL
EXPOSE 5432
