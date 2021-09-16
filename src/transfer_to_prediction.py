from log import get_manager, log_detail
from load_data import read_params
from shutil import copytree, ignore_patterns
import argparse


def transfer_to_prediction(source, destination, logger):
    try:
        log_detail(logger, ["Inside transfer_to_prediction.py, transfer_to_prediction function"])
        copytree(source, destination, ignore=ignore_patterns("*.gitignore"))
        log_detail(logger, ["Successfully transfered files to prediction_service"])
    except Exception as e:
        log_detail(logger, [str(e)])


def transfer(config_path_, logger):
    try:
        log_detail(logger, ["Inside transfer_to_prediction.py, transfer function"])
        config = read_params(config_path_, logger)
        source = config["transfer_requirements"]["source"]
        destination = config["transfer_requirements"]["destination"]

        transfer_to_prediction(source, destination, logger)
        log_detail(logger, ["Completed transfer"])
    except Exception as e:
        log_detail(logger, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    transfer(config_path, manager)
