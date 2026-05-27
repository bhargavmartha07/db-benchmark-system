from app.queries.postgres_queries import (
    rolling_revenue_postgres,
    cohort_top_performers_postgres,
    boundary_events_postgres,
    churn_risk_postgres,
    revenue_contribution_postgres
)

from app.queries.mongo_queries import (
    rolling_revenue_mongo,
    cohort_top_performers_mongo,
    boundary_events_mongo,
    churn_risk_mongo,
    revenue_contribution_mongo
)


# ----------------------------------------
# HELPER
# ----------------------------------------

def compare_lengths(pg, mongo, query_name):

    print(f"\n{query_name}")

    print("-" * 50)

    print(f"PostgreSQL rows : {len(pg)}")

    print(f"MongoDB rows    : {len(mongo)}")

    if len(pg) == len(mongo):

        print("STATUS: MATCH")

    else:

        print("STATUS: MISMATCH")


# ----------------------------------------
# MAIN VERIFICATION
# ----------------------------------------

def verify():

    # ----------------------------------------
    # QUERY 1
    # ----------------------------------------

    pg = rolling_revenue_postgres()

    mongo = rolling_revenue_mongo()

    compare_lengths(
        pg,
        mongo,
        "Rolling Revenue"
    )

    print("\nSample PostgreSQL Result:")

    for row in pg[:3]:
        print(row)

    print("\nSample MongoDB Result:")

    for row in mongo[:3]:
        print(row)

    # ----------------------------------------
    # QUERY 2
    # ----------------------------------------

    pg = cohort_top_performers_postgres()

    mongo = cohort_top_performers_mongo()

    compare_lengths(
        pg,
        mongo,
        "Cohort Top Performers"
    )

    # ----------------------------------------
    # QUERY 3
    # ----------------------------------------

    pg = boundary_events_postgres()

    mongo = boundary_events_mongo()

    compare_lengths(
        pg,
        mongo,
        "Boundary Events"
    )

    # ----------------------------------------
    # QUERY 4
    # ----------------------------------------

    pg = churn_risk_postgres()

    mongo = churn_risk_mongo()

    compare_lengths(
        pg,
        mongo,
        "Churn Risk"
    )

    # ----------------------------------------
    # QUERY 5
    # ----------------------------------------

    pg = revenue_contribution_postgres()

    mongo = revenue_contribution_mongo()

    compare_lengths(
        pg,
        mongo,
        "Revenue Contribution"
    )

    print("\nVERIFICATION COMPLETED")


# ----------------------------------------
# ENTRYPOINT
# ----------------------------------------

if __name__ == "__main__":
    verify()