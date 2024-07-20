## Running Locally
1 - Clone the repo
2 python -m venv venv
3  Windows run in bash
    - Run 'source venv/Scripts/activate'
    - Run 'pip install -r requirements.txt'
4 Update or create .env file based on the .env.local file
5 Update the database setting in .env
6 Update alembic.ini:
    sqlalchemy.url = mysql+pymsql://user:password@localhost/yourlocaldb
7
    