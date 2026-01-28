from consts import OPENAI_API_KEY
from openai import OpenAI
from services.logger import logger


def ask_gpt(prompt: str, params: list) -> bool:
    logger.info("Executando prompt junto ao GPT AI.")
    prompt = prompt.format(*params)

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )
    response = response.to_dict()

    for value in response["output"]:
        if "content" in value.keys():
            for c in value["content"]:
                return c["text"]
