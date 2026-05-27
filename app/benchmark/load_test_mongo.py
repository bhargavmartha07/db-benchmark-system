import threading
import time

from app.generator.db_connections import (
    get_mongo_connection
)


QUERY_DURATION = 60
THREADS = 10

query_count = 0


def worker():

    global query_count

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$group": {

                "_id": {

                    "cohort_month":
                        "$user.cohort_month",

                    "user_id":
                        "$user.user_id"
                },

                "total_events": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "total_events": -1
            }
        },

        {
            "$limit": 10
        }
    ]

    end_time = time.time() + QUERY_DURATION

    while time.time() < end_time:

        list(
            db.events.aggregate(pipeline)
        )

        query_count += 1


def main():

    threads = []

    start = time.time()

    for _ in range(THREADS):

        t = threading.Thread(
            target=worker
        )

        t.start()

        threads.append(t)

    for t in threads:
        t.join()

    total_time = time.time() - start

    tps = query_count / total_time

    print(f"Total Queries: {query_count}")
    print(f"TPS: {tps:.2f}")


if __name__ == "__main__":
    main()