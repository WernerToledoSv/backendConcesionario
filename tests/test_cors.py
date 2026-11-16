def test_allows_preflight_from_frontend(client):
    origins = [
        "https://frontendautomarket-git-main-werner-toledos-projects.vercel.app",
        "https://frontendautomarket.vercel.app",
    ]

    for origin in origins:
        for method in ["GET", "POST", "PUT", "DELETE"]:
            response = client.options(
                "/health",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": method,
                },
            )

            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == origin
            assert method in response.headers["access-control-allow-methods"]


def test_rejects_unconfigured_method(client):
    response = client.options(
        "/health",
        headers={
            "Origin": "https://frontendautomarket-git-main-werner-toledos-projects.vercel.app",
            "Access-Control-Request-Method": "PATCH",
        },
    )

    assert response.status_code == 400


def test_rejects_preflight_from_other_origins(client):
    response = client.options(
        "/health",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in response.headers
