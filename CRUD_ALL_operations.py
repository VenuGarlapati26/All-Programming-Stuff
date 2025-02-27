# Importing libraries
from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Database connection details
server = 'dbpython1.database.windows.net'
database = 'Pythonapi'
username = 'venugarlapati'
password = 'Chowdary123$'
driver = '{ODBC Driver 18 for SQL Server}'


# Connecting to DB
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};'
            'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


# Define class Company
class Company(BaseModel):
    name: str
    location: str


# GET operation
@app.get("/company")
def get_all_companies():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to DB")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM company")
        rows = cursor.fetchall()
        companies = [
            {"CompanyID": row[0], "Name": row[1], "Location": row[2]}
            for row in rows
        ]

        return {"companies": companies}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")

    finally:
        cursor.close()
        conn.close()


# PUT operation
@app.put("/company/{name}")
def update_company(name: str, company: Company):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM company WHERE name = ?", (name,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Company not found")

        cursor.execute("UPDATE company SET name = ?, location = ? WHERE name = ?",
                       (company.name, company.location, name))
        conn.commit()

        return {"message": f"Company '{name}' updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()


# POST operation
@app.post("/company")
def create_company(company: Company):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM company WHERE name=?", (company.name,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Company already exists")

        cursor.execute("INSERT INTO company (name, location) VALUES (?, ?)", (company.name, company.location))
        conn.commit()

        return {"message": f"Company '{company.name}' created successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()


# DELETE operation
@app.delete("/company/{name}")
def delete_company(name: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Failed to connect to DB")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM company WHERE name=?", (name,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Company not found")

        cursor.execute("DELETE FROM company WHERE name=?", (name,))
        conn.commit()

        return {"message": f"Company '{name}' deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()


# Run the application
if __name__ == "__main__":
    uvicorn.run("CRUD_ALL_operations:app", host="0.0.0.0", port=8017, reload=True)
