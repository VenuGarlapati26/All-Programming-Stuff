from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# ✅ Database Connection Configuration
server = 'dbpython1.database.windows.net'
database = 'Pythonapi'
username = 'venugarlapati'
password = 'Chowdary123$'
driver = '{ODBC Driver 18 for SQL Server}'

# ✅ Function to Connect to Azure SQL Database
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};'
            'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None  # Return None if connection fails

# ✅ Pydantic Model for Updating a Single Field
class LocationUpdate(BaseModel):
    location: str
    name: str


# ✅ PUT API to Update `Location` Field Only
@app.put("/company/{company_id}")
def update_company(company_id: int, data: LocationUpdate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to DB")

    cursor = conn.cursor()
    try:
        # ✅ Check if Company Exists
        cursor.execute("SELECT CompanyID FROM Company WHERE CompanyID = ?", (company_id,))
        existing_company = cursor.fetchone()
        if not existing_company:
            raise HTTPException(status_code=404, detail="Company not found")

        # ✅ Update Only the `Location` Field
        cursor.execute("UPDATE Company SET Location = ?, Name = ? WHERE CompanyID = ?", (data.location,data.name, company_id))
        conn.commit()

        return {"message": f"Company {company_id} location updated to {data.location}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

# ✅ Running Uvicorn Server
if __name__ == "__main__":
    uvicorn.run("CRUD_PUT_operation:app", host="0.0.0.0", port=8011, reload=True)
