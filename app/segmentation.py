prompt = """
Você é um analista de conteúdo político especializado em segmentação temática de discursos longos. Eu vou te fornecer a transcrição completa (com timestamps) de uma live de aproximadamente 2 horas. Essa live é dinâmica, com o orador mudando frequentemente de assunto (ex: Bolsonaro, Alexandre de Moraes, STF, MBL, eleições, mídia, etc.).

Objetivo:
Identificar cortes temáticos, onde cada corte representa um assunto central dominante.

Regras de segmentação:
- Um corte começa quando um novo assunto se torna claramente dominante.
- Um corte termina quando há transição clara para outro assunto.
- Assuntos podem ser politicamente relacionados, mas se o foco muda, é um novo corte.
- Ignore pequenas digressões curtas (comentários de até aproximadamente 1–2 minutos).
- Cada corte deve ter preferencialmente:
  - Duração mínima: ~7 minutos
  - Duração máxima: ~15 minutos
- Se um assunto durar mais de 15 minutos, divida em dois cortes coerentes.
- Se um assunto durar menos de 7 minutos, tente agrupar com o assunto anterior, se fizer sentido sem perder clareza temática.

O que você deve analisar:
- Mudança de foco discursivo
- Mudança de personagens centrais (ex: sai Bolsonaro, entra Alexandre de Moraes)
- Mudança de tese ou narrativa principal
- Mudança clara de contexto político

Formato da resposta (obrigatório):
Retorne apenas um JSON no seguinte formato:
[
  {
    "start": 0,
    "end": 540,
    "topic": "Descrição do assunto central deste corte"
  },
  ...
]

INPUT PARA A ANÁLISE:
{}
""".format()


from openai import OpenAI
import os
client = OpenAI(
    api_key="",
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input=prompt,
    model="openai/gpt-oss-20b",
)
print(response.output_text)