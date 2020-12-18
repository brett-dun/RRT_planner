# RRT Planner
Implementation of RRT path planner and several dynamic models


## Quick Start
### Prerequisites
There are some packages needed:
* **pygame**
* **numpy**
### Run
Simply type:
```
python main.py input/[model].json
```
For example:
```
python main.py input/Car_Dynamic.json
```
## Dynamic Models
### Car Dynamic Model

A bicycle dynamic car model. 

Source Paper: http://www.cs.cmu.edu/~motionplanning/reading/PlanningforDynamicVeh-1.pdf

Note: there are some mistakes in the paper. 

1) r is always yaw rate; not tire radius
2) the matrix in equation(4) should be [A B C D]


### Quadrotor Model

A Quadcopter dynamic model. 

Source Paper: https://easychair.org/publications/open/sr6 

Model 3.3

### Car Kinematic Model

A kinematic single track car model. 

Source: [CommonRoad: Vehicle Models](https://gitlab.com/commonroad/commonroad.gitlab.io/raw/master/documentation/vehicleModels_commonRoad.pdf)

Model 3: Kinematic Single-Track Model 

### Car Linear Model
A linear dynamic car model. 

It is developed by simply eliminated sin and cos terms in the Car_Dyanmic model. 

The way we do that is using small angle approximation. 
