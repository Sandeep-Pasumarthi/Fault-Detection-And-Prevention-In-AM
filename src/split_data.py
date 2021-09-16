from log import get_manager, log_detail
from load_data import read_params, pd
from sklearn.model_selection import train_test_split
import argparse


def get_data(path_, logger):
    try:
        log_detail(logger, ["Inside split_data.py, inside get_data function"])
        df = pd.read_csv(path_)
        log_detail(logger, ["Successfully read data"])
        return df
    except Exception as e:
        log_detail(logger, [str(e)])


def split_data(config_path_, logger):
    try:
        log_detail(logger, ["Inside split_data.py, inside split_data function"])
        config = read_params(config_path_, logger)
        data_path = config["initial_processed_data"]["processed_data_csv"]
        train_path = config["split_data"]["train_path"]
        test_path = config["split_data"]["test_path"]
        test_size = config["split_data"]["test_size"]
        random_state = config["base"]["random_state"]
        target = config["base"]["target_col"]

        df = get_data(data_path, logger)
        train, test = train_test_split(df, test_size=test_size, random_state=random_state, stratify=df[target])

        train.to_csv(train_path, index=False)
        test.to_csv(test_path, index=False)
        log_detail(logger, ["Successfully split data and exported data"])
    except Exception as e:
        log_detail(logger, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    split_data(config_path, manager)
