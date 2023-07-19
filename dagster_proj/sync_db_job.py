from dagster import define_asset_job, AssetSelection, AssetKey

sync_database_job = define_asset_job(
    name="sync_database",
    selection=AssetSelection.keys(AssetKey("orders_cleaned")).upstream(),
    tags={"dagster/max_retries": "1"},
)