-- =====================================================
-- BASE DE DATOS: VENTA_CARROS
-- MOTOR: PostgreSQL (NEON)
-- MONEDA: USD
-- =====================================================

-- 1. ADMINISTRADORES
CREATE TABLE IF NOT EXISTS administradores (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ NULL DEFAULT NOW()
);

-- 2. VEHICULOS
CREATE TABLE IF NOT EXISTS vehiculos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    condicion VARCHAR(10) NOT NULL DEFAULT 'usado'
        CHECK (condicion IN ('nuevo', 'usado')),
    marca VARCHAR(80) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    anio SMALLINT NOT NULL CHECK (anio >= 1900),
    precio NUMERIC(12,2) NOT NULL CHECK (precio >= 0),
    kilometraje INTEGER NOT NULL DEFAULT 0
        CHECK (kilometraje >= 0),
    transmision VARCHAR(15) NOT NULL DEFAULT 'automatica'
        CHECK (transmision IN ('manual', 'automatica', 'otra')),
    combustible VARCHAR(15) NOT NULL DEFAULT 'gasolina'
        CHECK (combustible IN ('gasolina', 'diesel', 'hibrido', 'electrico', 'otro')),
    descripcion TEXT,
    fotoauto TEXT,
    estado VARCHAR(15) NOT NULL DEFAULT 'disponible'
        CHECK (estado IN ('disponible', 'reservado', 'vendido')),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ NULL DEFAULT NOW()
);


-- 3. SOLICITUDES DE COMPRA
CREATE TABLE IF NOT EXISTS solicitudes_compra (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_cliente VARCHAR(150) NOT NULL,
    correo_cliente VARCHAR(180) NOT NULL,
    telefono_cliente VARCHAR(30) NOT NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN (
            'pendiente',
            'contactado',
            'confirmada',
            'rechazada',
            'cancelada',
            'completada'
        )),
    total_estimado NUMERIC(12,2) NOT NULL DEFAULT 0.00
        CHECK (total_estimado >= 0),
    mensaje_cliente TEXT,
    notas_administrador TEXT,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ NULL DEFAULT NOW()
);


-- 4. DETALLE DE SOLICITUD
CREATE TABLE IF NOT EXISTS detalle_solicitud (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    solicitud_id BIGINT NOT NULL,
    vehiculo_id BIGINT NOT NULL,
    precio_unitario NUMERIC(12,2) NOT NULL
        CHECK (precio_unitario >= 0),

    CONSTRAINT uq_solicitud_vehiculo
        UNIQUE (solicitud_id, vehiculo_id),

    CONSTRAINT fk_detalle_solicitud
        FOREIGN KEY (solicitud_id)
        REFERENCES solicitudes_compra (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_detalle_vehiculo
        FOREIGN KEY (vehiculo_id)
        REFERENCES vehiculos (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- =====================================================
-- DESCRIPCIONES DE TABLAS Y COLUMNAS
-- =====================================================

-- ADMINISTRADORES
COMMENT ON TABLE administradores IS
'Cuentas autorizadas para ingresar al panel administrativo de la tienda.';

COMMENT ON COLUMN administradores.id IS
'Identificador único del administrador.';

COMMENT ON COLUMN administradores.nombre IS
'Nombre completo del administrador.';

COMMENT ON COLUMN administradores.correo IS
'Correo electrónico utilizado para iniciar sesión. Debe ser único.';

COMMENT ON COLUMN administradores.password_hash IS
'Hash seguro de la contraseña. Nunca almacenar la contraseña en texto plano.';

COMMENT ON COLUMN administradores.activo IS
'Indica si la cuenta del administrador está habilitada.';

COMMENT ON COLUMN administradores.creado_en IS
'Fecha y hora en que se creó la cuenta.';

COMMENT ON COLUMN administradores.actualizado_en IS
'Fecha y hora de la última modificación de la cuenta.';


-- VEHICULOS
COMMENT ON TABLE vehiculos IS
'Inventario de automóviles publicados en el catálogo de la tienda.';

COMMENT ON COLUMN vehiculos.id IS
'Identificador único del vehículo.';

COMMENT ON COLUMN vehiculos.condicion IS
'Condición comercial del vehículo: nuevo o usado.';

COMMENT ON COLUMN vehiculos.marca IS
'Marca o fabricante del vehículo.';

COMMENT ON COLUMN vehiculos.modelo IS
'Modelo comercial del vehículo.';

COMMENT ON COLUMN vehiculos.anio IS
'Año de fabricación o modelo del vehículo.';

COMMENT ON COLUMN vehiculos.precio IS
'Precio de venta del vehículo expresado en dólares estadounidenses (USD).';

COMMENT ON COLUMN vehiculos.kilometraje IS
'Kilometraje recorrido por el vehículo. Para un vehículo nuevo puede ser cero.';

COMMENT ON COLUMN vehiculos.transmision IS
'Tipo de transmisión del vehículo: manual, automática u otra.';

COMMENT ON COLUMN vehiculos.combustible IS
'Tipo de combustible o energía utilizada por el vehículo.';

COMMENT ON COLUMN vehiculos.descripcion IS
'Descripción adicional del vehículo que se mostrará en el catálogo.';

COMMENT ON COLUMN vehiculos.fotoauto IS
'Fotografía principal del vehículo almacenada como ruta o URL.';

COMMENT ON COLUMN vehiculos.estado IS
'Disponibilidad comercial del vehículo: disponible, reservado o vendido.';

COMMENT ON COLUMN vehiculos.creado_en IS
'Fecha y hora en que se registró el vehículo en el inventario.';

COMMENT ON COLUMN vehiculos.actualizado_en IS
'Fecha y hora de la última modificación de los datos del vehículo.';


-- SOLICITUDES DE COMPRA
COMMENT ON TABLE solicitudes_compra IS
'Solicitudes de información, compra o reserva enviadas por los clientes.';

COMMENT ON COLUMN solicitudes_compra.id IS
'Identificador único de la solicitud de compra.';

COMMENT ON COLUMN solicitudes_compra.nombre_cliente IS
'Nombre completo de la persona que envía la solicitud.';

COMMENT ON COLUMN solicitudes_compra.correo_cliente IS
'Correo electrónico de contacto del cliente.';

COMMENT ON COLUMN solicitudes_compra.telefono_cliente IS
'Número telefónico de contacto del cliente.';

COMMENT ON COLUMN solicitudes_compra.estado IS
'Estado de atención de la solicitud: pendiente, contactado, confirmada, rechazada, cancelada o completada.';

COMMENT ON COLUMN solicitudes_compra.total_estimado IS
'Suma estimada de los vehículos incluidos en la solicitud, expresada en USD.';

COMMENT ON COLUMN solicitudes_compra.mensaje_cliente IS
'Mensaje o comentario que el cliente agrega al enviar la solicitud.';

COMMENT ON COLUMN solicitudes_compra.notas_administrador IS
'Notas internas del administrador sobre la atención de la solicitud.';

COMMENT ON COLUMN solicitudes_compra.creado_en IS
'Fecha y hora en que el cliente envió la solicitud.';

COMMENT ON COLUMN solicitudes_compra.actualizado_en IS
'Fecha y hora de la última actualización de la solicitud.';


-- DETALLE DE SOLICITUD
COMMENT ON TABLE detalle_solicitud IS
'Detalle de los vehículos incluidos en cada solicitud de compra.';

COMMENT ON COLUMN detalle_solicitud.id IS
'Identificador único del detalle de solicitud.';

COMMENT ON COLUMN detalle_solicitud.solicitud_id IS
'Identificador de la solicitud a la que pertenece este detalle.';

COMMENT ON COLUMN detalle_solicitud.vehiculo_id IS
'Identificador del vehículo incluido en la solicitud.';

COMMENT ON COLUMN detalle_solicitud.precio_unitario IS
'Precio del vehículo al momento de enviar la solicitud, expresado en USD.';


-- =====================================================
-- INDICES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_vehiculos_catalogo
ON vehiculos (estado, marca, anio);

CREATE INDEX IF NOT EXISTS idx_vehiculos_precio
ON vehiculos (precio);

CREATE INDEX IF NOT EXISTS idx_vehiculos_condicion
ON vehiculos (condicion);

CREATE INDEX IF NOT EXISTS idx_solicitudes_estado_fecha
ON solicitudes_compra (estado, creado_en);

CREATE INDEX IF NOT EXISTS idx_solicitudes_correo
ON solicitudes_compra (correo_cliente);

CREATE INDEX IF NOT EXISTS idx_detalle_vehiculo
ON detalle_solicitud (vehiculo_id);

INSERT INTO public.administradores
(nombre, correo, password_hash)
VALUES('admin ', 'admin@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$QlFjbHKIwMU3dBVGsy0mfA$4YJ7Y2uNq3apwsybV0a54t/hCQ2eTKKais24NPnPDYo');