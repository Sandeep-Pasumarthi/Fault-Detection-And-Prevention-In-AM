from log import get_manager, log_detail
from load_data import read_params, pd
from sklearn.preprocessing import RobustScaler, StandardScaler, OrdinalEncoder
from pickle import dump, load
import json
import argparse


def generate_schema(train, encoder_schema_path, robust_standard_schema_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_data.py, inside generate_schema function"])
        encode_cols = list(train.select_dtypes(include=['object']).columns)
        encoder_schema = {"cols": encode_cols}

        with open(encoder_schema_path, "w") as f:
            json.dump(encoder_schema, f)

        scalar_cols = list(train.drop(target, axis=1).columns)
        scalar_schema = {"cols": scalar_cols}

        with open(robust_standard_schema_path, "w") as f:
            json.dump(scalar_schema, f)

        log_detail(logger, ["Successfully generated schema"])
    except Exception as e:
        log_detail(logger, [str(e)])


def fit_encoder(train, encoder_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_data.py, inside fit_encoder function"])
        encoder = OrdinalEncoder()
        encode_cols = list(train.select_dtypes(include=['object']).columns)
        if target in encode_cols:
            encode_cols.remove(target)
        encode_data = train[encode_cols]
        encode_data = encoder.fit_transform(encode_data)
        train[encode_cols] = encode_data

        with open(encoder_path, "wb") as f:
            dump(encoder, f)

        log_detail(logger, ["Successfully fitted encoder to train"])
        return train
    except Exception as e:
        log_detail(logger, [str(e)])


def fit_robust_scalar(train, scalar_path, master_scalar_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_Data.py, inside fit_robust_scalar function"])
        scalar = RobustScaler()
        scaled_data = scalar.fit_transform(train.drop(target, axis=1))

        with open(scalar_path, "wb") as f:
            dump(scalar, f)

        with open(master_scalar_path, "wb") as f:
            dump(scalar, f)

        train[train.drop(target, axis=1).columns] = scaled_data
        log_detail(logger, ["Successfully fitted robust scalar to train"])
        return train
    except Exception as e:
        log_detail(logger, [str(e)])


def fit_standard_scalar(train, scalar_path, master_scalar_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_data.py, inside fit_standard_scalar function"])
        scalar = StandardScaler()
        scaled_data = scalar.fit_transform(train.drop(target, axis=1))

        with open(scalar_path, "wb") as f:
            dump(scalar, f)

        with open(master_scalar_path, "wb") as f:
            dump(scalar, f)

        train[train.drop(target, axis=1).columns] = scaled_data
        log_detail(logger, ["Successfully fitted standard scalar to train"])
        return train
    except Exception as e:
        log_detail(logger, [str(e)])


def encode_test(test, encoder_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_data.py, inside encode_test function"])
        with open(encoder_path, "rb") as f:
            encoder = load(f)

        encode_cols = list(test.select_dtypes(include=['object']).columns)
        if target in encode_cols:
            encode_cols.remove(target)
        encode_data = test[encode_cols]
        encode_data = encoder.transform(encode_data)
        test[encode_cols] = encode_data
        log_detail(logger, ["Successfully encoded test"])
        return test
    except Exception as e:
        log_detail(logger, [str(e)])


def transform_robust_test(test, robust_scalar_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_data.py, inside transform_robust_test function"])
        with open(robust_scalar_path, "rb") as f:
            robust_scalar = load(f)

        transform_cols = list(test.drop(target, axis=1).columns)
        transform_data = test[transform_cols]
        transformed_data = robust_scalar.transform(transform_data)

        test[transform_cols] = transformed_data
        log_detail(logger, ["Successfully transformed test with robust scalar"])
        return test
    except Exception as e:
        log_detail(logger, [str(e)])


def transform_standard_test(test, standard_scalar_path, target, logger):
    try:
        log_detail(logger, ["Inside scale_data.py, inside transform_standard_test function"])
        with open(standard_scalar_path, "rb") as f:
            standard_scalar = load(f)

        transform_cols = list(test.drop(target, axis=1).columns)
        transform_data = test[transform_cols]
        transformed_data = standard_scalar.transform(transform_data)

        test[transform_cols] = transformed_data
        log_detail(logger, ["Successfully transformed test with standard scalar"])
        return test
    except Exception as e:
        log_detail(logger, [str(e)])


def export_trainable_data(config_path_, logger):
    try:
        log_detail(manager, ["Inside scale_data.py, inside export_trainable_data function"])
        config = read_params(config_path_, logger)
        encoder_path = config["scale_data"]["encoders"]
        robust_scalar_path = config["scale_data"]["robust_scalar"]
        standard_scalar_path = config["scale_data"]["standard_scalar"]
        master_robust_scalar_path = config["scale_data"]["master_robust_scalar"]
        master_standard_scalar_path = config["scale_data"]["master_standard_scalar"]
        train_path = config["split_data"]["train_path"]
        test_path = config["split_data"]["test_path"]
        scaled_train_path = config["scale_data"]["scaled_train_path"]
        scaled_test_path = config["scale_data"]["scaled_test_path"]
        target = config["base"]["target_col"]
        encoder_schema_path = config["scale_data"]["encoder_schema_path"]
        scalar_schema_path = config["scale_data"]["scalar_schema_path"]

        train = pd.read_csv(train_path)
        test = pd.read_csv(test_path)

        generate_schema(train, encoder_schema_path, scalar_schema_path, target, logger)

        train = fit_encoder(train, encoder_path, target, logger)
        train = fit_robust_scalar(train, robust_scalar_path, master_robust_scalar_path, target, logger)
        train = fit_standard_scalar(train, standard_scalar_path, master_standard_scalar_path, target, logger)

        test = encode_test(test, encoder_path, target, logger)
        test = transform_robust_test(test, robust_scalar_path, target, logger)
        test = transform_standard_test(test, standard_scalar_path, target, logger)

        train.to_csv(scaled_train_path, index=False)
        test.to_csv(scaled_test_path, index=False)
        log_detail(manager, ["Successfully exported trainable data"])
    except Exception as e:
        log_detail(manager, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    export_trainable_data(config_path, manager)
