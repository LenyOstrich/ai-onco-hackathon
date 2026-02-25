import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pprint import pprint

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("YANDEX_API_KEY"),
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=os.getenv("YANDEX_FOLDER_ID"),
)


async def call_agent(history_text: str, agent_id: str) -> dict:
    response = await client.responses.create(
        prompt={
            "id": agent_id,
        },
        input=history_text,
    )
    pprint(response)

    if response.error:
        return {"error": response.error.message}

    output_text = response.output_text

    output_text = (
        output_text.removeprefix("```")
        .removeprefix("json")
        .removesuffix("```")
    )

    return output_text
