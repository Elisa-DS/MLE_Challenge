# MLE_Challenge
Task - To take a predictive model into production environment.

## Milk price predictions ##

This repository contains 3 files:

1 - *MP_Preprocessing.py*

2 - *MP_Training.py*

3 - *MP_Prediction_API.py*

This code are using 3 datasets (banco_central.csv, precio_leche.csv, preciptaciones.csv). In *MP_Preprocessing.py* file contain all the preprocessing/cleaning of these 3 datasets mentioned above.
The *MP_Training.py* is the training model that it will predict the milk price in Chile.It was separated the training coding from the prediction code. 

For serializing the code was used *Pickle*, it is used to serializing and de-serializing a Python object structure. In which python object is converted into the byte stream.dump() method dumps the object into the file specified in the arguments.
The model was saved in a file named *lr_columns.pkl*, it can be used by the server. To deploy the model wil be using Flask as an API.

The figure below shows the steps followed in this MLE challenge.

![image](https://user-images.githubusercontent.com/51644705/179316413-d8b6bc64-cb25-4882-99d0-9c321f7cb087.png)

The *MP_Prediction_API.py* is going to request the server for predictions.It was used a REST API testing tool such as Postman (https://www.postman.com/) for testing. 



