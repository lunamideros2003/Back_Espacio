import json
import random

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_current_user_optional
from app.database import get_db
from app.models import QuizAttempt, QuizQuestion, User

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


class AnswerIn(BaseModel):
    id: int
    choice: int


class SubmitIn(BaseModel):
    answers: list[AnswerIn]
    level: str | None = None


@router.get("/generate")
def generate(
    level: str = Query("beginner"),
    count: int = Query(5),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    chosen = level or (user.level if user else "beginner")
    rows = db.query(QuizQuestion).filter(QuizQuestion.level.in_([chosen, "beginner"])).all()
    random.shuffle(rows)
    picked = rows[: min(10, max(1, count))]
    return {
        "level": chosen,
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "options": json.loads(q.options),
                "level": q.level,
            }
            for q in picked
        ],
    }


@router.post("/submit")
def submit(body: SubmitIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not body.answers:
        raise HTTPException(400, "Envía las respuestas del quiz")
    ids = [a.id for a in body.answers]
    db_qs = {q.id: q for q in db.query(QuizQuestion).filter(QuizQuestion.id.in_(ids)).all()}
    score = 0
    review = []
    for ans in body.answers:
        q = db_qs.get(ans.id)
        correct = bool(q and q.correct_index == ans.choice)
        if correct:
            score += 1
        review.append(
            {
                "id": ans.id,
                "question": q.question if q else None,
                "correct": correct,
                "correctIndex": q.correct_index if q else None,
                "explanation": q.explanation if q else None,
                "options": json.loads(q.options) if q else [],
            }
        )
    attempt = QuizAttempt(
        user_id=user.id,
        score=score,
        total=len(body.answers),
        level=body.level or user.level or "beginner",
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {
        "attempt": {
            "id": attempt.id,
            "score": attempt.score,
            "total": attempt.total,
            "level": attempt.level,
            "createdAt": attempt.created_at.isoformat(),
        },
        "score": score,
        "total": len(body.answers),
        "review": review,
    }


@router.get("/scores")
def scores(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.desc())
        .limit(20)
        .all()
    )
    best = 0.0
    for a in attempts:
        if a.total:
            best = max(best, a.score / a.total)
    return {
        "attempts": [
            {
                "id": a.id,
                "score": a.score,
                "total": a.total,
                "level": a.level,
                "createdAt": a.created_at.isoformat(),
            }
            for a in attempts
        ],
        "bestPercent": round(best * 100),
    }
