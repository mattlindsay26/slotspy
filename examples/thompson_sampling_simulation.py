import random
from collections import namedtuple, Counter
from bandits.mab import ThompsonSamplingMAB


N_ITER = 10000
ALPHA = 10
BETA = 3

Arm = namedtuple("Arm", ["get_reward", "name"])

def _create_arm(p):
    def _():
        return 0 if ( random.uniform(0, 1) > p ) else 1
    return _


# arm_two will be the winner
arms = {
    1: Arm(_create_arm(0.1), "arm_one"),
    2: Arm(_create_arm(0.11), "arm_two"),
    3: Arm(_create_arm(0.05), "arm_three"),
}
bandit = ThompsonSamplingMAB(arms.keys(), alpha=ALPHA, beta=BETA)


actions = []
rewards = []
for unit_id in range(N_ITER):
    action = bandit.select(unit_id)
    reward = arms[action.arm_id].get_reward()
    bandit.record(action, reward)

    actions.append(action)
    rewards.append(reward)

# TODO: plot rolling avg of reward over time

c = Counter([action.arm_id for action in actions])
print("Arm Two wins with One clearly outperforming Three: ", c)
