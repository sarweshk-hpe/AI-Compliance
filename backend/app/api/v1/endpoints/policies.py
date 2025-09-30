from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.services.policy_service import PolicyEngine
from app.schemas.policy import PolicyTagResponse, PolicyPackResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/tags", response_model=List[PolicyTagResponse])
async def get_policy_tags(db: Session = Depends(get_db)):
    """Get all available policy tags"""
    try:
        policy_engine = PolicyEngine()
        tags = policy_engine.get_policy_tags(db=db)
        return tags
    except Exception as e:
        logger.error(f"Failed to get policy tags: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/packs", response_model=List[PolicyPackResponse])
async def get_policy_packs(db: Session = Depends(get_db)):
    """Get all policy packs"""
    try:
        from app.models.policy import PolicyPack
        packs = db.query(PolicyPack).all()
        
        return [
            PolicyPackResponse(
                id=pack.id,
                name=pack.name,
                version=pack.version,
                description=pack.description,
                is_active=pack.is_active,
                created_at=pack.created_at,
                updated_at=pack.updated_at
            )
            for pack in packs
        ]
    except Exception as e:
        logger.error(f"Failed to get policy packs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
