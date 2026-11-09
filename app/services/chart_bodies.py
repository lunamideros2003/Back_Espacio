"""Static astronomy data used by the sky chart."""

CHART_BODIES = [
    {"slug": "sol", "name": "Sol", "astronomy_body": "sun", "type": "star", "size": 13.0},
    {"slug": "luna", "name": "Luna", "astronomy_body": "moon", "type": "moon", "size": 11.0},
    {"slug": "mercurio", "name": "Mercurio", "astronomy_body": "mercury", "type": "planet", "size": 7.0},
    {"slug": "venus", "name": "Venus", "astronomy_body": "venus", "type": "planet", "size": 8.5},
    {"slug": "marte", "name": "Marte", "astronomy_body": "mars", "type": "planet", "size": 7.5},
    {"slug": "jupiter", "name": "Júpiter", "astronomy_body": "jupiter", "type": "planet", "size": 9.5},
    {"slug": "saturno", "name": "Saturno", "astronomy_body": "saturn", "type": "planet", "size": 8.5},
    {"slug": "urano", "name": "Urano", "astronomy_body": "uranus", "type": "planet", "size": 6.5},
    {"slug": "neptuno", "name": "Neptuno", "astronomy_body": "neptune", "type": "planet", "size": 6.5},
]

CARDINALS = [(0, "N"), (90, "E"), (180, "S"), (270, "O")]

