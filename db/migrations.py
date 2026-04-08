import sqlite3
from consts import DB_LINK

def creating_tables():
    con = sqlite3.connect(DB_LINK)
    cursor = con.cursor()
    cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(30) UNIQUE,
                    password VARCHAR(255),
                    name VARCHAR(35),
                    surname VARCHAR(35),
                    patronymic VARCHAR(35),
                    phone VARCHAR(11) UNIQUE,
                    email VARCHAR(50) UNIQUE,
                    pasport VARCHAR(16) UNIQUE,
                    card VARCHAR(19) UNIQUE
                );
        """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    price DECIMAL(11, 2) not NULL,
                    description VARCHAR(20) NULL,
                    photo_url VARCHAR(100) not NULL UNIQUE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
        """
    )
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS basket_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                art_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (art_id) REFERENCES posts (id)
            )
        """
    )