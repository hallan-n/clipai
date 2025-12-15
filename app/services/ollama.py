import requests
from logger import logger

def ask_ollama(prompt: str, params: list) -> bool:
    logger.info('Executando prompt junto ao Ollama AI.')
    prompt = prompt.format(*params)
    
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature":  0,
                "num_predict": 200
            }
        }
    )
    
    if r.status_code != 200:
        logger.error(f'Erro ao comunicar com Ollama AI: {r.json()["response"]}')
        raise ValueError(f'Erro ao comunicar com Ollama AI: {r.json()["response"]}')
    
    logger.info('Processamento finalizado.')
    return r.json()["response"]

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

Formato da resposta (OBRIGATÓRIO ser em formato JSON):
<abre chaves>
'nota': X  
'justificativa': 'no máximo 1 frase curta, citando o assunto de cada bloco.'
<fecha chaves>

Bloco A:
{0}

Bloco B:
{1}
"""