from enum import Enum


class Directions(Enum):
    UP = 'UP'
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'
    LEFT = 'LEFT'

    def __neg__(self):
        if self == Directions.UP:
            return Directions.DOWN
        if self == Directions.DOWN:
            return Directions.UP
        if self == Directions.LEFT:
            return Directions.RIGHT
        if self == Directions.RIGHT:
            return Directions.LEFT


for a in Directions:
    print(a)