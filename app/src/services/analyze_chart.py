import json
import os

from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from openai import OpenAI

from ..config import prompt_analysis

load_dotenv()


async def analyze_chart_stream(base64_image: str, model: str = "gpt-4o-mini", user: dict = None):
    if model == "gpt-4o-mini":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_MINI"))
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_4O"))

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": [
            {
            "type": "text",
            "text": prompt_analysis
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]}
        ],
        max_tokens=4096,
        response_format={"type": "json_object"},
        stream=True
    )

    async def event_generator():
        collected_messages = []
        for chunk in stream:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message is not None:
                collected_messages.append(chunk_message)
                yield f"data: {chunk_message}\n\n"
                print(chunk_message)
        
        full_reply_content = ''.join(collected_messages)
        yield f"data: {json.dumps({'full_response': json.loads(full_reply_content)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


async def analyze_chart_non_stream(base64_image: str, model: str = "gpt-4o-mini"):
    if model == "gpt-4o-mini":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_MINI"))
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_4O"))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": [
            {
            "type": "text",
            "text": prompt_analysis
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]}
        ],
        max_tokens=4096,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)