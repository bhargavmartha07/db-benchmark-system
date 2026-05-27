from app.generator.db_connections import get_mongo_connection
from datetime import timedelta

def rolling_revenue_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$match": {
                "event_type": "purchase"
            }
        },

        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at"
                    }
                },

                "daily_avg": {
                    "$avg": "$payload.amount"
                }
            }
        },

        {
            "$sort": {
                "_id": 1
            }
        },

        {
            "$setWindowFields": {

                "sortBy": {
                    "_id": 1
                },

                "output": {

                    "rolling_7_day_avg": {

                        "$avg": "$daily_avg",

                        "window": {
                            "documents": [-6, 0]
                        }
                    }
                }
            }
        }
    ]

    results = list(
        db.events.aggregate(pipeline)
    )

    return results
def cohort_top_performers_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$group": {

                "_id": {

                    "cohort_month":
                        "$user.cohort_month",

                    "user_id":
                        "$user.user_id"
                },

                "total_events": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "total_events": -1
            }
        },

        {
            "$setWindowFields": {

                "partitionBy":
                    "$_id.cohort_month",

                "sortBy": {
                    "total_events": -1
                },

                "output": {

                    "rank_num": {
                        "$documentNumber": {}
                    }
                }
            }
        },

        {
            "$match": {
                "rank_num": {
                    "$lte": 10
                }
            }
        },

        {
            "$project": {

                "_id": 0,

                "cohort_month":
                    "$_id.cohort_month",

                "user_id":
                    "$_id.user_id",

                "total_events": 1
            }
        }
    ]

    results = list(
        db.events.aggregate(pipeline)
    )

    return results

def boundary_events_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$group": {

                "_id": "$user.user_id",

                "first_event": {
                    "$min": "$created_at"
                },

                "last_event": {
                    "$max": "$created_at"
                }
            }
        },

        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    results = list(
        db.events.aggregate(pipeline)
    )

    return results

def churn_risk_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$group": {

                "_id": "$user_id",

                "recent_sessions": {

                    "$sum": {

                        "$cond": [

                            {
                                "$gte": [

                                    "$start_time",

                                    {
                                        "$dateSubtract": {

                                            "startDate": "$$NOW",

                                            "unit": "day",

                                            "amount": 7
                                        }
                                    }
                                ]
                            },

                            1,
                            0
                        ]
                    }
                },

                "previous_sessions": {

                    "$sum": {

                        "$cond": [

                            {
                                "$and": [

                                    {
                                        "$gte": [

                                            "$start_time",

                                            {
                                                "$dateSubtract": {

                                                    "startDate": "$$NOW",

                                                    "unit": "day",

                                                    "amount": 14
                                                }
                                            }
                                        ]
                                    },

                                    {
                                        "$lt": [

                                            "$start_time",

                                            {
                                                "$dateSubtract": {

                                                    "startDate": "$$NOW",

                                                    "unit": "day",

                                                    "amount": 7
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },

                            1,
                            0
                        ]
                    }
                }
            }
        },

        {
            "$match": {

                "$expr": {

                    "$lt": [
                        "$recent_sessions",
                        "$previous_sessions"
                    ]
                }
            }
        },

        {
            "$sort": {
                "previous_sessions": -1
            }
        }
    ]

    results = list(
        db.sessions.aggregate(pipeline)
    )

    return results

def revenue_contribution_mongo():

    client = get_mongo_connection()

    db = client["benchmarkdb"]

    pipeline = [

        {
            "$match": {
                "event_type": "purchase"
            }
        },

        {
            "$setWindowFields": {

                "partitionBy": "$user.user_id",

                "output": {

                    "lifetime_total": {

                        "$sum": "$payload.amount",

                        "window": {
                            "documents": [
                                "unbounded",
                                "unbounded"
                            ]
                        }
                    }
                }
            }
        },

        {
            "$project": {

                "_id": 0,

                "user_id": "$user.user_id",

                "event_id": 1,

                "purchase_amount":
                    "$payload.amount",

                "revenue_percentage": {

                    "$round": [

                        {
                            "$multiply": [

                                {
                                    "$divide": [
                                        "$payload.amount",
                                        "$lifetime_total"
                                    ]
                                },

                                100
                            ]
                        },

                        2
                    ]
                }
            }
        }
    ]

    results = list(
        db.events.aggregate(pipeline)
    )

    return results