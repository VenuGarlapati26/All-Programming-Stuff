#importing libraries
from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from pydantic import BaseModel
app = FastAPI()
#DB connection details
server = 'dbpython1.database.windows.net'
database = 'Pythonapi'
username = 'venugarlapati'
password = 'Chowdary123$'
driver = '{ODBC driver 18 for SQL server}'
# connecting to db
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};''encrypt=yes;TrustServerCertificate=no,COnnection Timeout=30;'
        )
        return conn
    except Exception as e:
        print(f"database connection failed: {e}")
        return None
# define delete operation
class Company(BaseModel):
    name:str
    location: str
@app.get("/company/{name")
def get_company(name: str):
    conn = get_db_connection()
    if not conn
        raise HTTPException(status_code=500, detail="failed to connect to db")
    cursor = conn.cursor()
    try:
        cursor.execute("select * from company")


