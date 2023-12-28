from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from operations.models import operation

from operations.schemas import Operation, OperationSchema


router = APIRouter(
    prefix="/operation",
    tags=["Operation"]

)

#@router.get("/")
@router.get("", response_model=OperationSchema)
async def get_operation(operate: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operate)
        print(query)
        res = await session.execute(query)
        return {"status": "success",
                "data": res.all(),
                "details": "None"}


    except Exception:
        raise HTTPException(status_code=500,detail={"status": "error",
                "data": None,
                'details': None})


@router.post("/")
async def set_operation(operate: Operation, session: AsyncSession = Depends(get_async_session)):
    # query = select(operation).where(operation.c.id==1)
    stmt = insert(operation).values(**operate.dict())
    # stmt = insert(operation).values(id=3,quantity='three',figi='for',instrument_type='del',type='del')
    print(stmt)
    # res = await session.execute(query)
    await session.execute(stmt)
    await session.commit()
    return "yes, data was inserted"
    # return "1"
