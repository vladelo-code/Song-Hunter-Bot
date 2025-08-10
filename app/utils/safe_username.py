from app.messages.texts import NO_USERNAME_USER


def get_safe_username(username: str | None) -> str:
    return username or NO_USERNAME_USER
