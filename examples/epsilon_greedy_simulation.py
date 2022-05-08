import random
from collections import namedtuple, Counter
from bandits.mab import EpsilonGreedyMAB


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
bandit = EpsilonGreedyMAB(arms.keys(), epsilon=EPSILON)


actions = []
rewards = []
for unit_id in range(N_ITER):
    action = bandit.select(unit_id)
    reward = arms[action.arm_id].get_reward()
    bandit.record(action, reward)

    actions.append(action)
    rewards.append(reward)


c = Counter([action.arm_id for action in actions])
print("Arm Three is the clear winner: ", c)



