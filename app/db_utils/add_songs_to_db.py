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

    added = 0  # счетчик добавленных записей

    for filename in os.listdir(CLIPS_FOLDER):
        if filename.lower().endswith(".mp3"):
            clip_path = os.path.join("clips", filename)
            name = filename.rsplit(".", 1)[0]

            if " - " in name:
                artist, title = name.split(" - ", 1)
            else:
                artist, title = None, name

            cursor.execute("SELECT id FROM songs WHERE clip_path = ?", (clip_path,))
            if cursor.fetchone() is None:
                cursor.execute("""
                    INSERT INTO songs (title, artist, category, year, clip_path)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, artist, None, None, clip_path))
                added += 1
            else:
                print(f"Пропускаем {clip_path}, запись уже есть в базе.")

    conn.commit()
    conn.close()

    if added > 0:
        print(f"✅ Обновление базы данных завершено! Добавлено записей: {added}")


if __name__ == "__main__":
    add_songs_to_db()
