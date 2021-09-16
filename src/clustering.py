from log import get_manager, log_detail
from load_data import read_params, pd
from sklearn.cluster import KMeans
from scale_data import fit_robust_scalar, fit_standard_scalar, transform_robust_test, transform_standard_test
from pickle import dump, load
import json
import argparse


def generate_schema(train, schema_path, target, logger):
    try:
        log_detail(logger, ["inside clustering.py, inside function generate_schema"])
        cols = list(train.columns)
        cols.remove(target)
        schema = {"cols": cols}

        with open(schema_path, "w") as f:
            json.dump(schema, f)
        log_detail(logger, ["Successfully generated schema"])
    except Exception as e:
        log_detail(logger, [str(e)])


def cluster_train_data(train, n_clusters, cluster_model_path, cluster_col, target, random_state, logger):
    try:
        log_detail(logger, ["inside clustering.py, inside function cluster_train_data"])
        cluster = KMeans(n_clusters=n_clusters, random_state=random_state)
        cluster.fit(train.drop(target, axis=1))

        with open(cluster_model_path, "wb") as f:
            dump(cluster, f)

        train[cluster_col] = cluster.labels_
        log_detail(logger, ["Successfully clustered train data"])
        return train
    except Exception as e:
        log_detail(logger, [str(e)])


def cluster_test_data(test, cluster_model_path, cluster_col, target, logger):
    try:
        log_detail(logger, ["inside clustering.py, inside function cluster_test_data"])
        with open(cluster_model_path, "rb") as f:
            cluster = load(f)

        test[cluster_col] = cluster.predict(test.drop(target, axis=1))
        log_detail(logger, ["Successfully clustered test data"])
        return test
    except Exception as e:
        log_detail(logger, [str(e)])


def export_master_data(config_path_, logger):
    try:
        log_detail(logger, ["inside clustering.py, inside function export_master_data"])
        config = read_params(config_path_, logger)
        robust_scalar_path = config["cluster"]["robust_scalar"]
        standard_scalar_path = config["cluster"]["standard_scalar"]
        scalar_schema_path = config["cluster"]["scalar_schema_path"]
        encoder_path = config["scale_data"]["encoders"]
        master_encoder_path = config["cluster"]["encoders"]
        train_path = config["scale_data"]["scaled_train_path"]
        test_path = config["scale_data"]["scaled_test_path"]
        target = config["base"]["target_col"]
        n_clusters = config["cluster"]["kmeans"]["n_clusters"]
        cluster_col = config["cluster"]["cluster_col"]
        cluster_model_path = config["cluster"]["cluster_model"]
        master_train = config["cluster"]["master_train"]
        master_test = config["cluster"]["master_test"]
        random_state = config["base"]["random_state"]

        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)

        train = cluster_train_data(train, n_clusters, cluster_model_path, cluster_col, target, random_state, logger)
        test = cluster_test_data(test, cluster_model_path, cluster_col, target, logger)

        generate_schema(train, scalar_schema_path, target, logger)

        train = fit_robust_scalar(train, robust_scalar_path, robust_scalar_path, target, logger)
        train = fit_standard_scalar(train, standard_scalar_path, robust_scalar_path, target, logger)

        test = transform_robust_test(test, robust_scalar_path, target, logger)
        test = transform_standard_test(test, standard_scalar_path, target, logger)

        with open(encoder_path, "rb") as f:
            encoder = load(f)

        with open(master_encoder_path, "wb") as f:
            dump(encoder, f)

        train.to_csv(master_train, index=False)
        test.to_csv(master_test, index=False)
        log_detail(logger, ["Successfully exported master data"])
    except Exception as e:
        log_detail(logger, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    export_master_data(config_path, manager)
