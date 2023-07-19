from dagster import multi_asset_sensor, asset, AssetExecutionContext, define_asset_job, AssetKey, AssetSelection, RunRequest, RetryPolicy

@asset(
    non_argument_deps={"summary"},
    compute_kind="powerbi",
    retry_policy=RetryPolicy(max_retries=3),
    group_name="downstream_data_product"
)
def bi_report(context: AssetExecutionContext):
    """ Updates the power BI report using the Power BI REST API"""
    # code to update a powerbi report, something like
    # refresh_url = 'https://api.powerbi.com/v1.0/myorg/groups/<INSERT GROUP ID>/datasets/<INSERT DATASET KEY>/refreshes'
    # header = {'Authorization': f'Bearer {access_token}'}
    # r = requests.post(url=refresh_url, headers=header)
    # r.raise_for_status()
    context.log.info("Updating Power BI Report")
    return

run_summary = define_asset_job(
    name="run_summary",
    selection=AssetSelection.keys(AssetKey("summary"), AssetKey("bi_report"))
)

# this sensor will be responsible for running the dbt model summary 
# and the bi report when users_cleaned and orders_cleaned are both materialized
@multi_asset_sensor(
    monitored_assets=[AssetKey("users_cleaned"), AssetKey("orders_cleaned")],
    job=run_summary
)
def monitor_summary_upstreams(context):
    asset_events = context.latest_materialization_records_by_key()
    # update from if all() to if any() to materialize when either upstream is changed
    if all(asset_events.values()):
        context.advance_all_cursors()
        return RunRequest()
