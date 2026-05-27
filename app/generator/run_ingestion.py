import time

from generate_data import (
    generate_user,
    generate_session,
    generate_event
)

from bulk_insert_postgres import (
    bulk_insert_users as pg_users,
    bulk_insert_sessions as pg_sessions,
    bulk_insert_events as pg_events
)

from bulk_insert_mongo import (
    bulk_insert_users as mongo_users,
    bulk_insert_sessions as mongo_sessions,
    bulk_insert_events as mongo_events
)


# ----------------------------------------
# TARGET DATASET SIZE
# ----------------------------------------

USER_COUNT = 100000
SESSION_COUNT = 1000000
EVENT_COUNT = 5000000

BATCH_SIZE = 20000


# ----------------------------------------
# CHUNK HELPER
# ----------------------------------------

def chunked(data, size):

    for i in range(0, len(data), size):
        yield data[i:i + size]


# ----------------------------------------
# MAIN INGESTION PIPELINE
# ----------------------------------------

def main():

    # ----------------------------------------
    # GENERATE USERS
    # ----------------------------------------

    print("Generating users...")

    users = [
        generate_user()
        for _ in range(USER_COUNT)
    ]

    # ----------------------------------------
    # GENERATE SESSIONS
    # ----------------------------------------

    print("Generating sessions...")

    sessions = []

    for i in range(SESSION_COUNT):

        user = users[i % USER_COUNT]

        sessions.append(
            generate_session(user)
        )

    # ----------------------------------------
    # INSERT USERS + SESSIONS
    # ----------------------------------------

    print("Inserting users + sessions...")

    start = time.time()

    # PostgreSQL

    for batch in chunked(users, BATCH_SIZE):
        pg_users(batch)

    for batch in chunked(sessions, BATCH_SIZE):
        pg_sessions(batch)

    # MongoDB

    for batch in chunked(users, BATCH_SIZE):
        mongo_users(batch)

    for batch in chunked(sessions, BATCH_SIZE):
        mongo_sessions(batch)

    setup_time = time.time() - start

    print(
        f"Users + sessions inserted in "
        f"{setup_time:.2f} seconds"
    )

    # ----------------------------------------
    # STREAM EVENTS IN BATCHES
    # ----------------------------------------

    print("Generating + inserting events...")

    start = time.time()

    event_batch = []

    for i in range(EVENT_COUNT):

        user = users[i % USER_COUNT]

        session = sessions[i % SESSION_COUNT]

        event_batch.append(
            generate_event(user, session)
        )

        # ----------------------------------------
        # INSERT BATCH
        # ----------------------------------------

        if len(event_batch) >= BATCH_SIZE:

            # PostgreSQL
            pg_events(event_batch)

            # MongoDB
            mongo_events(event_batch)

            print(
                f"Inserted {i + 1} / "
                f"{EVENT_COUNT} events"
            )

            # Free memory
            event_batch = []

    # ----------------------------------------
    # INSERT REMAINING EVENTS
    # ----------------------------------------

    if event_batch:

        pg_events(event_batch)
        mongo_events(event_batch)

    event_time = time.time() - start

    print(
        f"Event ingestion completed in "
        f"{event_time:.2f} seconds"
    )

    print("\nFULL INGESTION COMPLETED")


# ----------------------------------------
# ENTRYPOINT
# ----------------------------------------

if __name__ == "__main__":
    main()