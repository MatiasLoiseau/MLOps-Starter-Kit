from dagster import Definitions, define_asset_job, AssetSelection, with_resources, EnvVar

from recommender_system.assets import core_assets, recommender_assets
from recommender_system.configs import job_data_config, job_training_config
from dagster_airbyte import AirbyteResource, build_airbyte_assets

airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    username=EnvVar("AIRBYTE_USER"),
    password=EnvVar("AIRBYTE_PASSWORD"),
)

airbyte_assets = with_resources(
    build_airbyte_assets(
        connection_id="e50425cb-eaf9-4af1-90b1-753016549a64",
        destination_tables=["movies"],
        destination_database="mlops",
        destination_schema="source",
    ),
    {"airbyte": airbyte_instance},
)


all_assets = [*core_assets, *recommender_assets, *airbyte_assets]

data_job = define_asset_job(
    name='get_data',
    selection=['core_movies', 'users', 'scores', 'training_data'],
    config=job_data_config
)

only_training_job = define_asset_job(
    "only_training",
    selection=AssetSelection.groups('recommender'),
    config=job_training_config
)

airbyte_sync_job = define_asset_job(
    name="airbyte_sync_job",
    selection=AssetSelection.assets(*airbyte_assets),  
    # Or: .upstream() / .required_multi_asset_neighbors() if you have multiple
    # Airbyte multi-assets that need to sync together
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        data_job,
        only_training_job,
        airbyte_sync_job
    ],
)
