from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, LargeBinary
from sqlalchemy.sql import func
from app.core.database import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(255), unique=True, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    input_hash = Column(String(255), nullable=False)  # SHA256 hash of input
    user = Column(String(255), nullable=False)
    client_id = Column(String(255), nullable=False)
    input_type = Column(String(50), nullable=False)  # text, image, file
    decision = Column(String(50), nullable=False)  # allow, flag, block
    policy_tags = Column(JSON)  # List of triggered policy tags
    risk_level = Column(String(50))  # unacceptable, high, limited, minimal
    evidence_refs = Column(JSON)  # List of evidence file references
    policy_version = Column(String(100), nullable=False)
    signature = Column(String(255), nullable=False)  # HMAC signature
    explanation = Column(Text)  # Human-readable explanation
    confidence_score = Column(Integer)  # 0-100 confidence in decision
    
    def __repr__(self):
        return f"<AuditEvent(event_id='{self.event_id}', decision='{self.decision}')>"

class AuditOverride(Base):
    __tablename__ = "audit_overrides"
    
    id = Column(Integer, primary_key=True, index=True)
    override_id = Column(String(255), unique=True, nullable=False, index=True)
    original_event_id = Column(String(255), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    operator = Column(String(255), nullable=False)  # Who performed the override
    reason = Column(Text, nullable=False)
    new_decision = Column(String(50), nullable=False)  # New decision after override
    duration = Column(Integer)  # Override duration in minutes (null = permanent)
    signature = Column(String(255), nullable=False)  # HMAC signature
    
    def __repr__(self):
        return f"<AuditOverride(override_id='{self.override_id}', operator='{self.operator}')>"
