from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from routers import *

app = FastAPI()

app.include_router(router_data)
app.include_router(router_quest)
app.include_router(router_home)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    # fallback for other HTTP errors if you want
    return HTMLResponse(
        content=f"<h1>{exc.status_code} Error</h1><p>{exc.detail}</p>",
        status_code=exc.status_code
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
