import time
import statistics
import threading

from app.generator.db_connections import (
    get_postgres_connection
)


THREADS = 10
DURATION = 60

latencies = []


QUERY = """

SELECT

    u.cohort_month,

    u.user_id,

    COUNT(e.event_id) AS total_events

FROM users u

JOIN sessions s
    ON u.user_id = s.user_id

JOIN events e
    ON s.session_id = e.session_id

GROUP BY
    u.cohort_month,
    u.user_id

ORDER BY total_events DESC

LIMIT 10;

"""


def worker():

    conn = get_postgres_connection()

    cur = conn.cursor()

    end_time = time.time() + DURATION

    while time.time() < end_time:

        start = time.time()

        cur.execute(QUERY)

        cur.fetchall()

        elapsed = (
            time.time() - start
        ) * 1000

        latencies.append(elapsed)

    conn.close()


def percentile(data, percent):

    size = len(data)

    return sorted(data)[
        int(size * percent / 100)
    ]


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

    p95 = percentile(latencies, 95)

    avg = statistics.mean(latencies)

    print(f"Total Queries: {len(latencies)}")

    print(f"Average Latency: {avg:.2f} ms")

    print(f"P95 Latency: {p95:.2f} ms")

    print(f"Benchmark Duration: {total_time:.2f} sec")


if __name__ == "__main__":
    main()