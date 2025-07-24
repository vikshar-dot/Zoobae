# LLM Setup Guide (Gemini API - Free Tier)

## Prerequisites

1. **Google AI Studio API Key**: You need a Google AI Studio API key (FREE!)
2. **Python Dependencies**: Install the required packages

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the backend directory with:

```env
# Google AI Studio API Configuration (FREE!)
GOOGLE_API_KEY=your_google_ai_studio_api_key_here

# MongoDB Configuration (optional, defaults to localhost)
MONGO_URL=mongodb://localhost:27017/

# Server Configuration
HOST=0.0.0.0
PORT=8001
```

### 3. Get Google AI Studio API Key (FREE!)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and paste it in your `.env` file

**Benefits of Google AI Studio:**
- ✅ **Completely FREE** for prototyping
- ✅ **Generous limits**: 15 requests per minute, 1500 requests per day
- ✅ **High quality**: Gemini Pro model is very capable
- ✅ **No credit card required**
- ✅ **Easy setup**

### 4. Test the Setup

Start the backend server:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## Features

### RAG-Based AI Chat
- **Natural Conversations**: AI responds contextually like ChatGPT
- **Personality Analysis**: Automatically extracts insights from conversations
- **Follow-up Questions**: Generates relevant questions to continue the conversation
- **Conversation Memory**: Remembers chat history for context

### System Prompt
The AI is configured with a comprehensive system prompt that defines:
- **Personality**: Warm, supportive, non-judgmental
- **Goals**: Help users discover themselves and find meaningful connections
- **Approach**: Natural conversation, not interrogation
- **Topics**: Values, experiences, relationships, goals, interests

### API Endpoints

- `POST /chat/ai` - Chat with AI
- `GET /chat/history` - Get chat history
- `GET /chat/personality-summary` - Get comprehensive personality analysis

## Usage

The AI will:
1. Analyze user messages for personality insights
2. Generate contextual responses
3. Suggest follow-up questions
4. Store conversation history
5. Build comprehensive personality profiles

## Free Tier Limits

- **Rate Limit**: 15 requests per minute
- **Daily Limit**: 1500 requests per day
- **Perfect for**: Prototyping, testing, and small-scale usage

## Troubleshooting

- **API Key Error**: Ensure your Google AI Studio API key is valid
- **Import Errors**: Make sure all dependencies are installed
- **Rate Limiting**: If you hit limits, wait a minute and try again
- **Memory Issues**: The system keeps last 10 messages for context to manage memory usage

## Alternative Free Options

If you need even more requests, consider:
- **Hugging Face Inference API**: Free tier with many models
- **Ollama**: Run models locally (requires more setup)
- **Anthropic Claude**: Free tier available 