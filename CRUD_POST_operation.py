from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from pydantic import BaseModel
app = FastAPI()
server = 'dbpython1.database.windows.net'
database = 'Pythonapi'
username = 'venugarlapati'
password = 'Chowdary123$'
driver = '{ODBC Driver 18 for SQL Server}'

def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};''Encrypt=yes;TrustServerCertificate=no;ConnectionTimeout=30;'
        )
        return conn
    except Exception as e:
        print(f" Database connection failed: {e}")
        return None
class CompanyData(BaseModel):
    name:str
    location:str
@app.post("/company")
def insert_company(data: CompanyData):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to DB")
    cursor = conn.cursor()
    try:
        cursor.execute("insert into company (name, location) values(?, ?)", (data.name, data.location))
        conn.commit()
        return {"message": f"company '{data.name}' inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    uvicorn.run("CRUD_POST_operation:app", host="0.0.0.0", port = 8013, reload=True)
