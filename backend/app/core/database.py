from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(settings.database_url)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Initialize default data
        await init_default_data()
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def init_default_data():
    """Initialize default policy data"""
    try:
        from app.services.policy_service import PolicyEngine
        from app.models.policy import PolicyPack, PolicyTag
        
        db = SessionLocal()
        
        # Check if default policy pack exists
        existing_pack = db.query(PolicyPack).filter(PolicyPack.name == "EU AI Act Compliance").first()
        if not existing_pack:
            # Create default policy pack
            default_pack = PolicyPack(
                name="EU AI Act Compliance",
                version="pack-2025-01-01-v1",
                description="Default policy pack for EU AI Act compliance",
                is_active=True
            )
            db.add(default_pack)
            db.commit()
            db.refresh(default_pack)
            
            # Create default policy tags
            default_tags = [
                PolicyTag(
                    name="ProhibitedBiometric",
                    description="Real-time remote biometric identification & untargeted facial-database collection",
                    risk_level="unacceptable",
                    patterns=["biometric", "facial", "identification", "face recognition"],
                    action="block",
                    policy_pack_id=default_pack.id
                ),
                PolicyTag(
                    name="HighRiskAI",
                    description="High-risk AI systems requiring additional controls",
                    risk_level="high",
                    patterns=["high risk", "critical infrastructure", "safety", "healthcare"],
                    action="flag",
                    policy_pack_id=default_pack.id
                ),
                PolicyTag(
                    name="LimitedRiskAI",
                    description="Limited risk AI systems with transparency obligations",
                    risk_level="limited",
                    patterns=["limited risk", "transparency", "disclosure"],
                    action="flag",
                    policy_pack_id=default_pack.id
                )
            ]
            
            for tag in default_tags:
                db.add(tag)
            
            db.commit()
            logger.info("Default policy data initialized successfully")
        
        db.close()
        
    except Exception as e:
        logger.error(f"Failed to initialize default data: {e}")
        raise
