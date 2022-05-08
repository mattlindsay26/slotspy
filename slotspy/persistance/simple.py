from collections import namedtuple, defaultdict
from datetime import datetime
from slotspy.utils import ClosedBanditAction
from slotspy.utils.optimizations import (
    ARM_AVERAGE_REWARD, ARM_REWARD_ONE_COUNT, ARM_REWARD_ZERO_COUNT
)

class SimplePersistance():

    optimizations = (ARM_AVERAGE_REWARD, ARM_REWARD_ONE_COUNT, ARM_REWARD_ZERO_COUNT)

    def __init__(self):
        self.open_actions = []
        self.closed_actions = []
        self.arms = []
        self.step_id = 0
        self.optimization_data = defaultdict(lambda: {"count": 0, "total_reward": 0, "is_one": 0, "is_zero": 0})


    def get_optimization(self, optimization):
        # TODO: the datatypes being returned here are crazy
        if optimization not in self.optimizations:
            raise ValueError(f"{optimization} is not an allowed optimization for SimplePersistance")
        if optimization==ARM_AVERAGE_REWARD:
            return [{"arm_id": arm_id, "avg_reward": d['total_reward']/d['count']} for arm_id, d in self.optimization_data.items()]
        if optimization==ARM_REWARD_ONE_COUNT:
            return {arm_id: d['is_one'] for arm_id, d in self.optimization_data.items()}
        if optimization==ARM_REWARD_ZERO_COUNT:
            return {arm_id: d['is_zero'] for arm_id, d in self.optimization_data.items()}


    def create_arms(self, arms):
        self.arms = arms


    def get_open_action(self, unit_id, step_id):
        for open_action in self.open_actions:
            if (open_action.unit_id==unit_id) and (open_action.step_id==step_id):
                return open_action.action


    def create_open_action(self, action):
        # TODO: tz
        created_at = datetime.now()
        self.open_actions.append(
            {
                'action': action,
                "created_at": created_at
            })

    def get_step_id(self):
        return self.step_id

    def add_reward(self, action, reward):
        # TODO: better
        self.open_actions = [oa for oa in self.open_actions if oa['action']!=action]
        self.closed_actions.append(
            ClosedBanditAction(action, reward)
        )
        # this relies on some crazy inplace nonsense - fix
        arm_data = self.optimization_data[action.arm_id]
        arm_data["count"] += 1
        arm_data["total_reward"] += reward
        if (reward == 1):
            arm_data["is_one"] += 1
        if reward == 0:
            arm_data["is_zero"] += 1

    def get_open_actions(self):
        return tuple(self.open_actions)

    def get_closed_actions(self):
        return tuple(self.closed_actions)

    def get_arms(self):
        return tuple(self.arms)
