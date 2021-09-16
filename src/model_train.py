from log import get_manager, log_detail
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, r2_score
from initial_processing import get_raw_data, read_params
from json import dump
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


def generate_schema(train, model_schema_path, target, logger):
    try:
        log_detail(logger, ["inside model_train.py, inside function generate_schema"])
        cols = list(train.columns)
        cols.remove(target)
        model_schema = {"cols": cols}

        with open(model_schema_path, "w") as f:
            dump(model_schema, f)
        log_detail(logger, ["Successfully generated schema"])
    except Exception as e:
        log_detail(logger, [str(e)])


def remove_unimportant_columns(train, test, train_path, test_path, columns, logger):
    try:
        log_detail(logger, ["inside model_train.py, inside function remove_unimportant_columns"])
        train = train.drop(columns, axis=1)
        test = test.drop(columns, axis=1)

        train.to_csv(train_path, index=False)
        test.to_csv(test_path, index=False)
        log_detail(logger, ["Successfully removed unimportant columns"])
        return train, test
    except Exception as e:
        log_detail(logger, [str(e)])


def train_random_forest(train, target, params, logger):
    try:
        log_detail(logger, ["inside model_train.py, inside function train_random_forest"])
        model = RandomForestClassifier(**params)
        model.fit(train, target)
        log_detail(logger, ["Successfully trained model"])
        return model
    except Exception as e:
        log_detail(logger, [str(e)])


def test_model(model, test, target, reports_dir, reports_feature_importance, logger):
    try:
        log_detail(logger, ["inside model_train.py, inside function test_model"])
        predictions = model.predict(test)
        report = dict()
        report["Accuracy Score"] = accuracy_score(target, predictions)
        report["Precision Score"] = precision_score(target, predictions)
        report["Recall Score"] = recall_score(target, predictions)
        report["F1 Score"] = f1_score(target, predictions)
        report["R2 Score"] = r2_score(target, predictions)

        with open(reports_dir, "w") as f:
            dump(report, f)

        columns = test.columns
        values = model.feature_importances_
        plt.figure(figsize=(20, 8))
        fig = sns.barplot(columns, values)
        fig.set_xlabel("Columns", fontsize=20)
        fig.set_ylabel("Feature Importance", fontsize=20)
        fig.set_title("Model's Feature Importance", fontsize=25)
        fig.figure.savefig(reports_feature_importance)
        log_detail(logger, ["Successfully tested model"])
    except Exception as e:
        log_detail(logger, [str(e)])


def export_model(model, model_dir, logger):
    try:
        log_detail(logger, ["inside model_train.py, inside function export_model"])
        with open(model_dir, "wb") as f:
            pickle.dump(model, f)
        log_detail(logger, ["Successfully exported model"])
    except Exception as e:
        log_detail(logger, [str(e)])


def model_training(config_path_, logger):
    try:
        log_detail(logger, ["inside model_train.py, inside function model_training"])
        config = read_params(config_path_, logger)
        unimportant_cols = ["TYPE", "TORQUE_[NM]", "TOOL_WEAR_[MIN]", "RNF"]
        train_path = config["cluster"]["master_train"]
        test_path = config["cluster"]["master_test"]
        model_train_path = config["final_train"]["master_model_train"]
        model_test_path = config["final_train"]["master_model_test"]
        model_params = config["final_train"]["random_forest"]
        model_path = config["final_train"]["final_model"]
        reports_json = config["final_train"]["reports_json"]
        reports_feature_importance = config["final_train"]["reports_feature_importance"]
        target = config["base"]["target_col"]
        model_schema_path = config["final_train"]["model_schema_path"]

        train = get_raw_data(train_path, logger)
        test = get_raw_data(test_path, logger)

        train, test = remove_unimportant_columns(train, test, model_train_path,
                                                 model_test_path, unimportant_cols, logger)
        generate_schema(train, model_schema_path, target, logger)
        model = train_random_forest(train.drop(target, axis=1), train[target], model_params, logger)
        test_model(model, test.drop(target, axis=1), test[target], reports_json, reports_feature_importance, logger)

        export_model(model, model_path, logger)
        log_detail(logger, ["Successfully completed model training"])
    except Exception as e:
        log_detail(logger, [str(e)])


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config
    manager = get_manager()
    model_training(config_path, manager)
