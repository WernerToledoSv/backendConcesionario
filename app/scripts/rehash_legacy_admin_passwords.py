from argon2 import extract_parameters
from argon2.exceptions import InvalidHashError

from app.core.security import hash_password
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.models.administrador_model import AdministradorModel


def main() -> None:
    with SessionLocal() as db:
        administrators = db.query(AdministradorModel).all()
        updated_count = 0
        for administrator in administrators:
            try:
                extract_parameters(administrator.password_hash)
            except InvalidHashError:
                administrator.password_hash = hash_password(
                    administrator.password_hash
                )
                updated_count += 1
        db.commit()
    print(f"Contraseñas migradas a Argon2id: {updated_count}.")


if __name__ == "__main__":
    main()
