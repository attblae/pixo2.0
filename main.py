from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
 
app = FastAPI()

@app.get("/")
def main_page():
    return FileResponse("static/main.html")

@app.get("/create")
def create_page():
    return FileResponse("static/create.html")

@app.get("/login")
def login_page():
    return FileResponse("static/login.html")

@app.get("/account")
def account_page():
    return FileResponse("static/account.html")

@app.get("/backet")
def backet_page():
    return FileResponse("static/backet.html")

@app.get("/catalog")
def catalog_page():
    return FileResponse("static/catalog.html")

@app.get("/support")
def support_page():
    return FileResponse("static/support.html")

@app.get("/about_us")
def about_us_page():
    return FileResponse("static/about_us.html")

if __name__ == "__main__":
    # 127.0.0.1
    # 0.0.0.0
    # con = sqlite3.connect("static/database.db")
    # cursor = con.cursor()
    # create_tables(con, cursor)
    # con.commit()
    # con.close()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8657,
        reload=True
    )