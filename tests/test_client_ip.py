from app.services.client_ip import client_ip, is_public_ip


def test_forwarded_for_wins():
    headers = {"X-Forwarded-For": "8.8.8.8, 10.0.0.1", "X-Real-IP": "1.1.1.1"}
    assert client_ip(headers, "127.0.0.1") == "8.8.8.8"


def test_real_ip_is_used_without_forwarded():
    assert client_ip({"x-real-ip": "1.1.1.1"}, "127.0.0.1") == "1.1.1.1"


def test_client_host_fallback():
    assert client_ip({}, "127.0.0.1") == "127.0.0.1"


def test_missing_ip():
    assert client_ip({}, None) is None


def test_private_and_public_detection():
    assert is_public_ip("8.8.8.8") is True
    assert is_public_ip("127.0.0.1") is False
    assert is_public_ip("192.168.1.10") is False
    assert is_public_ip("10.0.0.1") is False
    assert is_public_ip("not-an-ip") is False
    assert is_public_ip(None) is False
