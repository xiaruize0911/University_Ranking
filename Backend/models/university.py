from ..db.database import get_db_connection

def search_universities(query: str, limit: int = 50):
    conn = get_db_connection()
    like_query = f"%{query.lower()}%"
    cur = conn.execute("""
        SELECT id, name, country, city, photo
        FROM Universities
        WHERE LOWER(name) LIKE ?
           OR LOWER(normalized_name) LIKE ?
        LIMIT ?
    """, (like_query, like_query, limit))
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows
