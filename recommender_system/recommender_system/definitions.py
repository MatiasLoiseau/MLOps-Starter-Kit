from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection
from recommender_system.configs import job_data_config, job_training_config

from recommender_system.assets import (
    core_assets, recommender_assets
)

# all_assets = load_assets_from_modules([movies_users])
all_assets = [*core_assets, *recommender_assets]





data_job = define_asset_job(
    name='get_data',
    selection=['movies', 'users', 'scores', 'training_data'],
    config=job_data_config
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        data_job,
        define_asset_job(
            "only_training",
            # selection=['preprocessed_training_data', 'user2Idx', 'movie2Idx'],
            selection=AssetSelection.groups('recommender'),
            config=job_training_config
        )
    ]
)
