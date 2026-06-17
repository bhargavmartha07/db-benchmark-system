# PostgreSQL vs MongoDB Benchmark System

A production-scale benchmarking platform designed to compare PostgreSQL and MongoDB across analytical workloads, schema flexibility, indexing strategies, concurrency behavior, and large-scale ingestion performance.

This project benchmarks:

- PostgreSQL 15+ with JSONB + GIN indexing
- MongoDB 7+ with Time-Series Collections
- Relational vs Document database architectures
- Analytical query execution performance
- Concurrent load behavior
- Schema migration strategies
- p95 latency under stress

---

# Project Objectives

The primary goal of this project is to evaluate:

- Relational vs document database tradeoffs
- Query planner efficiency
- Aggregation pipeline performance
- Window function performance
- Index utilization
- Denormalization benefits
- Scalability under concurrent load
- Schema evolution complexity

---

# System Architecture

The system consists of three major services orchestrated using Docker Compose.

```text
+------------------------------------------------------+
|                  Docker Compose Network              |
+------------------------------------------------------+

        +-----------------------------+
        |     Python Benchmark App    |
        |-----------------------------|
        | Faker Data Generator        |
        | Query Execution Engine      |
        | Benchmark Runner            |
        | Verification Framework      |
        +-------------+---------------+
                      |
        -----------------------------------------
        |                                       |
        v                                       v

+----------------------+        +----------------------+
|   PostgreSQL 15      |        |      MongoDB 7       |
|----------------------|        |----------------------|
| Normalized Schema    |        | Denormalized Schema  |
| JSONB + GIN Indexes  |        | Time-Series Events   |
| Window Functions     |        | Aggregation Pipelines|
| Relational Queries   |        | Replica Set Enabled  |
+----------------------+        +----------------------+
```

---

# Dataset Specification

Synthetic SaaS activity data was generated using Faker.

| Entity   | Count      |
|----------|------------|
| Users    | 100,000    |
| Sessions | 1,000,000  |
| Events   | 5,000,000  |

---

# Data Model

## Users

```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "cohort_month": "2026-01",
  "signup_date": "2026-01-12"
}
```

---

## Sessions

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "device_type": "mobile",
  "start_time": "2026-02-01T12:30:00"
}
```

---

## Events

```json
{
  "event_id": "uuid",
  "event_type": "purchase",
  "payload": {
    "product_id": "sku_123",
    "amount": 99.99,
    "currency": "USD"
  },
  "created_at": "2026-03-01T08:12:00"
}
```

---

# PostgreSQL Features

## Normalized Schema

Tables:

- users
- sessions
- events

---

## JSONB Payload Storage

Event payloads are stored using:

```sql
payload JSONB
```

---

## Indexing Strategy

### Composite Index

```sql
CREATE INDEX idx_events_session_created
ON events(session_id, created_at);
```

### GIN Index

```sql
CREATE INDEX idx_events_payload_gin
ON events
USING GIN(payload jsonb_path_ops);
```

### Event Type Index

```sql
CREATE INDEX idx_events_event_type
ON events(event_type);
```

### Composite User-Time Index

```sql
CREATE INDEX idx_events_user_created
ON events(user_id, created_at);
```

---

# MongoDB Features

## Denormalized Events

MongoDB embeds:

- user context
- session context

directly into event documents.

---

## Time-Series Collection

```javascript
db.createCollection("events", {
  timeseries: {
    timeField: "created_at",
    metaField: "user_id",
    granularity: "hours"
  }
})
```

---

## Compound Index

```javascript
db.events.createIndex({ user_id: 1, created_at: -1 })
```

---

## Replica Set Configuration

MongoDB runs as a single-node replica set:

```bash
mongod --replSet rs0 --bind_ip_all
```

---

# Analytical Benchmark Queries

The benchmark suite contains 5 complex analytical workloads.

---

## 1. 7-Day Rolling Revenue

Calculates rolling average purchase amount over the previous 7 days.

### PostgreSQL

- Window Functions
- OVER()
- Aggregation

### MongoDB

- Aggregation Pipelines
- $setWindowFields

---

## 2. Cohort Top Performers

Finds top users within signup-month cohorts.

### PostgreSQL

- JOINs
- GROUP BY
- Aggregation

### MongoDB

- Aggregation Pipelines
- Denormalized filtering

---

## 3. Boundary Events

Finds first and last event timestamps for every user.

### PostgreSQL

- Composite index optimization

### MongoDB

- Aggregation grouping

---

## 4. Churn Risk Detection

Detects users whose recent session activity declined.

### PostgreSQL

- Conditional aggregation
- Session window comparisons

### MongoDB

- Session collection aggregation
- Temporal filtering

---

## 5. Revenue Contribution

Calculates percentage contribution of purchases to user lifetime value.

### PostgreSQL

- Window Functions

### MongoDB

- Aggregation pipelines
- Group accumulators

---

# Benchmarking Methodology

---

## PostgreSQL Profiling

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT ...
```

Metrics analyzed:

- Index scans
- Sequential scans
- Buffer hits
- Disk reads
- Execution plans

---

## MongoDB Profiling

```javascript
db.events.aggregate([...]).explain("executionStats")
```

Metrics analyzed:

- totalDocsExamined
- executionTimeMillis
- index usage
- collection scans

---

# Concurrent Load Testing

The benchmark system simulates concurrent analytical traffic.

---

## PostgreSQL

Tool used:

```bash
python -m app.benchmark.p95_benchmark
```

---

## MongoDB

Custom multithreaded Python benchmark runner.

---

# p95 Latency Benchmarking

Concurrent analytical queries were executed using:

- 10 worker threads
- 60-second benchmark duration

Measured:

- average latency
- p95 latency
- total throughput

---

# Benchmark Results

| Query | PostgreSQL | MongoDB |
|-------|------------|----------|
| Rolling Revenue | 2.26s | 18.10s |
| Cohort Top Performers | 3.36s | 4.94s |
| Boundary Events | 1.96s | 4.69s |
| Churn Risk | 1.78s | 1.81s |
| Revenue Contribution | 19.30s | 21.54s |

---

# p95 Latency Results

| Metric | Value |
|--------|--------|
| Total Queries | 21 |
| Average Latency | 31559 ms |
| p95 Latency | 66024 ms |
| Duration | 68 sec |

---

# Key Findings

## PostgreSQL Strengths

- Excellent relational query optimization
- Strong window function performance
- Efficient JOIN execution
- Mature query planner
- Powerful JSONB indexing

---

## MongoDB Strengths

- Flexible schema evolution
- Efficient denormalized reads
- Strong aggregation framework
- Time-series ingestion optimization
- Horizontal scalability architecture

---

# Schema Migration Experiment

The migration script at `app/benchmark/mongo_lazy_migration.py` runs both PostgreSQL and MongoDB migrations sequentially and measures execution time.

## PostgreSQL

```sql
ALTER TABLE events
ADD COLUMN app_version TEXT DEFAULT '1.0';
```

### Observations

- Strict schema enforcement via ALTER TABLE
- Locking behavior depends on table size and write load
- Strong consistency guarantees after migration
- Timed automatically by the migration script

---

## MongoDB

```javascript
db.events.updateMany(
  { app_version: { $exists: false } },
  { $set: { app_version: "1.0.0" } }
)
```

### Observations

- Flexible schema evolution with no downtime
- Lazy migration strategy using conditional updates
- No rigid schema enforcement required
- Target collection is events (not sessions)

---

# Dockerized Setup

---

## Start Services

```bash
docker compose up -d
```

---

## Initialize Mongo Replica Set

```bash
docker exec -it mongo_benchmark mongosh
```

```javascript
rs.initiate()
```

---

## Create Schemas

```bash
docker exec -it benchmark_app python app/generator/main.py
```

---

## Generate Dataset

```bash
docker exec -it benchmark_app python app/generator/run_ingestion.py
```

---

# Run Benchmark Suite

```bash
docker exec -it benchmark_app python -m app.queries.benchmark_runner
```

---

# Run Verification Framework

```bash
docker exec -it benchmark_app python -m app.benchmark.verify_results
```

---

# Run p95 Benchmark

```bash
docker exec -it benchmark_app python -m app.benchmark.p95_benchmark
```

---

# Project Structure

```text
db-benchmark-system/
│
├── app/
│   ├── generator/
│   ├── queries/
│   ├── benchmark/
│
├── docker-compose.yml
├── Dockerfile
├── benchmark_report.json
├── submission.json
├── README.md
│
└── requirements.txt
```

---

# Generate Benchmark Report

```bash
docker exec -it benchmark_app python -m app.benchmark.generate_report
```

The report is written to `benchmarks/report.json` containing:
- Execution times for all 5 queries on both databases
- Insert throughput (TPS) metrics
- p95 latency metrics

---

# Run Schema Migration

```bash
docker exec -it benchmark_app python -m app.benchmark.mongo_lazy_migration
```

Runs ALTER TABLE on PostgreSQL and updateMany on MongoDB, timing both operations.

---

# Technologies Used

- Python 3.11
- PostgreSQL 15
- MongoDB 7
- Docker
- Docker Compose
- Faker
- Psycopg
- PyMongo
- pgbench

---

# Final Conclusion

This benchmark demonstrates the tradeoffs between relational and document-oriented database systems under analytical workloads.

PostgreSQL excelled in:

- relational joins
- window functions
- structured analytical queries

MongoDB excelled in:

- schema flexibility
- denormalized reads
- time-series ingestion

Both systems proved capable of handling multi-million-row analytical workloads effectively when indexed and modeled appropriately.

---

# Author

Bhargav


Backend Engineering & Database Benchmarking Project