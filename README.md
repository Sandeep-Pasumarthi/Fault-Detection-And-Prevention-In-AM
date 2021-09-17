# AI14-Predictive-Maintenance
* Objective - To find whether a machine created in industrial process will fail to wok or not.
* Proposed Solution - Using data preprocessing, machine learning to achieve this task.<br>

**Website Link - [Click Here](https://machine-failure-ml.herokuapp.com/)** <br>

:information_source: **Website may load slow because of used free resources for database management(cassandra) and deploying(heroku).**
## Data Description
The data set is a synthetic dataset that reflects real predictive maintenance encountered in industry. This includes 14 attributes/columns includes target attribute also.<br>

**Download Data set Here - [Download](https://archive.ics.uci.edu/ml/machine-learning-databases/00601/ai4i2020.csv)**

* UID - Unique Identifier.
* Product ID - First letter indicates the quality and the next numbers represents serial number.
* Type - Indicates quality.
* Air Temperature[k] - Air temperature in kelvin scale. Generated using a random walk process later normalized to a standard deviation of 2 K around 300 K
* Process Temperature[k] - Process temperature in kelvin scale. Generated using a random walk process normalized to a standard deviation of 1 K, added to the air temperature plus 10 K.
* Rotational Speed[RPM] - Rotation speed in RPM. Calculated from a power of 2860 W, overlaid with a normally distributed noise.
* Torque[NM] - Torque generated in NM. Values are normally distributed around 40 Nm with a Ïƒ = 10 Nm and no negative values.
* Tool Wear[MIN] - The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process.
* Tool Wear Failure[TWF] - Indicates how many times the tool wear failed and replaced.
* Heat Dissipation Failure[HDF] - 1 indicate fail condition, 0 indicates good condition. Heat dissipation can cause process failure which leads to machine failure.
* Power Failure[PWF] - 1 indicate fail condition, 0 indicates good condition. If the power is below 3500W or above 9000W leads to process failure and machine failure.
* OverStrain Failure[OSF] - 1 indicate fail condition, 0 indicates good condition. It is product of tool war and torque. 11000, 12000, 13000 respectively for L, M, H indicates over strain failure leads to process and machine failure.
* Random Failure[RNF] - 1 indicate fail condition, 0 indicates good condition. Each process has a chance of 0.1 % to fail regardless of its process parameters.
* Machine Failure - 1 indicate fail condition, 0 indicates good condition.

## Tools and Frameworks Used
* Data Preprocessing and model training - python 3.7, pandas, numpy, sklearn, logger, cassandra driver, data version control(dvc).
* Exploratory Data Analysis - matplotlib, seaborn.
* Web pages - html, css, bootstrap.
* Routing - flask.
* Workflow and deployement - gunicorn, heroku, github actions.