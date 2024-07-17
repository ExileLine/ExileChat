# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:49
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : chat_ws.py
# @Software: PyCharm


from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.responses import HTMLResponse

from common.libs.custom_exception import CustomException

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
            const ws = new WebSocket("ws://0.0.0.0:7569/api/chat/ws/my_token");
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


async def check_user(token):
    """验证用户身份-例子"""

    user = {
        "id": 1,
        "username": "admin",
        "token": token
    }
    return user


@chat_ws_router.websocket("/ws/{token}")
async def chat(websocket: WebSocket, user: dict = Depends(check_user)):
    """对话"""

    await websocket.accept()

    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        print("鉴权验证失败 ws 关闭...")
        raise CustomException(status_code=404, detail="鉴权验证失败...", custom_code=10005)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"用户: {user} 消息: {data}")

    except WebSocketDisconnect:
        print("客户端断开连接")
        await websocket.close()
