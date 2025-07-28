# Zoobae - AI-Powered Dating App

A modern dating app with an intelligent AI chat system, comprehensive user registration flow, and personality-based matching through questionnaire insights.

## 🚀 Features

### Core Dating App Features
- **User Authentication** - Google Sign-In and phone number OTP
- **Profile Management** - Complete user profiles with photos
- **Multi-Step Registration** - Guided onboarding with personality questionnaire
- **Photo Gallery** - Multiple photos with captions and AI suggestions
- **Modern UI** - Beautiful cherry blossom themed interface

### AI Chat System
- **RAG-Based LLM Chat** - Natural conversations like ChatGPT
- **Personality Analysis** - Automatic insight extraction
- **Conversation Memory** - Contextual responses based on chat history
- **Follow-up Questions** - Smart questions to continue conversations
- **Personality Insights** - MBTI, attachment styles, values, interests
- **Free Tier Support** - Works with Google AI Studio (free) or simple fallback

### Registration & Questionnaire System
- **Multi-Screen Registration** - Step-by-step profile creation
- **Personality Questions** - 10 questions about personality traits
- **Relationship Questions** - 5 questions about relationship preferences
- **Values Questions** - 5 questions about money, goals, and values
- **Optional Final Question** - "What do you want?" descriptive text
- **Progress Tracking** - Saves progress and prevents data loss
- **Completion Validation** - Ensures full questionnaire completion

## 🛠️ Tech Stack

### Frontend
- **React Native** - Cross-platform mobile app
- **React Navigation** - Tab and stack navigation
- **AsyncStorage** - Local data persistence
- **Google Sign-In** - OAuth authentication
- **Image Crop Picker** - Photo selection and cropping

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database with collections: users, profiles, photos, prompts, chat_messages, personality_insights
- **Google Gemini AI** - Free LLM for chat (with fallback)
- **JWT Authentication** - Secure user sessions
- **File Upload** - Photo storage with local file system

## 📦 Complete Setup Guide

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (running locally or cloud instance)
- **Android Studio** (for Android development)
- **Xcode** (for iOS development, macOS only)

### 1. Clone and Setup
```bash
git clone <your-repo>
cd App
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env  # If .env.example exists
# Or create .env manually with:
# MONGO_URL=mongodb://localhost:27017/
# GOOGLE_API_KEY=your_google_ai_studio_key
```

### 3. MongoDB Setup
```bash
# Install MongoDB (if not already installed)
# macOS: brew install mongodb-community
# Ubuntu: sudo apt install mongodb
# Windows: Download from mongodb.com

# Start MongoDB
mongod

# Create database (optional - will be created automatically)
mongo
use dating_app
exit
```

### 4. Get Free API Key (Optional)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create API key (FREE!)
3. Add to `backend/.env` file: `GOOGLE_API_KEY=your_api_key_here`

### 5. Start Backend Server
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 6. Frontend Setup
```bash
cd AppFrontend

# Install dependencies
npm install

# Install iOS dependencies (macOS only)
cd ios && pod install && cd ..

# Start Metro bundler
npx react-native start
```

### 7. Run on Device/Emulator
```bash
# Android
npx react-native run-android

# iOS (macOS only)
npx react-native run-ios
```

## 🎯 App Flow

### Registration Process
1. **Welcome Screen** - App introduction and Google Sign-In
2. **Phone Number Screen** - Phone verification or Google Sign-In
3. **Create Profile** - Basic information (name, age, etc.)
4. **Personality Questions** - 10 questions about personality
5. **Relationship Questions** - 5 questions about relationships
6. **Values Questions** - 5 questions about money and goals
7. **What Do You Want** - Optional descriptive text
8. **Main App** - Access to all features

### Login Process
- **Existing Users** - Direct access to main app
- **Incomplete Registration** - Redirected to continue questionnaire
- **New Users** - Guided through registration flow

## 🔧 Configuration

### Environment Variables (backend/.env)
```env
# MongoDB Connection
MONGO_URL=mongodb://localhost:27017/

# Google AI Studio API (Optional - FREE!)
GOOGLE_API_KEY=your_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8001
```

### Database Collections
- **users** - User accounts and authentication
- **profiles** - Basic profile information
- **photos** - User photos with metadata
- **prompts** - Questionnaire answers (20-21 per user)
- **chat_messages** - AI chat conversation history
- **personality_insights** - AI-generated personality analysis

## 📱 App Screens

### Authentication Screens
- **Welcome Screen** - App introduction and initial sign-in
- **Phone Number Screen** - Phone verification and Google Sign-In

### Registration Screens
- **Create Profile** - Basic profile information
- **Personality Questions** - 10 personality assessment questions
- **Relationship Questions** - 5 relationship preference questions
- **Values Questions** - 5 values and goals questions
- **What Do You Want** - Optional descriptive text input

### Main App Screens
- **Profile Screen** - User profile with completion status
- **Chat AI Screen** - AI conversation interface
- **Settings Screen** - App settings and account management
- **Photo Gallery** - Photo management and editing

## 🎨 UI Features

### Design System
- **Cherry Blossom Theme** - Beautiful pink/white color scheme
- **Consistent Spacing** - Unified margins and padding
- **Modern Cards** - Clean, rounded interface elements
- **Responsive Layout** - Works on different screen sizes
- **Progress Indicators** - Visual feedback for multi-step processes

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
- **User Isolation** - Each user's chat data completely separate

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

## 🔍 Troubleshooting

### Common Issues

#### Backend Issues
- **Port 8001 in use**: Change port in uvicorn command
- **MongoDB connection failed**: Ensure MongoDB is running
- **Import errors**: Check Python virtual environment is activated
- **500 errors**: Check server logs for specific error messages

#### Frontend Issues
- **Metro bundler issues**: Clear cache with `npx react-native start --reset-cache`
- **Build errors**: Clean and rebuild with `cd android && ./gradlew clean`
- **Google Sign-In issues**: Check Google Services configuration
- **Network errors**: Verify backend server is running on correct IP

#### Database Issues
- **Collections not found**: They will be created automatically on first use
- **Data persistence issues**: Check MongoDB connection and permissions
- **User data isolation**: Each user's data is properly separated by user_id

### Debug Commands
```bash
# Check backend status
curl http://localhost:8001/

# Check MongoDB collections
mongo dating_app --eval "db.getCollectionNames()"

# Check user data
mongo dating_app --eval "db.users.find().pretty()"
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

- **Setup Issues**: Follow the complete setup guide above
- **API Limits**: Check Google AI Studio dashboard
- **Dependencies**: Ensure all packages are installed
- **Database**: MongoDB must be running and accessible
- **Network**: Ensure backend is accessible from frontend device

## 🎉 Current Status

### ✅ Completed Features
- **User Authentication** - Google Sign-In and phone verification
- **Multi-Step Registration** - Complete questionnaire flow
- **Profile Management** - Photo uploads and profile editing
- **AI Chat System** - Natural conversations with personality insights
- **Data Persistence** - User-specific data isolation
- **Progress Tracking** - Registration progress saved and restored
- **Completion Validation** - Ensures full questionnaire completion

### 🚧 In Progress
- **Matching Algorithm** - Using questionnaire insights for better matches
- **Advanced Analytics** - Relationship insights and trends

### 🔮 Future Features
- **Video Chat** - Real-time video conversations
- **Group Chats** - Community features
- **Push Notifications** - Real-time updates
- **Advanced Matching** - AI-powered compatibility scoring
