from services.ollama import ask_ollama
import json


prompt = """
Você é um AVALIADOR DE SIMILARIDADE DE ASSUNTO em conversas.

Tarefa:
Avaliar o quão semelhantes são os assuntos do Bloco A e do Bloco B.

Definição:
- Assunto = TEMA ESPECÍFICO PRINCIPAL (objeto central) do texto.
- Considere que os blocos fazem parte da mesma conversa.

Regra fundamental (OBRIGATÓRIA):
Avalie a similaridade pelo OBJETO CENTRAL.
Relações indiretas, consequências ou exemplos NÃO significam mesmo assunto.

Escala de pontuação (RÍGIDA):
0–2  → domínios totalmente diferentes
3–4  → mesmo domínio, assunto específico diferente
5–6  → assuntos relacionados ou consequenciais
7–8  → mesmo assunto, foco diferente
9–10 → mesmo assunto específico e mesmo foco

Regras adicionais:
- Se o foco principal mudar, a nota NÃO pode ser maior que 6.
- Não agrupe por domínio geral.
- Não relativize por continuidade da conversa.
- Ignore estilo, tom e transições narrativas.
- Seja criterioso: prefira notas menores em caso de dúvida.

Formato da resposta: responda somente a nota, literalmente o nuḿero da NOTA:


Bloco A:
{0}

Bloco B:
{1}
"""


import json
import spacy


WINDOW_SECONDS = 160
MIN_OVERLAP = 0.2
PERSISTENCE = 3


nlp = spacy.load("pt_core_news_sm")


def group_by_time(transcript, window_seconds):
    blocks = []
    buffer = []
    start = transcript[0]["start"]

    for seg in transcript:
        buffer.append(seg["text"])

        if seg["end"] - start >= window_seconds:
            blocks.append({
                "start": start,
                "end": seg["end"],
                "text": " ".join(buffer)
            })
            buffer = []
            start = seg["end"]

    if buffer:
        blocks.append({
            "start": start,
            "end": transcript[-1]["end"],
            "text": " ".join(buffer)
        })

    return blocks


def extract_topics(text):
    doc = nlp(text.lower())
    topics = set()

    for token in doc:
        if token.is_alpha and not token.is_stop:
            if token.pos_ in {"NOUN", "PROPN"}:
                topics.add(token.lemma_)

    return topics


def is_continuation(context_topics, curr_topics, min_overlap):
    if not context_topics:
        return True

    overlap = len(context_topics & curr_topics) / max(len(context_topics), 1)
    return overlap >= min_overlap


def detect_topic_changes(blocks):
    for b in blocks:
        b["topics"] = extract_topics(b["text"])

    changes = []
    context_topics = set(blocks[0]["topics"])
    streak = 0

    for i in range(1, len(blocks)):
        curr_topics = blocks[i]["topics"]

        if is_continuation(context_topics, curr_topics, MIN_OVERLAP):
            context_topics |= curr_topics
            streak = 0
            continue

        streak += 1

        if streak >= PERSISTENCE:
            changes.append({
                "timestamp": blocks[i]["start"],
                "block_index": i,
                "topics": curr_topics
            })
            context_topics = set(curr_topics)
            streak = 0

    return changes


def build_topic_segments(blocks, changes):
    segments = []

    if not changes:
        return [{
            "start": blocks[0]["start"],
            "end": blocks[-1]["end"],
            "topics": sorted(blocks[0]["topics"]),
            "text": " ".join(b["text"] for b in blocks)
        }]

    start_block = 0

    for change in changes:
        end_block = change["block_index"]

        segment_blocks = blocks[start_block:end_block]

        segments.append({
            "start": segment_blocks[0]["start"],
            "end": segment_blocks[-1]["end"],
            "topics": sorted(segment_blocks[0]["topics"]),
            "text": " ".join(b["text"] for b in segment_blocks)
        })

        start_block = end_block

    segment_blocks = blocks[start_block:]

    segments.append({
        "start": segment_blocks[0]["start"],
        "end": segment_blocks[-1]["end"],
        "topics": sorted(segment_blocks[0]["topics"]),
        "text": " ".join(b["text"] for b in segment_blocks)
    })

    return segments


def main():
    with open("transcribe.json", "r", encoding="utf-8") as f:
        transcript = json.load(f)

    blocks = group_by_time(transcript, WINDOW_SECONDS)
    changes = detect_topic_changes(blocks)
    segments = build_topic_segments(blocks, changes)

    print(json.dumps(segments, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
