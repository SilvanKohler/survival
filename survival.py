import random
import time

import numpy as np


class creature:
    creatures = np.array([])
    crowding_coefficient = 0.001
    def propertydeformation(x):
        property_ = x + random.randint(-10, 10)/100
        return 1 if property_ > 1 else 0 if property_ < 0 else property_

    def __init__(self, b, d, r, m, g):
        self.birth_chance = b
        self.death_chance = d
        self.replication_chance = r
        self.mutation_chance = m
        self.generation = g
    def mutate(self):
        return creature(
            0,
            creature.propertydeformation(self.death_chance),
            creature.propertydeformation(self.replication_chance),
            creature.propertydeformation(self.mutation_chance),
            self.generation + 1
        )

    def replicate(self):
        if random.random() < self.replication_chance:
            creature.creatures = np.append(creature.creatures, self.mutate())


gen0 = creature(0.08, 0.01, 0.1, 0.05, 0)
with open("output.csv", "w") as f:
    f.write("time,creatures,death_chance,replication_chance,birth_chance,mutation_chance,crowding_death_chance\n")
    try:
        while True:
            if random.random() < gen0.birth_chance:
                creature.creatures = np.append(creature.creatures, gen0)
            for c in creature.creatures:
                c.birth_chance = max(0, c.birth_chance)
                c.death_chance = max(0, c.death_chance)
                c.replication_chance = max(0, c.replication_chance)
                c.mutation_chance = max(0, c.mutation_chance)
                c.replicate()
                if random.random() < c.death_chance+creature.crowding_coefficient*len(creature.creatures):
                    creature.creatures = np.delete(creature.creatures, np.where(c))
            try: f.write(f"{time.thread_time()},{len(creature.creatures)},{sum(c.death_chance for c in creature.creatures)/len(creature.creatures)},{sum(c.replication_chance for c in creature.creatures)/len(creature.creatures)},{sum(c.birth_chance for c in creature.creatures)/len(creature.creatures)},{sum(c.mutation_chance for c in creature.creatures)/len(creature.creatures)},{creature.crowding_coefficient*len(creature.creatures)}\n")
            except: continue
            print(len(creature.creatures))
            # if time.thread_time() >= 30:
                # break
        f.close()
    except KeyboardInterrupt:
        f.close()