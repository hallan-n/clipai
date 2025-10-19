import random

segments = [
    {"index": 0, "start": 0.0,  "end": 20.0,  "text": "Introdução ao tema, poucas novidades aqui."},
    {"index": 1, "start": 20.0, "end": 40.0,  "text": "Explicando a técnica: isso parece chato, mas olha isso! funciona bem."},
    {"index": 2, "start": 40.0, "end": 60.0,  "text": "Exemplo prático com números: veja os resultados impressionantes."},
    {"index": 3, "start": 60.0, "end": 80.0,  "text": "Momento engraçado, risada da audiência! isso quebrou tudo."},
    {"index": 4, "start": 80.0, "end": 100.0, "text": "Resumo e call-to-action: inscreva-se e ative as notificações!"}
]

# ---------- 2) HEURÍSTICA DE RELEVÂNCIA ----------
KEYWORDS = ["olha", "importante", "risada", "insight", "mudar",
            "incrível", "resultados", "call-to-action", "inscreva", "!"]

def heuristic_score(text: str) -> float:
    text_lower = text.lower()
    score = 0.0
    for kw in KEYWORDS:
        if kw in text_lower:
            score += 1.4
    score += len(text_lower.split()) * 0.04
    if "!" in text:
        score += 0.6
    score += random.uniform(-0.2, 0.3)
    return round(score, 3)

# Calcula o score de cada segmento
for seg in segments:
    seg["score"] = heuristic_score(seg["text"])

# ---------- 3) SELECIONA TOP HIGHLIGHTS ----------
TOP_K = 3
highlights = sorted(segments, key=lambda s: s["score"], reverse=True)[:TOP_K]

# ---------- 4) RESULTADO ----------
print("=== SEGMENTOS ORDENADOS POR RELEVÂNCIA ===")
for h in highlights:
    print(f"Index: {h['index']} | Start-End: {h['start']}-{h['end']} | Score: {h['score']}")
    print(f"Text: {h['text']}\n")
