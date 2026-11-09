from app.services.client_ip import client_ip, is_public_ip
from app.services.coords import coords_ok, parse_coord
from app.services.fallback_place import fallback_place
from app.services.ip_lookup import lookup_ip as default_lookup_ip
from app.services.reverse_place import reverse_label as default_reverse_label


async def resolve_place(lat, lng, user, headers, client_host, lookup_ip=None, reverse_label=None) -> dict:
    lookup_ip = lookup_ip or default_lookup_ip
    reverse_label = reverse_label or default_reverse_label

    lat_n = parse_coord(lat)
    lng_n = parse_coord(lng)
    if lat_n is not None and lng_n is not None and coords_ok(lat_n, lng_n):
        label = await reverse_label(lat_n, lng_n) or "Tu zona"
        return {"latitude": lat_n, "longitude": lng_n, "label": label, "source": "browser"}

    if user is not None and user.latitude is not None and user.longitude is not None and coords_ok(user.latitude, user.longitude):
        label = (getattr(user, "city", None) or "").strip() or "Tu perfil"
        return {"latitude": user.latitude, "longitude": user.longitude, "label": label, "source": "profile"}

    ip = client_ip(headers, client_host)
    found = await lookup_ip(ip if is_public_ip(ip) else None)
    if found:
        return found
    return fallback_place()
