from celery import Celery
from fastapi import APIRouter, Depends, BackgroundTasks

from auth.local_config import current_user

from tasks.tasks import sent_email

router = APIRouter(
    prefix="/celery")


@router.get("/data-long")
def data_long(user=Depends(current_user)):
    #back_tasks.add_task(sent_email,user.username)
    sent_email.delay(user.username)
    return {"success": 200,
            "data": "письмо отправлено",
            "details": None}
