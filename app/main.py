from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

from .db import get_connection
from .security import validate_sql

app = FastAPI(title="SQL Dashboard API")

ALLOWED_ORIGINS = ["http://localhost:5173","http://127.0.0.1:5173","https://sql-dashboard-demo.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    sql: str

@app.get("/schema")
def schema():
    con = get_connection()
    cols = con.execute("DESCRIBE sales").fetchall()
    return {"table": "sales", "columns": [{"name": c[0], "type": c[1]} for c in cols]}

@app.post("/query")
def query(req: QueryRequest):
    validate_sql(req.sql)
    sql = req.sql.strip()

    if re.search(r"\blimit\b", sql.lower()) is None:
        sql = f"{sql} LIMIT 5000"

    try:
        con = get_connection()
        result = con.execute(sql)
        columns = [d[0] for d in result.description]
        rows = result.fetchall()
        return {"columns": columns, "rows": rows}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error SQL: {str(e)}")
