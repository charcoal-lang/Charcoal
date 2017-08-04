from enum import Enum


class Direction(Enum):
    left = 1
    up = 2
    right = 3
    down = 4
    up_left = 5
    up_right = 6
    down_left = 7
    down_right = 8

DirectionToString = {
    Direction.left: "←",
    Direction.up: "↑",
    Direction.right: "→",
    Direction.down: "↓",
    Direction.up_left: "↖",
    Direction.up_right: "↗",
    Direction.down_left: "↙",
    Direction.down_right: "↘"
}


class Pivot(Enum):
    left = 1
    right = 2
