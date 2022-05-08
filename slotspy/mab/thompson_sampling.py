from bandits.mab.base import BaseMAB
from bandits.persistance import SimplePersistance
from bandits.processor import SimpleProcessor
from bandits.utils import BanditAction
from bandits.utils.optimizations import ARM_REWARD_ONE_COUNT, ARM_REWARD_ZERO_COUNT
# from numpy import random
import random
from collections import defaultdict


class ThompsonSamplingMAB(BaseMAB):

    optimizations = (ARM_REWARD_ONE_COUNT, ARM_REWARD_ZERO_COUNT)

    def __init__(self, arms, alpha=None, beta=None, alphas=None, betas=None, persistance=None, processor=None):
        if (alpha is not None) or (beta is not None):
            if (alpha is None) or (beta is None):
                raise ValueError("If either alpha or beta are provided then both alpha and beta must be provided as positive numbers")
            if alpha<=0:
                raise ValueError("alpha must be postive.")
            if beta<=0:
                raise ValueError("beta must be postive.")
            if (alphas is not None) or (betas is not None):
                raise ValueError("Cannot use { alpha,  beta } and { alphas, betas }. Must use one set or the other")
            self.initial_alphas = {arm: alpha for arm in arms}
            self.initial_betas = {arm: beta for arm in arms}
        else:
            if (alphas is None) or (betas is None):
                raise ValueError("Must provide one of { alpha,  beta } or { alphas, betas }. Must use one set or the other")
            # TODO: check alphas & betas are array-like
            if (len(alphas) != len(arms)) or (len(betas) != len(arms)):
                raise ValueError("alphas and betas must be the same length as arms")
            for idx, a in enumerate(alphas):
                if a<=0:
                    raise ValueError(f"The {idx} element of alphas is {a} which is negative and invalid. Provide a positive value")

            for idx, b in enumerate(betas):
                if b<=0:
                    raise ValueError(f"The {idx} element of betas is {b} which is negative and invalid. Provide a positive value")
            self.initial_alphas = {arm: alpha for arm, alpha in zip(arms, alphas)}
            self.initial_betas = {arm: beta for arm, beta in zip(arms, betas)}
        
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
        if not self.optimized:
            raise NotImplemented
        arm_one_counts = self.persistance.get_optimization(ARM_REWARD_ONE_COUNT)
        arm_zero_counts = self.persistance.get_optimization(ARM_REWARD_ZERO_COUNT)
        # print(arm_zero_counts)
        max_sample, winning_arm = -1, self.arms[0] # is this the right initial value for winning_arm?
        for arm in self.arms:
            a = arm_one_counts.get(arm, 0) + self.initial_alphas[arm]
            b = arm_zero_counts.get(arm, 0) + self.initial_betas[arm]
            sample = random.betavariate(a, b)

            # print(arm, arm_one_counts.get(arm, 0), arm_zero_counts.get(arm, 0), self.initial_alphas[arm], self.initial_betas[arm])
            # print(arm, a, b, sample)
            # print()

            if sample>max_sample:
                max_sample, winning_arm = sample, arm
        return BanditAction(unit_id, step_id, winning_arm)

    def _record(self, action, reward):
        if reward not in (0, 1):
            raise ValueError("ThompsonSampling reward must be 0 or 1")
        self.persistance.add_reward(action, reward)
