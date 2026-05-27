from postgres_schema import create_postgres_schema
from mongo_schema import create_mongo_schema


def main():

    print("Initializing schemas...")

    create_postgres_schema()
    create_mongo_schema()

    print("Setup completed")


if __name__ == "__main__":
    main()