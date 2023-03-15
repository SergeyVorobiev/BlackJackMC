from montecarlo.grid.Visual import Visual
from montecarlo.sap.Policy import Policy
from montecarlo.sap.State import State
from montecarlo.StateInfoMap import StateInfoMap


class BJStateInfoMap(StateInfoMap):

    def __init__(self, grid=None):
        super().__init__()
        self.__states: [State] = []
        self.__visuals: [Visual] = []
        _id = 0
        self.__states_list: [State] = []
        for player_score in range(4, 22):
            self.__states.append([])
            for dealer_score in range(2, 12):
                visual = None
                if grid is not None:
                    visual = grid[player_score - 4][dealer_score - 2]
                    self.__visuals.append(visual)
                name = str(player_score) + " - " + str(dealer_score)
                state = State(state_id=_id, name=name, actions=[0, 1], info=[player_score, dealer_score], visual=visual)
                self.__states[player_score - 4].append(state)
                _id += 1
                self.__states_list.append(state)
        Policy.build_uniform_policy(self.__states_list)

    def get_states(self) -> [State]:
        return self.__states_list

    def get_visuals(self) -> [Visual]:
        return self.__visuals

    def get_state(self, info) -> State:
        return self.__states[info[0] - 4][info[1] - 2]