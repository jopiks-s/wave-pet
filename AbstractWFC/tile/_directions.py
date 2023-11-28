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

    def symbol(self):
        if self == Directions.UP:
            return '↑'
        if self == Directions.DOWN:
            return '↓'
        if self == Directions.LEFT:
            return '←'
        if self == Directions.RIGHT:
            return '→'
