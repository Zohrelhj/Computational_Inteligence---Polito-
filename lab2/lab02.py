import random, logging
from collections import namedtuple
seed = 42
N = 10

logging.getLogger().setLevel(logging.DEBUG)

def problem(N, seed=None):
    """Creates an instance of the problem"""

    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


all_lists = problem(10, 42)



logging.debug(f"all_lists is {all_lists}")

def fitness(genome, n=N):
    correct_n = len(set(genome))
    repeated_n = len(genome) - correct_n
    return correct_n - repeated_n

def cross_over(g1, g2):
    return g1 + g2

def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


    from collections import namedtuple
from collections import Counter

Individual = namedtuple("Individual", ["genome", "fitness"])
population = list()

for i in range(10):
    genome = random.choice(all_lists)
    indv = Individual(genome, fitness(genome, 10))
    population.append(indv)

logging.debug(f"poulation is {population}")


logging.getLogger().setLevel(logging.INFO)

NUM_GENERATIONS = 100
OFFSPRING_SIZE = 3
POPULATION_SIZE = 10

for g in range(NUM_GENERATIONS):
    offspring = list()
    for i in range(OFFSPRING_SIZE):
        p1 = tournament(population)
        p2 = tournament(population)
        o = cross_over(p1.genome, p2.genome)
        f = fitness(o)
        offspring.append(Individual(o, f))
    population += offspring
    population = sorted(population, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]

logging.info(f"population is {population}")