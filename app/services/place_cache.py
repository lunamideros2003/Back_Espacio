import time


class TtlCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
        self._data: dict[str, tuple[float, object]] = {}

    def get(self, key: str):
        row = self._data.get(key)
        if not row:
            return None
        saved_at, value = row
        if time.time() - saved_at > self.ttl:
            self._data.pop(key, None)
            return None
        return value

    def set(self, key: str, value) -> None:
        self._data[key] = (time.time(), value)
