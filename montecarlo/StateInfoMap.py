from abc import abstractmethod

from montecarlo.sap.State import State


class StateInfoMap(object):

    def __init__(self):
        pass

    @abstractmethod
    def get_state(self, info) -> State:
        ...

    @abstractmethod
    def get_states(self) -> [State]:
        ...
