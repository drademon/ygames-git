from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.models import Message

from database import async_session_maker

from database import get_async_session

router = APIRouter()



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, bol: bool):
        if bol:
            await self.insert_mess(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    async def insert_mess(self, mess: str):
        async with async_session_maker() as session:
            stmt=insert(Message).values(user_id=mess, message=mess)
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()
templates = Jinja2Templates(directory="templates")


@router.get("/chat")
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html",{"request": request})


@router.get("/mess")
async def get_message(session: AsyncSession = Depends(get_async_session)):
    query=select(Message).order_by(Message.id.desc()).limit(7)
    res=await session.execute(query)
    all_messages = res.all()
    list_messages=[i[0].as_dict() for i in all_messages]
    return list_messages


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", False)

#@router.post("/")
# async def set_operation(operate: Operation, session: AsyncSession = Depends(get_async_session)):
#     # query = select(operation).where(operation.c.id==1)
#     stmt = insert(operation).values(**operate.dict())
#     # stmt = insert(operation).values(id=3,quantity='three',figi='for',instrument_type='del',type='del')
#     print(stmt)
#     # res = await session.execute(query)
#     await session.execute(stmt)
#     await session.commit()
#     return "yes, data was inserted"
#     # return "1"