'use strict';

var XMovement = new Array(Direction.MAXIMUM + 1);
YMovement = new Array(Direction.MAXIMUM + 1);
NewlineDirection = new Array(Direction.MAXIMUM + 1);
DirectionCharacters = new Array(Direction.MAXIMUM + 1);

XMovement[Direction.left] = -1;
XMovement[Direction.up] = 0;
XMovement[Direction.right] = 1;
XMovement[Direction.down] = 0;
XMovement[Direction.upLeft] = -1;
XMovement[Direction.upRight] = 1;
XMovement[Direction.downLeft] = -1;
XMovement[Direction.downRight] = 1

YMovement[Direction.left] = 0;
YMovement[Direction.up] = -1;
YMovement[Direction.right] = 0;
YMovement[Direction.down] = 1;
YMovement[Direction.upLeft] = -1;
YMovement[Direction.upRight] = -1;
YMovement[Direction.downLeft] = 1;
YMovement[Direction.downRight] = 1

NewlineDirection[Direction.left] = Direction.up;
NewlineDirection[Direction.up] = Direction.right;
NewlineDirection[Direction.right] = Direction.down;
NewlineDirection[Direction.down] = Direction.left;
NewlineDirection[Direction.upLeft] = Direction.upRight;
NewlineDirection[Direction.upRight] = Direction.downRight;
NewlineDirection[Direction.downLeft] = Direction.upLeft;
NewlineDirection[Direction.downRight] = Direction.downLeft

DirectionCharacters[Direction.left] = "-";
DirectionCharacters[Direction.up] = "|";
DirectionCharacters[Direction.right] = "-";
DirectionCharacters[Direction.down] = "|";
DirectionCharacters[Direction.upLeft] = "\\";
DirectionCharacters[Direction.upRight] = "/";
DirectionCharacters[Direction.downLeft] = "/";
DirectionCharacters[Direction.downRight] = "\\"

var PivotLookup = new Array(Pivot.MAXIMUM + 1);
PivotLookup[Pivot.left] = new Array(Direction.MAXIMUM + 1);
PivotLookup[Pivot.right] = new Array(Direcion.MAXIMUM + 1);

PivotLookup[Pivot.left][Direction.left] = Direction.downLeft;
PivotLookup[Pivot.left][Direction.up] = Direction.upLeft;
PivotLookup[Pivot.left][Direction.right] = Direction.upRight;
PivotLookup[Pivot.left][Direction.down] = Direction.downRight;
PivotLookup[Pivot.left][Direction.upLeft] = Direction.left;
PivotLookup[Pivot.left][Direction.upRight] = Direction.up;
PivotLookup[Pivot.left][Direction.downLeft] = Direction.down;
PivotLookup[Pivot.left][Direction.downRight] = Direction.right

PivotLookup[Pivot.right][Direction.left] = Direction.upLeft;
PivotLookup[Pivot.right][Direction.up] = Direction.upRight;
PivotLookup[Pivot.right][Direction.right] = Direction.downRight;
PivotLookup[Pivot.right][Direction.down] = Direction.downLeft;
PivotLookup[Pivot.right][Direction.upLeft] = Direction.up;
PivotLookup[Pivot.right][Direction.upRight] = Direction.right;
PivotLookup[Pivot.right][Direction.downLeft] = Direction.left;
PivotLookup[Pivot.right][Direction.downRight] = Direction.down

var DirectionFromXYSigns = {
    '-1': {
        '-1': Direction.upLeft,
        '0': Direction.left,
        '1': Direction.downLeft
    },
    '0': {
        '-1': Direction.up,
        '0': Direction.right, // actually any would do
        '1': Direction.down
    },
    '1': {
        '-1': Direction.upRight,
        '0': Direction.Right,
        '1': Direction.downRight
    }
}

