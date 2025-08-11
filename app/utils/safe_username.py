from app.messages.texts import NO_USERNAME_USER


def get_safe_username(username: str | None) -> str:
    """
    Возвращает безопасное отображение имени пользователя.
    Если username равен None или пустой строке, возвращает значение по умолчанию.

    :param username: Имя пользователя или None.
    :return: Имя пользователя или строка-заглушка, если username отсутствует.
    """
    return username or NO_USERNAME_USER
