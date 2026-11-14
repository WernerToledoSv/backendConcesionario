from app.core.security import hash_password
from app.infrastructure.models.administrador_model import AdministradorModel
from app.infrastructure.models.solicitud_model import SolicitudCompraModel
from app.infrastructure.models.vehiculo_model import VehiculoModel


def add_vehicle(test_db, marca, precio):
    with test_db() as db:
        vehicle = VehiculoModel(
            condicion="usado",
            marca=marca,
            modelo="Modelo",
            anio=2022,
            precio=precio,
            kilometraje=10000,
            transmision="automatica",
            combustible="gasolina",
            estado="disponible",
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle.id


def login_headers(client, test_db):
    with test_db() as db:
        db.add(
            AdministradorModel(
                nombre="Admin Test",
                correo="admin@example.com",
                password_hash=hash_password("secure-password-123"),
                activo=True,
            )
        )
        db.commit()
    response = client.post(
        "/api/v1/administradores/IniciarSesion",
        json={"correo": "admin@example.com", "password": "secure-password-123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_public_request_uses_server_prices_and_is_atomic(client, test_db):
    first_id = add_vehicle(test_db, "Marca A", "12000.00")
    second_id = add_vehicle(test_db, "Marca B", "8500.50")
    response = client.post(
        "/api/v1/solicitudes/CrearSolicitud",
        json={
            "nombre_cliente": "Cliente Ejemplo",
            "correo_cliente": "cliente@example.com",
            "telefono_cliente": "555-0101",
            "vehiculos_ids": [first_id, second_id],
            "mensaje_cliente": "Quiero información.",
        },
    )

    assert response.status_code == 201
    request_data = response.json()["item"]
    assert request_data["total_estimado"] == "20500.50"
    assert [detail["precio_unitario"] for detail in request_data["detalles"]] == [
        "12000.00",
        "8500.50",
    ]

    duplicate = client.post(
        "/api/v1/solicitudes/CrearSolicitud",
        json={
            "nombre_cliente": "Cliente Ejemplo",
            "correo_cliente": "cliente@example.com",
            "telefono_cliente": "555-0101",
            "vehiculos_ids": [first_id, first_id],
        },
    )
    missing = client.post(
        "/api/v1/solicitudes/CrearSolicitud",
        json={
            "nombre_cliente": "Cliente Ejemplo",
            "correo_cliente": "cliente@example.com",
            "telefono_cliente": "555-0101",
            "vehiculos_ids": [first_id, 999999],
        },
    )
    price_from_client = client.post(
        "/api/v1/solicitudes/CrearSolicitud",
        json={
            "nombre_cliente": "Cliente Ejemplo",
            "correo_cliente": "cliente@example.com",
            "telefono_cliente": "555-0101",
            "vehiculos_ids": [first_id],
            "total_estimado": 1,
        },
    )

    assert duplicate.status_code == 422
    assert missing.status_code == 404
    assert price_from_client.status_code == 422
    with test_db() as db:
        assert db.query(SolicitudCompraModel).count() == 1


def test_notes_and_state_changes_require_admin_and_update_request(client, test_db):
    vehicle_id = add_vehicle(test_db, "Marca A", "12000.00")
    created = client.post(
        "/api/v1/solicitudes/CrearSolicitud",
        json={
            "nombre_cliente": "Cliente Ejemplo",
            "correo_cliente": "cliente@example.com",
            "telefono_cliente": "555-0101",
            "vehiculos_ids": [vehicle_id],
        },
    )
    request_id = created.json()["item"]["id"]
    assert (
        client.patch(
            f"/api/v1/solicitudes/ActualizarNotas/{request_id}",
            json={"notas_administrador": "Llamar mañana."},
        ).status_code
        == 401
    )
    assert (
        client.patch(
            f"/api/v1/solicitudes/ActualizarEstado/{request_id}",
            json={"estado": "contactado"},
        ).status_code
        == 401
    )

    headers = login_headers(client, test_db)
    notes_response = client.patch(
        f"/api/v1/solicitudes/ActualizarNotas/{request_id}",
        json={"notas_administrador": "Llamar mañana."},
        headers=headers,
    )
    assert notes_response.status_code == 200

    for state in ("contactado", "confirmada", "completada"):
        response = client.patch(
            f"/api/v1/solicitudes/ActualizarEstado/{request_id}",
            json={"estado": state},
            headers=headers,
        )
        assert response.status_code == 200

    invalid_transition = client.patch(
        f"/api/v1/solicitudes/ActualizarEstado/{request_id}",
        json={"estado": "cancelada"},
        headers=headers,
    )
    invalid_state = client.patch(
        f"/api/v1/solicitudes/ActualizarEstado/{request_id}",
        json={"estado": "archivada"},
        headers=headers,
    )
    assert invalid_transition.status_code == 409
    assert invalid_state.status_code == 422

    listed = client.get(
        "/api/v1/solicitudes/ListarSolicitudes",
        headers=headers,
    )
    request_data = listed.json()["items"][0]
    assert request_data["estado"] == "completada"
    assert request_data["notas_administrador"] == "Llamar mañana."
    assert request_data["actualizado_en"] is not None
