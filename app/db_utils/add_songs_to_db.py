import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")
CLIPS_FOLDER = os.path.join(BASE_DIR, "clips")


def add_songs_to_db():
    """
    Сканирует папку с mp3 файлами и добавляет записи о песнях в базу данных SQLite.
    Формат имени файла должен быть "Artist - Title.mp3" или просто "Title.mp3".
    Вставляет относительный путь к аудиофайлу в поле clip_path.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for filename in os.listdir(CLIPS_FOLDER):
        if filename.lower().endswith(".mp3"):
            clip_path = os.path.join("clips", filename)  # относительный путь
            name = filename.rsplit(".", 1)[0]

            if " - " in name:
                artist, title = name.split(" - ", 1)
            else:
                artist, title = None, name

            cursor.execute("""
            INSERT INTO songs (title, artist, category, year, clip_path)
            VALUES (?, ?, ?, ?, ?)
            """, (title, artist, None, None, clip_path))

    conn.commit()
    conn.close()
    print("✅ Песни успешно добавлены в базу данных!")


if __name__ == "__main__":
    add_songs_to_db()
