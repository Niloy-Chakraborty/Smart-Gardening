# Smart-Gardening
In this project a gardening system has been automated using IoT in the Raspberry Pi platform.
telegramapp.py, iotcontrol.py - These files controls the telegram bot.
lampplanner.py, waterplanner.py- automates the optimum usage of water and light(generates problem files and execute the planner).
smartGarden_domain.pddl, smartGarden_problem - The domain and sample problem file to automate watering of multiple plants.
smartGardenlighting_domain.pddl, smartGardenlighting_problem - The domain and sample problem file to turn on/off lamp in the garden area based on present luminance level.
water.py, lamp.py- handles the output of the planner turn on/off the plugwise connected to motor/lamp
publish.py- publish to cloudmqtt broker
subscribe.py-subscribe to cloudmqtt broker
storeindb.py-store the subscribed data in the AWS RDS for monitoring and planning purpose.
cnn.py- This script is used for training a CNN-based Machine Learning Model and the model can be saved as .h5 file
PlantIdentification.py - This script is used for predicting the plant name and health status using the deployed ML model. The model can be downloaded from https://drive.google.com/open?id=1stVThnVNt8yhOze6h0iQPJXKuZLaV2cC

PLEASE NOTE: Install all the necessary packages mentioned in the respective script. 
