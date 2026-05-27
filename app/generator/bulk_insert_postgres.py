from db_connections import get_postgres_connection
from psycopg.rows import dict_row
from psycopg import sql

import psycopg


def bulk_insert_users(users):

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        cur.executemany(
            """
            INSERT INTO users (
                user_id,
                email,
                cohort_month,
                signup_date
            )
            VALUES (%s, %s, %s, %s)
            """,

            [
                (
                    u["user_id"],
                    u["email"],
                    u["cohort_month"],
                    u["signup_date"]
                )
                for u in users
            ]
        )

    conn.commit()
    conn.close()

    print(f"Inserted {len(users)} users into PostgreSQL")


def bulk_insert_sessions(sessions):

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        cur.executemany(
            """
            INSERT INTO sessions (
                session_id,
                user_id,
                device_type,
                start_time
            )
            VALUES (%s, %s, %s, %s)
            """,

            [
                (
                    s["session_id"],
                    s["user_id"],
                    s["device_type"],
                    s["start_time"]
                )
                for s in sessions
            ]
        )

    conn.commit()
    conn.close()

    print(f"Inserted {len(sessions)} sessions into PostgreSQL")


def bulk_insert_events(events):

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        cur.executemany(
            """
            INSERT INTO events (
                event_id,
                session_id,
                event_type,
                payload,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s)
            """,

            [
                (
                    e["event_id"],
                    e["session"]["session_id"],
                    e["event_type"],
                    psycopg.types.json.Jsonb(e["payload"]),
                    e["created_at"]
                )
                for e in events
            ]
        )

    conn.commit()
    conn.close()

    print(f"Inserted {len(events)} events into PostgreSQL")