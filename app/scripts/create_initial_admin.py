from getpass import getpass

from app.application.dto.administrador_dto import CrearAdministradorDTO
from app.application.use_cases.administradores.crear_administrador import (
    CrearAdministradorUseCase,
)
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.repositories.sqlalchemy_administrador_repository import (
    SQLAlchemyAdministradorRepository,
)
from app.presentation.api.v1.schemas.administrador_schema import (
    AdministradorCreateRequest,
)


def main() -> None:
    with SessionLocal() as db:
        repository = SQLAlchemyAdministradorRepository(db)
        if repository.get_all():
            raise SystemExit(
                "Ya existe un administrador. Use la API autenticada para crear otros."
            )

        nombre = input("Nombre del administrador: ").strip()
        correo = input("Correo del administrador: ").strip()
        password = getpass("Contraseña (mínimo 12 caracteres): ")
        password_confirm = getpass("Confirme la contraseña: ")
        if password != password_confirm:
            raise SystemExit("Las contraseñas no coinciden.")

        payload = AdministradorCreateRequest(
            nombre=nombre,
            correo=correo,
            password=password,
        )
        creado = CrearAdministradorUseCase(repository).execute(
            CrearAdministradorDTO(
                nombre=payload.nombre,
                correo=str(payload.correo),
                password=payload.password,
            )
        )
        print(f"Administrador inicial creado con ID {creado.id}.")


if __name__ == "__main__":
    main()
