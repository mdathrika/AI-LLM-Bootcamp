import os
import chainlit as cl
import openai

api_key = os.getenv("OPENAI_API_KEY")

endpoint_url = "https://api.openai.com/v1"
client = openai.AsyncClient(api_key=api_key, base_url=endpoint_url)

# https://platform.openai.com/docs/models/gpt-4o
model_kwargs = {
    "model": "chatgpt-4o-latest",
    "temperature": 1.2,
    "max_tokens": 1000
}

@cl.on_message
async def on_message(message: cl.Message):
    # Your custom logic goes here...
    print(f"Received message: {message.content}")

    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": message.content}],
        **model_kwargs
    )
    # https://platform.openai.com/docs/guides/chat-completions/response-format
    response_content = response.choices[0].message.content

    await cl.Message(
        content=response_content,
    ).send()
        