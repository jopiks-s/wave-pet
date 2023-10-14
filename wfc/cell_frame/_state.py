from enum import Enum


class State(Enum):
    Stable = 'Neither collapsed nor broken'
    Collapsed = 'Cell was successfully collapsed'
    Broken = 'WFC failed to collapse this cell'
