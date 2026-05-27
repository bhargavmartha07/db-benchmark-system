import json

from app.generator.db_connections import (
    get_postgres_connection
)


def explain_query(query):

    conn = get_postgres_connection()

    cur = conn.cursor()

    explain_sql = f"""
    EXPLAIN (
        ANALYZE,
        BUFFERS,
        FORMAT JSON
    )
    {query}
    """

    cur.execute(explain_sql)

    result = cur.fetchone()[0]

    conn.close()

    return result


if __name__ == "__main__":

    query = """

    SELECT

        s.user_id,

        COUNT(e.event_id)

    FROM sessions s

    JOIN events e
        ON s.session_id = e.session_id

    GROUP BY s.user_id

    ORDER BY COUNT(e.event_id) DESC

    LIMIT 10;
    """

    result = explain_query(query)

    print(
        json.dumps(
            result,
            indent=2
        )
    )