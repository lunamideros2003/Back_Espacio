import ipaddress


def client_ip(headers: dict, client_host: str | None) -> str | None:
    lowered = {str(key).lower(): value for key, value in (headers or {}).items()}
    forwarded = lowered.get("x-forwarded-for") or ""
    if forwarded:
        first = str(forwarded).split(",")[0].strip()
        if first:
            return first
    real = str(lowered.get("x-real-ip") or "").strip()
    if real:
        return real
    return client_host


def is_public_ip(value: str | None) -> bool:
    if not value:
        return False
    try:
        ip = ipaddress.ip_address(str(value).split("%")[0])
    except ValueError:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local or ip.is_unspecified)
