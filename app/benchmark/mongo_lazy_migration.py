import time

from app.generator.db_connections import (
    get_postgres_connection,
    get_mongo_connection
)


def migrate_postgres():

    conn = get_postgres_connection()
    cur = conn.cursor()

    start = time.time()

    cur.execute("""
        ALTER TABLE events
        ADD COLUMN IF NOT EXISTS app_version TEXT DEFAULT '1.0';
    """)

    conn.commit()

    total_time = time.time() - start

    cur.execute("""
        SELECT COUNT(*) FROM events WHERE app_version = '1.0';
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    print(f"PostgreSQL: ALTER TABLE completed in {total_time:.4f} sec")
    print(f"PostgreSQL: {count} rows now have app_version = '1.0'")


def migrate_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    start = time.time()

    result = db.events.update_many(

        {
            "app_version": {
                "$exists": False
            }
        },

        {
            "$set": {
                "app_version": "1.0.0"
            }
        }
    )

    total_time = time.time() - start

    print(f"MongoDB — Matched: {result.matched_count}")
    print(f"MongoDB — Modified: {result.modified_count}")
    print(f"MongoDB — Migration Time: {total_time:.4f} sec")


def migrate():

    print("=== PostgreSQL Schema Migration ===")
    migrate_postgres()

    print("\n=== MongoDB Schema Migration ===")
    migrate_mongo()


if __name__ == "__main__":
    migrate()