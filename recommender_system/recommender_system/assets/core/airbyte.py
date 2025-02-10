import dagster as dg
from dagster import EnvVar, with_resources
from dagster_airbyte import AirbyteResource, build_airbyte_assets

# Definir la instancia de Airbyte
airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    username=EnvVar("AIRBYTE_USER"),
    password=EnvVar("AIRBYTE_PASSWORD"),
)

# Assets para la conexión "movies"
airbyte_assets_connection_movies = with_resources(
    build_airbyte_assets(
        connection_id="e50425cb-eaf9-4af1-90b1-753016549a64",
        destination_tables=["movies"],
        destination_database="mlops",
        destination_schema="source",
        asset_key_prefix=["airbyte"],
    ),
    {"airbyte": airbyte_instance},
)

# Assets para la conexión "scores"
airbyte_assets_connection_scores = with_resources(
    build_airbyte_assets(
        connection_id="9de59fbe-9e59-45ad-8798-289a68bddc4a",
        destination_tables=["scores"],
        destination_database="mlops",
        destination_schema="source",
        asset_key_prefix=["airbyte"],
    ),
    {"airbyte": airbyte_instance},
)

# Assets para la conexión "users"
airbyte_assets_connection_users = with_resources(
    build_airbyte_assets(
        connection_id="ff79d07f-8dee-43ba-a12e-67240320231d",
        destination_tables=["users"],
        destination_database="mlops",
        destination_schema="source",
        asset_key_prefix=["airbyte"],
    ),
    {"airbyte": airbyte_instance},
)

# Colección de todos los assets de Airbyte
all_airbyte_assets = [
    *airbyte_assets_connection_movies,
    *airbyte_assets_connection_scores,
    *airbyte_assets_connection_users,
]
