from db_connections import get_mongo_connection
from pymongo.errors import CollectionInvalid


def create_mongo_schema():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    # ----------------------------------------
    # USERS COLLECTION
    # ----------------------------------------

    try:
        db.create_collection("users")
        print("Created collection: users")

    except CollectionInvalid:
        print("Collection already exists: users")

    # ----------------------------------------
    # SESSIONS COLLECTION
    # ----------------------------------------

    try:
        db.create_collection("sessions")
        print("Created collection: sessions")

    except CollectionInvalid:
        print("Collection already exists: sessions")

    # ----------------------------------------
    # EVENTS TIME-SERIES COLLECTION
    # ----------------------------------------

    try:

        db.create_collection(
            "events",
            timeseries={
                "timeField": "created_at",
                "metaField": "user_id",
                "granularity": "hours"
            }
        )

        print("Created time-series collection: events")

    except CollectionInvalid:
        print("Collection already exists: events")

    # ----------------------------------------
    # INDEXES
    # ----------------------------------------

    db.events.create_index("event_type")
    db.events.create_index("session.session_id")
    db.events.create_index("user.cohort_month")
    db.events.create_index("created_at")

    print("MongoDB collections + indexes ready")