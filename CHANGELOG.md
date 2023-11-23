<!-- id='changelog-0.0.3'-->
# 0.0.3 — 2023-11-XX

## Added

- added a mechanic initially adding all connected coordinates to a Set GraphMatrix.matrix_coords

## Changed

- switched blocked movement for GraphMatrix and methods from 0 to negative values and updated unittests

## Fixed

- fixed the shields being displayed after the link to the pypi page for pygame-pgu and HexGrid in the readme

<!-- id='changelog-0.0.2'-->
# 0.0.2 — 2023-11-03

## Changed

- Moved breadth_first_search() from an independent function to being a method of GraphMatrix
- dijkstras_algorithm() from an independent function to being a method of GraphMatrix
- a_star_algorithm() from an independent function to being a method of GraphMatrix
- removed block_var, being a Boolean from dist_lim_flood_fill and replaced it with movement_cost, being numerical, blocking movement if equal to 0
- adapted unittests to changes


<!-- id='changelog-0.0.1'-->
# 0.0.1 — 2023-10-25

## Added

- Initial release.



