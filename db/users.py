import sqlite3
from consts import DB_LINK

class UserRepository:
    @classmethod
    def get_password_by_username(cls, username: str) -> str | None:
        """
        Метод для получения пороля полязователя по его нику
        :param username: str
        :return: str | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            hash_pass = cursor.execute(
                "SELECT password FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        return hash_pass[0] if hash_pass else None

    @classmethod
    def check_existing_of_username(cls, username: str) -> str | None:
        """
        Метод для проверки уникальности username, сравнивая его с тем username, который был введен
        :param username: str
        :return: str | None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            username = cursor.execute(
                "SELECT username FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        return username[0] if username else None

    @classmethod
    def create_user(
            cls,
            username: str,
            password: str,
            name: str,
            surname: str,
            patronymic: str,
            phone: str,
            email: str,
            pasport: str,
            card: str
    ):
        """
        Метод для создания пользователя и добавления всех его данных в таблицу users
        :param username: str
        :param password: str
        :param name: str
        :param surname: str
        :param patronymic: str
        :param phone: str
        :param email: str
        :param pasport: str
        :param card: str
        :return: None
        """
        with sqlite3.connect(DB_LINK, timeout=5) as con:
            cursor = con.cursor()
            cursor.execute(
                """
                    INSERT INTO users (
                    username, 
                    password, 
                    name, 
                    surname, 
                    patronymic,
                    phone, 
                    email, 
                    pasport,
                    card
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    username,
                    password,
                    name,
                    surname,
                    patronymic,
                    phone,
                    email,
                    pasport,
                    card
                )
            )
            con.commit()