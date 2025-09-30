from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.services.audit_service import AuditService
from app.schemas.audit import AuditEventResponse, AuditOverrideRequest, AuditOverrideResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/events", response_model=List[AuditEventResponse])
async def get_audit_events(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    decision: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    user: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get audit events with optional filtering"""
    try:
        audit_service = AuditService()
        events = audit_service.get_audit_events(
            db=db,
            limit=limit,
            offset=offset,
            decision=decision,
            risk_level=risk_level,
            user=user
        )
        
        return [
            AuditEventResponse(
                event_id=event.event_id,
                timestamp=event.timestamp,
                user=event.user,
                client_id=event.client_id,
                input_type=event.input_type,
                decision=event.decision,
                policy_tags=event.policy_tags or [],
                risk_level=event.risk_level,
                policy_version=event.policy_version,
                explanation=event.explanation,
                confidence_score=event.confidence_score,
                signature=event.signature
            )
            for event in events
        ]
    except Exception as e:
        logger.error(f"Failed to get audit events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}", response_model=AuditEventResponse)
async def get_audit_event(event_id: str, db: Session = Depends(get_db)):
    """Get a specific audit event by ID"""
    try:
        audit_service = AuditService()
        event = audit_service.get_audit_event(db=db, event_id=event_id)
        
        if not event:
            raise HTTPException(status_code=404, detail="Audit event not found")
        
        return AuditEventResponse(
            event_id=event.event_id,
            timestamp=event.timestamp,
            user=event.user,
            client_id=event.client_id,
            input_type=event.input_type,
            decision=event.decision,
            policy_tags=event.policy_tags or [],
            risk_level=event.risk_level,
            policy_version=event.policy_version,
            explanation=event.explanation,
            confidence_score=event.confidence_score,
            signature=event.signature
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get audit event {event_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events/{event_id}/override", response_model=AuditOverrideResponse)
async def create_override(
    event_id: str,
    override_request: AuditOverrideRequest,
    db: Session = Depends(get_db)
):
    """Create an override for an audit event"""
    try:
        audit_service = AuditService()
        override = audit_service.create_override(
            db=db,
            original_event_id=event_id,
            operator=override_request.operator,
            reason=override_request.reason,
            new_decision=override_request.new_decision,
            duration=override_request.duration
        )
        
        return AuditOverrideResponse(
            override_id=override.override_id,
            original_event_id=override.original_event_id,
            timestamp=override.timestamp,
            operator=override.operator,
            reason=override.reason,
            new_decision=override.new_decision,
            duration=override.duration,
            signature=override.signature
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create override for event {event_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}/overrides", response_model=List[AuditOverrideResponse])
async def get_event_overrides(event_id: str, db: Session = Depends(get_db)):
    """Get all overrides for a specific audit event"""
    try:
        audit_service = AuditService()
        overrides = audit_service.get_overrides_for_event(db=db, event_id=event_id)
        
        return [
            AuditOverrideResponse(
                override_id=ovr.override_id,
                original_event_id=ovr.original_event_id,
                timestamp=ovr.timestamp,
                operator=ovr.operator,
                reason=ovr.reason,
                new_decision=ovr.new_decision,
                duration=ovr.duration,
                signature=ovr.signature
            )
            for ovr in overrides
        ]
    except Exception as e:
        logger.error(f"Failed to get overrides for event {event_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{event_id}")
async def export_audit_bundle(event_id: str, db: Session = Depends(get_db)):
    """Export complete audit bundle for external auditors"""
    try:
        audit_service = AuditService()
        bundle = audit_service.export_audit_bundle(db=db, event_id=event_id)
        return bundle
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to export audit bundle for event {event_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
