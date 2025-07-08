from db.database import get_db_connection

def search_universities(query: str = None,sort_credit: str = "Universities.id" ,limit: int = 50):
    conn = get_db_connection()
    if query is not None:
        like_query = f"%{query.lower()}%"
    else:
        like_query = None 
    print(f"found query {query}, {like_query}, sort_credit {sort_credit}")
    
    valid_sort_columns = {"id", "name", "country", "city", "photo"}
    if sort_credit not in valid_sort_columns:
        sort_credit = "Universities.id" 

    like_query = f"%{query.lower()}%" if query else "%"

    sql = f"""
        SELECT DISTINCT Universities.id, name, country, city, photo, subject, rank_value
        FROM Universities
        JOIN Rankings ON Universities.normalized_name = Rankings.normalized_name
        JOIN UniversityStats ON Universities.normalized_name = UniversityStats.normalized_name
        WHERE (LOWER(name) LIKE '{like_query}' OR LOWER(Universities.normalized_name) LIKE '{like_query}' OR '{query}' IS NULL)
        AND (type = {sort_credit} or '{sort_credit}' = 'Universities.id')
        ORDER BY rank_value ASC NULLS LAST
        LIMIT {limit}
    """

    cur = conn.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

# sort is not completed!

