from sqlalchemy.orm import Session
from sqlalchemy import select, func
import random
from app.models.song import Song


def generate_questions(session: Session, num_questions=5) -> list:
    songs_result = session.execute(
        select(Song).order_by(func.random()).limit(num_questions)
    )
    songs = songs_result.scalars().all()

    questions = []
    for song in songs:
        correct_answer = song.title

        # Берём 3 случайных неверных названия
        wrong_songs_result = session.execute(
            select(Song.title).where(Song.id != song.id).order_by(func.random()).limit(3)
        )
        wrong_answers = wrong_songs_result.scalars().all()

        options = wrong_answers + [correct_answer]
        random.shuffle(options)

        correct_index = options.index(correct_answer)

        questions.append({
            "song_id": song.id,
            "clip_path": song.clip_path,
            "options": options,
            "correct": correct_index,
        })

    return questions
