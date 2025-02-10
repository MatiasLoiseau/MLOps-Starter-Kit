import dagster as dg
from dagster_dbt import dbt_assets, DbtCliResource, DbtProject
from dagster import EnvVar, AssetExecutionContext
from pathlib import Path

# Ruta del proyecto DBT (ajusta en caso necesario)
#DBT_PROJECT_DIR = Path(__file__).resolve().parent.parent.parent / "db_postgres"

DBT_PROJECT_DIR = Path("/home/matias/workspace/MLOps-Started-Kit/recommender_system/db_postgres")

# Recurso para interactuar con DBT vía CLI
dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

# Prepara el proyecto si estás en modo desarrollo
dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=DBT_PROJECT_DIR / "target/manifest.json")
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    """Assets generados a partir de modelos dbt."""
    yield from dbt.cli(["build"], context=context).stream()
    