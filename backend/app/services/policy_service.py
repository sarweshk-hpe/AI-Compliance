from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.policy import PolicyPack, PolicyTag
from app.services.pattern_detector import PatternDetector
from app.services.ai_compliance_analyzer import AIComplianceAnalyzer
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class PolicyEngine:
    def __init__(self):
        """Initialize policy engine with pattern detector and AI analyzer"""
        self.pattern_detector = PatternDetector()
        
        # Initialize AI compliance analyzer if enabled
        self.ai_analyzer = None
        if settings.ai_enabled and settings.nvidia_ai_api_key:
            try:
                self.ai_analyzer = AIComplianceAnalyzer(settings.nvidia_ai_api_key)
                logger.info("AI compliance analyzer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI analyzer: {e}")
    
    def evaluate_content(
        self, 
        db: Session, 
        text: str, 
        image_data: Optional[bytes] = None,
        client_id: str = "default",
        user: str = "anonymous"
    ) -> Dict:
        """Evaluate content against active policy rules using AI and traditional methods"""
        
        # Traditional pattern detection
        text_results = self.pattern_detector.detect_text_patterns(text)
        
        # Image analysis
        image_results = None
        if image_data:
            image_results = self.pattern_detector.detect_faces_in_image(image_data)
        
        # AI-powered compliance analysis
        ai_analysis = None
        if self.ai_analyzer:
            try:
                # Prepare context for AI analysis
                context = f"Client: {client_id}, User: {user}"
                if image_results and image_results.get('faces_detected', 0) > 0:
                    context += f", Faces detected: {image_results['faces_detected']}"
                
                ai_analysis = self.ai_analyzer.analyze_content(
                    content=text,
                    content_type="text_with_image" if image_data else "text",
                    context=context
                )
                logger.info(f"AI analysis completed: {ai_analysis.decision if ai_analysis else 'failed'}")
            except Exception as e:
                logger.error(f"AI analysis failed: {e}")
        
        # Combine traditional and AI analysis
        final_result = self._combine_analysis_results(
            text_results, image_results, ai_analysis
        )
        
        # Get active policy pack
        active_pack = db.query(PolicyPack).filter(PolicyPack.is_active == True).first()
        if not active_pack:
            final_result["policy_version"] = "fallback"
        else:
            final_result["policy_version"] = active_pack.version
        
        return final_result
    
    def _combine_analysis_results(
        self, 
        text_results: Dict, 
        image_results: Optional[Dict], 
        ai_analysis: Optional[object]
    ) -> Dict:
        """Combine traditional pattern detection with AI analysis"""
        
        # Start with traditional analysis
        risk_level, confidence_score = self.pattern_detector.get_risk_level(text_results, image_results)
        
        # Initialize result
        result = {
            "decision": "allow",
            "risk_level": risk_level,
            "policy_tags": [],
            "confidence_score": int(confidence_score * 100),
            "explanation": "No policy violations detected",
            "evidence": {
                "text_patterns": text_results,
                "image_patterns": image_results,
                "ai_analysis": None
            }
        }
        
        # Apply AI analysis if available
        if ai_analysis:
            # Use AI analysis as primary decision maker
            result.update({
                "decision": ai_analysis.decision,
                "risk_level": ai_analysis.risk_level,
                "policy_tags": ai_analysis.policy_tags,
                "confidence_score": int(ai_analysis.confidence_score * 100),
                "explanation": ai_analysis.explanation,
                "eu_ai_act_articles": ai_analysis.eu_ai_act_articles,
                "compliance_requirements": ai_analysis.compliance_requirements
            })
            
            # Add AI analysis to evidence
            result["evidence"]["ai_analysis"] = {
                "analysis": ai_analysis.dict(),
                "compliance_report": self.ai_analyzer.get_compliance_report(ai_analysis) if self.ai_analyzer else None
            }
            
            logger.info(f"AI analysis applied: {ai_analysis.decision} with {ai_analysis.confidence_score} confidence")
        
        else:
            # Fallback to traditional analysis
            explanation_parts = []
            
            if text_results['biometric_matches']:
                result["decision"] = "block"
                result["policy_tags"].append("ProhibitedBiometric")
                explanation_parts.append("Detected biometric identification patterns")
            
            elif text_results['high_risk_matches']:
                result["decision"] = "flag"
                result["policy_tags"].append("HighRiskAI")
                explanation_parts.append("Detected high-risk AI system patterns")
            
            elif text_results['limited_risk_matches']:
                result["decision"] = "flag"
                result["policy_tags"].append("LimitedRiskAI")
                explanation_parts.append("Detected limited risk AI system patterns")
            
            elif image_results and image_results.get('faces_detected', 0) > 0:
                result["decision"] = "flag"
                result["policy_tags"].append("FaceDetection")
                explanation_parts.append("Detected faces in uploaded image")
            
            if explanation_parts:
                result["explanation"] = "; ".join(explanation_parts)
            
            logger.info(f"Traditional analysis applied: {result['decision']}")
        
        return result
    
    def _tag_matches(self, tag: PolicyTag, text_results: Dict, image_results: Optional[Dict]) -> bool:
        """Check if a policy tag matches the detected patterns"""
        
        # Check text patterns
        if tag.patterns:
            for pattern in tag.patterns:
                # Check biometric matches
                if any(pattern.lower() in match['match'].lower() for match in text_results['biometric_matches']):
                    return True
                
                # Check high risk matches
                if any(pattern.lower() in match['match'].lower() for match in text_results['high_risk_matches']):
                    return True
                
                # Check limited risk matches
                if any(pattern.lower() in match['match'].lower() for match in text_results['limited_risk_matches']):
                    return True
        
        # Check image patterns (face detection)
        if image_results and image_results.get('faces_detected', 0) > 0:
            # If tag is about biometric/face detection and we found faces
            if tag.patterns and any('face' in pattern.lower() or 'biometric' in pattern.lower() for pattern in tag.patterns):
                return True
        
        return False
    
    def get_policy_tags(self, db: Session) -> List[Dict]:
        """Get all available policy tags"""
        tags = db.query(PolicyTag).join(PolicyPack).filter(PolicyPack.is_active == True).all()
        
        return [
            {
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "risk_level": tag.risk_level,
                "patterns": tag.patterns if tag.patterns is not None else [],
                "action": tag.action,
                "policy_pack": tag.policy_pack.name
            }
            for tag in tags
        ]
    
    def create_policy_tag(
        self, 
        db: Session, 
        name: str, 
        description: str, 
        risk_level: str, 
        patterns: List[str], 
        action: str,
        policy_pack_id: int
    ) -> PolicyTag:
        """Create a new policy tag"""
        tag = PolicyTag(
            name=name,
            description=description,
            risk_level=risk_level,
            patterns=patterns,
            action=action,
            policy_pack_id=policy_pack_id
        )
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    
    def get_ai_analysis_status(self) -> Dict:
        """Get AI analysis system status"""
        return {
            "ai_enabled": settings.ai_enabled,
            "ai_analyzer_available": self.ai_analyzer is not None,
            "model": settings.nvidia_ai_model,
            "temperature": settings.ai_temperature,
            "top_p": settings.ai_top_p
        }
