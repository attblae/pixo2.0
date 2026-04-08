from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()

@router.get("/")
def main_page():
    return FileResponse("static/main.html")

@router.get("/support")
def support_page():
    return FileResponse("static/support.html")

@router.get("/about_us")
def about_us_page():
    return FileResponse("static/about_us.html")