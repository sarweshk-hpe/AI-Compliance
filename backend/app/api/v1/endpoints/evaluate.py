from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.services.policy_service import PolicyEngine
from app.services.audit_service import AuditService
from app.schemas.evaluate import EvaluateRequest, EvaluateResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=EvaluateResponse)
async def evaluate_content(
    request: EvaluateRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluate content against EU AI Act compliance policies.
    
    This endpoint accepts text content and optionally an image file,
    evaluates them against configured policy rules, and returns a decision
    with audit trail information.
    """
    
    try:
        # Initialize services
        policy_engine = PolicyEngine()
        audit_service = AuditService()
        
        # Evaluate content
        evaluation_result = policy_engine.evaluate_content(
            db=db,
            text=request.input,
            image_data=None,  # TODO: Add image support
            client_id=request.client_id,
            user=request.user
        )
        
        # Create audit event
        audit_event = audit_service.create_audit_event(
            db=db,
            input_data=request.input,
            user=request.user,
            client_id=request.client_id,
            input_type=request.input_type,
            decision=evaluation_result["decision"],
            policy_tags=evaluation_result["policy_tags"],
            risk_level=evaluation_result["risk_level"],
            policy_version=evaluation_result["policy_version"],
            explanation=evaluation_result["explanation"],
            confidence_score=evaluation_result["confidence_score"],
            evidence=evaluation_result["evidence"]
        )
        
        # Return response
        return EvaluateResponse(
            decision=evaluation_result["decision"],
            policy_tags=evaluation_result["policy_tags"],
            risk_level=evaluation_result["risk_level"],
            audit_event_id=audit_event.event_id,
            explanation=evaluation_result["explanation"],
            confidence_score=evaluation_result["confidence_score"],
            policy_version=evaluation_result["policy_version"]
        )
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.post("/with-image", response_model=EvaluateResponse)
async def evaluate_content_with_image(
    text: str = Form(...),
    client_id: str = Form("default"),
    user: str = Form("anonymous"),
    input_type: str = Form("text"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Evaluate content with image upload support.
    
    This endpoint accepts text content and an image file,
    performs face detection on the image, and evaluates both
    against compliance policies.
    """
    
    try:
        # Initialize services
        policy_engine = PolicyEngine()
        audit_service = AuditService()
        
        # Read image data if provided
        image_data = None
        if image:
            image_data = await image.read()
        
        # Evaluate content
        evaluation_result = policy_engine.evaluate_content(
            db=db,
            text=text,
            image_data=image_data,
            client_id=client_id,
            user=user
        )
        
        # Create audit event
        audit_event = audit_service.create_audit_event(
            db=db,
            input_data=text,
            user=user,
            client_id=client_id,
            input_type="text_with_image" if image else "text",
            decision=evaluation_result["decision"],
            policy_tags=evaluation_result["policy_tags"],
            risk_level=evaluation_result["risk_level"],
            policy_version=evaluation_result["policy_version"],
            explanation=evaluation_result["explanation"],
            confidence_score=evaluation_result["confidence_score"],
            evidence=evaluation_result["evidence"]
        )
        
        # Return response
        return EvaluateResponse(
            decision=evaluation_result["decision"],
            policy_tags=evaluation_result["policy_tags"],
            risk_level=evaluation_result["risk_level"],
            audit_event_id=audit_event.event_id,
            explanation=evaluation_result["explanation"],
            confidence_score=evaluation_result["confidence_score"],
            policy_version=evaluation_result["policy_version"]
        )
        
    except Exception as e:
        logger.error(f"Evaluation with image failed: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the evaluation service"""
    return {"status": "healthy", "service": "content evaluation"}
