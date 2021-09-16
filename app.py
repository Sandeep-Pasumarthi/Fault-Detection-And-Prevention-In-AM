from flask import Flask, request, render_template
from prediction_service.prediction import make_prediction
from log import get_manager, log_detail
import os


webapp_root = "web_app"
cols_to_change = ["TWF", "HDF", "PWF", "OSF", "RNF"]
logger = get_manager()

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


def change_data_dict(data_dict):
    try:
        log_detail(logger, ["Inside app.py, inside change_data_dict function"])
        new_data = dict()
        for i in data_dict.keys():
            if i in cols_to_change:
                if data_dict[i] == str(0):
                    new_data[i] = "No"
                else:
                    new_data[i] = "Yes"
            else:
                new_data[i] = data_dict[i]
        log_detail(logger, ["Successfully changed dict"])
        return new_data
    except Exception as e:
        log_detail(logger, [str(e)])


@app.route("/", methods=["POST", "GET"])
def home():
    try:
        log_detail(logger, ["Inside app.py, inside home function"])
        if request.method == "POST":
            log_detail(logger, ["It's a POST request"])
            data_dict = dict(request.form)
            log_detail(logger, [f"data = {data_dict}"])
            final_data_dict = change_data_dict(data_dict)
            prediction, probability = make_prediction(data_dict)
            log_detail(logger, [f"prediction = {prediction}"])
            if prediction == 0:
                return render_template("result.html", data=final_data_dict, prediction="No Failure")
            else:
                return render_template("result.html", data=final_data_dict, prediction="Machine can Fail")
        else:
            log_detail(logger, ["It's not a POST request"])
            return render_template("home.html")
    except Exception as e:
        log_detail(logger, [str(e)])
        return render_template("404.html", error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
