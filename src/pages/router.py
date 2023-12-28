from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from operations.router import get_operation

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]

)

templates = Jinja2Templates(directory="templates")


@router.get("/base")
def page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/search/{operate}")
def search_page(request: Request, operations=Depends(get_operation)):
    return templates.TemplateResponse("search.html", {"request": request, "operations": operations["data"]})
