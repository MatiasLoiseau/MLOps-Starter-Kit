import dagster as dg
from dagster_dbt import dbt_assets, DbtCliResource, DbtProject
from dagster import EnvVar, AssetExecutionContext
from pathlib import Path

#change me
DBT_PROJECT_DIR = Path("/home/matias/workspace/MLOps-Started-Kit/recommender_system/db_postgres")

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=DBT_PROJECT_DIR / "target/manifest.json")
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    """Assets generados a partir de modelos dbt."""
    yield from dbt.cli(["build"], context=context).stream()
    