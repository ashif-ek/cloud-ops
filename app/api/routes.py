from fastapi import APIRouter, HTTPException, status

from app.db.database import check_database


router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to CloudOps Task Manager",
        "status": "running",
    }


@router.get("/health/live")
def liveness():
    return {"status": "alive"}


@router.get("/health/ready")
def readiness():
    try:
        check_database()

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "database": "unavailable",
            },
        )