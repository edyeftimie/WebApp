# Football Players Manager - Web Application
This web application allows users to efficiently manage a database of football players and teams.
The application and its database were deployed on AWS, ensuring scalability and cloud accessibility.

## Features
### Backend (Fastapi - Python)
- **CRUD Operations**: Full create, read, update, and delete functionality.
- **Authentication & Tokens**: Secure user authentication with token-based mechanisms.
- **Local Session Management**: Tracks user sessions locally.
- **Layered Architecture**: Organized into multiple layers for separation of concerns.
- **Encapsulation**: Ensures data hiding and structured access to methods.
- **Data Persistence**: Long-term storage and management of player/team data.
- **SQL ORM**: Utilizes object-relational mapping for database interactions.
- **Data Validation**: Ensures input data is correct before processing.
- **Error Handling**: Robust mechanisms to handle and report errors.
- **Fake Data Autogeneration**: Automatically generates mock data for testing.
### Frontend (React - JavaScript)
- **Add/Edit Forms**: Manage player and team information.
- **Table Display**: Displays teams and players in a table format.
- **Protected Routes**: Secure route access based on authentication.
- **Material UI Integration**: Enhances UI/UX with Material Design components.
- **Context Hooks**: Share data across components to avoid code repetition.
- **Charts**: Visualize data trends and statistics.
- **Online Status Check**: Internet connectivity and backend accessibility.
- **Environment Variables**: Secures sensitive information like API keys.

## Libraries
### Backend
- SQLAlchemy: Using create_engine for connection, sessionmaker, declarative_base, and session for ORM.
- CORSMiddleware: Handles cross-origin resource sharing.
- FastAPI.Security: Provides security utilities and authentication tools.
- Pydantic: Data validation and configuration management.
- Uvicorn: ASGI server to run the FastAPI application.
### Frontend
- React Hooks: useEffect, useState, useParams, useNavigate, useLocation.
- React Router DOM: For routing and navigation between views.
- Material UI (@mui): For Material Design UI components.
- Axios: For making HTTP requests to the backend.
