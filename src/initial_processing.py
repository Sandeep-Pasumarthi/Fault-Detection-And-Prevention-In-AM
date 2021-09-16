from log import get_manager, log_detail
from load_data import read_params, pd
import argparse


def get_raw_data(path_, logger):
    try:
        log_detail(logger, ["Inside initial_processing.py, inside get_raw_data function"])
        df = pd.read_csv(path_)
        log_detail(logger, ["Successfully read raw data"])
        return df
    except Exception as e:
        log_detail(logger, [str(e)])


def drop(df, columns, logger):
    try:
        log_detail(logger, ["Inside initial_processing.py, inside drop function"])
        df = df.drop(columns, axis=1)
        log_detail(logger, [f"Successfully dropped columns {columns}"])
        return df
    except Exception as e:
        log_detail(logger, [str(e)])


def feature_engineering(df, logger):
    try:
        log_detail(logger, ["Inside initial_processing.py, inside feature_engineering function"])
        mean_torque_vs_rpm = (df["TORQUE_[NM]"] / df["ROTATIONAL_SPEED_[RPM]"]).mean()
        df["TORQUE_[NM]"] = df["TORQUE_[NM]"].apply(lambda x: x + mean_torque_vs_rpm)
        df = drop(df, "ROTATIONAL_SPEED_[RPM]", logger)
        df["TEMPERATURE_DIFFERENCE"] = df["PROCESS_TEMPERATURE_[K]"] - df["AIR_TEMPERATURE_[K]"]
        df = drop(df, ["PROCESS_TEMPERATURE_[K]", "AIR_TEMPERATURE_[K]"], logger)
        log_detail(logger, ["Successfully feature engineered data"])
        return df
    except Exception as e:
        log_detail(logger, [str(e)])


def data_processing(config_path_, logger):
    try:
        log_detail(logger, ["Inside initial_processing.py, inside data_processing function"])
        config = read_params(config_path_, logger)
        data_path = config["load_data"]["raw_dataset_csv"]
        processed_data_path = config["initial_processed_data"]["processed_data_csv"]
        df = get_raw_data(data_path, logger)
        df = drop(df, ["UDI", "PRODUCT_ID"], logger)
        df = feature_engineering(df, logger)
        df.to_csv(processed_data_path, index=False)
        log_detail(logger, ["Successfully processed data"])
    except Exception as e:
        log_detail(logger, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    data_processing(config_path, manager)
