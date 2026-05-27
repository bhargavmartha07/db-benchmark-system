import json

from app.generator.db_connections import (
    get_mongo_connection
)


def explain_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$group": {

                "_id": "$user.user_id",

                "event_count": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "event_count": -1
            }
        },

        {
            "$limit": 10
        }
    ]

    result = db.command({

        "explain": {

            "aggregate": "events",

            "pipeline": pipeline,

            "cursor": {}
        },

        "verbosity": "executionStats"
    })

    print(
        json.dumps(
            result,
            indent=2,
            default=str
        )
    )


if __name__ == "__main__":
    explain_mongo()