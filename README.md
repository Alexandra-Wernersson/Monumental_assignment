# Monumental take-home assignment
Repository to create a masonary wall with a 4-DOF robotic crane.

## Install the requirements
Install the ```requirements.txt``` note that it is assumed you already have python installed on your machine.
```
pip install requirements.txt
```
Note that I use Manim (https://github.com/ManimCommunity/manim) for the vizualisations. Manim is a community-maintained Python framework for creating mathematical animations originally developed by Grant Sanderson. I have used it in the past for some science communication animations so I decided to use it again for this project.

## Initial testing
The notebook ```Testing_notebook.ipynb``` can be ignored. It was created to get a feel for the problem and test out the build orders.

## First_brick_exercise.py
This is the first brick exercise which dynamically calculates the number of full/half bricks that fit on a wall. It also outputs the built wall using ASCII art on the terminal. It can be run with the following command:
```
python first_brick_exercise.py
```

## interactive_bricks.py
This exercise adds some interaction to the build. It allows you to build up the wall brick by brick from bottom to top by adding a ‘built’ brick on every press of the ENTER key. It can be run with the following command:
```
manim -pql --renderer=opengl interactive_bricks.py InteractiveBricksScene
```

## optimal_interactive_bricks.py
This algorithm tries to minimize the number of times moving up/down by building the wall in a zigzag type pattern. Each build order has its own color to seperate when we move the robot. It can be run with the following command:

```
manim -pql --renderer=opengl optimal_interactive_bricks.py InteractiveBricksScene
```
Note that this built pattern is highly speculative. I was atempting to make sure that there always was a stable row beneath each brick being laid down. 

## To Do
- Try out the bonus exercises with English Cross Bond or wild bond pattern.
