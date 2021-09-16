import os

dirs = [
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    os.path.join("data", "master"),
    os.path.join("reports", "EDA_figs"),
    os.path.join("reports", "best_model"),
    os.path.join("data_processing_service", "schema"),
    os.path.join("data_processing_service", "scalers"),
    os.path.join("data_processing_service", "master_service"),
    os.path.join("prediction_service", "best_model"),
    os.path.join("web_app", "static"),
    os.path.join("web_app", "templates"),
    "data_source",
    "note_books",
    "src"
]


for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as d:
        pass


files = [
    os.path.join("prediction_service", "prediction.py"),
    os.path.join("src", "cassandra_ops.py"),
    os.path.join("src", "clustering.py"),
    os.path.join("src", "initial_processing.py"),
    os.path.join("src", "load_data.py"),
    os.path.join("src", "log.py"),
    os.path.join("src", "model_train.py"),
    os.path.join("src", "scale_data.py"),
    os.path.join("src", "schema_generator.py"),
    os.path.join("src", "split_data.py"),
    "requirements.txt",
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    "README.md"
]

for file_ in files:
    with open(file_, "w") as f:
        pass
