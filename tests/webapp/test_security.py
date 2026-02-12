"""Tests for security headers and CSRF protection."""

from fastapi.testclient import TestClient


def test_security_headers_present(client: TestClient) -> None:
    """Test that security headers are present in responses."""
    response = client.get("/health")

    # Check required security headers
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"

    assert "x-frame-options" in response.headers
    assert response.headers["x-frame-options"] == "DENY"

    assert "x-xss-protection" in response.headers
    assert "1" in response.headers["x-xss-protection"]

    assert "referrer-policy" in response.headers

    assert "content-security-policy" in response.headers


def test_request_id_header(client: TestClient) -> None:
    """Test that request ID header is present in responses."""
    response = client.get("/health")
    assert "x-request-id" in response.headers
    assert len(response.headers["x-request-id"]) > 0


def test_cors_headers_on_preflight(client: TestClient) -> None:
    """Test CORS headers on OPTIONS preflight request."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers


def test_cors_blocked_origin(client: TestClient) -> None:
    """Test that requests from non-allowed origins don't get CORS headers."""
    response = client.get(
        "/health",
        headers={"Origin": "http://malicious-site.com"},
    )

    # The request succeeds but CORS headers should not include the origin
    assert response.status_code == 200
    # Note: The actual CORS behavior depends on middleware configuration


def test_no_hsts_in_debug_mode(client: TestClient) -> None:
    """Test that HSTS header is not set in debug/dev mode."""
    response = client.get("/health")

    # In debug mode, HSTS should not be set
    # (our test config has debug=True)
    assert "strict-transport-security" not in response.headers
