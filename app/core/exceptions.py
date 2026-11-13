class AdministradorNotFoundError(Exception):
    def __init__(self, administrador_id: int):
        self.administrador_id = administrador_id
        super().__init__(f"Administrador con id {administrador_id} no encontrado.")


class AdministradorEmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Ya existe un administrador con el email '{email}'.")


class CredencialesInvalidasError(Exception):
    def __init__(self):
        super().__init__("Correo o contraseña incorrectos.")


class VehiculoNotFoundError(Exception):
    def __init__(self, vehiculo_id: int):
        self.vehiculo_id = vehiculo_id
        super().__init__(f"Vehículo con id {vehiculo_id} no encontrado.")


class InvalidAccessTokenError(Exception):
    pass


class SolicitudNotFoundError(Exception):
    def __init__(self, solicitud_id: int):
        self.solicitud_id = solicitud_id
        super().__init__(f"Solicitud con id {solicitud_id} no encontrada.")


class VehiculosSolicitudNotFoundError(Exception):
    def __init__(self, vehiculo_ids: list[int]):
        self.vehiculo_ids = vehiculo_ids
        super().__init__(
            f"No se encontraron los vehículos: {', '.join(map(str, vehiculo_ids))}."
        )


class DuplicateVehiclesInSolicitudError(Exception):
    pass


class VehiclesNotProvidedError(Exception):
    pass


class InvalidSolicitudStateError(Exception):
    def __init__(self, estado: str):
        self.estado = estado
        super().__init__(f"El estado '{estado}' no es válido.")


class InvalidSolicitudTransitionError(Exception):
    def __init__(self, estado_actual: str, estado_nuevo: str):
        self.estado_actual = estado_actual
        self.estado_nuevo = estado_nuevo
        super().__init__(
            f"No se permite cambiar una solicitud de "
            f"'{estado_actual}' a '{estado_nuevo}'."
        )


class ConcurrentSolicitudUpdateError(Exception):
    pass
