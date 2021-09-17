# AI14-Predictive-Maintenance
**Website Link - [Click Here](https://machine-failure-ml.herokuapp.com/)** <br>
:information_source: **Website may load slow beacuse of used free resources for database management(cassandra) and deploying(heroku).**
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

## Process Followed
1. Removed unimportant columns like UID(which is nothing but a unique identifier), Product ID(The detail is given in Type column).
2. Generated schema for remaining columns excluding target. For numeric attributes, minimum and maximum are stored and for discrete attributes, unique values are stored.
3. Exploratory Data Analysis.
4. Initial Processing like removing skewness and feature engineering.
5. Split data for training and testing.
6. Encoding discrete columns using ordinal encoder.
7. Scaling training data using robust scalar(for making outliers to fall in usual range) first and then using standard scalar(for normalizing data).
8. Transforming and encoding test data using same scalars and encoder.
9. Clustered train data using KMeans clustering. K=8 after experimenting with different values.
10. Experimented different models like logistic regression, decision tree, random forest etc. But random forest gave importances to attributes better than other algorithms.
11. Grid Search CV for hyper parameter tuning.
12. Training random forest model and stored it.
13. Removed unimportant features using random forest feature importances and trained again random forest model with new train data.
14. Created prediction process.
15. Created web pages for web application.
16. Using flask created app.
17. Deployed it in heroku platform using github actions.
