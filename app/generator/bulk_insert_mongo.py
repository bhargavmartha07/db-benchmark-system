from db_connections import get_mongo_connection


def bulk_insert_users(users):

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    db.users.insert_many(users)

    print(f"Inserted {len(users)} users into MongoDB")


def bulk_insert_sessions(sessions):

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    db.sessions.insert_many(sessions)

    print(f"Inserted {len(sessions)} sessions into MongoDB")


def bulk_insert_events(events):

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    db.events.insert_many(events)

    print(f"Inserted {len(events)} events into MongoDB")