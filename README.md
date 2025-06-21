# HRMS Project

This project is a Human Resources Management System (HRMS) with a FastAPI backend and a Next.js frontend.

## Project Structure

- `backend/`: Contains the FastAPI application, database migrations (Alembic), and business logic.
- `frontend/`: Contains the Next.js application for the user interface.
- `docker-compose.yml`: Defines the services for running the application using Docker.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (optional, for containerized deployment)

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate # On Windows
    # source venv/bin/activate # On macOS/Linux
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run database migrations:
    ```bash
    python -m alembic upgrade head
    ```
5.  Run the initial data script to create an admin user:
    ```bash
    python initial_data.py
    ```
6.  Start the FastAPI application:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    The backend will be accessible at `http://localhost:8000`.

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the dependencies:
    ```bash
    npm install
    ```
3.  Start the Next.js development server:
    ```bash
    npm run dev
    ```
    The frontend will be accessible at `http://localhost:3000`.

## Docker Deployment (Optional)

1.  Ensure Docker is running on your system.
2.  From the project root directory, build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```
    This will start both the backend and frontend services in Docker containers.

## API Endpoints

### Authentication

-   **Login:** `POST /api/v1/token`
    -   Request Body: `{"username": "your_email@example.com", "password": "your_password"}`
    -   Response: Access and refresh tokens.
-   **Register:** `POST /api/v1/register`
    -   Request Body: `{"email": "new_user@example.com", "password": "new_password"}`
    -   Response: Newly created user details.

## Database

The project uses SQLite for the database, with the database file located at `backend/app.db`.

## Troubleshooting

If you encounter issues with the database (e.g., `no such table` errors or `Table 'X' is already defined` errors), you can try the following steps to reset your database:

1.  **Delete the existing database file**:
    ```bash
    rm backend/app.db # On macOS/Linux
    del backend\app.db # On Windows
    ```
2.  **Re-run database migrations**:
    Navigate to the `backend` directory and run:
    ```bash
    python -m alembic upgrade head
    ```
3.  **Re-run the initial data script**:
    Navigate to the `backend` directory and run:
    ```bash
    python initial_data.py
    ```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.