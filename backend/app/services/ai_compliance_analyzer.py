from typing import Dict, List, Optional, Tuple
import json
import logging
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import re

logger = logging.getLogger(__name__)

class ComplianceAnalysis(BaseModel):
    """Structured output for AI compliance analysis"""
    risk_level: str = Field(description="Risk level: unacceptable, high, limited, minimal")
    decision: str = Field(description="Decision: block, flag, allow")
    policy_tags: List[str] = Field(description="List of triggered policy tags")
    confidence_score: float = Field(description="Confidence score 0-1")
    explanation: str = Field(description="Detailed explanation of the analysis")
    eu_ai_act_articles: List[str] = Field(description="Relevant EU AI Act articles")
    compliance_requirements: List[str] = Field(description="Specific compliance requirements")
    evidence: Dict = Field(description="Supporting evidence for the decision")

class AIComplianceAnalyzer:
    def __init__(self, api_key: str):
        """Initialize AI compliance analyzer with NVIDIA AI endpoints"""
        self.llm = self._create_llm(api_key)
        self.parser = PydanticOutputParser(pydantic_object=ComplianceAnalysis)
        
        # EU AI Act specific prompts
        self.system_prompt = self._create_system_prompt()
        self.analysis_prompt = self._create_analysis_prompt()
        
    def _create_llm(self, api_key: str):
        """Create LLM instance with NVIDIA AI endpoints"""
        try:
            return ChatNVIDIA(
                model="meta/llama-3.3-70b-instruct",
                api_key=api_key,
                temperature=0.2,
                top_p=0.7
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            return None
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for EU AI Act compliance analysis"""
        return """You are an expert AI compliance analyst specializing in EU AI Act (Regulation 2024/1689) compliance. 

Your role is to analyze content and determine:
1. Risk level classification (unacceptable, high, limited, minimal)
2. Appropriate action (block, flag, allow)
3. Relevant EU AI Act articles and requirements
4. Specific compliance obligations

Key EU AI Act Provisions:

ARTICLE 5 - PROHIBITED AI PRACTICES:
- Real-time remote biometric identification in publicly accessible spaces
- Untargeted scraping of facial images to create facial recognition databases
- Emotion recognition in workplace and educational institutions
- Social scoring systems
- AI systems that manipulate human behavior
- AI systems that exploit vulnerabilities

ANNEX III - HIGH-RISK AI SYSTEMS:
- Biometric identification and categorization
- Critical infrastructure management
- Education and vocational training
- Employment, worker management, and access to self-employment
- Access to and enjoyment of essential private services and public services
- Law enforcement
- Migration, asylum, and border control management
- Administration of justice and democratic processes

ARTICLE 52 - TRANSPARENCY OBLIGATIONS:
- AI systems that interact with humans
- AI systems that generate or manipulate content
- AI systems that detect emotions or biometric categorization

Be thorough in your analysis and provide specific article references and compliance requirements."""

    def _create_analysis_prompt(self) -> str:
        """Create analysis prompt template"""
        return ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """
Analyze the following content for EU AI Act compliance:

Content: {content}
Content Type: {content_type}
Context: {context}

Provide a structured analysis including:
- Risk level assessment
- Decision recommendation
- Policy tags
- EU AI Act article references
- Specific compliance requirements
- Supporting evidence

{format_instructions}
""")
        ])
    
    def analyze_content(
        self, 
        content: str, 
        content_type: str = "text",
        context: str = ""
    ) -> Optional[ComplianceAnalysis]:
        """Analyze content using AI for EU AI Act compliance"""
        
        if not self.llm:
            logger.error("LLM not initialized")
            return None
        
        try:
            # Prepare the prompt
            prompt = self.analysis_prompt.format_prompt(
                content=content,
                content_type=content_type,
                context=context,
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Get AI analysis
            messages = prompt.to_messages()
            response = self.llm.invoke(messages)
            
            # Parse the response
            analysis = self.parser.parse(response.content)
            
            logger.info(f"AI analysis completed: {analysis.decision} with {analysis.confidence_score} confidence")
            return analysis
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._fallback_analysis(content)
    
    def _fallback_analysis(self, content: str) -> ComplianceAnalysis:
        """Fallback analysis when AI fails"""
        # Simple keyword-based fallback
        content_lower = content.lower()
        
        # Check for prohibited practices
        prohibited_keywords = [
            'facial recognition', 'biometric identification', 'real-time remote',
            'untargeted scraping', 'emotion recognition', 'social scoring',
            'behavior manipulation', 'vulnerability exploitation'
        ]
        
        high_risk_keywords = [
            'cv screening', 'recruitment', 'credit scoring', 'criminal risk',
            'healthcare diagnosis', 'education assessment', 'law enforcement',
            'border control', 'democratic processes'
        ]
        
        limited_risk_keywords = [
            'chatbot', 'deepfake', 'content generation', 'emotion detection',
            'biometric categorization'
        ]
        
        # Determine risk level
        if any(keyword in content_lower for keyword in prohibited_keywords):
            return ComplianceAnalysis(
                risk_level="unacceptable",
                decision="block",
                policy_tags=["ProhibitedAIPractice"],
                confidence_score=0.7,
                explanation="Detected prohibited AI practice keywords",
                eu_ai_act_articles=["Article 5"],
                compliance_requirements=["Prohibited under Article 5"],
                evidence={"keywords_found": [k for k in prohibited_keywords if k in content_lower]}
            )
        elif any(keyword in content_lower for keyword in high_risk_keywords):
            return ComplianceAnalysis(
                risk_level="high",
                decision="flag",
                policy_tags=["HighRiskAI"],
                confidence_score=0.6,
                explanation="Detected high-risk AI system keywords",
                eu_ai_act_articles=["Annex III"],
                compliance_requirements=["Additional controls required"],
                evidence={"keywords_found": [k for k in high_risk_keywords if k in content_lower]}
            )
        elif any(keyword in content_lower for keyword in limited_risk_keywords):
            return ComplianceAnalysis(
                risk_level="limited",
                decision="flag",
                policy_tags=["LimitedRiskAI"],
                confidence_score=0.5,
                explanation="Detected limited risk AI system keywords",
                eu_ai_act_articles=["Article 52"],
                compliance_requirements=["Transparency obligations"],
                evidence={"keywords_found": [k for k in limited_risk_keywords if k in content_lower]}
            )
        else:
            return ComplianceAnalysis(
                risk_level="minimal",
                decision="allow",
                policy_tags=[],
                confidence_score=0.8,
                explanation="No compliance concerns detected",
                eu_ai_act_articles=[],
                compliance_requirements=[],
                evidence={"analysis": "No prohibited or high-risk keywords found"}
            )
    
    def analyze_image_content(self, image_description: str, face_detected: bool = False) -> Optional[ComplianceAnalysis]:
        """Analyze image content for compliance"""
        context = f"Image analysis: {image_description}"
        if face_detected:
            context += " - Face detected in image"
        
        return self.analyze_content(
            content=image_description,
            content_type="image",
            context=context
        )
    
    def get_compliance_report(self, analysis: ComplianceAnalysis) -> Dict:
        """Generate a comprehensive compliance report"""
        return {
            "analysis": analysis.dict(),
            "eu_ai_act_mapping": {
                "articles": analysis.eu_ai_act_articles,
                "requirements": analysis.compliance_requirements,
                "risk_classification": analysis.risk_level,
                "decision_rationale": analysis.explanation
            },
            "compliance_status": {
                "compliant": analysis.decision == "allow",
                "requires_attention": analysis.decision in ["block", "flag"],
                "action_required": analysis.decision == "block"
            },
            "evidence_summary": analysis.evidence
        }
