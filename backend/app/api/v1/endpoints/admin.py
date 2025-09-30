from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def admin_health_check():
    """Admin health check endpoint"""
    return {
        "status": "healthy",
        "service": "admin",
        "version": "1.0.0"
    }

@router.get("/stats")
async def get_system_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        from app.models.audit import AuditEvent
        from app.models.policy import PolicyPack, PolicyTag
        
        # Count audit events by decision
        total_events = db.query(AuditEvent).count()
        blocked_events = db.query(AuditEvent).filter(AuditEvent.decision == "block").count()
        flagged_events = db.query(AuditEvent).filter(AuditEvent.decision == "flag").count()
        allowed_events = db.query(AuditEvent).filter(AuditEvent.decision == "allow").count()
        
        # Count policy packs and tags
        total_packs = db.query(PolicyPack).count()
        active_packs = db.query(PolicyPack).filter(PolicyPack.is_active == True).count()
        total_tags = db.query(PolicyTag).count()
        
        return {
            "audit_events": {
                "total": total_events,
                "blocked": blocked_events,
                "flagged": flagged_events,
                "allowed": allowed_events
            },
            "policies": {
                "total_packs": total_packs,
                "active_packs": active_packs,
                "total_tags": total_tags
            }
        }
    except Exception as e:
        logger.error(f"Failed to get system stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
