from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings
from app.core.security import hash_password
from app.infrastructure.models.administrador_model import AdministradorModel


def add_admin(test_db, password="secure-password-123"):
    with test_db() as db:
        administrator = AdministradorModel(
            nombre="Admin Test",
            correo="admin@example.com",
            password_hash=hash_password(password),
            activo=True,
        )
        db.add(administrator)
        db.commit()
        db.refresh(administrator)
        return administrator.id


def login(client):
    response = client.post(
        "/api/v1/administradores/IniciarSesion",
        json={"correo": "admin@example.com", "password": "secure-password-123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login_issues_jwt_and_protects_admin_routes(client, test_db):
    add_admin(test_db)
    response = client.post(
        "/api/v1/administradores/IniciarSesion",
        json={"correo": "admin@example.com", "password": "secure-password-123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["expires_in"] == 900
    assert payload["item"]["correo"] == "admin@example.com"
    assert "password_hash" not in payload["item"]
    with test_db() as db:
        stored_hash = db.query(AdministradorModel).one().password_hash
    assert stored_hash.startswith("$argon2id$")
    assert stored_hash != "secure-password-123"

    claims = jwt.decode(
        payload["access_token"],
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithms=["HS256"],
        issuer=settings.JWT_ISSUER,
    )
    assert claims["sub"] == str(payload["item"]["id"])
    assert "iat" in claims and "exp" in claims
    assert client.get("/api/v1/administradores/ListarAdministradores").status_code == 401
    response = client.get(
        "/api/v1/administradores/ListarAdministradores",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )
    assert response.status_code == 200


def test_login_errors_are_generic_for_unknown_and_wrong_password(client, test_db):
    add_admin(test_db)
    wrong_password = client.post(
        "/api/v1/administradores/IniciarSesion",
        json={"correo": "admin@example.com", "password": "wrong-password"},
    )
    unknown_user = client.post(
        "/api/v1/administradores/IniciarSesion",
        json={"correo": "missing@example.com", "password": "wrong-password"},
    )

    assert wrong_password.status_code == unknown_user.status_code == 401
    assert wrong_password.json()["detail"] == unknown_user.json()["detail"]


def test_expired_and_invalid_tokens_are_rejected(client, test_db):
    admin_id = add_admin(test_db)
    expired_token = jwt.encode(
        {
            "sub": str(admin_id),
            "iat": datetime.now(timezone.utc) - timedelta(minutes=5),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
            "iss": settings.JWT_ISSUER,
        },
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm="HS256",
    )
    wrong_algorithm_token = jwt.encode(
        {
            "sub": str(admin_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "iss": settings.JWT_ISSUER,
        },
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm="HS384",
    )
    for token in ("not-a-jwt", expired_token, wrong_algorithm_token):
        response = client.get(
            "/api/v1/administradores/ListarAdministradores",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401


def test_token_is_rejected_if_admin_becomes_inactive(client, test_db):
    admin_id = add_admin(test_db)
    token = login(client)
    with test_db() as db:
        db.query(AdministradorModel).filter_by(id=admin_id).update(
            {"activo": False}
        )
        db.commit()

    response = client.get(
        "/api/v1/administradores/ListarAdministradores",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_administrative_routes_require_authentication(client):
    assert client.get("/api/v1/solicitudes/ListarSolicitudes").status_code == 401
    assert client.get("/api/v1/estadisticas/Resumen").status_code == 401
    assert (
        client.post(
            "/api/v1/administradores/CrearAdministrador",
            json={
                "nombre": "Otro Admin",
                "correo": "other@example.com",
                "password": "another-secure-password",
            },
        ).status_code
        == 401
    )


def test_vehicle_mutations_require_authentication(client):
    create_response = client.post(
        "/api/v1/vehiculos/CrearVehiculo",
        data={
            "marca": "Marca",
            "modelo": "Modelo",
            "anio": "2022",
            "precio": "12000.00",
        },
    )
    delete_response = client.delete("/api/v1/vehiculos/EliminarVehiculo/1")

    assert create_response.status_code == 401
    assert delete_response.status_code == 401
