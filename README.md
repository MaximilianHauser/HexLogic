<!-- PROJECT TITLE -->
# HexLogic


<!-- PROJECT SHIELDS -->

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/MaximilianHauser/HexLogic)
![Static Badge](https://img.shields.io/badge/python-%3E3.9-blue)
![GitHub](https://img.shields.io/github/license/MaximilianHauser/HexLogic)


<!-- DISCRIPTION -->
HexLogic aims to be a Python package, without dependencies outside of the 
built-in library, providing fully documented functions to deal with the 
relations between objects on a hexagon tiled grid. Including conversion from 
„hexagonal“ to „pixel“ coordinates and pathfinding with varying movement cost. 
As well as various operations like line-drawing.

<!-- WHY HEXLOGIC -->
## Is there a requirement for Hexlogic?

Although there have been various attempts at bundling the functionalities, 
outlined by Amit Patel on redblobgames.com and providing them on the Python 
Package Index, there is currently no package available, that provides all 
the following features:

 - documentation
 - type-hinted
 - drop-in usability
 - includes pathfinding algorithms
 - not an OOP focused implementation

<!-- DESIGNCHOICES -->
## On design choices
 - Drop-in usability can be achieved using an object-oriented approach, as Python allows for multiple inheritance. Despite that opting for a function based approach, has the benefit, of only having to add the coordinates to the objects positioned on the hexagonal grid, which ultimately keeps the separation between the different building blocks of code cleaner and sidesteps possible conflicts between parent classes.
 - The file started out as a part of a Pygame-CE project, as a result, the design is built around the idea of positioning units, tiles etc. being childclasses of pygame.sprite.Sprite on a map.
 - A lesson learned from this ongoing project, is that with increasing scope of the project it becomes desirable to catch errors early, which is the reason for the divergence from the minimalistic pythonic approach to code.

<!-- PREREQUESITES -->
## Prerequisites
 - Python 3.9 or newer
 - Pandas (to be removed as dependency in the future)
 - Numpy (to be removed as dependency in the future)

<!-- INSTALLATION -->
## Installation

### Python Package Index

```sh
   pip install hexlogic
```

### Manually (Github)

```sh
  git clone https://github.com/MaximilianHauser/HexLogic.git
```

<!-- USAGE -->
## Usage
These functions assume you're using objects to represent tiles, units, items, 
etc. on a map that is made up of hexagonal shaped tiles, with a flat side as top.
It furthermore assumes you are using a 3-dimensional cartesian coordinate system,
that assigns the coordinates along axis parallel to the orientation of the sides
of each hexagon. Like in the example given below. When using Pygame-CE it is 
recommended to use square images and draw a hexagon on them. An example of a 
64x64 tile is provided.
```
      +s \        / -r
          \  _   /                   A: ( q=0, r=0, s=0 )
         _ / B \ _                   B: ( q=0, r=-1, s=1 )
       / G \ _ / C \                 C: ( q=1, r=-1, s=0 )
 -q __ \ _ / A \ _ / __ +q           D: ( q=1, r=0, s=-1 )
       / F \ _ / D \                 E: ( q=0, r=1, s=-1 )
       \ _ / E \ _ /                 F: ( q=-1, r=1, s=0 )
           \ _ /                     G: ( q=-1, r=0, s=1 )
         /      \
     +r /        \ -s
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
    
Functions:
----------
**float_to_int(num_in:int|float) -> int|float:**  
Returns an Integer if passed an Integer or if passed a Float with its decimal being zero. Returns a Float if passed a Float, with a non zero decimal.

**tuple_or_object(tuple_or_object:object|tuple|RectCoords|HexCoords, expected_len:2|3, return_coords_obj:bool=False) -> tuple|RectCoords|HexCoords:**  
Returns a tuple or a namedtuple of predefined length, when passed an object or a tuple.

**linint(a:int|float, b:int|float, t:int|float) -> int|float:**  
Linear interpolation returns point at t of distance between a and b.
    
**rect_linint(xy_a:object|tuple|RectCoords, xy_b:object|tuple|RectCoords, t:int|float, return_coords_obj:bool=False) -> tuple|RectCoords:**  
Linear interpolation returns point at t of distance between a and b on a cartesian coordinates system.
    
**cube_linint(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords, t:int|float, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Returns the hextile coordinates of a point situated at t part of the way from obj_a to obj_b.
    
**round_container(container:dict|list|set|tuple|RectCoords, *, d:int=0) -> dict|list|set|tuple|RectCoords:**  
Rounds each number in a container to the specified decimal, if None is specified to the nearest Integer.
    
**round_hex(qrs:tuple|HexCoords, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Rounds each of the coordinates to the nearest integer.
    
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
    
**pixel_to_hex(xy:object|tuple|RectCoords, *, tile_width:int=64, tile_height:int=64, return_coords_obj:bool=False) -> tuple|HexCoords:**  
Converts pixel coordinates to cube coordinates.
    
**neighbors(qrs:object|tuple|HexCoords) -> set:**  
Return a list of coordinates of neighboring hexagons.
    
**distance(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> int|float:**
Returns distance from one object to another in a cube coordinate system.
    
**in_range(obj:object|tuple|HexCoords, n:int) -> set:**
Returns a set containing the cube coordinates of every hexagon in distance n from obj.
    
**line_draw(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> tuple:**  
Draws a line from one hexagon to another, returns a tuple containing the hexagons with the center closest to the line.
    
**dist_lim_flood_fill(start_obj:object|tuple|HexCoords, n:int, obj_grp:list|set, block_var:str=None) -> set:**  
All cube coordinates within n distance from an object, factoring in block_var (variable if True blocks object traversability).

**create_graph_matrix(tile_grp:list|set) -> pd.DataFrame:**
Creates a Pandas DataFrame, containing a directed, weighted graph, from the objects or coordinates contained in tile_grp.

**breadth_first_search(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, graph_matrix_df:pd.DataFrame) -> list:**  
Algorithm for searching a tree data structure for a node that satisfies a given property.

**dijkstras_algorithm(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, graph_matrix_df:pd.DataFrame) -> list:**  
Supports weighted movement cost.
    
**a_star_algorithm(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, graph_matrix_df:pd.DataFrame) -> list:**  
Modified version of Dijkstra’s Algorithm that is optimized for a single destination. It prioritizes paths that seem to be leading closer to a goal.

<!-- TODO -->
## To Do
* [ ] eliminate dependency on NumPy and Pandas, by replacing the interim solution for graph matrix storage with built-in types
* [ ] identify and test for edge cases
* [ ] add example.py
* [ ] modify round_container to work for infinitely nested containers

<!-- REFERENCES -->
## References
redblobgames.com (Amit Patel):
[Hexagons](https://www.redblobgames.com/grids/hexagons/),
[Hexagons Implementation Guide](https://www.redblobgames.com/grids/hexagons/implementation.html),
[Hexagons Generated Code](https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py),
[Pathfinding](https://www.redblobgames.com/pathfinding/a-star/introduction.html),
[Pathfinding Implementation Guide](https://www.redblobgames.com/pathfinding/a-star/implementation.html)


