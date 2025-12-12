import re
from fastapi import HTTPException

BANNED = ["insert", "update", "delete", "drop", "alter", "create", "attach", "copy", "pragma"]

def validate_sql(sql: str):
    s = sql.strip().lower()

    if not s:
        raise HTTPException(status_code=400, detail="SQL vacío.")
    if ";" in s:
        raise HTTPException(status_code=400, detail="Solo una sentencia (sin ';').")
    if not s.startswith("select"):
        raise HTTPException(status_code=400, detail="Solo se permiten consultas SELECT.")
    if any(re.search(rf"\b{w}\b", s) for w in BANNED):
        raise HTTPException(status_code=400, detail="Consulta no permitida.")
