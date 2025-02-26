#importing required libraries
from http.client import HTTPException

from fastapi import FastAPI
import pyodbc
import uvicorn
from pydantic import BaseModel
#calling api
app = FastAPI()
#DB connection details
server='dbpython1.database.windows.net'
database = 'Pythonapi'
username = 'venugarlapati'
password = 'Chowdary123$'
driver = '{ODBC driver 18 for SQL server}'

#now connecting to db
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};''Encrypt=yes;TrustServerCertificate=no;ConnectionTimeout=30;'
        )
        return conn
    except Exception as e:
        print(f"database connection failed: {e}")
        return None
#defining delete operation
class Company(BaseModel):
    company_name: str
@app.delete("/company")
def delete_company(company: Company):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to the DataBase")
    cursor = conn.cursor()
    try:
        cursor.execute("select name from company where name=?", (company.company_name,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="company not found")
        cursor.execute("delete from Company where name=?",(company.company_name,))
        conn.commit()
        return {"messsge": f"company '{company.company_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"database error: {e}")
    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    uvicorn.run("CRUD_DELETE_operation:app", host="0.0.0.0", port=8015, reload=True)