prompt = """
Você é um especialista em analisar segmentos de falar de lives/videos longos de {0}

Cada segmento possui:
{{
    "text": "conteúdo falado",
    "start": "tempo inicial em segundos",
    "end": "tempo final em segundos",
}}

Sua tarefa é analisar todos os segmentos e identificar os melhores cortes temáticos para transformar a live em videos interessantes.

Regras:
1. Analise o contexto global e não apenas cada segmento isoladamente.
2. Agrupe segmentos consecutivos quando fizerem parte do mesmo tema.
3. Priorize momentos que:
   - explicam algo útil
   - contam uma história
   - têm opinião forte
   - contêm dicas práticas
   - geram curiosidade ou aprendizado
4. Ignore trechos inicios e fins que contenham:
   - pausas
   - cumprimentos ou despedidas
5. Cada corte deve ter entre {1} minutos e {2} minutos, se possível.
6. Os cortes devem ser coerentes, ou seja, não podem começar ou terminar no meio de uma ideia.
7. Priorize cortes que funcionariam bem para YouTube.

Para cada corte encontrado retorne um objeto com o seguinte formato:

{{
  "title": "título curto e chamativo, apelativo, citando nome do autor das falar quando possível, com foco em SEO pra youtube",
  "start": tempo_em_segundos,
  "end": tempo_em_segundos,
  "summary": "breve descrição do que foi tratado no trecho"
}}

Retorne uma lista JSON minificada com os melhores cortes.

Aqui estão os segmentos:

{3}
"""


description = """
{0}

👉 Quer saber mais? Acompanhe as lives do MBL, de segunda à sexta-feira no canal:    https://www.youtube.com/@MBLiveTV

👀 Vídeo original:    • {1}

Se gostou do vídeo, não se esqueça de deixar o like e se inscrever no canal 💪

Até a próxima e fique com Deus 🙏

#cortesmbl #partidomissao #mbl #renansantos #mamaefalei #kimkataguiri
"""