from dagster import observable_source_asset, asset, AssetExecutionContext, DataVersion, AutoMaterializePolicy
import pandas as pd
from dagster._utils import file_relative_path
from dagster_proj.resources.storage import MyStorage
import os

USERS_CSV_PATH = file_relative_path(__file__, "../../data/users.csv")

@observable_source_asset(
        auto_observe_interval_minutes=1,
        group_name="users_data_product"
)
def users_raw(storage: MyStorage):
    return DataVersion(str(storage.get_last_update_time()))

@asset(
    non_argument_deps={"users_raw"},
    io_manager_key="db_io_manager", 
    key_prefix="postgres_replica", 
    group_name="users_data_product", 
    auto_materialize_policy=AutoMaterializePolicy.eager()
)
def users(context: AssetExecutionContext):
    
    users_raw = pd.read_csv(USERS_CSV_PATH)

    # add any additional metadata
    context.add_output_metadata({
        "nrows": len(users_raw)
    })

    # the db io manager will handle writing this dataframe to the database table users
    return users_raw 

