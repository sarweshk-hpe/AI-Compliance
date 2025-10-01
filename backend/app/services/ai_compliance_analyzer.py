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
Key Definitions:
AI System: A machine-based system designed to operate with varying levels of autonomy. It infers from the input it receives how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments.
Provider: The entity that develops an AI system or has it developed and places it on the market or into service under its own name or trademark.
Deployer: The entity using an AI system under its authority, except for personal, non-professional activities.
High-Risk AI System: An AI system that poses a significant risk to the health, safety, or fundamental rights of individuals.
General-Purpose AI (GPAI) Model: An AI model with significant generality, capable of performing a wide range of distinct tasks, that can be integrated into various downstream systems.
A. Prohibited AI Practices:
The following AI practices are strictly prohibited:
Manipulative Techniques: AI systems that use subliminal, manipulative, or deceptive techniques to materially distort a person's behavior, causing significant harm.
Exploitation of Vulnerabilities: AI systems that exploit the vulnerabilities of a person or group due to age, disability, or socio-economic situation to cause significant harm.
Social Scoring: AI systems that evaluate or classify individuals or groups based on their social behavior or personal characteristics, leading to detrimental or unfavorable treatment in unrelated social contexts.
Risk Assessment for Criminal Offenses: AI systems that make risk assessments of individuals to predict the commission of a criminal offense based solely on profiling or personality traits.
Untargeted Scraping of Facial Images: Creating or expanding facial recognition databases by untargeted scraping of facial images from the internet or CCTV footage.
Emotion Recognition in the Workplace and Education: AI systems that infer emotions of individuals in workplaces and educational institutions, except for medical or safety reasons.
Biometric Categorization: Systems that categorize individuals based on their biometric data to deduce or infer sensitive attributes like race, political opinions, or sexual orientation.
'Real-time' Remote Biometric Identification: The use of 'real-time' remote biometric identification systems in publicly accessible spaces for law enforcement purposes, with very narrow and strictly defined exceptions.
B. High-Risk AI Systems:
High-risk AI systems are subject to strict obligations. An AI system is considered high-risk if it is a safety component of a product, is itself a product covered by specific EU legislation, or falls into one of the categories below.
Key High-Risk Areas:
Biometrics (where permitted)
Critical infrastructure management
Education and vocational training
Employment, workers management, and access to self-employment
Access to and enjoyment of essential private and public services and benefits
Law enforcement
Migration, asylum, and border control management
Administration of justice and democratic processes
Core Requirements for High-Risk AI Systems:
Risk Management System: Providers must establish, implement, document, and maintain a continuous risk management system throughout the AI system's lifecycle.
Data Governance and Quality: Training, validation, and testing data must be relevant, representative, and free of errors and biases.
Technical Documentation: Providers must draw up and maintain technical documentation demonstrating compliance with the Act's requirements.
Record-Keeping: High-risk AI systems must have logging capabilities to ensure traceability of their functioning.
Transparency and Information to Deployers: Systems must be transparent, allowing deployers to interpret the output and use it appropriately. Clear instructions for use must be provided.
Human Oversight: Systems must be designed to be effectively overseen by humans.
Accuracy, Robustness, and Cybersecurity: Systems must achieve an appropriate level of accuracy, be resilient against errors, and have a high level of cybersecurity.
Quality Management System: Providers must have a quality management system in place to ensure compliance.
Conformity Assessment: High-risk AI systems must undergo a conformity assessment before being placed on the market.
Registration: Providers must register their high-risk AI systems in an EU database.
C. Transparency Obligations for Certain AI Systems:
Interaction with Humans: Users must be informed that they are interacting with an AI system unless it is obvious.
Synthetic Content: AI systems generating synthetic audio, image, video, or text content must ensure outputs are marked in a machine-readable format as artificially generated or manipulated.
Deep Fakes: Deployers of AI systems that generate or manipulate image, audio, or video content constituting a "deep fake" must disclose that the content is artificial.
Emotion Recognition and Biometric Categorization: Individuals exposed to these systems must be informed of their operation.
D. General-Purpose AI (GPAI) Models:
Transparency: All GPAI model providers must provide technical documentation, instructions for use, comply with copyright law, and publish a summary of the content used for training.
Systemic Risk: GPAI models with "high-impact capabilities" that may pose systemic risks are subject to stricter obligations, including model evaluations, adversarial testing, and reporting of serious incidents.
E. Obligations of Providers and Deployers:
Providers: Are primarily responsible for ensuring their AI systems meet all the requirements of the Act before placing them on the market. This includes conducting conformity assessments, drawing up technical documentation, and being transparent about the system's capabilities and limitations.
Deployers: Must use high-risk AI systems in accordance with their instructions, ensure human oversight, and monitor the system's operation. For certain high-risk systems, deployers must also conduct a fundamental rights impact assessment.

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
