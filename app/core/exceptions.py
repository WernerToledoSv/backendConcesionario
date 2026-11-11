class AdministradorNotFoundError(Exception):
    def __init__(self, administrador_id: int):
        self.administrador_id = administrador_id
        super().__init__(f"Administrador con id {administrador_id} no encontrado.")


class AdministradorEmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Ya existe un administrador con el email '{email}'.")
