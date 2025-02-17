from fastapi import FastAPI
import pyodbc
import uvicorn

app = FastAPI()

# ✅ Database Configuration
server = 'dbpython1.database.windows.net'
database = 'Pythonapi'
username = 'venugarlapati'
password = 'Chowdary123$'
driver = '{ODBC Driver 18 for SQL Server}'


# ✅ Function to Establish DB Connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
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
    cursor.execute("SELECT * FROM Company")  # Fetch all records
    rows = cursor.fetchall()

    companies = []
    for row in rows:
        companies.append({"CompanyID": row[0], "Name": row[1], "Location": row[2]})

    # ✅ Close the connection
    cursor.close()
    conn.close()

    return {"companies": companies}

if __name__ == "__main__":
    uvicorn.run("CRUD_GET_operation:app", host="0.0.0.0", port=5059, reload=True)