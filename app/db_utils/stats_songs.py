from sqlalchemy.orm import Session
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
