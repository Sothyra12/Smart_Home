## Running Locally

### Requirements
1. Python 3.11
    Make sure Python is running on your machine.
1. Pip
1. MySQL server running locally
    Install MySQL server locally or use Docker to have a MySQL server
1. (Optional) MySQL Workbench to manage your database


### Steps:

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
    DATABASE_URL=mysql+pymysql://default:secret@localhost:3306/sampledb
    SECRET_KEY=randomstuffhere
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    GOOGLE_API_KEY=randomstuffhere
    SUPABASE_URL=http://127.0.0.1:54321
    SUPABASE_SERVICE_KEY=
    ```

1. Update the database settings in the `.env` file as necessary.

1. Create a new `alembic.ini` file by copying the `alembic.ini.example` file:
    ```ini
    sqlalchemy.url = mysql+pymysql://default:secret@localhost:3306/sampledb
    ```

1. Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```
