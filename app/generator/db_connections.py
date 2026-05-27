import psycopg
from pymongo import MongoClient


def get_postgres_connection():
    return psycopg.connect(
        host="postgres",
        port=5432,
        dbname="benchmarkdb",
        user="postgres",
        password="postgres"
    )


def get_mongo_connection():
    client = MongoClient(
        "mongodb://mongo:27017/?directConnection=true"
    )
    return client