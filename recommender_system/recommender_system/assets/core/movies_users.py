from dagster import asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue
from dagster_mlflow import mlflow_tracking
from recommender_system.configs import data_ops_config
import pandas as pd

movies_categories_columns = [
    'unknown', 'Action', 'Adventure', 'Animation',
    "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
    'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']



@asset(
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=5),
    code_version="2",
    config_schema={'uri': String},
)
def core_movies(context) -> Output[pd.DataFrame]:
    uri = data_ops_config['core_movies']['config']['uri']
    result = pd.read_csv(uri)
    return Output(
        result,
        metadata={
            "Total rows": len(result),
            **result[movies_categories_columns].sum().to_dict(),
            "preview": MetadataValue.md(result.head().to_markdown()),
        },
    )


@asset
def users() -> Output[pd.DataFrame]:
    uri = data_ops_config['users']['config']['uri']
    result = pd.read_csv(uri)
    return Output(
        result,
        metadata={
            "Total rows": len(result),
            **result.groupby('Occupation').count()['id'].to_dict(),
        },
    )


@asset(
    resource_defs={'mlflow': mlflow_tracking}
    )
def scores(context) -> Output[pd.DataFrame]:
    uri = data_ops_config['scores']['config']['uri']
    result = pd.read_csv(uri)
    mlflow = context.resources.mlflow
    metrics = {
        "Total rows": len(result),
        "scores_mean": float(result['rating'].mean()),
        "scores_std": float(result['rating'].std()),
        "unique_movies": len(result['movie_id'].unique()),
        "unique_users": len(result['user_id'].unique())
    }
    mlflow.log_metrics(metrics)
    return Output(result, metadata=metrics)

@asset(ins={
    "scores": AssetIn(
        # key_prefix=["snowflake", "co  re"],
        # metadata={"columns": ["id"]}
    ),
    "core_movies": AssetIn(
        # key_prefix=["snowflake", "core"],
        # metadata={"columns": ["id"]}
    ),
    "users": AssetIn(
        # key_prefix=["snowflake", "core"],
        # metadata={"columns": ["id", "user_id", "parent"]}
    ),
})
def training_data(users: pd.DataFrame, core_movies: pd.DataFrame, scores: pd.DataFrame) -> Output[pd.DataFrame]:
    scores_users = pd.merge(scores, users, left_on='user_id', right_on='id')
    all_joined = pd.merge(scores_users, core_movies, left_on='movie_id', right_on='id')

    return Output(
        all_joined,
        metadata={
            "Total rows": len(all_joined)
        },
    )
