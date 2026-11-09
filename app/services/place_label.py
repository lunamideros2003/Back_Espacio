def format_label(*parts: str | None, limit: int = 80) -> str:
    seen: list[str] = []
    for part in parts:
        if not part:
            continue
        text = " ".join(str(part).split())
        if text and text not in seen:
            seen.append(text)
    label = ", ".join(seen[:2])
    return label[:limit]
