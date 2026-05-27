import uuid
import random
from faker import Faker

fake = Faker()

EVENT_TYPES = ["page_view", "purchase", "click"]


# ----------------------------------------
# PAYLOAD GENERATION
# ----------------------------------------

def generate_payload(event_type):

    if event_type == "page_view":
        return {
            "url": random.choice(
                ["/home", "/dashboard", "/pricing"]
            ),
            "load_time_ms": random.randint(50, 500)
        }

    elif event_type == "purchase":
        return {
            "product_id": f"sku_{random.randint(100,999)}",
            "amount": round(random.uniform(10, 500), 2),
            "currency": "USD"
        }

    elif event_type == "click":
        return {
            "element_id": random.choice(
                ["btn_submit", "btn_buy", "nav_menu"]
            ),
            "x": random.randint(0, 1920),
            "y": random.randint(0, 1080)
        }


# ----------------------------------------
# USER GENERATION
# ----------------------------------------

def generate_user():

    signup_date = fake.date_time_this_year()

    return {
        "user_id": str(uuid.uuid4()),
        "email": fake.email(),
        "cohort_month": signup_date.strftime("%Y-%m"),
        "signup_date": signup_date
    }


# ----------------------------------------
# SESSION GENERATION
# ----------------------------------------

def generate_session(user):

    return {
        "session_id": str(uuid.uuid4()),

        "user_id": user["user_id"],

        "device_type": random.choice(
            ["mobile", "desktop"]
        ),

        "start_time": fake.date_time_this_year()
    }


# ----------------------------------------
# EVENT GENERATION (DENORMALIZED)
# ----------------------------------------

def generate_event(user, session):

    event_type = random.choice(EVENT_TYPES)

    return {

        "event_id": str(uuid.uuid4()),

        # ----------------------------------------
        # EMBEDDED USER CONTEXT
        # ----------------------------------------

        "user": {
            "user_id": user["user_id"],
            "cohort_month": user["cohort_month"]
        },

        # Required for time-series metaField
        "user_id": user["user_id"],

        # ----------------------------------------
        # EMBEDDED SESSION CONTEXT
        # ----------------------------------------

        "session": {
            "session_id": session["session_id"],
            "device_type": session["device_type"]
        },

        "event_type": event_type,

        "payload": generate_payload(event_type),

        "created_at": fake.date_time_this_year()
    }