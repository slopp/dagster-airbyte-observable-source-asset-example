from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from dagster_airbyte import airbyte_resource
from dagster_dbt import dbt_cli_resource

from dagster_proj import assets
from dagster_proj.sync_db_job import sync_database_job
from dagster_proj.resources.db_io_manager import db_io_manager, POSTGRES_CONFIG
from dagster_proj.assets.airbyte_iaac import airbyte_instance
from dagster_proj.assets.airbyte_and_dbt import DBT_CONFIG 
from dagster_proj.resources.storage import MyStorage
from dagster_proj.assets.bi_report import monitor_summary_upstreams, run_summary, bi_report
from dagster._utils import file_relative_path

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    jobs=[sync_database_job, run_summary],
    resources={
        "storage": MyStorage(path=file_relative_path(__file__, "../data/users.csv")),
        "dbt": dbt_cli_resource.configured(DBT_CONFIG),
        "db_io_manager": db_io_manager.configured(POSTGRES_CONFIG),
    },
    schedules=[
        ScheduleDefinition(
            job=sync_database_job, cron_schedule="@daily"
        ),
    ],
    sensors=[monitor_summary_upstreams]
)
