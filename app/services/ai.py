import re

import httpx

from app.config import settings
from app.models import CelestialObject

TYPE_LABEL = {
    "planet": "planeta",
    "star": "estrella",
    "galaxy": "galaxia",
    "phenomenon": "fenómeno",
    "moon": "luna",
    "nebula": "nebulosa",
}


def local_reply(message: str, objects: list[CelestialObject], user_level: str = "beginner") -> str:
    text = message.lower().strip()
    if re.search(r"hola|buenas|hey|saludos", text):
        return (
            "Hola, soy AstroIA. Puedo explicarte planetas, estrellas y fenómenos, "
            "decirte qué observar esta noche o prepararte un quiz. ¿Qué te gustaría explorar?"
        )
    if re.search(r"observ|esta noche|cielo|qué ver|que ver", text):
        return (
            "Abre «¿Qué puedo observar esta noche?». Usaré tu ubicación, la fecha, "
            "el clima (Open-Meteo) y la posición real de planetas."
        )
    if re.search(r"quiz|pregunta|examen|test", text):
        return "En Quiz Astronómico genero preguntas según tu nivel. Cada intento se guarda en tu puntuación."
    if re.search(r"clasific", text):
        return "En Clasificar objeto dime color, brillo y si se mueve: te ayudo a distinguir planeta, estrella, galaxia, satélite o avión."

    hit = None
    for obj in objects:
        hay = f"{obj.name} {obj.slug} {obj.tags}".lower()
        if any(len(w) > 3 and w in text for w in hay.replace(",", " ").split()):
            hit = obj
            break
        if obj.name.lower() in text or obj.slug in text:
            hit = obj
            break

    if hit:
        expl = {
            "beginner": hit.explain_beginner,
            "intermediate": hit.explain_medium,
            "advanced": hit.explain_advanced,
        }.get(user_level, hit.explain_beginner)
        kind = TYPE_LABEL.get(hit.type, hit.type)
        return f"{hit.name} ({kind}). {expl}\n\nDato curioso: {hit.fun_fact}"

    return (
        "Puedo hablar de Mercurio, Venus, Marte, Júpiter, Saturno, la Luna, Sirio, "
        "Betelgeuse, Andrómeda, auroras, eclipses y más. Pregúntame por un objeto "
        "o dime «qué puedo ver esta noche»."
    )


async def chat_with_astroia(message: str, objects: list[CelestialObject], level: str, history: list[dict] | None = None):
    history = history or []
    if not settings.groq_api_key:
        return {"reply": local_reply(message, objects, level), "provider": "local"}

    catalog = "\n".join(
        f"- {o.name} [{o.type}]: {o.explain_beginner[:180]}" for o in objects[:24]
    )
    system = (
        f"Eres AstroIA, tutora de astronomía en español. Adapta el nivel: {level}. "
        f"Sé clara, entusiasta y precisa. Catálogo:\n{catalog}"
    )
    messages = [{"role": "system", "content": system}]
    for item in history[-8:]:
        if item.get("role") in {"user", "assistant"} and item.get("content"):
            messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "temperature": 0.5,
                    "max_tokens": 500,
                },
            )
        if res.status_code != 200:
            return {"reply": local_reply(message, objects, level), "provider": "local"}
        data = res.json()
        reply = (data.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
        return {"reply": reply or local_reply(message, objects, level), "provider": "groq"}
    except httpx.HTTPError:
        return {"reply": local_reply(message, objects, level), "provider": "local"}


def classify_description(brightness: int, color: str, moving: str, shape: str) -> dict:
    reasons = []
    kind = "star"
    confidence = 0.55
    title = "Probable estrella"

    if moving == "yes" and brightness >= 4:
        kind = "satellite"
        title = "Probable satélite o ISS"
        confidence = 0.78
        reasons.append("Se desplaza de forma constante y es brillante.")
    elif moving == "yes" and brightness <= 3:
        kind = "airplane"
        title = "Podría ser un avión"
        confidence = 0.7
        reasons.append("Luces en movimiento a baja o media altura suelen ser aeronaves.")
    elif shape == "extended" and color == "white":
        kind = "galaxy"
        title = "Posible galaxia o cúmulo"
        confidence = 0.62
        reasons.append("Objeto extendido y difuso, no un punto.")
    elif moving in {"no", "", None}:
        if color in {"yellow", "cream"} and brightness >= 4:
            kind = "planet"
            title = "Probable planeta (Venus/Júpiter)"
            confidence = 0.8
            reasons.append("Punto brillante que no parpadea tanto como una estrella.")
        elif color == "red" and brightness >= 3:
            kind = "planet"
            title = "Podría ser Marte o una estrella roja"
            confidence = 0.66
            reasons.append("Tono rojizo: Marte o gigantes como Betelgeuse.")
        elif color == "blue":
            kind = "star"
            title = "Estrella caliente (tipo O/B)"
            confidence = 0.74
            reasons.append("El azul indica alta temperatura superficial.")
        else:
            reasons.append("Punto fijo: las estrellas parpadean por la atmósfera.")

    if shape == "disk":
        kind = "planet"
        title = "Planeta o la Luna"
        confidence = 0.85
        reasons.append("Se aprecia disco, no un punto.")

    return {"type": kind, "title": title, "confidence": confidence, "reasons": reasons}
