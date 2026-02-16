from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.question_utils import *

router = APIRouter(prefix="/questions")
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def questions_page(
        request: Request,
        q: str | None = ''):
    info = questions_info()
    answer, number, errors = a1(q, len(info))

    return templates.TemplateResponse("questions.html", {
        "request": request,
        "questions_info": info,
        'answer': answer,
        "number": number,
        "errors": errors,


    })
