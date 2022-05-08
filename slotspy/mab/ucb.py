from bandits.mab.base import BaseMAB
from bandits.persistance import SimplePersistance
from bandits.processor import SimpleProcessor
from bandits.utils import BanditAction
# from numpy import random
import random
from collections import defaultdict


class UCBMAB(BaseMAB):

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

    # move to base?
    @property
    def arms(self):
        return self.persistance.get_arms()

    @property
    def open_actions(self):
        return self.persistance.get_open_actions()

    def _select(self, unit_id, step_id):
        raise NotImplemented


    def _record(self, action, reward):
        raise NotImplemented