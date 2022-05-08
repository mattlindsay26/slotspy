from collections import namedtuple
from datetime import datetime
import sqlite3


ClosedBanditAction = namedtuple("ClosedBanditAction", ["action", "reward"])


OPEN_ACTIONS_CREATE_TABLE = """
    create table if not exixts bandits_open_actions as (
        unit_id: VARCHAR,
        step_id: VARCHAR,
        arm_id: VARCHAR,
        created_at: DATETIME
    )
"""

CLOSED_ACTIONS_CREATE_TABLE = """
    create table if not exixts bandits_closed_actions as (
        unit_id: VARCHAR,
        step_id: VARCHAR,
        arm_id: VARCHAR,
        reward: FLOAT
    )
"""

ARMS_CREATE_TABLE = """
    create table if not exixts bandits_arms as (
        arm_id: VARCHAR,
        is_active: BOOLEAN
    )
"""

# should this just be SQL (SQL Alchemy) and BYO-DB
class SqlitePersistance():

    def __init__(self, filename):
        # check if file exixts
        pass

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

    def get_open_actions(self):
        return tuple(self.open_actions)

    def get_closed_actions(self):
        return tuple(self.closed_actions)

    def get_arms(self):
        return tuple(self.arms)