from abc import abstractmethod

from montecarlo.sap.Action import Action
from montecarlo.sap.State import State


class Transition(object):

    @abstractmethod
    def get_transition(self, s: State, a: Action, sn: State) -> (float, float):
        ...
