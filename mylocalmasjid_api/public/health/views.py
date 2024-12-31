from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import sentry_sdk

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.config.models import Config

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_session)):
    """
    Check the health of the API and its dependencies.
    Tests database connection and Sentry integration.
    """
    health_status = {
        "status": "healthy",
        "database": "healthy",
        "sentry": "healthy",
        "details": {}
    }
    
    # Check database connection
    try:
        # Try to execute a simple query
        db.exec(select(Config)).first()
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = "unhealthy"
        health_status["details"]["database_error"] = str(e)
    
    # Check Sentry
    try:
        client = sentry_sdk.Hub.current.client
        if not client:
            health_status["status"] = "unhealthy"
            health_status["sentry"] = "unhealthy"
            health_status["details"]["sentry_error"] = "Sentry client not initialized"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["sentry"] = "unhealthy"
        health_status["details"]["sentry_error"] = str(e)
    
    # If any component is unhealthy, return 503 Service Unavailable
    if health_status["status"] == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status
        )
    
    return health_status 