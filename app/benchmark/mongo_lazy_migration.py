import time

from app.generator.db_connections import (
    get_mongo_connection
)


def migrate():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    start = time.time()

    result = db.sessions.update_many(

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

    print(f"Matched: {result.matched_count}")
    print(f"Modified: {result.modified_count}")
    print(f"Migration Time: {total_time:.4f} sec")


if __name__ == "__main__":
    migrate()