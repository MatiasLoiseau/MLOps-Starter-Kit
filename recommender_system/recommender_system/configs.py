mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}

data_ops_config = {
    'core_movies': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
        }
    },
    'core_users': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv'
        }
    },
    'core_scores': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv'
        }
    }
}

job_data_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **data_ops_config,
    }
}

training_config = {
    'model_trained': {
        'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

job_training_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config
    }
}

training_config_20 = {
    'model_trained': {
        'config': {
            'batch_size': 256,
            'epochs': 20,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

job_training_config_20 = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config_20
    }
}
