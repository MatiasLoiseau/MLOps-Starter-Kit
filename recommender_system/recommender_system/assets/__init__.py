from dagster import load_assets_from_package_module
from . import core
from . import recommender

core_assets = load_assets_from_package_module(
    package_module=core, group_name='core',
    
)
recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)