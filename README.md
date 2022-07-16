# MLE_Challenge
**Task:** To take a predictive model into production environment.

## Milk price predictions ##

This repository contains 4 files:

**1 - *MP_Preprocessing.py***

**2 - *MP_Training.py***

**3 - *run_prep-n-training.py***

**3 - *run_Prediction_API.py***

This code are using 3 datasets located in data folder above (*banco_central.csv*, *precio_leche.csv*, *preciptaciones.csv*). In *MP_Preprocessing.py* file contain all the preprocessing/cleaning and merge of these 3 datasets mentioned above. 
The *MP_Training.py* is the training model that it will predict the milk price in Chile.It was separated the training coding from the prediction code. 

For serializing the code was used *Pickle*, it is used to serializing and de-serializing a Python object structure. In which python object is converted into the byte stream.dump() method dumps the object into the file specified in the arguments.
The model was saved in a file named *linearRegression.pkl*, it can be used by the server. To deploy the model wil be using Flask as an API. Flask is a web service development framework, it supports extensions that can add application features as if they were implemented in Flask itself.

The figure below shows the steps followed in this MLE challenge.

![image](https://user-images.githubusercontent.com/51644705/179316413-d8b6bc64-cb25-4882-99d0-9c321f7cb087.png)

The *MP_Prediction_API.py* is going to request the server for predictions. To do it was used a REST API testing tool such as Postman (https://www.postman.com/) for testing. Enter the showed URL beside POST action and click on the Send button, the prediction result will appear in the body. Check the image below. Now, it is possible to check milk price predictions with new data using your model previously trained.

![image](https://user-images.githubusercontent.com/51644705/179322247-c1ed2595-948e-4d7c-8ce0-5c738129be8e.png)

### **How to run this repository** ###
______________________________________________________________________________________________________________________________________________________________________

**1 - run_prep_n_Training.py for run preprocessing and training modules all together**

**2 - run_Prediction_API.py**

PS: run_prep_n_Training.py is serialized, so they can also run separately.
