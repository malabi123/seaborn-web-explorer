from fastapi import APIRouter, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.data_utils import *
from typing import List


router = APIRouter(prefix="/data")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(
    request: Request,
    selected_columns: List[str] = Query([]),
    filtered_column: str | None = None,
    operation: str | None = None,
    number: str | None = None
):
    columns, filter_columns = get_columns()
    html, selected_columns, filtered_column, operation, number, errors = a1(
        selected_columns, filtered_column, operation, number)
    return templates.TemplateResponse('data.html', {
        'request': request,
        'table': html,
        'columns': columns,
        'selected_columns': selected_columns,
        'filter_columns': filter_columns,
        'operations': OPERATIONS,
        'filtered_column': filtered_column,
        'operation': operation,
        'number': number,
        'errors': errors,
    })
