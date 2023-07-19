
import pandas as pd
from dagster import asset
from dagster_airbyte import load_assets_from_connections
from dagster_dbt import load_assets_from_dbt_project
from dagster._utils import file_relative_path
from dagster_proj.assets.airbyte_iaac import airbyte_instance, postgres_to_postgres

DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_project")
DBT_PROFILES_DIR = file_relative_path(__file__, "../../dbt_project/config")
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}

airbyte_assets = load_assets_from_connections(
    airbyte=airbyte_instance, 
    connections=[postgres_to_postgres], 
    key_prefix="postgres_replica",
    connection_to_group_fn= lambda x: "orders_data_product"
)


order_dbt_asset = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, io_manager_key="db_io_manager",
    select="orders_cleaned",
    node_info_to_group_fn=lambda x: "orders_data_product"
)

users_dbt_asset = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, io_manager_key="db_io_manager",
    select="users_cleaned",
    node_info_to_group_fn=lambda x: "users_data_product"
)

summary_dbt_asset = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, io_manager_key="db_io_manager",
    select="summary",
    node_info_to_group_fn=lambda x: "downstream_data_product"
)




