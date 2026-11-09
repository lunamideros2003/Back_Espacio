def parse_coord(value):
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number or number in (float("inf"), float("-inf")):
        return None
    return number


def coords_ok(lat: float, lng: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lng <= 180
