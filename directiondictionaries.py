from direction import Direction, Pivot

XMovement = {
    Direction.left: -1,
    Direction.up: 0,
    Direction.right: 1,
    Direction.down: 0,
    Direction.up_left: -1,
    Direction.up_right: 1,
    Direction.down_left: -1,
    Direction.down_right: 1
}

YMovement = {
    Direction.left: 0,
    Direction.up: -1,
    Direction.right: 0,
    Direction.down: 1,
    Direction.up_left: -1,
    Direction.up_right: -1,
    Direction.down_left: 1,
    Direction.down_right: 1
}

NewlineDirection = {
    Direction.left: Direction.up,
    Direction.up: Direction.right,
    Direction.right: Direction.down,
    Direction.down: Direction.left,
    Direction.up_left: Direction.up_right,
    Direction.up_right: Direction.down_right,
    Direction.down_left: Direction.up_left,
    Direction.down_right: Direction.down_left
}

NextDirection = {
    Direction.left: Direction.up_left,
    Direction.up: Direction.up_right,
    Direction.right: Direction.down_right,
    Direction.down: Direction.down_left,
    Direction.up_left: Direction.up,
    Direction.up_right: Direction.right,
    Direction.down_left: Direction.left,
    Direction.down_right: Direction.down
}

DirectionCharacters = {
    Direction.left: "-",
    Direction.up: "|",
    Direction.right: "-",
    Direction.down: "|",
    Direction.up_left: "\\",
    Direction.up_right: "/",
    Direction.down_left: "/",
    Direction.down_right: "\\"
}

PivotLookup = {
    Pivot.left: {
        Direction.left: Direction.down_left,
        Direction.up: Direction.up_left,
        Direction.right: Direction.up_right,
        Direction.down: Direction.down_right,
        Direction.up_left: Direction.left,
        Direction.up_right: Direction.up,
        Direction.down_left: Direction.down,
        Direction.down_right: Direction.right
    },
    Pivot.right: {
        Direction.left: Direction.up_left,
        Direction.up: Direction.up_right,
        Direction.right: Direction.down_right,
        Direction.down: Direction.down_left,
        Direction.up_left: Direction.up,
        Direction.up_right: Direction.right,
        Direction.down_left: Direction.left,
        Direction.down_right: Direction.down
    }
}

DirectionFromXYSigns = {
    -1: {-1: Direction.up_left, 0: Direction.left, 1: Direction.down_left},
    0: {-1: Direction.up, 0: Direction.right, 1: Direction.down},
    1: {-1: Direction.up_right, 0: Direction.right, 1: Direction.down_right}
}
