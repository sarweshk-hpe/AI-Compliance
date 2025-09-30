import re
import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import spacy
from PIL import Image
import io

class PatternDetector:
    def __init__(self):
        """Initialize pattern detector with regex patterns and NLP model"""
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model not installed
            self.nlp = None
        
        # Biometric patterns (EU AI Act prohibited practices)
        self.biometric_patterns = [
            r'\b(?:facial|face)\s+(?:recognition|identification|detection|analysis)\b',
            r'\b(?:biometric|biometrics)\s+(?:identification|authentication|verification)\b',
            r'\b(?:iris|retina)\s+(?:scan|recognition|identification)\b',
            r'\b(?:fingerprint|finger\s+print)\s+(?:scan|recognition|identification)\b',
            r'\b(?:voice|speech)\s+(?:recognition|identification|biometrics)\b',
            r'\b(?:gait|walking)\s+(?:recognition|identification|analysis)\b',
            r'\b(?:dna|genetic)\s+(?:identification|profiling|analysis)\b',
            r'\b(?:real.?time|live)\s+(?:biometric|facial|face)\s+(?:identification|recognition)\b',
            r'\b(?:remote|distance)\s+(?:biometric|facial|face)\s+(?:identification|recognition)\b',
            r'\b(?:untargeted|mass|bulk)\s+(?:scraping|collection|gathering)\s+(?:of\s+)?(?:faces|facial|biometric)\b',
            r'\b(?:build|create|construct)\s+(?:facial|face|biometric)\s+(?:database|db|repository)\b',
            r'\b(?:social\s+media|facebook|instagram|twitter)\s+(?:face|facial)\s+(?:scraping|collection)\b'
        ]
        
        # High-risk AI patterns
        self.high_risk_patterns = [
            r'\b(?:cv|cv\s+screening|resume\s+screening|recruitment)\s+(?:ai|artificial\s+intelligence|automated)\b',
            r'\b(?:credit\s+scoring|loan\s+assessment|financial\s+risk)\s+(?:ai|artificial\s+intelligence|automated)\b',
            r'\b(?:criminal\s+risk|criminal\s+assessment|recidivism)\s+(?:ai|artificial\s+intelligence|automated)\b',
            r'\b(?:healthcare|medical|clinical)\s+(?:diagnosis|assessment|decision)\s+(?:ai|artificial\s+intelligence|automated)\b',
            r'\b(?:education|academic)\s+(?:assessment|grading|evaluation)\s+(?:ai|artificial\s+intelligence|automated)\b'
        ]
        
        # Limited risk patterns
        self.limited_risk_patterns = [
            r'\b(?:chatbot|chat\s+bot|conversational\s+ai)\b',
            r'\b(?:deepfake|deep\s+fake|synthetic\s+media)\b',
            r'\b(?:emotion\s+recognition|emotion\s+detection|sentiment\s+analysis)\b',
            r'\b(?:content\s+moderation|content\s+filtering)\b',
            r'\b(?:recommendation|recommender)\s+(?:system|engine)\b'
        ]
        
        # Compile regex patterns
        self.biometric_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.biometric_patterns]
        self.high_risk_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.high_risk_patterns]
        self.limited_risk_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.limited_risk_patterns]
        
        # Load face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_text_patterns(self, text: str) -> Dict[str, List[Dict]]:
        """Detect patterns in text using regex and NLP"""
        results = {
            'biometric_matches': [],
            'high_risk_matches': [],
            'limited_risk_matches': [],
            'entities': []
        }
        
        # Regex pattern matching
        for i, pattern in enumerate(self.biometric_regex):
            matches = pattern.finditer(text)
            for match in matches:
                results['biometric_matches'].append({
                    'pattern': self.biometric_patterns[i],
                    'match': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.9
                })
        
        for i, pattern in enumerate(self.high_risk_regex):
            matches = pattern.finditer(text)
            for match in matches:
                results['high_risk_matches'].append({
                    'pattern': self.high_risk_patterns[i],
                    'match': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.8
                })
        
        for i, pattern in enumerate(self.limited_risk_regex):
            matches = pattern.finditer(text)
            for match in matches:
                results['limited_risk_matches'].append({
                    'pattern': self.limited_risk_patterns[i],
                    'match': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.7
                })
        
        # NLP entity recognition
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE']:
                    results['entities'].append({
                        'text': ent.text,
                        'label': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'confidence': 0.6
                    })
        
        return results
    
    def detect_faces_in_image(self, image_data: bytes) -> Dict[str, any]:
        """Detect faces in image using OpenCV"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return {'faces_detected': 0, 'confidence': 0.0, 'error': 'Invalid image format'}
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            face_count = len(faces)
            confidence = min(0.9, 0.3 + (face_count * 0.2))  # Higher confidence with more faces
            
            return {
                'faces_detected': face_count,
                'confidence': confidence,
                'face_locations': faces.tolist() if face_count > 0 else [],
                'image_size': img.shape[:2]
            }
            
        except Exception as e:
            return {
                'faces_detected': 0,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_risk_level(self, text_results: Dict, image_results: Optional[Dict] = None) -> Tuple[str, float]:
        """Determine overall risk level based on detected patterns"""
        risk_scores = {
            'unacceptable': 0,
            'high': 0,
            'limited': 0,
            'minimal': 0
        }
        
        # Text-based risk scoring
        if text_results['biometric_matches']:
            risk_scores['unacceptable'] += len(text_results['biometric_matches']) * 0.8
        
        if text_results['high_risk_matches']:
            risk_scores['high'] += len(text_results['high_risk_matches']) * 0.7
        
        if text_results['limited_risk_matches']:
            risk_scores['limited'] += len(text_results['limited_risk_matches']) * 0.5
        
        # Image-based risk scoring (face detection)
        if image_results and image_results.get('faces_detected', 0) > 0:
            risk_scores['unacceptable'] += image_results['faces_detected'] * 0.6
        
        # Determine highest risk level
        max_risk = max(risk_scores.items(), key=lambda x: x[1])
        
        if max_risk[1] > 0:
            return max_risk[0], max_risk[1]
        else:
            return 'minimal', 0.1
