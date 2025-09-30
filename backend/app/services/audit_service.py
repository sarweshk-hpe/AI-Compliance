from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditEvent, AuditOverride
from app.core.security import create_hmac_signature, hash_input
from app.services.storage_service import StorageService
import uuid
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AuditService:
    def __init__(self):
        """Initialize audit service with storage service"""
        self.storage_service = StorageService()
    
    def create_audit_event(
        self,
        db: Session,
        input_data: str,
        user: str,
        client_id: str,
        input_type: str,
        decision: str,
        policy_tags: List[str],
        risk_level: str,
        policy_version: str,
        explanation: str,
        confidence_score: int,
        evidence: Dict
    ) -> AuditEvent:
        """Create an immutable audit event with HMAC signature"""
        
        # Generate unique event ID
        event_id = f"evt-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Hash the input data
        input_hash = hash_input(input_data)
        
        # Store evidence in object storage
        evidence_refs = self._store_evidence(event_id, evidence)
        
        # Create audit event data for signing
        event_data = {
            "event_id": event_id,
            "timestamp": datetime.now().isoformat(),
            "input_hash": input_hash,
            "user": user,
            "client_id": client_id,
            "decision": decision,
            "policy_tags": policy_tags,
            "risk_level": risk_level,
            "policy_version": policy_version
        }
        
        # Create HMAC signature
        signature_data = json.dumps(event_data, sort_keys=True)
        signature = create_hmac_signature(signature_data)
        
        # Create audit event
        audit_event = AuditEvent(
            event_id=event_id,
            input_hash=input_hash,
            user=user,
            client_id=client_id,
            input_type=input_type,
            decision=decision,
            policy_tags=policy_tags,
            risk_level=risk_level,
            evidence_refs=evidence_refs,
            policy_version=policy_version,
            signature=signature,
            explanation=explanation,
            confidence_score=confidence_score
        )
        
        db.add(audit_event)
        db.commit()
        db.refresh(audit_event)
        
        logger.info(f"Created audit event {event_id} with decision {decision}")
        return audit_event
    
    def create_override(
        self,
        db: Session,
        original_event_id: str,
        operator: str,
        reason: str,
        new_decision: str,
        duration: Optional[int] = None
    ) -> AuditOverride:
        """Create an audit override event"""
        
        # Verify original event exists
        original_event = db.query(AuditEvent).filter(AuditEvent.event_id == original_event_id).first()
        if not original_event:
            raise ValueError(f"Original audit event {original_event_id} not found")
        
        # Generate override ID
        override_id = f"ovr-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Create override data for signing
        override_data = {
            "override_id": override_id,
            "original_event_id": original_event_id,
            "timestamp": datetime.now().isoformat(),
            "operator": operator,
            "new_decision": new_decision,
            "reason": reason,
            "duration": duration
        }
        
        # Create HMAC signature
        signature_data = json.dumps(override_data, sort_keys=True)
        signature = create_hmac_signature(signature_data)
        
        # Create override event
        override = AuditOverride(
            override_id=override_id,
            original_event_id=original_event_id,
            operator=operator,
            reason=reason,
            new_decision=new_decision,
            duration=duration,
            signature=signature
        )
        
        db.add(override)
        db.commit()
        db.refresh(override)
        
        logger.info(f"Created override {override_id} for event {original_event_id}")
        return override
    
    def get_audit_event(self, db: Session, event_id: str) -> Optional[AuditEvent]:
        """Get audit event by ID"""
        return db.query(AuditEvent).filter(AuditEvent.event_id == event_id).first()
    
    def get_audit_events(
        self,
        db: Session,
        limit: int = 100,
        offset: int = 0,
        decision: Optional[str] = None,
        risk_level: Optional[str] = None,
        user: Optional[str] = None
    ) -> List[AuditEvent]:
        """Get audit events with filtering"""
        query = db.query(AuditEvent)
        
        if decision:
            query = query.filter(AuditEvent.decision == decision)
        
        if risk_level:
            query = query.filter(AuditEvent.risk_level == risk_level)
        
        if user:
            query = query.filter(AuditEvent.user == user)
        
        return query.order_by(AuditEvent.timestamp.desc()).offset(offset).limit(limit).all()
    
    def get_overrides_for_event(self, db: Session, event_id: str) -> List[AuditOverride]:
        """Get all overrides for a specific audit event"""
        return db.query(AuditOverride).filter(AuditOverride.original_event_id == event_id).all()
    
    def export_audit_bundle(self, db: Session, event_id: str) -> Dict:
        """Export complete audit bundle for external auditors"""
        audit_event = self.get_audit_event(db, event_id)
        if not audit_event:
            raise ValueError(f"Audit event {event_id} not found")
        
        # Get overrides
        overrides = self.get_overrides_for_event(db, event_id)
        
        # Create export bundle
        bundle = {
            "audit_event": {
                "event_id": audit_event.event_id,
                "timestamp": audit_event.timestamp.isoformat(),
                "input_hash": audit_event.input_hash,
                "user": audit_event.user,
                "client_id": audit_event.client_id,
                "input_type": audit_event.input_type,
                "decision": audit_event.decision,
                "policy_tags": audit_event.policy_tags,
                "risk_level": audit_event.risk_level,
                "policy_version": audit_event.policy_version,
                "explanation": audit_event.explanation,
                "confidence_score": audit_event.confidence_score,
                "signature": audit_event.signature
            },
            "overrides": [
                {
                    "override_id": ovr.override_id,
                    "timestamp": ovr.timestamp.isoformat(),
                    "operator": ovr.operator,
                    "reason": ovr.reason,
                    "new_decision": ovr.new_decision,
                    "duration": ovr.duration,
                    "signature": ovr.signature
                }
                for ovr in overrides
            ],
            "export_metadata": {
                "exported_at": datetime.now().isoformat(),
                "export_version": "1.0",
                "compliance_framework": "EU AI Act"
            }
        }
        
        return bundle
    
    def _store_evidence(self, event_id: str, evidence: Dict) -> List[str]:
        """Store evidence in object storage and return references"""
        evidence_refs = []
        
        try:
            # Store text patterns evidence
            if 'text_patterns' in evidence:
                text_evidence_path = f"evidence/{event_id}/text_patterns.json"
                self.storage_service.store_json(text_evidence_path, evidence['text_patterns'])
                evidence_refs.append(f"s3://{text_evidence_path}")
            
            # Store image patterns evidence
            if 'image_patterns' in evidence and evidence['image_patterns']:
                image_evidence_path = f"evidence/{event_id}/image_patterns.json"
                self.storage_service.store_json(image_evidence_path, evidence['image_patterns'])
                evidence_refs.append(f"s3://{image_evidence_path}")
            
        except Exception as e:
            logger.error(f"Failed to store evidence for event {event_id}: {e}")
            evidence_refs.append("evidence_storage_failed")
        
        return evidence_refs
