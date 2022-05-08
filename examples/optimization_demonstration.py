import random
from collections import namedtuple, Counter
import matplotlib.pyplot as plt
from bandits.mab import EpsilonGreedyMAB
from datetime import datetime


N_ITER = 10000
EPSILON = 0.1

Arm = namedtuple("Arm", ["get_reward", "name"])

def _create_arm(mean, var):
    def _():
        return random.random()*var+mean
    return _


# arm_three will be the winner
arms = {
    1: Arm(_create_arm(1, 1), "arm_one"),
    2: Arm(_create_arm(1.1, 1.2), "arm_two"),
    3: Arm(_create_arm(1.2, 2), "arm_three"),
}
# optimization is turned on since SimplePersistence implements ARM_AVG_REWARD
bandit = EpsilonGreedyMAB(arms.keys(), epsilon=EPSILON)

start = datetime.now()
actions = []
rewards = []
for unit_id in range(N_ITER):
    action = bandit.select(unit_id)
    reward = arms[action.arm_id].get_reward()
    bandit.record(action, reward)

    actions.append(action)
    rewards.append(reward)


# something like 0.25s on my computer
print("should be fast: ", (datetime.now()-start).total_seconds())

bandit = EpsilonGreedyMAB(arms.keys(), epsilon=EPSILON)
bandit.optimized = False # manually turn off available optimizations


start = datetime.now()
actions = []
rewards = []
for unit_id in range(N_ITER):
    action = bandit.select(unit_id)
    reward = arms[action.arm_id].get_reward()
    bandit.record(action, reward)

    actions.append(action)
    rewards.append(reward)

# something like 10s on my computer
print("should be slow: ", (datetime.now()-start).total_seconds())

c = Counter([action.arm_id for action in actions])
print("Arm Three is the clear winner: ", c)
