import dagster as dg
from dagster import (
    Definitions,
    define_asset_job,
    AssetSelection,
)
from recommender_system.assets import recommender_assets
from recommender_system.configs import job_training_config, job_training_config_20
from recommender_system.assets.core.airbyte import all_airbyte_assets
from recommender_system.assets.core.dbt import dbt_models, dbt_resource
all_assets = [
    *all_airbyte_assets,
    dbt_models,
    *recommender_assets,
]

only_training_job = define_asset_job(
    "only_training",
    selection=AssetSelection.groups("recommender"),
    config=job_training_config
)

airbyte_sync_job = define_asset_job(
    name="airbyte_sync_job",
    selection=AssetSelection.assets(*all_airbyte_assets),
)

dbt_job = define_asset_job(
    name="dbt_job",
    selection=AssetSelection.assets(dbt_models),
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        only_training_job,
        airbyte_sync_job,
        dbt_job
    ],
    resources={
        "dbt": dbt_resource
    }
)
