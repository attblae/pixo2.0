import sqlite3
from consts import DB_LINK


def test_posts():
    URLS = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1rcs_XvkjaUyusP18Mw2Gm0qKenbA411a9Q&s",
        "https://static.vecteezy.com/vite/assets/photo-masthead-375-BoK_p8LG.webp",
        "https://media.istockphoto.com/id/1317323736/photo/a-view-up-into-the-trees-direction-sky.jpg?s=612x612&w=0&k=20&c=i4HYO7xhao7CkGy7Zc_8XSNX_iqG0vAwNsrH1ERmw2Q=",
        "https://img.freepik.com/free-photo/waterfall-chae-son-national-park-lampang-thailand_554837-639.jpg?semt=ais_user_personalization&w=740&q=80"
    ]
    for url in URLS:
        con = sqlite3.connect(DB_LINK)
        cursor = con.cursor()
        cursor.execute(
            """
                INSERT INTO posts(
                    user_id,
                    price,
                    description,
                    photo_url
                )
                values(
                    1,
                    100.50,
                    'какойц то арт для теста',
                    ?
                )
            """,
            (url,)
        )
        con.commit()
        con.close()

# if __name__ == "__main__":
#     con = sqlite3.connect(DB_LINK)
#     cursor = con.cursor()
#     s = cursor.execute("select * from basket_posts")
#     from pprint import pprint
#     pprint(s.fetchall())

print(4 * 555555555555555555 + 765)