# pylint: disable=print-call
"""
A basic script that will create tables in the source postgres database, then automatically
create an Airbyte Connection between the source database and destination database.
"""
# pylint: disable=print-call
import random
import string

import numpy as np
import pandas as pd
from dagster_postgres.utils import get_conn_string
from dagster._utils import file_relative_path
from dagster_proj.resources.db_io_manager import POSTGRES_BASE_CONFIG

PG_SOURCE_CONFIG = POSTGRES_BASE_CONFIG
PG_SOURCE_CONFIG["database"] = "postgres"


# configures the number of records for each table
N_USERS = 100
N_ORDERS = 10000
USER_CSV_PATH = file_relative_path(__file__, "../../data/users.csv")

def _random_dates():
    start = pd.to_datetime("2021-01-01")
    end = pd.to_datetime("2022-01-01")

    start_u = start.value // 10**9
    end_u = end.value // 10**9

    dist = np.random.standard_exponential(size=N_ORDERS) / 10

    clipped_flipped_dist = 1 - dist[dist <= 1]
    clipped_flipped_dist = clipped_flipped_dist[:-1]

    if len(clipped_flipped_dist) < N_ORDERS:
        clipped_flipped_dist = np.append(
            clipped_flipped_dist, clipped_flipped_dist[: N_ORDERS - len(clipped_flipped_dist)]
        )

    return pd.to_datetime((clipped_flipped_dist * (end_u - start_u)) + start_u, unit="s")


def add_data():
    con_string = get_conn_string(
        username=PG_SOURCE_CONFIG["username"],
        password=PG_SOURCE_CONFIG["password"],
        hostname=PG_SOURCE_CONFIG["host"],
        port=str(PG_SOURCE_CONFIG["port"]),
        db_name=PG_SOURCE_CONFIG["database"],
    )

    users = pd.DataFrame(
        {
            "user_id": range(N_USERS),
            "username": [random.choice(string.ascii_letters) for _ in range(N_USERS)],
        }
    )

    users.to_csv(USER_CSV_PATH)
    print("Created users data.")
   

    orders = pd.DataFrame(
        {
            "user_id": [random.randint(0, N_USERS) for _ in range(N_ORDERS)],
            "order_time": _random_dates(),
            "order_value": np.random.normal(loc=100.0, scale=15.0, size=N_ORDERS),
        }
    )

    orders.to_sql("orders", con=con_string, if_exists="replace")
    print("Created orders table.")


add_data()

next_step = """
    Data added to postgres source. Be sure to create sink database by running:
    PGPASSWORD=password psql -h localhost -p 5432 -U postgres -d postgres -c "CREATE DATABASE postgres_replica;"
"""
print(next_step)
