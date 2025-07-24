import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

class SimpleLLMService:
    """
    Simple LLM service that doesn't require any API keys.
    Perfect for testing and prototyping without external dependencies.
    """
    
    def __init__(self):
        # Pre-defined responses that feel natural and contextual
        self.contextual_responses = [
            "That's really interesting! I'd love to hear more about that. What made you feel that way?",
            "I can sense there's a lot of depth to what you're sharing. How has that experience shaped who you are today?",
            "That's such a unique perspective! What are some of your biggest values in life?",
            "I'm curious to know more about your thoughts on relationships. What do you think makes a connection meaningful?",
            "That sounds like it was quite an experience. How did that influence your approach to relationships?",
            "I love how you think about things! Have you always felt this way, or has your perspective changed over time?",
            "That's really insightful! How do you usually handle challenges or difficult situations?",
            "I'm getting to know you better! What are some things you're looking for in a potential partner?",
            "That's fascinating! What are some of your dreams or goals for the future?",
            "I appreciate you sharing that with me. What are some of your favorite ways to spend your time?",
            "That's such a thoughtful response! What are some of your interests or passions?",
            "I can tell you've put a lot of thought into this. How do you usually communicate in relationships?",
            "That's really meaningful! What are some of your core values when it comes to relationships?",
            "I'd love to hear more about your experiences. What have you learned about yourself through relationships?",
            "That's such an honest answer! What are some of your boundaries or deal-breakers?",
        ]
        
        # Follow-up questions to keep conversation flowing
        self.follow_up_questions = [
            "What are some of your biggest values in life?",
            "How do you usually handle stress or difficult situations?",
            "What are you looking for in a relationship right now?",
            "What are some of your interests or hobbies?",
            "How do you prefer to communicate in relationships?",
            "What are some of your goals for the future?",
            "How do you usually spend your free time?",
            "What are some of your deal-breakers in relationships?",
            "How do you like to be supported by a partner?",
            "What are some of your favorite ways to connect with people?",
        ]

    def generate_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a contextual AI response using simple pattern matching
        """
        try:
            # Analyze the message for context
            message_lower = user_message.lower()
            
            # Generate contextual response based on keywords
            response = self._generate_contextual_response(message_lower)
            
            # Extract personality insights
            insights = self._extract_insights(message_lower)
            
            # Generate follow-up questions
            follow_up_questions = self._generate_follow_up_questions(insights)
            
            return {
                "message": response,
                "personality_insights": insights,
                "follow_up_questions": follow_up_questions,
                "conversation_context": {
                    "last_message": user_message,
                    "response_length": len(response),
                    "timestamp": datetime.utcnow().isoformat(),
                    "method": "simple_llm"
                }
            }
            
        except Exception as e:
            print(f"Error generating simple LLM response: {e}")
            return {
                "message": "That's really interesting! Tell me more about what's on your mind.",
                "personality_insights": {},
                "follow_up_questions": ["What's been on your mind lately?"],
                "conversation_context": {"error": str(e)}
            }

    def _generate_contextual_response(self, message_lower: str) -> str:
        """
        Generate contextual response based on keywords in the message
        """
        # Check for specific keywords and return appropriate responses
        if any(word in message_lower for word in ["relationship", "dating", "partner"]):
            return "I'd love to hear more about your thoughts on relationships. What do you think makes a connection meaningful?"
        
        if any(word in message_lower for word in ["work", "career", "job"]):
            return "That's really interesting! How do you balance your work life with your personal relationships?"
        
        if any(word in message_lower for word in ["family", "parents", "siblings"]):
            return "Family can have such a big impact on how we approach relationships. How has your family influenced you?"
        
        if any(word in message_lower for word in ["hobby", "interest", "passion", "music", "sports"]):
            return "That's such a great passion! How do your interests shape the kind of person you're looking for?"
        
        if any(word in message_lower for word in ["travel", "adventure", "explore"]):
            return "I love that adventurous spirit! How do you think that affects what you want in a relationship?"
        
        if any(word in message_lower for word in ["introvert", "quiet", "alone"]):
            return "I can understand that need for space and quiet. How do you balance that with the desire for connection?"
        
        if any(word in message_lower for word in ["extrovert", "social", "people"]):
            return "Your social energy is amazing! How do you think that affects your relationships?"
        
        if any(word in message_lower for word in ["anxious", "worry", "insecurity"]):
            return "I can sense you're someone who really cares about connections. What helps you feel more secure in relationships?"
        
        if any(word in message_lower for word in ["independent", "space", "freedom"]):
            return "I notice you value your independence, which is totally healthy! How do you balance that with the desire for connection?"
        
        # Default to random contextual response
        return random.choice(self.contextual_responses)

    def _extract_insights(self, message_lower: str) -> Dict[str, Any]:
        """
        Extract personality insights using keyword analysis
        """
        insights: Dict[str, Any] = {
            "personality_traits": [],
            "values": [],
            "interests": [],
            "boundaries": [],
            "immediate_needs": []
        }
        
        # MBTI indicators
        if any(word in message_lower for word in ["introvert", "quiet", "alone", "solitude", "recharge"]):
            insights["mbti_type"] = "I"
        elif any(word in message_lower for word in ["extrovert", "social", "people", "party", "energized"]):
            insights["mbti_type"] = "E"
        
        # Attachment style indicators
        if any(word in message_lower for word in ["anxious", "worry", "clingy", "insecurity", "fear"]):
            insights["attachment_style"] = "anxious"
        elif any(word in message_lower for word in ["avoidant", "distant", "independent", "space", "freedom"]):
            insights["attachment_style"] = "avoidant"
        elif any(word in message_lower for word in ["secure", "trust", "comfortable", "balance", "confident"]):
            insights["attachment_style"] = "secure"
        
        # Personality traits
        if any(word in message_lower for word in ["creative", "artistic", "imaginative", "creative"]):
            insights["personality_traits"].append("creative")
        if any(word in message_lower for word in ["analytical", "logical", "rational", "thinker"]):
            insights["personality_traits"].append("analytical")
        if any(word in message_lower for word in ["empathetic", "caring", "compassionate", "understanding"]):
            insights["personality_traits"].append("empathetic")
        if any(word in message_lower for word in ["adventurous", "spontaneous", "risk-taker", "explorer"]):
            insights["personality_traits"].append("adventurous")
        
        # Values
        if any(word in message_lower for word in ["family", "relationships", "connection", "love"]):
            insights["values"].append("family")
        if any(word in message_lower for word in ["career", "success", "achievement", "work"]):
            insights["values"].append("career")
        if any(word in message_lower for word in ["travel", "exploration", "experiences", "adventure"]):
            insights["values"].append("experiences")
        if any(word in message_lower for word in ["learning", "growth", "development", "improvement"]):
            insights["values"].append("personal growth")
        
        # Interests
        if any(word in message_lower for word in ["music", "concert", "playlist", "songs"]):
            insights["interests"].append("music")
        if any(word in message_lower for word in ["sports", "fitness", "exercise", "workout"]):
            insights["interests"].append("fitness")
        if any(word in message_lower for word in ["cooking", "food", "restaurant", "cuisine"]):
            insights["interests"].append("food")
        if any(word in message_lower for word in ["reading", "books", "literature", "novels"]):
            insights["interests"].append("reading")
        
        return insights

    def _generate_follow_up_questions(self, insights: Dict[str, Any]) -> List[str]:
        """
        Generate follow-up questions based on current insights
        """
        questions = []
        
        # Ask about missing insights
        if not insights.get("mbti_type"):
            questions.append("Are you more of an introvert or extrovert?")
        
        if not insights.get("attachment_style"):
            questions.append("How do you typically feel in relationships?")
        
        if len(insights.get("interests", [])) < 2:
            questions.append("What are some things you're passionate about?")
        
        if len(insights.get("values", [])) < 2:
            questions.append("What are some of your core values in life?")
        
        # Add some random questions if we don't have enough
        while len(questions) < 3:
            random_question = random.choice(self.follow_up_questions)
            if random_question not in questions:
                questions.append(random_question)
        
        return questions[:3]

    def analyze_conversation_summary(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Generate a simple personality summary from conversation history
        """
        try:
            # Extract all user messages
            user_messages = [msg['message'].lower() for msg in conversation_history if msg['sender'] == 'user']
            all_text = ' '.join(user_messages)
            
            # Simple analysis based on frequency of keywords
            summary = {
                "overall_personality": "A thoughtful individual who values meaningful connections",
                "key_traits": [],
                "communication_style": "reflective",
                "relationship_patterns": "seeks understanding and connection",
                "values_and_priorities": [],
                "potential_challenges": "may overthink relationships",
                "growth_opportunities": "building confidence in connections",
                "compatibility_factors": "values communication and emotional intelligence"
            }
            
            # Add traits based on keyword frequency
            if any(word in all_text for word in ["creative", "artistic", "imaginative"]):
                summary["key_traits"].append("creative")
            
            if any(word in all_text for word in ["analytical", "logical", "thinker"]):
                summary["key_traits"].append("analytical")
            
            if any(word in all_text for word in ["empathetic", "caring", "understanding"]):
                summary["key_traits"].append("empathetic")
            
            if any(word in all_text for word in ["adventurous", "explorer", "spontaneous"]):
                summary["key_traits"].append("adventurous")
            
            return summary
            
        except Exception as e:
            print(f"Error analyzing conversation: {e}")
            return {"error": str(e)}

# Global simple LLM service instance
simple_llm_service = SimpleLLMService() 