# Solving set covering problem by using genetic algorithm

## Functions
In this solution, three main functions are proposed:
1. fitness: computes the fitness of genome, by counting the correct and repeated elements and subtracting them. In this way, lists with repeated elements get a lower fitness.
2. crossover: adds two genomes together.
3. tournament: chooses the best of given genomes, based on fitness.

## Creating the population
Population is created by selecting random genomes from all_lists, calculating their fitness and making an individual.

## The offspring creation loop
1. Two individuals are chosen in two different tournaments.
2. They are cossed over.
3. They are added to offspring list.

## The Main loop
1. Offsprings are added to population.
2. N fittest individual from population are chosen for the next generation. (N = POPULATION_SIZE)

## Summary
This solution tries to solve the problem by using genetic algorithm. However it never checks for the final solution in the fitness calculation. Therefore, we might have a perfect list in the population and discarding it because of high number of repeated elements. A better solution can try to detect the goal state in fitness calculation.

## Team
300451, Zohreh Lahijaniamiri, https://github.com/Zohrelhj

301425, Shayan Taghinezhad Roudbaraki, https://github.com/drustthecoder


