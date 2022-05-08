import random
from datetime import datetime


class SimpleProcessor():
    """
    Very simple processor for managing actions. Will be triggered pct_process% of the time
    Will keep len(actions)<=max_open_actions and will keep oldest action younger than time_to_expire
    'cleared' actions will be set to reward 0.
    """

    def __init__(self, default_reward=0, pct_process=1.0, time_to_expire=3600, max_open_actions=2048):
        if (pct_process<=0) or (pct_process>1):
            raise ValueError("pct_processs must be in (0, 1].")
        if (time_to_expire is not None) and (time_to_expire<0):
            raise ValueError("time_to_expire must be positive or None. To allow arbitarily old open, set time_to_expire=None")
        if (max_open_actions is not None) and (max_open_actions<0):
            raise ValueError("max_open_actions must be positive or None. To allow unlimited open, set max_open_actions=None")

        self.default_reward = default_reward
        self.pct_process = pct_process
        self.time_to_expire = time_to_expire
        self.max_open_actions = max_open_actions

    def should_process_open(self, *args, **kwargs):
        return random.uniform(0, 1) < self.pct_process

    def process_open(self, persistance):
        # eliminate old action first, then check length vs max_open_actions
        # when this step is over, length will be less than max_open_actions
        # & oldest action will be younger than time_to_expire

        # TODO: performance - do not pull all but don't be a burden on BasePersistance
        actions = persistance.get_open_actions()
        if not actions:
            return None
        now = datetime.now()

        # handle old actions
        actions_to_close = [o for o in actions if ( now - o['created_at'] ).total_seconds() > self.time_to_expire]
        for open_action in actions_to_close:
            persistance.add_reward(open_action["action"], reward=self.default_reward)

        # trim list to max_open_actions
        if ( len(actions)-len(actions_to_close) ) > self.max_open_actions:
            num_actions_to_close = len(actions) - len(actions_to_close) - self.max_open_actions
            sorted_actions = sorted(actions, key=lambda x: x['created_at'])
            for open_action in sorted_actions[:num_actions_to_close]:
                persistance.add_reward(open_action["action"], reward=self.default_reward)
