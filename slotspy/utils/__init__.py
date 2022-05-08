from collections import namedtuple


BanditAction = namedtuple(
    'BanditAction',
    ['unit_id', 'step_id', 'arm_id']
)

ClosedBanditAction = namedtuple("ClosedBanditAction", ["action", "reward"])
