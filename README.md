## Smart-Gardening
### A Smart Solution to your Gardening Problems
> N. Chakraborty, A. Mukherjee, and M. Bhadra, “Smart Gardening: A Solution to Your Gardening Issues”, EAI Endorsed Trans IoT, vol. 8, no. 30, p. e3, Aug. 2022.

### Cite the work: 




------------------------------------------------
### Architecture of the Smart-Gardening System:
![Architecture](https://github.com/Niloy-Chakraborty/Smart-Gardening/blob/master/Architecture.png)

------------------------------------------------

### Paper:
Please see the detailed report from [here](https://www.researchgate.net/publication/339412317_Smart_Gardening_A_solution_to_your_gardening_issues?_sg%5B0%5D=U_O-f1a3XHIaBI4_ER6dQGMTr_cj1cCMjCd1nszVCSeVTU9Igqs_LXNtbB3TDwtyX22HLEC1iXF3sA.ROHM8E4iQN2fdYqhWW9fkJAmQCORy_93BUaQDxEIxEF8O7CwbJcOcsemQ_TXd1-R-SKLEODkfLB3GCO7LK-t4Q&_sg%5B1%5D=kcJR-K5YcFrhiJzWfAnEB1FskrGex0z4zEKCbNQa3hAXdsC7PLdMyqSfdqbLgqN2vhV7tuBuAC4zXjf-bb0gBXKgc66ju9y8zdVAoLTlj4JFbRH-QGc) and cite the work for future use.

------------------------------------------------
### Guidelines:
1. [**AI PLAN**](https://github.com/Niloy-Chakraborty/Smart-Gardening/tree/master/AI_PLAN) contains all the Domain and Problem files for the AI Planning.  

**smartGarden_domain.pddl, smartGarden_problem** - The domain and sample problem file to automate watering of multiple plants.

**smartGardenlighting_domain.pddl, smartGardenlighting_problem** - The domain and sample problem file to turn on/off lamp in the garden area based on present luminance level.

-------------------------
2. [**CONTROLLER**](https://github.com/Niloy-Chakraborty/Smart-Gardening/tree/master/CONTROLLER) contains all the .py files for controlling the Telegram bot and automating the AI planning problems. 

**telegramapp.py, iotcontrol.py** - These files controls the telegram bot.

**lampplanner.py, waterplanner.py**- automates the optimum usage of water and light(generates problem files and execute the planner).

**water.py, lamp.py**- handles the output of the planner turn on/off the plugwise connected to motor/lamp

**publish.py**- publish to cloudmqtt broker

**subscribe.py**-subscribe to cloudmqtt broker

**storeindb.py**-store the subscribed data in the AWS RDS for monitoring and planning purpose.

-------------------------
3. [**DL MODEL**](https://github.com/Niloy-Chakraborty/Smart-Gardening/tree/master/DL_MODEL) contains all the files related to training the model for plant identification and health info.

**cnn.py**- This script is used for training a CNN-based Machine Learning Model and the model can be saved as .h5 file
PlantIdentification.py - This script is used for predicting the plant name and health status using the deployed ML model. The model can be downloaded from [here](https://drive.google.com/open?id=1stVThnVNt8yhOze6h0iQPJXKuZLaV2cC)

-----------------------------------------------
#### PLEASE NOTE:

1. Install all the necessary packages mentioned in the respective script. 

2. The folder structures shown here were not maintained during the project. These are shown here for better understanding about the code. After cloning the repo, please paste all the files in a common folder.

