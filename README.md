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
line1: row col
line2: movements for the experiment
line3: wind_direction wind_speed

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
 meanings for columns from left to right:
 probability for staying in the sector, duration rate, arrive rate, arrive number, die rate.

## Running the program
