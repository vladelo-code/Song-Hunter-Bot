from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Song
from app.models.song_stat import SongStat


def get_or_create_song_stats(session: Session, song_id: int) -> SongStat:
    stats = session.query(SongStat).filter_by(song_id=song_id).first()
    if not stats:
        stats = SongStat(song_id=song_id, times_played=0, correct_count=0, wrong_count=0)
        session.add(stats)
        session.commit()
        session.refresh(stats)
    return stats


def update_song_stats(session: Session, song_id: int, correct: bool) -> None:
    stats = get_or_create_song_stats(session, song_id)
    stats.times_played += 1
    if correct:
        stats.correct_count += 1
    else:
        stats.wrong_count += 1
    session.commit()


def get_most_guessed_songs(session: Session, limit: int = 10, min_plays: int = 0) -> list[SongStat]:
    query = (
        session.query(SongStat, Song)
        .join(Song, Song.id == SongStat.song_id)
        .filter(SongStat.times_played >= min_plays)
        .order_by(desc(SongStat.correct_count / SongStat.times_played))
        .limit(limit)
    )
    return query.all()
