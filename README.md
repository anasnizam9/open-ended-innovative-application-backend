# AI Studio Backend

A FastAPI-based backend server with Google Gemini AI integration, user authentication, and PostgreSQL database support.

## Features

- **FastAPI Framework**: Modern, fast Python web framework
- **AI Integration**: Google Gemini API for content generation and analysis
- **Authentication**: JWT-based user authentication
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **CORS Support**: Cross-origin resource sharing enabled

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   export DATABASE_URL="postgresql://user:password@localhost/ai_studio"
   ```

3. **Start development server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Project Structure

```
backend/
├── routes/            # API route handlers
│   ├── auth.py       # Authentication endpoints
│   ├── ai.py         # AI service endpoints
│   └── dashboard.py  # Dashboard data endpoints
├── models.py         # Database models
├── database.py       # Database configuration
├── auth.py           # Authentication utilities
├── config.py         # Application configuration
├── main.py           # FastAPI application
└── requirements.txt  # Python dependencies
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### AI Services
- `POST /api/ai/generate-content` - Generate AI content
- `POST /api/ai/analyze-data` - Analyze data with AI
- `POST /api/ai/recommendations` - Get AI recommendations

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/analytics` - Get analytics data
- `GET /api/dashboard/projects` - Get user projects

## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost/ai_studio
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-secret-key-for-jwt-tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Setup

1. **Create database:**
   ```sql
   CREATE DATABASE ai_studio;
   ```

2. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

## Google Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Set the `GEMINI_API_KEY` environment variable

## Development

The backend runs on port 8000 and provides API endpoints for the frontend.

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Deployment

### Docker Deployment
```bash
docker build -t ai-studio-backend .
docker run -p 8000:8000 ai-studio-backend
```

### Direct Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Technologies Used

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **Google Gemini AI** - AI content generation
- **JWT** - JSON Web Tokens for authentication
- **Alembic** - Database migrations
- **Uvicorn** - ASGI server

## License

MIT License