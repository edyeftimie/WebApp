# Football Players Manager - Web Application
This web application allows users to efficiently manage a database of football players and teams.

## Features
### Backend (Fastapi)
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
### Backend Libraries
- SQLAlchemy: Using create_engine for connection, sessionmaker, declarative_base, and session for ORM.
- CORSMiddleware: Handles cross-origin resource sharing.
- FastAPI.Security: Provides security utilities and authentication tools.
- Pydantic: Data validation and configuration management.
- Uvicorn: ASGI server to run the FastAPI application.
