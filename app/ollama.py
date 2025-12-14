import requests


def ask_llm_change(context: str, text_a: str, text_b: str) -> bool:
    prompt = f"""
Contexto geral:
{context}

Compare os dois blocos de transcrição abaixo. 

Critério:
- MESMO ASSUNTO: os blocos tratam do mesmo tema principal, mesmo que usem palavras diferentes.
- ASSUNTO DIFERENTE: os blocos tratam de tópicos independentes, sem relação direta.

Exemplos:
Bloco A: Falo sobre inflação e aumento de preços.
Bloco B: Falo sobre juros bancários e investimentos.
Resposta: SIM (mesmo assunto)

Bloco A: Falo sobre inflação e aumento de preços.
Bloco B: Falo sobre métodos de ensino e educação pública.
Resposta: NAO (assunto diferente)

Agora compare os blocos abaixo. Responda APENAS com SIM ou NAO.

Bloco A:
{text_a}

Bloco B:
{text_b}
"""





    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral:7b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 2
            }
        }
    )
    response = r.json()["response"]
    print(response)
    # return True if response == 'sim' else False
context = "Neste vídeo, o autor comenta sobre política, analisando decisões recentes do governo, impactos econômicos e a reação da população às medidas adotadas."
text_a = "Durante a conversa, o autor passa a falar sobre a inflação, explicando como o aumento dos preços afeta o poder de compra da população e o custo de vida no dia a dia."
text_b = "Em outro momento, ele muda o foco para a educação, criticando a qualidade do ensino público e a falta de investimento em infraestrutura e professores."
ask_llm_change(context, text_a, text_b)