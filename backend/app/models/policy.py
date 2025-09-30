from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PolicyPack(Base):
    __tablename__ = "policy_packs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    version = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policy_tags = relationship("PolicyTag", back_populates="policy_pack", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PolicyPack(id={self.id}, name='{self.name}', version='{self.version}')>"

class PolicyTag(Base):
    __tablename__ = "policy_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    risk_level = Column(String(50), nullable=False)  # unacceptable, high, limited, minimal
    patterns = Column(JSON)  # List of patterns to match
    action = Column(String(50), nullable=False)  # block, flag, allow
    policy_pack_id = Column(Integer, ForeignKey("policy_packs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    policy_pack = relationship("PolicyPack", back_populates="policy_tags")
    
    def __repr__(self):
        return f"<PolicyTag(id={self.id}, name='{self.name}', risk_level='{self.risk_level}')>"
