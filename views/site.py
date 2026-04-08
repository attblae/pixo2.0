from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()

@router.get("/")
def main_page():
    """
    Модель для перехода на главную страницу
    :return: FileResponse
    """
    return FileResponse("static/main.html")

@router.get("/support")
def support_page():
    """
    Модель для перехода на страницу подержки
    :return: FileResponse
    """
    return FileResponse("static/support.html")

@router.get("/about_us")
def about_us_page():
    """
    Модель для перехода на страницу с информацией о сайте и разработчике
    :return: FileResponse
    """
    return FileResponse("static/about_us.html")