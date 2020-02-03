# Maze_CP
<img src="https://raw.githubusercontent.com/Marius-450/screenshots/master/maze.png" align="right">
A little maze ball game for Circuit Playground boards with TFT Gizmo, driven by the accelerometer.

## Requirements 

* A Circuit Playground board (express or bluefruit) and TFT-Gizmo.

### Libraries

* adafruit_gizmo
* adafruit_lis3dh
* adafruit_imageload

## Gameplay 

Tilt the board to make the ball move. When the ball reach the goal (red cross), the maze reinitialize.
<img src="https://raw.githubusercontent.com/Marius-450/screenshots/master/maze_creation1.png" height="200"><img src="https://raw.githubusercontent.com/Marius-450/screenshots/master/maze_creation.png" height="200">
## Todo and issues

* going thru walls randomly (rare bug hard to reproduce)
* buttons actions ? 
* victory sound ?
* grab a "key" to open/activate the "exit"

## Thanks

For the maze generating algo :
* http://reeborg.ca/docs/fr/reference/mazes.html
* https://rosettacode.org/wiki/Maze_generation#Python

For everything else (examples, libs, community, etc.) :
* https://www.adafruit.com/

