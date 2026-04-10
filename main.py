from fastapi import Request, HTTPException, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from db.migrations import creating_tables
from views.users import router as users_router
from views.posts import router as posts_router
from views.site import router as site_router

app = FastAPI()
app.include_router(site_router, prefix="", tags=["site"])
app.include_router(users_router, prefix="", tags=["users"])
app.include_router(posts_router, prefix="", tags=["posts"])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status_code": exc.status_code},
    )


if __name__ == "__main__":
    # 127.0.0.1
    # 0.0.0.0
    creating_tables()
    # test_posts()
    uvicorn.run("main:app", host="127.0.0.1", port=8657, reload=True)
