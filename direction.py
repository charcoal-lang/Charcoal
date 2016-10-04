from enum import Enum

class Direction(Enum):
    left = 1
    up = 2
    right = 4
    down = 8
    up_left = 16
    up_right = 32
    down_left = 64
    down_right = 128

class Pivot(Enum):
    left = 1
    right = 2