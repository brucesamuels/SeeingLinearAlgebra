# Checkpoint 131 - Generalized Encasement and Shoelace

This revision corrects both visual methods.

## Encasement
The parallelogram has labeled vertices `(0,0)`, `(a,c)`, `(a+b,c+d)`, `(b,d)` and is enclosed by the actual bounding rectangle from `(0,0)` to `(a+b,c+d)`.

The six exterior pieces are shown and labeled:
`ac/2, bc, bd/2, bd/2, bc, ac/2`.

Thus:
`A_box=(a+b)(c+d)`
`A_outside=ac+bd+2bc`
`A_para=(a+b)(c+d)-(ac+bd+2bc)=ad-bc`.

## Shoelace
The same generalized coordinates are placed in two columns with the first row repeated. Green descending diagonals and red ascending diagonals visibly create the forward and backward products before simplifying to `ad-bc`.

## Visual refinement

The red shoelace diagonals now mirror the green diagonal spacing: each line stops just before the coordinate glyph at both ends instead of crossing through the text.
