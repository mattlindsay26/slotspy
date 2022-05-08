from bandits.mab.base import BaseMAB
from bandits.persistance import SimplePersistance
from bandits.processor import SimpleProcessor
from bandits.utils import BanditAction
from bandits.utils.optimizations import ARM_AVERAGE_REWARD
# from numpy import random
import random
from collections import defaultdict


class EpsilonGreedyMAB(BaseMAB):

    optimizations = (ARM_AVERAGE_REWARD,)

    def __init__(self, arms, epsilon=0.1, burn_in=100, persistance=None, processor=None):
        self.epsilon = epsilon
        self.burn_in = burn_in

        if persistance is None:
            self.persistance = SimplePersistance()
        else:
            self.persistance = persistance

        self.persistance.create_arms(arms)

        if processor is None:
            self.processor = SimpleProcessor()
        else:
            self.processor = processor

        self.optimized = all([opt in self.persistance.optimizations for opt in self.optimizations])
            


    # move to base?
    @property
    def arms(self):
        return self.persistance.get_arms()

    @property
    def open_actions(self):
        return self.persistance.get_open_actions()

    def _select(self, unit_id, step_id):
        if ( self.burn_in is not None ) and ( len(self.persistance.get_closed_actions())<self.burn_in ):
            arm_id = self._random_arm()
        elif random.uniform(0, 1)<self.epsilon:
            arm_id = self._random_arm()
        else:
            arm_id = self._best_arm()
        return BanditAction(unit_id, step_id, arm_id)


    def _record(self, action, reward):
        self.persistance.add_reward(action, reward)

    def _random_arm(self):
        return random.choice(self.persistance.get_arms())

    def _best_arm(self):
        if self.optimized:
            return self._optimized_best_arm()

        # TODO: improve
        closed_actions =  self.persistance.get_closed_actions()
        if not closed_actions:
            return self._random_arm()

        results = defaultdict(lambda: {'count': 0, 'total_reward':0})
        for closed_action in closed_actions:
            results[closed_action.action.arm_id]["count"] += 1
            results[closed_action.action.arm_id]["total_reward"] += closed_action.reward

        sorted_arms = sorted(
            [(arm_id, result) for arm_id, result in results.items()],
            key=lambda x: -x[1]['total_reward']/x[1]['count']
        )
        return sorted_arms[0][0]

    def _optimized_best_arm(self):
        arm_avg_rewards = self.persistance.get_optimization(ARM_AVERAGE_REWARD)
        sorted_arms = sorted(arm_avg_rewards, key=lambda x: -x['avg_reward'])
        return sorted_arms[0]['arm_id']