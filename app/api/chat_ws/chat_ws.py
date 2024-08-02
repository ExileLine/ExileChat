# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:49
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : chat_ws.py
# @Software: PyCharm

from asyncio import sleep

from fastapi import APIRouter, WebSocket, Depends, status
from fastapi.responses import HTMLResponse

from common.libs.custom_exception import CustomException
from utils.ai.llm_engine import LLMEngine
from app.models.chat.models import Chat
from api_key import api_key

chat_ws_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id="messages">
        </ul>
        <div id="error-message" style="color: red;"></div>
        <script>
            const ws = new WebSocket("ws://0.0.0.0:7569/api/chat/ws/my_token/okc");
            ws.onmessage = function(event) {
                console.log("aaa")
                const messages = document.getElementById('messages');
                const message = document.createElement('li');
                const content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };

            ws.onclose = function(event) {
                if (event.code === 1008) { // WS_1008_POLICY_VIOLATION
                    console.log("123")
                    const errorMessage = document.getElementById('error-message');
                    errorMessage.textContent = 'Invalid token. Connection refused.';
                    alert("Invalid token. Connection refused.")
                }
            };

            function sendMessage(event) {
                const input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>

"""


@chat_ws_router.get("/")
async def get():
    return HTMLResponse(html)


async def check_user(token) -> dict | bool:
    """验证用户身份-例子"""

    user = {
        "id": 1,
        "username": "admin",
        "token": token
    }
    return user


async def get_chat(chat_id) -> bool:
    """获取对话历史记录"""

    query_chat = await Chat.get_or_none(id=chat_id)
    if not query_chat:
        return False

    # TODO 补充业务逻辑
    return True


@chat_ws_router.websocket("/chat")
async def chat(websocket: WebSocket):
    """对话"""

    await websocket.accept()

    query_params = websocket.query_params
    token = query_params.get("token")
    chat_id = query_params.get("chat_id", None)

    user = await check_user(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        print("鉴权验证失败 ws 关闭...")
        raise CustomException(status_code=403, detail="鉴权验证失败...", custom_code=10005)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"用户: {user} token: {token} 对话: {chat_id} 消息: {data}\n")

            llm_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)
            llm_engine.system_prompt = "你是一名Python专家"
            response_generator = llm_engine.chat(input=data)

            async for chunk in response_generator:
                if isinstance(chunk, str):
                    await sleep(0.1)
                    await websocket.send_text(chunk)
                else:
                    print(type(chunk), chunk)

            await websocket.close()
            break
    except Exception as e:
        print(f"WebSocket连接发生异常: {e}")
        await websocket.close()
