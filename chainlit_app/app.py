import os
import time
from dotenv import load_dotenv

load_dotenv()

os.environ.pop("DATABASE_URL", None)

auth_secret = os.getenv("CHAINLIT_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY")
if not auth_secret:
    raise RuntimeError(
        "CHAILIT_AUTH_SECRET (or JWT_SECRET_KEY) environment variable is not configured."
    )
os.environ["CHAINLIT_AUTH_SECRET"] = auth_secret


import chainlit as cl
import httpx

FASTAPI_URL = os.getenv(
    "BACKEND_URL",
    os.getenv("LOCAL_BACKEND_URL", "http://127.0.0.1:8000/ai/chat")
)

AUTH_BASE_URL = FASTAPI_URL.replace("/ai/chat","")

SESSION_TIMEOUT_MINUTES = 120


@cl.password_auth_callback
async def auth_callback(username: str, password: str):
    """
    Authenticate against existing registered customers in Neon DB.
    STRICT AUTHENTICATION: NO auto-registration.
    Users must register via the Customer Portal first.
    """
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                f"{AUTH_BASE_URL}/auth/customer/login",
                json={"email":username.strip().lower(),"password":password},
                timeout = 15.0
            )
            if res.status_code == 200:
                data = res.json()
                token = data.get("access_token")

                me_res = await client.get(
                    f"{AUTH_BASE_URL}/auth/customer/me",
                    headers={"Authorization":f"Bearer {token}"},
                    timeout=15.0
                )

                if me_res.status_code == 200:
                    profile = me_res.json()
                    return cl.User(
                        identifier=profile["email"],
                        metadata={
                            "customer_id":profile["id"],
                            "name":profile["name"],
                            "email":profile["email"],
                            "phone":profile.get("phone",""),
                            "address":profile.get("address",""),
                            "login_timestamp":time.time(),
                            "token":token
                        }
                    )
                return None
        except Exception as e:
            print(f"Auth error: {e}")
            return None

 
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])

    user: cl.User = cl.user_session.get("user")
    if user and user.metadata:
        customer_name = user.metadata.get("name","Valued Customer")
        customer_id = user.metadata.get("customer_id")
        delivery_address = user.metadata.get("address") or "Not registered"

        cl.user_session.set("customer_id",customer_id)
        cl.user_session.set("customer_name",customer_name)
        cl.user_session.set("login_timestamp", user.metadata.get("login_timestamp",time.time()))

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
                "For your security, please refresh and log in again to continue placing orders."
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
 