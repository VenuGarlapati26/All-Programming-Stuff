from fastapi import FastAPI
import pyodbc
import uvicorn
import os

app = FastAPI()

# ✅ Database Configuration (Using Environment Variables for Security)
server = os.getenv("DB_SERVER", "dbpython1.database.windows.net")
database = os.getenv("DB_NAME", "Pythonapi")
username = os.getenv("DB_USER", "venugarlapati")
password = os.getenv("DB_PASSWORD", "Chowdary123$")
driver = "{ODBC Driver 18 for SQL Server}"  # ✅ Fixed Syntax

# ✅ Function to Establish DB Connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
        return conn
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
        return None  # Return None if connection fails

# ✅ GET API to Fetch All Companies
@app.get("/company")
def get_all_companies():
    conn = get_db_connection()
    if not conn:
        return {"error": "Failed to connect to the database"}

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Company")  # Fetch all records
        rows = cursor.fetchall()

        companies = [
            {"CompanyID": row[0], "Name": row[1], "Location": row[2]}
            for row in rows
        ]

        return {"companies": companies}

    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

    finally:
        # ✅ Close the connection properly
        cursor.close()
        conn.close()

# ✅ Running Uvicorn Server
if __name__ == "__main__":
    uvicorn.run("CRUD_GET_operation:app", host="0.0.0.0", port=8010, reload=True)
