from db_connections import get_postgres_connection


def create_postgres_schema():

    conn = get_postgres_connection()
    cur = conn.cursor()

    print("Creating PostgreSQL schema...")

    # EXTENSIONS
    cur.execute("""
    CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
    """)

    cur.execute("""
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    """)

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        email TEXT NOT NULL,
        cohort_month TEXT,
        signup_date TIMESTAMP
    );
    """)

    # SESSIONS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id UUID PRIMARY KEY,
        user_id UUID REFERENCES users(user_id),
        device_type TEXT,
        start_time TIMESTAMP
    );
    """)

    # EVENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id UUID PRIMARY KEY,
        session_id UUID REFERENCES sessions(session_id),
        user_id UUID REFERENCES users(user_id),
        event_type TEXT,
        payload JSONB,
        created_at TIMESTAMP
    );
    """)

    # ----------------------------------------
    # STANDARD INDEXES
    # ----------------------------------------

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_sessions_user_id
    ON sessions(user_id);
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_session_id
    ON events(session_id);
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_created_at
    ON events(created_at);
    """)

    # ----------------------------------------
    # COMPOSITE INDEX
    # ----------------------------------------

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_session_created
    ON events(session_id, created_at);
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_user_created
    ON events(user_id, created_at);
    """)

    # ----------------------------------------
    # EVENT TYPE INDEX
    # ----------------------------------------

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_event_type
    ON events(event_type);
    """)

    # ----------------------------------------
    # JSONB GIN INDEX
    # ----------------------------------------

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_payload_gin
    ON events
    USING GIN(payload jsonb_path_ops);
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("PostgreSQL schema + indexes created successfully")