<!-- id='changelog-1.0'-->
# 1.0 — 2025-??-??

## Added
 - example.py
 
## Changed

 - changed folder structure according to pypi packaging tutorial
 
## Fixed

 - line 107 and 108 in README.md, was still referring to an old version of the function

<!-- id='changelog-0.1'-->
# 0.1 — 2025-02-04

## Added

- added missing unittests for list and dictionary returns
- neighbors, in_range, line_draw and hex_in_range function optionally returns hexcoords, lists or a dictionary
- GraphMatrix breadth_first_search, dijkstras_algorithm and a_star_algorithm optionally returns the path coordinates as hexcoords, lists or dictionaries
- adddd a mechanic to GraphMatrix methods del_entry and update_entry that updates GraphMatrix.matrix_coords dictonary
- added radian as output option for get_angle 

## Changed

- removed the arbitrary positional arguments (*) where applicable (don't know what I was thinking in the first place)

## Fixed

- fixed GraphMatrix.update_entry
- fied GraphMatrix.del_entry
- neighbors function description return statement corrected
- added various missing parameter decriptions to docstrings
- various spelling, grammar and content-related mistakes

<!-- id='changelog-0.0.4'-->
# 0.0.4 — 2024-05-11

## Added

- added unittests for GraphMatrix.update_entry (only tests matrix_coords functionality)
- added unittests for GraphMatrix.del_entry (only tests matrix_coords functionality)
- added get_angle function, which calculates the angle from a line drawn from one point to another relative to the x-axis of a cartesian coordinate system
- added unittests for get_angle function

<!-- id='changelog-0.0.3'-->
# 0.0.3 — 2024-01-26

## Added

- added a mechanic initially adding all connected coordinates to a Set GraphMatrix.matrix_coords
- added List and Dictionary as return types for functions offering optional boolean choice to return RectCoords or HexCoords, selection is now based on entering the desired return data type as a String, the options being: "List", "Dict", "Tuple", "Coords" (for RectCoords or HexCoords, depending on returned length)
- added 64_px_example_tilemask.png
- added assertequals for dict and list output in unittests
- GraphMatrix based pathfinding returns None if no path from start to goal was found
- optional parameter for GraphMatrix based pathfinding, test_accessibility, tests if start and goal are connected to other tiles, if not returns None

## Changed

- switched blocked movement for GraphMatrix and methods from 0 to negative values and updated unittests
- switched method of parent directory import of hexlogic to pathlib for unittests

## Fixed

- fixed the shields being displayed after the link to the PyPi page for pygame-pgu and HexGrid in the readme
- spelling in hexlogic.py

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



