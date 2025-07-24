# Zoobae - AI-Powered Dating App

A modern dating app with an intelligent AI chat system that helps users discover themselves and find meaningful connections through natural conversation.

## 🚀 Features

### Core Dating App Features
- **User Authentication** - Secure login/register system
- **Profile Management** - Photo uploads with 4:5 aspect ratio cropping
- **Photo Gallery** - Multiple photos with captions
- **Modern UI** - Beautiful cherry blossom themed interface

### AI Chat System (NEW!)
- **RAG-Based LLM Chat** - Natural conversations like ChatGPT
- **Personality Analysis** - Automatic insight extraction
- **Conversation Memory** - Contextual responses based on chat history
- **Follow-up Questions** - Smart questions to continue conversations
- **Personality Insights** - MBTI, attachment styles, values, interests
- **Free Tier Support** - Works with Google AI Studio (free) or simple fallback

## 🛠️ Tech Stack

### Frontend
- **React Native** - Cross-platform mobile app
- **React Navigation** - Tab and stack navigation
- **Image Crop Picker** - Photo selection and cropping

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **Google Gemini AI** - Free LLM for chat (with fallback)
- **JWT Authentication** - Secure user sessions

## 📦 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo>
cd App
```

### 2. Backend Setup
```bash
cd backend
python setup.py  # Creates .env and checks dependencies
pip install -r requirements.txt
```

### 3. Get Free API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create API key (FREE!)
3. Add to `backend/.env` file

### 4. Start Backend
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 5. Frontend Setup
```bash
cd AppFrontend
npm install
npx react-native start
```

### 6. Run on Device/Emulator
```bash
# Android
npx react-native run-android

# iOS
npx react-native run-ios
```

## 🎯 AI Chat System

### How It Works
1. **Natural Conversations** - AI responds contextually like ChatGPT
2. **Personality Analysis** - Extracts insights from user messages
3. **Smart Follow-ups** - Generates relevant questions
4. **Memory** - Remembers conversation history
5. **Insights Storage** - Builds comprehensive personality profiles

### System Prompt
The AI is configured as "Zoobae" - a warm, supportive dating coach who:
- Helps users explore their personality and values
- Gathers insights about attachment styles and communication patterns
- Understands relationship goals and preferences
- Creates a safe space for honest sharing

### Free Tier Benefits
- **Google AI Studio**: 15 requests/minute, 1500/day (FREE!)
- **Simple Fallback**: Works without API keys for testing
- **No Credit Card Required**

## 📱 App Screens

### Profile Screen
- Photo gallery with cherry blossom background
- Profile information display
- Edit profile functionality

### Chat AI Screen
- Natural conversation interface
- Message bubbles with typing indicators
- Follow-up questions display
- Personality insights panel

### Edit Profile Screen
- Photo upload with 4:5 aspect ratio
- Photo deletion and caption editing
- Profile information editing

## 🔧 Configuration

### Environment Variables
```env
# Google AI Studio API (FREE!)
GOOGLE_API_KEY=your_api_key_here

# MongoDB
MONGO_URL=mongodb://localhost:27017/

# Server
HOST=0.0.0.0
PORT=8001
```

### API Endpoints
- `POST /chat/ai` - Chat with AI
- `GET /chat/history` - Get chat history
- `GET /chat/personality-summary` - Get personality analysis
- `POST /profile/photos` - Upload photos
- `GET /profile/photos` - Get user photos

## 🎨 UI Features

### Design System
- **Cherry Blossom Theme** - Beautiful pink/white color scheme
- **Consistent Spacing** - Unified margins and padding
- **Modern Cards** - Clean, rounded interface elements
- **Responsive Layout** - Works on different screen sizes

### Photo Handling
- **4:5 Aspect Ratio** - Instagram-style photo cropping
- **Multiple Photos** - Gallery with captions
- **Smooth Upload** - Progress indicators and error handling
- **Background Consistency** - Cherry blossom backgrounds

## 🧠 AI Capabilities

### Personality Analysis
- **MBTI Indicators** - Introvert/Extrovert detection
- **Attachment Styles** - Anxious/Avoidant/Secure patterns
- **Values Extraction** - Core values and priorities
- **Interest Detection** - Hobbies and passions
- **Communication Style** - Direct/Diplomatic patterns

### Conversation Features
- **Contextual Responses** - Based on conversation history
- **Smart Questions** - Generated based on missing insights
- **Emotional Intelligence** - Supportive and validating responses
- **Natural Flow** - Conversational, not interrogative

## 🚀 Deployment

### Backend Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY=your_key
export MONGO_URL=your_mongodb_url

# Start server
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### Frontend Deployment
```bash
# Build for production
cd AppFrontend
npx react-native run-android --variant=release
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- **Setup Issues**: Run `python setup.py` in backend directory
- **API Limits**: Check Google AI Studio dashboard
- **Dependencies**: Ensure all packages are installed
- **Database**: MongoDB must be running

## 🎉 What's Next?

- **Matching Algorithm** - Use personality insights for better matches
- **Video Chat** - Real-time video conversations
- **Group Chats** - Community features
- **Advanced Analytics** - Relationship insights and trends
