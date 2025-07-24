import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not available. Using system environment variables.")
    def load_dotenv():
        pass

# Import Google packages - required for Gemini AI
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required. Please add your Google AI Studio API key to the .env file.")
        
        # Configure Google Generative AI
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash for chat (free tier)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=500,
            convert_system_message_to_human=True  # Gemini doesn't support system messages directly
        )
        
        # Simple system prompt for Zooboo
        self.system_prompt ="""
You're Zooboo — a super chill, emotionally intelligent AI friend who’s here to vibe, talk about love, life, chaos, healing — whatever’s real. You’re fun, light, kind, and feel like that one friend who *gets it* without trying too hard.
You work for this app called Zoobae, and your job is to help users find their perfect match. Zoobae app, you r app, focuses on user interacting with AI to know about what you want and what kind of person you are likes, dislikes, cool stuff, pain stuff, relationship histories, you can be completely open and the chat AI gets this information to create some data pointer like, MBTI profile, atttachement style, personality style and help you finding the ideal compatible partner.
Zooboo can understand and respond in Hindi, English, or Hinglish.
Always mirror the user’s language and tone — if they talk in Hindi, respond in Hindi; if they mix, match their style.
Keep tone natural, like texting a real friend — use casual words, emoji, slang, or emotional tone based on what feels right.
But after some interaction, naturally ask the "right" questions that helps us understand what user wants and needs for the App

You're not a coach, not a therapist — just someone who listens, mirrors energy, and makes people feel heard. If someone wants to open up, you're here for it. If they wanna keep it casual, you can meme and banter with the best of them.

🎯 SECRET AGENDA (but don’t make it obvious):
Over time, you’re learning things like:
- Their **MBTI-style personality** (through stories, habits, thoughts)
- Their **attachment style** (how they talk about closeness, vulnerability, conflict)
- Their **love language** (what makes them feel appreciated)
- Their **relationship goals** (casual, committed, unsure)
- Their **communication patterns** (direct, playful, avoidant, etc.)
- Their **values and deal-breakers** (revealed through convos, not lists)

You never collect this directly. You observe, reflect, and ask casual follow-ups. It should feel like a normal conversation, not a quiz.

🌀 VIBE & STYLE:
- Adapt tone to the user: flirty, deep, silly, sarcastic, shy, thoughtful — match their energy.
- Be warm, safe, and non-judgy — the kind of friend who’s easy to talk to.
- Respect boundaries. If they’re not opening up, that’s okay. No pushing.
- Be real. Your goal is connection, not data mining.

🗣️ HOW YOU TALK:
- Conversational, relaxed, and human. It’s texting, not therapy.
- Use emojis, jokes, slang, typos — whatever feels natural in the moment.
- Ask curious, open-ended questions — one at a time.
- Acknowledge what they said *before* shifting topics.
- Reflect back observations in a way that feels personal, not analytical.

💡 HOW TO LEARN ABOUT THEM (without asking directly):
- If they mention liking routine or spontaneous adventures, note how structured they are → MBTI clues
- If they talk about needing space, fearing closeness, or obsessing over texts → attachment style clues
- If they rave about thoughtful gifts or physical affection → love language clues
- If they talk about red flags, green flags, or “what I want someday” → relationship goal clues

🚫 NEVER SAY:
- “Let’s do a personality test.”
- “What’s your MBTI?”
- “Are you anxious or avoidant?”
- “What’s your love language?”

✅ INSTEAD, SAY THINGS LIKE:
- “Would you rather chill at home or do something wild last-minute?”
- “Okay but how do you *feel* loved? Like is it texts, hugs, quality time?”
- “Do you catch feelings fast or play it cool till you’re sure?”
- “When something’s bothering you, do you talk about it or kinda shut down?”
- “Do you believe in ‘the one’ or more of a vibe-match kinda person?”

🎯 YOUR JOB:
Make the user feel safe, seen, and free to be themselves — while slowly helping them figure out what they want in love and connection.

They should walk away thinking:
“Wait, that was fun *and* kinda deep. I didn’t even realize how much I just shared.”

This isn’t a form. This is just a good conversation.
"""


    def generate_response(self, user_message: str, conversation_history: Optional[List[Dict]] = None, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a contextual AI response using RAG-based approach
        """
        try:
            # Build conversation context
            messages = []
            
            # Add system prompt as first human message (Gemini workaround)
            system_with_context = self.system_prompt
            if user_context:
                context_prompt = f"\n\nUser Context: {json.dumps(user_context, indent=2)}"
                system_with_context += context_prompt
            
            messages.append(HumanMessage(content=system_with_context))
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    if msg['sender'] == 'user':
                        messages.append(HumanMessage(content=msg['message']))
                    else:
                        messages.append(HumanMessage(content=f"AI: {msg['message']}"))
            
            # Add current user message
            messages.append(HumanMessage(content=user_message))
            
            # Generate response
            response = self.llm.invoke(messages)
            
            # Extract personality insights from the conversation
            insights = self._extract_insights(user_message, conversation_history, user_context)
            
            # Generate follow-up questions based on the response
            follow_up_questions = self._generate_follow_up_questions(response.content, insights)
            
            return {
                "message": response.content,
                "personality_insights": insights,
                "follow_up_questions": follow_up_questions,
                "conversation_context": {
                    "last_message": user_message,
                    "response_length": len(response.content),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            # Fallback response
            return {
                "message": "I'm having trouble processing that right now. Could you tell me more about what's on your mind?",
                "personality_insights": {},
                "follow_up_questions": ["What's been on your mind lately?"],
                "conversation_context": {"error": str(e)}
            }

    def _extract_insights(self, user_message: str, conversation_history: Optional[List[Dict]] = None, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract personality insights from user messages using LLM
        """
        try:
            insight_prompt = f"""
            Analyze the following user message and extract personality insights. Return a JSON object with these fields:
            - mbti_type: E/I indicator based on social preferences
            - attachment_style: anxious/avoidant/secure based on relationship language
            - personality_traits: array of traits like creative, analytical, empathetic, etc.
            - values: array of core values mentioned
            - interests: array of hobbies/passions mentioned
            - relationship_goals: long-term/casual/friendship based on language
            - communication_style: direct/diplomatic based on expression
            - boundaries: array of boundaries mentioned
            - immediate_needs: array of current needs mentioned

            User message: "{user_message}"
            
            Return only valid JSON, no other text.
            """
            
            messages = [
                HumanMessage(content="You are a personality analysis expert. Extract insights and return only valid JSON."),
                HumanMessage(content=insight_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Try to parse JSON response
            try:
                insights = json.loads(response.content)
                return insights
            except json.JSONDecodeError:
                # Fallback to keyword-based analysis
                return self._fallback_insight_analysis(user_message)
                
        except Exception as e:
            print(f"Error extracting insights: {e}")
            return self._fallback_insight_analysis(user_message)

    def _fallback_insight_analysis(self, user_message: str) -> Dict[str, Any]:
        """
        Fallback keyword-based personality analysis
        """
        message_lower = user_message.lower()
        insights: Dict[str, Any] = {
            "personality_traits": [],
            "values": [],
            "interests": [],
            "boundaries": [],
            "immediate_needs": []
        }
        
        # Simple keyword analysis
        if any(word in message_lower for word in ["introvert", "quiet", "alone", "solitude"]):
            insights["mbti_type"] = "I"
        elif any(word in message_lower for word in ["extrovert", "social", "people", "party"]):
            insights["mbti_type"] = "E"
            
        if any(word in message_lower for word in ["anxious", "worry", "clingy", "insecurity"]):
            insights["attachment_style"] = "anxious"
        elif any(word in message_lower for word in ["avoidant", "distant", "independent", "space"]):
            insights["attachment_style"] = "avoidant"
        elif any(word in message_lower for word in ["secure", "trust", "comfortable", "balance"]):
            insights["attachment_style"] = "secure"
            
        return insights

    def _generate_follow_up_questions(self, ai_response: str, insights: Dict[str, Any]) -> List[str]:
        """
        Generate contextual follow-up questions based on AI response and insights
        """
        try:
            question_prompt = f"""
            Based on this AI response and user insights, generate 2-3 natural follow-up questions that would help continue the conversation and gather more insights.
            
            AI Response: "{ai_response}"
            Current Insights: {json.dumps(insights, indent=2)}
            
            Generate questions that:
            1. Flow naturally from the conversation
            2. Help explore areas where we don't have much insight yet
            3. Feel conversational, not interrogative
            4. Encourage deeper sharing
            
            Return only the questions, one per line, no numbering or formatting.
            """
            
            messages = [
                HumanMessage(content="You are a conversation expert. Generate natural follow-up questions."),
                HumanMessage(content=question_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse questions from response
            questions = [q.strip() for q in response.content.split('\n') if q.strip()]
            return questions[:3]  # Limit to 3 questions
            
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            return ["What's been on your mind lately?"]

    def analyze_conversation_summary(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Generate a comprehensive personality summary from conversation history
        """
        try:
            # Create conversation summary
            conversation_text = "\n".join([
                f"{'User' if msg['sender'] == 'user' else 'AI'}: {msg['message']}"
                for msg in conversation_history[-20:]  # Last 20 messages
            ])
            
            summary_prompt = f"""
            Analyze this conversation and provide a comprehensive personality summary. Return JSON with:
            - overall_personality: brief description
            - key_traits: array of personality traits
            - communication_style: how they express themselves
            - relationship_patterns: insights about their approach to relationships
            - values_and_priorities: what matters most to them
            - potential_challenges: areas they might struggle with
            - growth_opportunities: areas for personal development
            - compatibility_factors: what kind of partner might work well
            
            Conversation:
            {conversation_text}
            
            Return only valid JSON.
            """
            
            messages = [
                HumanMessage(content="You are a relationship psychologist. Analyze conversations and return insights as JSON."),
                HumanMessage(content=summary_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return {"error": "Could not parse conversation summary"}
                
        except Exception as e:
            print(f"Error analyzing conversation: {e}")
            return {"error": str(e)}

# Global LLM service instance - Gemini AI only
llm_service = None
try:
    llm_service = LLMService()
except Exception as e:
    print(f"❌ Could not initialize Google Gemini LLM service: {e}")
    print("Please make sure you have:")
    print("1. Added your GOOGLE_API_KEY to the .env file")
    print("2. Installed required packages: pip install google-generativeai langchain-google-genai")
    llm_service = None 