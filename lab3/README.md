# Lab 3

### Task

Write agents able to play *Nim*, with an arbitrary number of rows and an upper bound ***k*** on the number of objects that can be removed in a turn (a.k.a., subtraction game). The player **taking the last object wins**.

* Task3.1: An agent using fixed rules based on *nim-sum* (i.e., an expert system)
* Task3.2: An agent using evolved rules
* Task3.3: An agent using min-max
* Task3.4: An agent using reinforcement learning

The task is implemented by the following people:

* **SeyedOmid Mahdavi s299837**
* **Zohreh Lahijani Amiri s300451**

### Algorithm Description

* Task 3.1: `expertSystem` agent makes the *nim-sum* equal to *0* after each move. If the *nim-sum* is already *0*, it removes one element from a non-empty row.

* Task 3.2: `evolvedRules` agent makes a move according to the current state of the game and some rules. The consideration of different rules is based on some parameters. These parameters are determined via a genetic algorithm `GA` through an arbitrary number of generations. The final set of parameters used for the evaluation step is the following:

  `rules = [0.249, 0.401, 0.453, 0.103, 0.89, 0.187, 0.616, 0.630, 0.571, 0.897, 0.196, 0.193]`

### Evaluations

In this project, every single evaluation is the win ratio after 20 matches with `randomAgent`. The result consists of a list containing 10 different single evaluations for each agent.

* Task 3.1: `resultHistory: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
* Task 3.2: `resultHistory: [0.55, 0.7, 0.8, 0.5, 0.9, 0.6, 0.65, 0.55, 0.75, 0.6]`

