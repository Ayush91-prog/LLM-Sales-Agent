import os
import time
import asyncio
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

os.environ.pop("DATABASE_URL", None)

import chainlit as cl
import httpx

raw_backend_url = os.getenv("BACKEND_URL") or os.getenv("LOCAL_BACKEND_URL") or "http://127.0.0.1:8000"
clean_url = raw_backend_url.rstrip("/")
if clean_url.endswith("/ai/chat"):
    AUTH_BASE_URL = clean_url[:-len("/ai/chat")]
    FASTAPI_URL = clean_url
else:
    AUTH_BASE_URL = clean_url
    FASTAPI_URL = f"{clean_url}/ai/chat"

PORTAL_URL = os.getenv("FRONTEND_PORTAL_URL", "https://ai-sales-marketplace-portal.onrender.com/customer_login.html")
SESSION_TIMEOUT_MINUTES = 120
 
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])

    customer_id = None
    customer_name = None
    delivery_address = None
    
    try:
        copilot_fn = getattr(cl, "CopilotFunction", None)
        if copilot_fn:
            res = await asyncio.wait_for(
                copilot_fn(name="get_customer_params", args={}).acall(),
                timeout=1.5
            )
            if isinstance(res, dict):
                cid_val = res.get("customer_id")
                if cid_val:
                    try:
                        customer_id = int(cid_val)
                    except (ValueError, TypeError):
                        customer_id = None
                customer_name = res.get("name")
                delivery_address = res.get("address")
    except Exception:
        pass


    if not customer_id or not customer_name:
        environ = getattr(cl.context.session, "environ", {}) or {}
        candidates = []

        raw_query = environ.get("QUERY_STRING", "")
        if raw_query and "customer_id" in raw_query:
            candidates.append(raw_query)

        session_referer = cl.user_session.get("http_referer") or ""
        if session_referer and "customer_id" in session_referer:
            candidates.append(session_referer)

        environ_referer = environ.get("HTTP_REFERER", "")
        if environ_referer and "customer_id" in environ_referer:
            candidates.append(environ_referer)

        scope = environ.get("asgi.scope", {})
        for header_name, header_val in scope.get("headers", []):
            if header_name.lower() == b"referer":
                ref_str = header_val.decode("utf-8", errors="ignore")
                if "customer_id" in ref_str:
                    candidates.append(ref_str)

        for candidate in candidates:
            query_str = candidate.split("?", 1)[1] if "?" in candidate else candidate
            parsed = urllib.parse.parse_qs(query_str)
            if "customer_id" in parsed and not customer_id:
                try:
                    customer_id = int(parsed["customer_id"][0])
                except (ValueError, IndexError):
                    pass
            if "name" in parsed and not customer_name:
                customer_name = parsed["name"][0]
            if "address" in parsed and not delivery_address:
                delivery_address = parsed["address"][0]
            if customer_id and customer_name:
                break

    if customer_id and customer_name:
        cl.user_session.set("customer_id",customer_id)
        cl.user_session.set("customer_name",customer_name)
        cl.user_session.set("customer_address",delivery_address)
        cl.user_session.set("login_timestamp",time.time())

        welcome_msg = (
            f"Hello **{customer_name}**! Welcome back to the **AI Marketplace**!\n\n"
            f"**Delivery Address:** {delivery_address}\n\n"
            "I can help you browse products across our verified sellers, "
            "negotiate policy discounts, and ship orders directly to your address.\n\n"
            "What can I help you find today? *(e.g. 'Show me electronics' or 'I need groceries')*"
        )
    else:
        welcome_msg = (
            "**Welcome to the AI Marketplace!**\n\n"
            "*(You are browsing as a guest. To place orders, please log in with your registered customer account.)*\n\n"
            "What products are you looking for today?"
        )
    await cl.Message(content=welcome_msg).send()
 
 
@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history", [])
    customer_id = cl.user_session.get("customer_id")
    login_time = cl.user_session.get("login_timestamp")

    if login_time:
        elapsed_minutes = (time.time() - login_time) / 60.0
        if elapsed_minutes > SESSION_TIMEOUT_MINUTES:
            cl.user_session.set("customer_id", None)
            cl.user_session.set("login_timestamp", None)
            customer_id = None

            await cl.Message(
                content = " ** Your login session has expired .** \n\n"
                f"For your security, please [**click here to log in again**]({PORTAL_URL}) to place orders."
            ).send()
            return
        

    history.append({
        "role": "user",
        "content": message.content
    })
 
    thinking_msg = cl.Message(content="")
    await thinking_msg.send()
 
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "message":message.content,
                "history":history
            }
            if customer_id:
                payload["customer_id"] = customer_id

            response = await client.post(
                FASTAPI_URL,
                json=payload,
                timeout=120.0
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
            "Can't connect to the backend. Make sure the backend is active."
        )
        await thinking_msg.update()
 
    except Exception as e:
        await thinking_msg.stream_token(
            f"Unexpected error: {str(e)}"
        )
        await thinking_msg.update()
 