# Project - pygrapher
## Description:
Used to plot many graphs that are needed in physics.

# INPUT TYPES:

## POSITION TIME
use when given (at least 3) points of (time, position)
```
POSITION TIME
(coord time, coord x-pos)
(coord time, coord x-pos)
(so on, so on)
STOP
```

### ex:
```
POSITION TIME
(3, 5)
(4, 6)
(5, 7)
STOP
```

## VELOCITY CONSTANTACCELERATION
Use this mode when given intial velocity and acceleration. 
Note: if time is -1, then it will be plotted until x is 0
```
VELOCITY CONSTANTACCELERATION
V0 initialv
A constantAcceleration
TIME howLongYouWantToSeeFor
X startingXPos
STOP
```

### ex:
Ex1
```
VELOCITY CONSTANTACCELERATION
V0 3.72
A -9.81
TIME 2
X 0
STOP
```
Ex2
```
VELOCITY CONSTANTACCELERATION
V0 22
A -9.81
TIME -1
x 37.232
STOP
```