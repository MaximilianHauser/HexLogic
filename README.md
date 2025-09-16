
# HexLogic


![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/MaximilianHauser/HexLogic)
![Static Badge](https://img.shields.io/badge/python-%3E3.10-blue)
![GitHub](https://img.shields.io/github/license/MaximilianHauser/HexLogic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hexlogic)



HexLogic aims to be a Python package, without dependencies outside of the 
built-in library, providing fully documented classes and functions to deal with 
the relations between objects on a hexagon tiled grid. Including conversion from 
„hexagonal“ to „pixel“ coordinates and pathfinding with varying movement cost. 
As well as various operations like line-drawing.


## Is there a requirement for Hexlogic?

Although there have been various attempts at bundling the functionalities, 
outlined by Amit Patel on redblobgames.com and providing them on the Python 
Package Index, there is currently no package available, that provides all 
the following features:

 - documentation
 - type-hinted
 - drop-in usability
 - includes pathfinding algorithms
 - not an OOP only implementation


## On design choices
 - Drop-in usability can be achieved using an object-oriented approach, as Python allows for multiple inheritance. Despite that opting for a function based approach, has the benefit, of only having to add the coordinates to the objects positioned on the hexagonal grid, which ultimately keeps the separation between the different building blocks of code cleaner and sidesteps possible conflicts between parent classes.
 - The file started out as a part of a Pygame-CE project, as a result, the design is built around the idea of positioning units, tiles etc. being childclasses of pygame.sprite.Sprite on a map.
 - A lesson learned from this ongoing project, is that with increasing scope of the project it becomes desirable to catch errors early, which is the reason for the divergence from the minimalistic pythonic approach to code.


## Prerequisites
 - Python 3.10 or newer


## Installation

### Python Package Index

```sh
   pip install hexlogic
```

### Manually (Github)

```sh
  git clone https://github.com/MaximilianHauser/HexLogic.git
```


## Usage
These functions assume you're using objects to represent tiles, units, items, 
etc on a map that is made up of hexagonal shaped tiles, with a flat side as top.
It furthermore assumes you're using a 3-dimensional cartesian coordinate system,
that assigns the coordinates along axis parallel to the orientation of the sides
of each hexagon. Like in the example given below. When using Pygame-CE it is 
recommended to use square images and draw a hexagon on them. An example of a 
64x64 tile is provided, it's intended to be used with the transparency colorcode 
set to (255, 0, 255). Currently the package does not support drawing hexagons.
```
     +s \         / -r
         \   _   /                   A: ( q=0, r=0, s=0 )
         _ / B \ _                   B: ( q=0, r=-1, s=1 )
       / G \ _ / C \                 C: ( q=1, r=-1, s=0 )
 -q __ \ _ / A \ _ / __ +q           D: ( q=1, r=0, s=-1 )
       / F \ _ / D \                 E: ( q=0, r=1, s=-1 )
       \ _ / E \ _ /                 F: ( q=-1, r=1, s=0 )
           \ _ /                     G: ( q=-1, r=0, s=1 )
        /        \
    +r /          \ -s
```
Contains all hextile logic, specified as logic handling the relationship 
between cartesian coordinates and cube coordinates, for the purpose of defining 
the relative position of hexagon tiles on the screen. In addition it provides
calculations in regards to hextile map related formulas and algorithms.

Custom Errors:
--------------
**ConstraintViolation(ValueError):**  
Custom Error to be raised when a logical constraint is violated. 

Classes:
--------
**RectCoords(namedtuple("RectCoords", "x y")):**  
Coordinates in a rectangular cartesian coordinate system.

**HexCoords(namedtuple("HexCoords", "q r s")):**  
Coordinates in a three-dimensional cartesian coordinate system, limited by the constraint q + r + s = 0.

**GraphMatrix(tile_grp:set|list):**  
    Creates a GraphMatrix object, containing a directed, weighted graph, from the 
    objects or coordinates contained in tile_grp, organized in a Dictionary.
    
Functions and Methods:
----------------------
**float_to_int(num_in:int|float) -> int|float:**  
Returns an Integer if passed an Integer or if passed a Float with its decimal being zero. Returns a Float if passed a Float, with a non zero decimal.

**container_or_object(container_or_object:object|tuple|RectCoords|HexCoords, expected_len:2|3, return_obj_type:str="Tuple") -> tuple|RectCoords|HexCoords|list|dict:**
Returns a Tuple, Namedtuple, List or Dictionary of predefined length, when passed an Object or a Tuple.

**linint(a:int|float, b:int|float, t:int|float) -> int|float:**  
Linear interpolation returns point at t of distance between a and b.
    
**rect_linint(xy_a:object|tuple|RectCoords, xy_b:object|tuple|RectCoords, t:int|float, return_coords_obj:bool=False) -> tuple|RectCoords:**  
Linear interpolation returns point at t of distance between a and b on a cartesian coordinates system.
    
**cube_linint(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords, t:int|float, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Returns the hextile coordinates of a point situated at t part of the way from obj_a to obj_b.
    
**round_container(container:dict|list|set|tuple|RectCoords, d:int=0) -> dict|list|set|tuple|RectCoords:**  
Rounds each number in a container to the specified decimal, if None is specified to the nearest Integer.
    
**round_hex(qrs:tuple|HexCoords, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Rounds each of the coordinates to the nearest Integer.
    
**get_xy(obj:object, return_coords_obj:bool=False) -> tuple|RectCoords:**  
Returns values of attributes x and y of obj as Tuple or RectCoords.
    
**set_xy(obj:object, x:int|float, y:int|float) -> None:**  
Set x and y attribute of obj to specified values.
    
**get_qrs(obj:object, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Returns values of attributes q, r, s of obj.
    
**set_qrs(obj:object, q:int|float, r:int|float, s:int|float) -> None:**  
Set q r and s attribute of obj to specified values.
    
**hex_to_pixel(qrs:object|tuple|HexCoords, tile_width:int=64, tile_height:int=64, return_coords_obj:bool=False) -> tuple|RectCoords:**  
Converts cube coordinates to pixel coordinates.
    
**pixel_to_hex(xy:object|tuple|RectCoords, tile_width:int=64, tile_height:int=64, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Converts pixel coordinates to cube coordinates.

**get_angle(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> float:**  
Returns the angle from a line through obj_a and abj_b relative to the x-axis of a two dimensional cartesian coordinate system.
    
**neighbors(qrs:object|tuple|HexCoords) -> set:**  
Return a List of coordinates of neighboring hexagons.
    
**distance(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> int|float:**
Returns distance from one Object to another in a cube coordinate system.
    
**in_range(obj:object|tuple|HexCoords, n:int) -> set:**
Returns a Set containing the cube coordinates of every hexagon in distance n from obj.
    
**line_draw(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> tuple:**  
Draws a line from one hexagon to another, returns a Tuple containing the hexagons with the center closest to the line.
    
**dist_lim_flood_fill(start_obj:object|tuple|HexCoords, n:int, obj_grp:list|set, movement_var:str=None) -> set:**  
All cube coordinates within n distance from an Object, factoring in movement_var (variable if 0 blocks object traversability).

**GraphMatrix.update_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords, movement_cost:int|float) -> None:**
Add or update a one-directional entry in the adjacency matrix.
    
**GraphMatrix.del_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> None:**
Delete a one-directional entry in the adjacency matrix. Does not raise an Error or Warning if no entry matching the input exists.
    
**GraphMatrix.connected(self, from_coord:object|tuple|HexCoords) -> set:**
Return all connected coordinates. Returns None, in case of there aren't being any.

**GraphMatrix.get_movement_cost(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> int|float:**
Get the movement cost from one Object or coordinate to another.

**GraphMatrix.breadth_first_search(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, test_accessibility:bool=False) -> list:**  
Algorithm for searching a tree data structure for a node that satisfies a given property.

**GraphMatrix.dijkstras_algorithm(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, test_accessibility:bool=False) -> list:**  
Supports weighted movement cost.
    
**GraphMatrix.a_star_algorithm(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, test_accessibility:bool=False) -> list:**  
Modified version of Dijkstra’s Algorithm that is optimized for a single destination. It prioritizes paths that seem to be leading closer to a goal.


## To Do
List of issues to be solved before the package will be released at version 1.0

* [x] eliminate dependency on NumPy and Pandas, by replacing the interim solution for graph matrix storage with built-in types
* [x] add example.py
* [x] ~~identify and test for edge cases~~
* [ ] modify round_container to work for infinitely nested containers
* [x] add a set ~~that is ?automatically? updated~~, containing all coordinates which are linked in GraphMatrix
* [ ] write a working testgrp_teardown
* [x] replace "block_var" artifacts with movement_cost = 0 -> tile = blocked for "dist_lim_flood_fill"
* [x] add pathfinding functions as methods to GraphMatrix
* [x] negative movement_cost for blocking movement instead of 0 ?
* [x] ~~refactor code to be organized around one class handling all the logic affecting objects in passed container (like observer.py etc.), keep functions only implementation ???~~
* [x] ~~find out why and~~ fix imports in test not working (RectCoords instead of hl.RectCoords etc.)
* [x] add ~~a raise error, if a goal or start is passed to pathfinding, which is inaccessible (has negative movement_cost)~~ option to test accessibility
* [x] add a "if not connected functionality" to pathfinding algorithms
* [x] update TestTestgrpGenerator unittest, block_var to movement_cost
* [x] add a mechanic to GraphMatrix methods del_entry and update_entry that update GraphMatrix.matrix_coords
* [x] add List and Dictionary as a return option for functions, which offered only Tuple and RectCoords/HexCoords
* [x] update remaining unittests to test for dictionary and list outputs, as well as modified GraphMatrix pathfinding
* [x] format text so it is displayed correctly in editors help function if possible
* [x] ~~find a way around the unhashable type error for~~ in_range or just return as list or dict instead of set
* [x] add missing GraphMatrix unittests
* [x] fix invalid escape sequence printout for diagram at the head of example.py
* [ ] breadth first search error: TypeError: argument of type 'NoneType' is not iterable
* [ ] "from_c not in self.matrix_coords and from_c not in destinations" printout in console when running unittests


## References
redblobgames.com (Amit Patel):  
[Hexagons](https://www.redblobgames.com/grids/hexagons/)  
[Hexagons Implementation Guide](https://www.redblobgames.com/grids/hexagons/implementation.html)  
[Hexagons Generated Code](https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py)  
[Pathfinding](https://www.redblobgames.com/pathfinding/a-star/introduction.html)  
[Pathfinding Implementation Guide](https://www.redblobgames.com/pathfinding/a-star/implementation.html)  
NumPy Style Guide:  
[syntax and best practices for docstrings](https://numpydoc.readthedocs.io/en/latest/format.html)  


## Other packages on the Python Package Index offering hexagonal grid functionalities:  
Prior to deciding to make Hexlogic a package available on PyPI, I researched other available 
implementations to check if it had already been implemented in the way envisioned and on the 
other hand to learn from other people's work. Below is a list of the packages found which are thematically 
closest to my own. Check them out! Depending on what you're trying to do some of them might be better 
suited for your needs.


**HexPex**  
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/solbero/hexpex)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hexpex)
https://pypi.org/project/hexpex/  
 - OOP implementation based on single coordinate
 - cube and axial coordinates, directions (facing up)
 - distances, neighbors, range, rings, rotation, spiral

**Hexutil**  
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/stephanh42/hexutil)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hexutil)
https://pypi.org/project/hexutil/
 - OOP implementation based on single coordinate
 - comprehensive implementation of "pointy side up" hexagonal game focused map logic
 - including pathfinding and field of view

**pygame-pgu**  
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/parogers/pgu)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pygame-pgu)
https://pypi.org/project/pygame-pgu/
 - a COMPREHENSIVE collection of handy modules and scripts for PyGame

**HexGrid**  
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/rosshamish/hexgrid)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hexgrid)
https://pypi.org/project/hexgrid/
 - "Settlers of Catan" - grid, complete with tile, edge and node coordinates
 - Used by JSettlers2, described in "Thomas, Robert S. 2003. Real-time Decision Making for Adversarial Environments Using a Plan-based Heuristic. PhD thesis, Northwestern University"


