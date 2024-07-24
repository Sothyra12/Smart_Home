## Running Locally
1. Clone the repo:
    ```bash
    git clone <repository-url>
    ```
   
1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

1. Activate the virtual environment:
    - **Windows (run in bash)**
        ```bash
        source venv/Scripts/activate
        ```
    - **Mac and Linux**
        ```bash
        source venv/bin/activate
        ```

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

1. Update or create the `.env` file based on the `.env.local` file. Your `.env` file should contain the following:
    ```ini
    DATABASE_URL=mysql+pymysql://default:secret@localhost:3306/apptrakr
    SECRET_KEY=randomstuffhere
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    GOOGLE_API_KEY=randomstuffhere
    SUPABASE_URL=http://127.0.0.1:54321
    SUPABASE_SERVICE_KEY=
    ```

1. Update the database settings in the `.env` file as necessary.

1. Update `alembic.ini`:
    ```ini
    sqlalchemy.url = mysql+pymysql://default:secret@localhost:3306/apptrakr
    ```

1. Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```
