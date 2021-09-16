from load_data import read_params
from initial_processing import get_raw_data
from log import get_manager, log_detail
from json import dump
import argparse


def numeric_schema_generator(df, schema_file, target, logger):
    try:
        log_detail(logger, ["Inside schema_generator.py, inside numeric_schema_generator function"])
        schema = df.describe().T
        numeric_cols = list(df.select_dtypes(exclude=['object']).columns)
        if target in numeric_cols:
            numeric_cols.remove(target)
        numeric_cols.remove("UDI")
        schema_num = {i: {"min": schema.loc[i]['min'], "max": schema.loc[i]['max']} for i in numeric_cols}

        with open(schema_file, "w") as f:
            dump(schema_num, f)
        log_detail(logger, ["Successfully generated numeric schema"])
    except Exception as e:
        log_detail(logger, [str(e)])


def categorical_schema_generator(df, schema_file, target, logger):
    try:
        log_detail(logger, ["Inside schema_generator.py, inside categorical_schema_generator function"])
        categorical_cols = list(df.select_dtypes(include=['object']).columns)
        if target in categorical_cols:
            categorical_cols.remove(target)
        categorical_cols.remove("PRODUCT_ID")
        schema_num = {i: list(df[i].unique()) for i in categorical_cols}

        with open(schema_file, "w") as f:
            dump(schema_num, f)
        log_detail(logger, ["Successfully generated categorical schema"])
    except Exception as e:
        log_detail(logger, [str(e)])


def extra_schema_generator(df, schema_file, logger):
    try:
        log_detail(logger, ["Inside schema_generator.py, inside extra_schema_generator function"])
        mean_torque_vs_rpm = (df["TORQUE_[NM]"] / df["ROTATIONAL_SPEED_[RPM]"]).mean()
        schema_extra = {"mean_torque_vs_rpm": mean_torque_vs_rpm}

        with open(schema_file, "w") as f:
            dump(schema_extra, f)
        log_detail(logger, ["Successfully generated extra schema"])
    except Exception as e:
        log_detail(logger, [str(e)])


def generate_schema(config_path_, logger):
    try:
        log_detail(manager, ["Inside schema_generator.py, inside generate_schema function"])
        config = read_params(config_path_, logger)
        data_path = config["load_data"]["raw_dataset_csv"]
        num_schema_path = config["schema"]["numerical"]
        cat_schema_path = config["schema"]["categorical"]
        extra_schema_path = config["schema"]["extra"]
        target = config["base"]["target_col"]
        df = get_raw_data(data_path, logger)
        df[["TWF", "HDF", "PWF", "OSF", "RNF"]] = df[["TWF", "HDF", "PWF", "OSF", "RNF"]].astype('object')

        numeric_schema_generator(df, num_schema_path, target, logger)
        categorical_schema_generator(df, cat_schema_path, target, logger)
        extra_schema_generator(df, extra_schema_path, logger)

        log_detail(manager, ["Successfully generated schema"])
    except Exception as e:
        log_detail(manager, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    generate_schema(config_path, manager)
