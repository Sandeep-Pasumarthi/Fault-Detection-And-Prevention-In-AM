from log import get_manager, log_detail
import yaml
import argparse
import pandas as pd


def read_params(config_path_, logger):
    try:
        log_detail(logger, ["Inside load_data.py, inside read_params function"])
        with open(config_path_) as yaml_file:
            config = yaml.safe_load(yaml_file)
        log_detail(logger, ["Successfully read params"])
        return config
    except Exception as e:
        log_detail(logger, [str(e)])


def get_data(config_path_, logger):
    try:
        log_detail(logger, ["Inside load_data.py, inside get_data function"])
        config = read_params(config_path_, logger)
        data_path = config["data_source"]["local_source"]
        df = pd.read_csv(data_path)
        log_detail(logger, ["Successfully get data"])
        return df
    except Exception as e:
        log_detail(logger, [str(e)])


def load_save_data(config_path_, logger):
    try:
        log_detail(logger, ["Inside load_data.py, inside load_save_data function"])
        config = read_params(config_path_, logger)
        df = get_data(config_path_, logger)
        new_cols = [col.replace(" ", "_").upper() for col in df.columns]
        raw_data_path = config["load_data"]["raw_dataset_csv"]

        df.to_csv(raw_data_path, header=new_cols, index=False)
        log_detail(logger, ["Successfully loaded and saved data"])
    except Exception as e:
        log_detail(logger, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    load_save_data(config_path, manager)
