# DroneExplorer with optimized environment and q-learning

This is a new module for our Drone Explorer research project. Here we simulate the whole flying policies, and add q-learning to make a next movement.

## Getting Started

1. Clone this project to your local machine.
2. Modify fix_paras.txt for fixed parameters.
   Example for fix_paras.txt
```
10 10   
600     
0 2     
```
   line1: row col<br />
   line2: movements for the experiment<br />
   line3: wind_direction wind_speed<br />

3. Modily indep_var.txt for variables.
   Example for indep_var.txt
 ```
  0.0 0.03 0.005 150 0.005
  0.1 0.03 0.005 150 0.005
  0.2 0.03 0.005 150 0.005
  0.3 0.03 0.005 150 0.005
  0.4 0.03 0.005 150 0.005
  0.5 0.03 0.005 150 0.005
  0.6 0.03 0.005 150 0.005
  0.7 0.03 0.005 150 0.005
  0.8 0.03 0.005 150 0.005
  0.9 0.03 0.005 150 0.005
  1 0.03 0.005 150 0.005
 ```
   meanings for columns from left to right:<br />
   probability for staying in the sector, events duration rate, events arrive rate, events arrive number, events die rate.

## Running the program
We have four script files for 4 different variables (though there are five variables, we set arrive rate and die rate same):<br />
   - DroneExplore_arrdie.sh
   - DroneExplore_arrnum.sh
   - DroneExplore_dur.sh
   - DroneExplore_prob.sh
For the variable to run experiments on, run the command
```
chmod 777 DroneExplore_(varname).sh
```
Then, run the script to start the experiment.
```
./DroneExplore_(varname).sh
```
Finally, after it finishes, a corresponding csv file will be generated.

## File Descriptions
### Arena.py
This file contains Arena class, which contains the map that our agent(UAV) is going to explore
### Board.py
This file contains Threading class, and this file will initiate the board to be explored
### Distribution.py
Contains distribution: exponential, random
### Drone.py
This file controls the drone action
### Event.py
This file generates corresponding graphs
### Main.py
This file contains main function for the board running in the background
### Policy.py
Contains policies drone will fly including: random, roomba
### WriteReport.py
Contains policies drone will fly including: random, roomba

