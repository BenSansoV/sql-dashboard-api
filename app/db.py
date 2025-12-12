import duckdb

def get_connection():
    con = duckdb.connect(database="data/app.duckdb", read_only=False)

    con.execute("""
    CREATE TABLE IF NOT EXISTS sales (
      order_date DATE,
      region TEXT,
      category TEXT,
      amount DOUBLE,
      quantity INTEGER
    );
    """)

    count = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    if count == 0:
        con.execute("""
        INSERT INTO sales VALUES
        ('2025-01-01','North','A',120.5,2),
        ('2025-01-02','North','B',80.0,1),
        ('2025-01-02','South','A',200.0,4),
        ('2025-01-03','South','C',50.0,1),
        ('2025-01-03','East','B',300.0,6);
        """)
    return con
