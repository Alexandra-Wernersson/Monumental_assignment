# Monumental take-home assignment
This repository contains a simulation of a 4-DOF robotic crane building a masonry wall, including visualizations of different build strategies.

## Install the requirements
Make sure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```
Note: This project uses Manim, a Python framework for creating mathematical animations originally developed by Grant Sanderson. I’ve used Manim previously for science communication animations, and chose it again for this project due to its flexibility and rendering quality.

If you encounter issues with Manim, they are often related to Cairo incompatibilities in Anaconda environments. You can usually resolve this with:
```
conda install -c conda-forge pycairo
```
## Initial testing
The notebook ```Testing_notebook.ipynb``` contains exploratory tests for understanding the problem and experimenting with build orders. It is not essential for running the main code.

## First_brick_exercise.py
This script calculates how many full and half bricks fit in a wall based on its dimensions. It outputs the result as ASCII art in the terminal.

Run with:
```
python first_brick_exercise.py
```

## interactive_bricks.py
This script introduces basic interactivity. Pressing the ```ENTER``` key builds the wall one brick at a time from bottom to top. Each brick is added to the visual scene incrementally.

```
manim -pql --renderer=opengl interactive_bricks.py InteractiveBricksScene
```

## optimal_interactive_bricks.py
This version attempts to optimize the build sequence by minimizing vertical movement using a zigzag/triangular pattern. Each build order is shown in a different color to indicate crane movement phases.

Run with:

```
manim -pql --renderer=opengl optimal_interactive_bricks.py InteractiveBricksScene
```
This build strategy is speculative. It assumes that each brick must always rest on a stable row beneath it. See the resulting structure in ```final_built_wall.jpeg```.

## To Do
-  Explore bonus exercises: English Cross Bond or wild bond pattern.
