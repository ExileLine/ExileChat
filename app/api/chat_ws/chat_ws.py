# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:49
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : chat_ws.py
# @Software: PyCharm


from fastapi import APIRouter, WebSocket, Depends, status
from fastapi.responses import HTMLResponse

from common.libs.custom_exception import CustomException
from utils.ai.llm_engine import LLMEngine
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


async def check_chat(chat_id) -> bool:
    """验证对话"""

    return True


@chat_ws_router.websocket("/{token}/{chat_id}")
async def chat(websocket: WebSocket, token: str, chat_id: str, user: dict = Depends(check_user)):
    """对话"""

    await websocket.accept()

    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        print("鉴权验证失败 ws 关闭...")
        raise CustomException(status_code=403, detail="鉴权验证失败...", custom_code=10005)

    try:
        # 测试代码
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"chat_id: {chat_id} 用户: {user} token: {token} 消息: {data}")

            # 测试代码
            llm_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)
            llm_engine.system_prompt = "你是一名Python专家"
            response_generator = llm_engine.chat(input="Python是什么时候诞生的")

            async for chunk in response_generator:
                if isinstance(chunk, str):
                    await websocket.send_text(chunk)
                else:
                    print(type(chunk), chunk)

            await websocket.close()
            break
    except Exception as e:
        print(f"WebSocket连接发生异常: {e}")
        await websocket.close()
