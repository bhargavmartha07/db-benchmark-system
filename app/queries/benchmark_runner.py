import time

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

def benchmark():

    # ----------------------------------------
    # PostgreSQL Benchmark
    # ----------------------------------------

    start = time.time()

    pg_results = rolling_revenue_postgres()

    pg_time = time.time() - start

    print("\nPostgreSQL Results")
    print("-------------------")

    for row in pg_results[:5]:
        print(row)

    print(f"\nPostgreSQL Query Time: {pg_time:.4f} sec")

    # ----------------------------------------
    # MongoDB Benchmark
    # ----------------------------------------

    start = time.time()

    mongo_results = rolling_revenue_mongo()

    mongo_time = time.time() - start

    print("\nMongoDB Results")
    print("-------------------")

    for row in mongo_results[:5]:
        print(row)

    print(f"\nMongoDB Query Time: {mongo_time:.4f} sec")

        # ----------------------------------------
    # QUERY 2 — Cohort Top Performers
    # ----------------------------------------

    print("\n")
    print("=" * 50)
    print("QUERY 2 — Cohort Top Performers")
    print("=" * 50)

    # PostgreSQL

    start = time.time()

    pg_results = cohort_top_performers_postgres()

    pg_time = time.time() - start

    print("\nPostgreSQL Results")
    print("-------------------")

    for row in pg_results[:5]:
        print(row)

    print(f"\nPostgreSQL Query Time: {pg_time:.4f} sec")

    # MongoDB

    start = time.time()

    mongo_results = cohort_top_performers_mongo()

    mongo_time = time.time() - start

    print("\nMongoDB Results")
    print("-------------------")

    for row in mongo_results[:5]:
        print(row)

    print(f"\nMongoDB Query Time: {mongo_time:.4f} sec")

        # ----------------------------------------
    # QUERY 3 — Boundary Events
    # ----------------------------------------

    print("\n")
    print("=" * 50)
    print("QUERY 3 — Boundary Events")
    print("=" * 50)

    # PostgreSQL

    start = time.time()

    pg_results = boundary_events_postgres()

    pg_time = time.time() - start

    print("\nPostgreSQL Results")
    print("-------------------")

    for row in pg_results[:5]:
        print(row)

    print(f"\nPostgreSQL Query Time: {pg_time:.4f} sec")

    # MongoDB

    start = time.time()

    mongo_results = boundary_events_mongo()

    mongo_time = time.time() - start

    print("\nMongoDB Results")
    print("-------------------")

    for row in mongo_results[:5]:
        print(row)

    print(f"\nMongoDB Query Time: {mongo_time:.4f} sec")

        # ----------------------------------------
    # QUERY 4 — Churn Risk
    # ----------------------------------------

    print("\n")
    print("=" * 50)
    print("QUERY 4 — Churn Risk")
    print("=" * 50)

    # PostgreSQL

    start = time.time()

    pg_results = churn_risk_postgres()

    pg_time = time.time() - start

    print("\nPostgreSQL Results")
    print("-------------------")

    for row in pg_results[:5]:
        print(row)

    print(f"\nPostgreSQL Query Time: {pg_time:.4f} sec")

    # MongoDB

    start = time.time()

    mongo_results = churn_risk_mongo()

    mongo_time = time.time() - start

    print("\nMongoDB Results")
    print("-------------------")

    for row in mongo_results[:5]:
        print(row)

    print(f"\nMongoDB Query Time: {mongo_time:.4f} sec")

        # ----------------------------------------
    # QUERY 5 — Revenue Contribution
    # ----------------------------------------

    print("\n")
    print("=" * 50)
    print("QUERY 5 — Revenue Contribution")
    print("=" * 50)

    # PostgreSQL

    start = time.time()

    pg_results = revenue_contribution_postgres()

    pg_time = time.time() - start

    print("\nPostgreSQL Results")
    print("-------------------")

    for row in pg_results[:5]:
        print(row)

    print(f"\nPostgreSQL Query Time: {pg_time:.4f} sec")

    # MongoDB

    start = time.time()

    mongo_results = revenue_contribution_mongo()

    mongo_time = time.time() - start

    print("\nMongoDB Results")
    print("-------------------")

    for row in mongo_results[:5]:
        print(row)

    print(f"\nMongoDB Query Time: {mongo_time:.4f} sec")


if __name__ == "__main__":
    benchmark()