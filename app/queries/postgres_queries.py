from app.generator.db_connections import get_postgres_connection


def rolling_revenue_postgres():

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        query = """
        WITH daily_revenue AS (

            SELECT
                DATE(created_at) AS revenue_day,

                AVG(
                    (payload->>'amount')::numeric
                ) AS daily_avg

            FROM events

            WHERE event_type = 'purchase'

            GROUP BY revenue_day
        )

        SELECT
            revenue_day,

            ROUND(
                AVG(daily_avg)
                OVER (
                    ORDER BY revenue_day
                    ROWS BETWEEN 6 PRECEDING
                    AND CURRENT ROW
                ),
                2
            ) AS rolling_7_day_avg

        FROM daily_revenue

        ORDER BY revenue_day;
        """

        cur.execute(query)

        results = cur.fetchall()

    conn.close()

    return results
def cohort_top_performers_postgres():

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        query = """

        WITH user_event_counts AS (

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
        ),

        ranked_users AS (

            SELECT

                cohort_month,

                user_id,

                total_events,

                ROW_NUMBER()
                OVER (
                    PARTITION BY cohort_month
                    ORDER BY total_events DESC
                ) AS rank_num

            FROM user_event_counts
        )

        SELECT
            cohort_month,
            user_id,
            total_events

        FROM ranked_users

        WHERE rank_num <= 10

        ORDER BY
            cohort_month,
            total_events DESC;
        """

        cur.execute(query)

        results = cur.fetchall()

    conn.close()

    return results

def boundary_events_postgres():

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        query = """

        SELECT

            s.user_id,

            MIN(e.created_at) AS first_event,

            MAX(e.created_at) AS last_event

        FROM sessions s

        JOIN events e
            ON s.session_id = e.session_id

        GROUP BY s.user_id

        ORDER BY s.user_id;
        """

        cur.execute(query)

        results = cur.fetchall()

    conn.close()

    return results

def churn_risk_postgres():

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        query = """

        WITH session_windows AS (

            SELECT

                user_id,

                COUNT(
                    CASE
                        WHEN start_time >= NOW() - INTERVAL '7 days'
                        THEN 1
                    END
                ) AS recent_sessions,

                COUNT(
                    CASE
                        WHEN start_time >= NOW() - INTERVAL '14 days'
                         AND start_time < NOW() - INTERVAL '7 days'
                        THEN 1
                    END
                ) AS previous_sessions

            FROM sessions

            GROUP BY user_id
        )

        SELECT
            user_id,
            recent_sessions,
            previous_sessions

        FROM session_windows

        WHERE recent_sessions < previous_sessions

        ORDER BY
            previous_sessions DESC;
        """

        cur.execute(query)

        results = cur.fetchall()

    conn.close()

    return results

def revenue_contribution_postgres():

    conn = get_postgres_connection()

    with conn.cursor() as cur:

        query = """

        SELECT

            s.user_id,

            e.event_id,

            (e.payload->>'amount')::numeric AS purchase_amount,

            ROUND(

                (
                    (e.payload->>'amount')::numeric

                    /

                    SUM(
                        (e.payload->>'amount')::numeric
                    )

                    OVER (
                        PARTITION BY s.user_id
                    )

                ) * 100,

                2

            ) AS revenue_percentage

        FROM events e

        JOIN sessions s
            ON e.session_id = s.session_id

        WHERE e.event_type = 'purchase'

        ORDER BY
            s.user_id;
        """

        cur.execute(query)

        results = cur.fetchall()

    conn.close()

    return results