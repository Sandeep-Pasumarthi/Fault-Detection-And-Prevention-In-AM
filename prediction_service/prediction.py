from json import load
import pickle
import os

model_path = os.path.join("best_model", "random_forest.pkl")
processing_path = os.path.join("prediction_service", "data_processing_service")
initial_not_needed = ["UDI", "PRODUCT_ID"]
feature_not_needed = ["ROTATIONAL_SPEED_[RPM]", "PROCESS_TEMPERATURE_[K]", "AIR_TEMPERATURE_[K]"]
pre_predicting_not_needed = ["TYPE", "TORQUE_[NM]", "TOOL_WEAR_[MIN]", "RNF"]
object_cols = ["PRODUCT_ID", "TYPE"]
target = "MACHINE_FAILURE"


class NotInRange(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def make_prediction(data_dict):
    data_dict = __response_to_data(data_dict)
    data_dict = __initial_filtering(data_dict)
    __validate_schema(data_dict)
    data_dict = __feature_engineering(data_dict)
    data_dict = __encode_data(data_dict)
    data_dict = __robust_scalar_transform(data_dict)
    data_dict = __standard_scalar_transform(data_dict)
    data_dict = __predict_cluster(data_dict)
    data_dict = __final_robust_scalar_transform(data_dict)
    data_dict = __final_standard_scalar_transform(data_dict)
    data_dict = __remove_pre_predict_unimportant(data_dict)

    prediction, probability = __predict(data_dict)
    return prediction, probability


def __response_to_data(data_dict):
    for i in data_dict.keys():
        if i not in object_cols:
            data_dict[i] = float(data_dict[i])
    return data_dict


def read_schema(file_path):
    with open(file_path, "r") as f:
        schema = load(f)
    return schema


def load_pickle(file_path):
    with open(file_path, "rb") as f:
        model = pickle.load(f)
    return model


def __initial_filtering(data_dict):
    new_data = dict()
    for i, j in data_dict.items():
        if i not in initial_not_needed:
            new_data[i] = j
    return new_data


def __validate_schema(data_dict):
    schema = read_schema(os.path.join(processing_path, "numeric_schema.json"))
    for col in schema.keys():
        if schema[col]["min"] <= data_dict[col] <= schema[col]["max"]:
            pass
        else:
            raise NotInRange(message=f"Entered unusual value for {col}. "
                                     f"The range of {col} is in B/W {schema[col]['min']} and {schema[col]['max']}")


def __feature_engineering(data_dict):
    new_data = dict()
    schema = read_schema(os.path.join(processing_path, "extra_schema.json"))
    for col in data_dict.keys():
        if col == "TORQUE_[NM]":
            new_data[col] = data_dict[col] + schema["mean_torque_vs_rpm"]
        elif col in feature_not_needed:
            pass
        else:
            new_data[col] = data_dict[col]

    new_data["TEMPERATURE_DIFFERENCE"] = data_dict["PROCESS_TEMPERATURE_[K]"] - data_dict["AIR_TEMPERATURE_[K]"]
    return new_data


def __encode_data(data_dict):
    encoder = load_pickle(os.path.join(processing_path, "encoder.pkl"))
    encoder_schema = read_schema(os.path.join(processing_path, "encoder_schema.json"))
    values = [[data_dict[col] for col in encoder_schema["cols"]]]
    transformed_values = encoder.transform(values)
    for i in range(len(encoder_schema["cols"])):
        data_dict[encoder_schema["cols"][i]] = transformed_values[i][0]
    return data_dict


def __robust_scalar_transform(data_dict):
    scalar = load_pickle(os.path.join(processing_path, "robust_scalar.pkl"))
    scalar_schema = read_schema(os.path.join(processing_path, "scalar_schema.json"))
    values = [[data_dict[col] for col in scalar_schema["cols"]]]
    scaled_values = scalar.transform(values)[0]
    for i in range(len(scalar_schema["cols"])):
        data_dict[scalar_schema["cols"][i]] = scaled_values[i]
    return data_dict


def __standard_scalar_transform(data_dict):
    scalar = load_pickle(os.path.join(processing_path, "standard_scalar.pkl"))
    scalar_schema = read_schema(os.path.join(processing_path, "scalar_schema.json"))
    values = [[data_dict[col] for col in scalar_schema["cols"]]]
    scaled_values = scalar.transform(values)[0]
    for i in range(len(scalar_schema["cols"])):
        data_dict[scalar_schema["cols"][i]] = scaled_values[i]
    return data_dict


def __predict_cluster(data_dict):
    model = load_pickle(os.path.join(processing_path, "cluster.pkl"))
    values = [[data_dict[col] for col in data_dict.keys() if col != target]]
    data_dict["GROUP"] = model.predict(values)[0]
    return data_dict


def __final_robust_scalar_transform(data_dict):
    scalar = load_pickle(os.path.join(processing_path, "final_robust_scalar.pkl"))
    scalar_schema = read_schema(os.path.join(processing_path, "final_scalar_schema.json"))
    values = [[data_dict[col] for col in scalar_schema["cols"]]]
    scaled_values = scalar.transform(values)[0]
    for i in range(len(scalar_schema["cols"])):
        data_dict[scalar_schema["cols"][i]] = scaled_values[i]
    return data_dict


def __final_standard_scalar_transform(data_dict):
    scalar = load_pickle(os.path.join(processing_path, "final_standard_scalar.pkl"))
    scalar_schema = read_schema(os.path.join(processing_path, "final_scalar_schema.json"))
    values = [[data_dict[col] for col in scalar_schema["cols"]]]
    scaled_values = scalar.transform(values)[0]
    for i in range(len(scalar_schema["cols"])):
        data_dict[scalar_schema["cols"][i]] = scaled_values[i]
    return data_dict


def __remove_pre_predict_unimportant(data_dict):
    new_data = dict()
    for i, j in data_dict.items():
        if i not in pre_predicting_not_needed:
            new_data[i] = j
    return new_data


def __predict(data_dict):
    model = load_pickle(os.path.join("prediction_service", "best_model", "random_forest.pkl"))
    schema = read_schema(os.path.join(processing_path, "model_schema.json"))
    values = [[data_dict[col] for col in schema["cols"]]]
    prediction = model.predict(values)[0]
    probability = float(model.predict_proba(values)[0][0])
    return prediction, probability*100
