from abc import ABC, abstractproperty, abstractmethod
from slotspy.utils import BanditAction


class BaseMAB(ABC):
    # TODO: be explicit about stationary vs non-stationary

    # some sort of load / save / create flow

    @abstractproperty
    def arms(self):
        # return list of arm_ids
        pass

    @abstractproperty
    def open_actions(self):
        # returns step_ids that are open
        pass

    def get_action(self, unit_id, step_id):
        return self.persistance.get_action(unit_id, step_id)
    
    # is step_id global or tracked in persistance? - tracked in persistance
    def select(self, unit_id):
        # TODO: pull out of base
        if self.processor.should_process_open(self.persistance):
            self.processor.process_open(self.persistance)
        step_id = self.persistance.get_step_id()
        action =  self._select(unit_id, step_id)
        self.persistance.create_open_action(action)
        return action

    def record(self, action, reward):
        if self.processor.should_process_open(self.persistance):
            self.processor.process_open(self.persistance)
        return self._record(action, reward)

    # def add_arm(self, arm_id, arm_name=None, **kwargs):
    #     pass

    # def remove_arm(self, arm_id):
    #     pass

    # def add / remove units

    # def increment step

    @abstractmethod
    def _select(self):
        # returns  arm_id
        pass

    @abstractmethod
    def _record(self, step_id, reward):
        pass



class BaseMABUnits():
    # needs to be able to handle switching cost
    pass


class BaseMABBatch():
    # is this needed?
    pass