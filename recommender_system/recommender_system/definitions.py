from dagster import Definitions, define_asset_job, AssetSelection, with_resources, EnvVar
from recommender_system.assets import core_assets, recommender_assets
from recommender_system.configs import job_data_config, job_training_config
from dagster_airbyte import AirbyteResource, build_airbyte_assets

# Define the Airbyte instance
airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    username=EnvVar("AIRBYTE_USER"),
    password=EnvVar("AIRBYTE_PASSWORD"),
)

airbyte_assets_connection_movies = with_resources(
    build_airbyte_assets(
        connection_id="e50425cb-eaf9-4af1-90b1-753016549a64",
        destination_tables=["movies"],
        destination_database="mlops",
        destination_schema="source",
    ),
    {"airbyte": airbyte_instance},
)

airbyte_assets_connection_scores = with_resources(
    build_airbyte_assets(
        connection_id="9de59fbe-9e59-45ad-8798-289a68bddc4a",
        destination_tables=["scores"],
        destination_database="mlops",
        destination_schema="source",
    ),
    {"airbyte": airbyte_instance},
)

airbyte_assets_connection_users = with_resources(
    build_airbyte_assets(
        connection_id="ff79d07f-8dee-43ba-a12e-67240320231d",
        destination_tables=["users"],
        destination_database="mlops",
        destination_schema="source",
    ),
    {"airbyte": airbyte_instance},
)

all_airbyte_assets = [
    *airbyte_assets_connection_movies,
    *airbyte_assets_connection_scores,
    *airbyte_assets_connection_users,
]

all_assets = [*core_assets, *recommender_assets, *all_airbyte_assets]

data_job = define_asset_job(
    name='get_data',
    selection=['core_movies', 'core_users', 'core_scores', 'training_data'],
    config=job_data_config
)

only_training_job = define_asset_job(
    "only_training",
    selection=AssetSelection.groups('recommender'),
    config=job_training_config
)

airbyte_sync_job = define_asset_job(
    name="airbyte_sync_job",
    selection=AssetSelection.assets(*all_airbyte_assets),
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        data_job,
        only_training_job,
        airbyte_sync_job
    ],
    )
