import os
import psycopg
from pymongo import MongoClient


def get_postgres_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "benchmarkdb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )


def get_mongo_connection():
    mongo_host = os.getenv("MONGO_HOST", "mongo")
    mongo_port = os.getenv("MONGO_PORT", "27017")
    client = MongoClient(
        f"mongodb://{mongo_host}:{mongo_port}/?directConnection=true"
    )
    return client