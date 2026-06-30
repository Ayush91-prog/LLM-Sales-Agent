import chainlit as cl
import httpx
import os

FASTAPI_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000/ai/chat"
)
 
 
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
 
    await cl.Message(
        content=(
            "Welcome to the **AI Sales Agent**!\n\n"
            "What can I help you with today?"
        )
    ).send()
 
 
@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history", [])
 
    history.append({
        "role": "user",
        "content": message.content
    })
 
    thinking_msg = cl.Message(content="")
    await thinking_msg.send()
 
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                FASTAPI_URL,
                json={
                    "message": message.content,
                    "history": history  
                },
                timeout=60
            )
 
            if response.status_code != 200:
                await thinking_msg.stream_token(
                    "Something went wrong on my end. Please try again in a moment."
                )
                await thinking_msg.update()
                return
 
            data = response.json()
            reply = data.get("response", "Sorry, I didn't get a response.")
 
            for chunk in reply:
                await thinking_msg.stream_token(chunk)
 
            await thinking_msg.update()
 
            history.append({
                "role": "assistant",
                "content": reply
            })
 
            if len(history) > 20:
                history = history[-20:]
 
            cl.user_session.set("history", history)
 
    except httpx.TimeoutException:
        await thinking_msg.stream_token(
            "The request timed out. The AI is taking too long to respond. "
            "Please try again."
        )
        await thinking_msg.update()
 
    except httpx.ConnectError:
        await thinking_msg.stream_token(
            "Can't connect to the backend. Make sure your FastAPI server is running:\n"
            "```\nuvicorn main:app --reload\n```"
        )
        await thinking_msg.update()
 
    except Exception as e:
        await thinking_msg.stream_token(
            f"Unexpected error: {str(e)}"
        )
        await thinking_msg.update()
 