import os
import chainlit as cl
import openai

# api_key = os.getenv("OPENAI_API_KEY")

api_key = os.getenv("RUNPOD_API_KEY")
runpod_serverless_id = os.getenv("RUNPOD_SERVERLESS_ID")

print(f"api_key: {api_key}")
print(f"runpod_serverless_id: {runpod_serverless_id}")

# endpoint_url = "https://api.openai.com/v1"
endpoint_url = f"https://api.runpod.ai/v2/{runpod_serverless_id}/openai/v1"

client = openai.AsyncClient(api_key=api_key, base_url=endpoint_url)

# https://platform.openai.com/docs/models/gpt-4o
# model_kwargs = {
#     "model": "chatgpt-4o-latest",
#     "temperature": 1.2,
#     "max_tokens": 500
# }

model_kwargs = {
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "temperature": 0.3,
    "max_tokens": 500
}

@cl.on_message
async def on_message(message: cl.Message):
    # Maintain an array of messages in the user session
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})

    response_message = cl.Message(content="")
    await response_message.send()
    
    # Pass in the full message history for each request
    stream = await client.chat.completions.create(messages=message_history, 
                                                  stream=True, **model_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    await response_message.update()

    # Record the AI's response in the history
    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)
        