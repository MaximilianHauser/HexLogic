"""
Created on Fri Sep  9 07:19:00 2022

HexLogic aims to be a Python package, without dependencies outside of the 
built-in library, providing fully-documented functions to deal with the relations 
between objects on a hexagon tiled grid. Including conversion from „hexagonal“ to 
„pixel“ coordinates and pathfinding with varying movement cost. As well as 
various operations like line-drawing. It was originally part of a Pygame-CE 
project I'm working on and is therefore primarily intended to position a 
hexagon tiled map on a screen and deal with game mechanics related to this type 
of grid.

These functions assume you're using objects to represent tiles, units, items, 
etc on a map that is made up of hexagonal shaped tiles, with a flat side as top.
It furthermore assumes you're using a 3-dimensional cartesian coordinate system,
that assigns the coordinates along axis parallel to the orientation of the sides
of each hexagon. Like in the example given below. When using Pygame-CE it is 
recommended to use square images and draw a hexagon on them. An example of a 
64x64 tile is provided, it's intended to be used with the transparency colorcode 
set to (255, 0, 255). Currently the package does not support drawing hexagons.

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

Contains all hextile logic, specified as logic handling the relationship 
between cartesian coordinates and cube coordinates, for the purpose of defining 
the relative position of hexagon tiles on the screen. In addition it provides
calculations in regards to hextile map related formulas and algorithms.

The functions are designed to catch divergence from the desired input as early 
as possible, this might be considered "unpythonic" by some, but given the scope 
of even a simple game, I found this to be my personal preference. A keywordargument 
will be added in the future to switch between current and a more pythonic functionality.


Dependencies:
-------------
collections.namedtuple
    Provides a new tuple subclass. The new subclass is used to create tuple-like 
    objects that have fields accessible by attribute lookup as well as being 
    indexable and iterable.
    
unittest
    The unittest unit testing framework supports test automation sharing of 
    setup and shutdown code for tests, aggregation of tests into collections,
    and independence of the tests from the reporting framework.


Custom Errors:
--------------
ConstraintViolation(ValueError)
    Custom Error to be raised when a logical constraint is violated. 


Classes:
--------
RectCoords(namedtuple("RectCoords", "x y")):
    Coordinates in a rectangular cartesian coordinate system.

HexCoords(namedtuple("HexCoords", "q r s")):
    Coordinates in a three-dimensional cartesian coordinate system, limited by 
    the constraint q + r + s = 0.
    
GraphMatrix(tile_grp:set|list):
    Creates a GraphMatrix Object, containing a directed, weighted graph, from the 
    Objects or coordinates contained in tile_grp, organized in a Dictionary, as 
    well as a Set containing all connected coordinates.
    
    
Functions:
----------
float_to_int(num_in:int|float) -> int|float:
    Returns an Integer if passed an Integer or if passed a Float with its
    decimal being zero. Returns a Float if passed a Float, with a non zero
    decimal.

container_or_object(container_or_object:object|tuple|RectCoords|HexCoords, 
                expected_len:2|3, *, return_obj_type="Tuple") 
                -> tuple|RectCoords|HexCoords|list|dict:
    Returns a Tuple, Namedtuple, List or Dictionary of predefined length, 
    when passed an Objector a Tuple.

linint(a:int|float, b:int|float, t:int|float) -> int|float:
    Linear interpolation returns point at t of distance between a and b.
    
rect_linint(xy_a:object|tuple|RectCoords, xy_b:object|tuple|RectCoords, 
            t:int|float, *, return_obj_type="Tuple") -> tuple|RectCoords|list|dict:
    Linear interpolation returns point at t of distance between a and b on
    a cartesian coordinates system.
    
cube_linint(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords, 
            t:int|float, *, return_obj_type="Tuple") -> tuple|HexCoords|list|dict:
    Returns the hextile coordinates of a point situated at t part of the way 
    from obj_a to obj_b.
    
round_container(container:dict|list|set|tuple|RectCoords, *,
                d:int=0) -> dict|list|set|tuple|RectCoords:
    Rounds each number in a container to the specified decimal, if None is 
    specified to the nearest Integer.
    
round_hex(qrs:tuple|HexCoords, *, return_obj_type="Tuple") -> tuple|HexCoords|list|dict:
    Rounds each of the coordinates to the nearest Integer.
    
get_xy(obj:object, *, return_obj_type="Tuple") -> tuple|RectCoords|list|dict:
    Returns values of attributes x and y of obj as Tuple, RectCoords, List or Dictionary.
    
set_xy(obj:object, x:int|float, y:int|float) -> None:
    Set x and y attribute of obj to specified values.
    
get_qrs(obj:object, *, return_obj_type="Tuple") -> tuple|HexCoords|list|dict:
    Returns values of attributes q, r, s of obj.
    
set_qrs(obj:object, q:int|float, r:int|float, s:int|float) -> None:
    Set q r and s attribute of obj to specified values.
    
hex_to_pixel(qrs:object|tuple|HexCoords, *, tile_width:int=64, tile_height:int=64, 
             return_obj_type="Tuple") -> tuple|RectCoords|list|dict:
    Converts cube coordinates to pixel coordinates.
    
pixel_to_hex(xy:object|tuple|RectCoords, *, tile_width:int=64, tile_height:int=64,
             return_obj_type="Tuple") -> tuple|HexCoords|list|dict:
    Converts pixel coordinates to cube coordinates.
    
neighbors(qrs:object|tuple|HexCoords) -> set:
    Return a List of coordinates of neighboring hexagons.
    
distance(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> int|float:
    Returns distance from one Object to another in a cube coordinate system.
    
in_range(obj:object|tuple|HexCoords, n:int) -> set:
    Returns a Set containing the cube coordinates of every hexagon in 
    distance n from obj.
    
line_draw(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> tuple:
    Draws a line from one hexagon to another, returns a Tuple containing 
    the hexagons with the center closest to the line.
    
dist_lim_flood_fill(start_obj:object|tuple|HexCoords, n:int, obj_grp:list|set, 
                        *, movement_var:str="movement_cost") -> set:
    All cube coordinates within n distance from an Object, factoring in movement_var 
    (variable if -1 blocks object traversability).

GraphMatrix.update_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords, movement_cost:int|float) -> None:
    Add or update a one-directional entry in the adjacency matrix.
    
GraphMatrix.del_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> None:
    Delete a one-directional entry in the adjacency matrix. Does not raise an Error or Warning if no entry matching the input exists.
    
GraphMatrix.connected(self, from_coord:object|tuple|HexCoords) -> set:
    Return all connected coordinates. Returns None, in case of there aren't being any.

GraphMatrix.get_movement_cost(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> int|float:
    Get the movement cost from one Object or coordinate to another.

GraphMatrix.breadth_first_search(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, 
                                 *, test_accessibility:bool=False) -> list:
    Algorithm for searching a tree data structure for a node that satisfies a given property.

GraphMatrix.dijkstras_algorithm(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, 
                                *, test_accessibility:bool=False) -> list:
    Supports weighted movement cost.
    
GraphMatrix.a_star_algorithm(start:object|tuple|HexCoords, goal:object|tuple|HexCoords, 
                             *, test_accessibility:bool=False) -> list:
    Modified version of Dijkstra’s Algorithm that is optimized for a single destination. It prioritizes paths that seem to be leading closer to a goal.
    

@author: Maximilian Hauser
@references: 
redblobgames.com (Amit Patel):
https://www.redblobgames.com/grids/hexagons/
https://www.redblobgames.com/grids/hexagons/implementation.html
https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py
https://www.redblobgames.com/pathfinding/a-star/introduction.html
https://www.redblobgames.com/pathfinding/a-star/implementation.html
NumPy Style Guide:
https://numpydoc.readthedocs.io/en/latest/format.html
"""


# import section ------------------------------------------------------------ #
from collections import namedtuple


# custom datatypes to ensure constraints ------------------------------------ #
# error for a hexagonal_coordinate that violates the zero-sum-constraint ---- #
class ConstraintViolation(ValueError):
    """
    Custom Error to be raised when a logical constraint is violated. 
    HexCoords(1, 1, 2) would be a valid coordinate in a 3-dimensional coordinates
    system, but the constraint q+r+s=0 is enforced, so all coordinates are on a 
    plane horizontal and vertical to the viewer, so they can be used to
    position hexagon-tiles on a screen. The example coordinate would be in 
    violation of this constraint and therefore raise a ConstraintViolation.
    """
    pass


# real_numbers for python built in types that means either Integer of Float - #
"""
Real number is a number that can be used to measure a continuous one-dimensional 
quantity. Out of Pythons built-in Numeric Types, Integers and Floating Point
Numbers satisfy this condition.
"""


# RectCoords object to ensure constraints without dependency on typing ------ #
class RectCoords(namedtuple("RectCoords", "x y")):
    """
    Coordinates in a rectangular cartesian coordinate system. Superclass 
    namedtuple is a fixed length structure with indices and named attributes.
    """
    def __new__(cls, x, y):
        
        if not isinstance(x, int|float):
            raise TypeError("Coordinate x needs to be of type Integer or Float.")
                            
        if not isinstance(y, int|float):
            raise TypeError("Coordinate y needs to be of type Integer or Float.")
                            
        return super().__new__(cls, x, y)


# HexCoords object to ensure constraints without dependency on typing ------- #
class HexCoords(namedtuple("HexCoords", "q r s")):
    """
    Coordinates in a three-dimensional cartesian coordinate system, limited by the 
    constraint q + r + s = 0, to ensure a canonical coordinate on the plane drawn
    by the constraint. Superclass Namedtuple is a fixed length structure with 
    indices and named attributes.
    """
    def __new__(cls, q, r, s):
        if not isinstance(q, int|float):
            raise TypeError("Coordinate q needs to be of type Integer or Float.")
            
        if not isinstance(r, int|float):
            raise TypeError("Coordinate r needs to be of type Integer or Float.")
            
        if not isinstance(s, int|float):
            raise TypeError("Coordinate s needs to be of type Integer or Float.")
            
        if (q + r + s) != 0:
            raise ConstraintViolation("""Constraint q + r + s = 0, ensures that 
                                      there is one canonical coordinate for the 
                                      relative position of a hexagontile on the 
                                      plane being drawn by the constraint""")
        return super().__new__(cls, q, r, s)
    
    
# GraphMatrix for storing weighted, directed graphs ------------------------- #
class GraphMatrix:
    """
    Creates a GraphMatrix object, containing a directed, weighted graph, from the 
    Objects or coordinates contained in tile_grp, organized in a Dictionary. 
    Enables the use of graph traversal algorithms in relation to the hexagonally 
    related Objects.
        
    Parameters:
    -----------
    tile_grp : List | Set | SpriteGroup
        A container containing Objects adjacent to each other in a cube 
        coordinate system (tiles in tilemap). The hexagonal coordinates need to 
        be stored in q, r and s coordinates and they must adhere to the zero 
        constraint.
        
    Attributes:
    -----------
    matrix_dict : Dictionary
        Dictionary containing a directed, weighted graph, stored in the following 
        structure, the keys being qrs-coordinates. 
        {from : { first_to : movement_cost, second_to : movement_cost}}
    
    matrix_coords : Set
        Set containing all coordinates, connected to another coordinate.
    
    Methods:
    --------
    update_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords, movement_cost:int|float) -> None
        Add or update a one-directional entry in the adjacency matrix.
        
    del_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> None
        Delete a one-directional entry in the adjacency matrix. Does not raise an Error or Warning if no entry matching the input exists.
        
    connected(self, from_coord:object|tuple|HexCoords) -> set
        Return all connected coordinates. Returns None, in case there aren't any.
        
    get_movement_cost(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> int|float
        Get the movement cost from one Object or coordinate to another.
        
    breadth_first_search(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords) -> list
        Algorithm for searching a tree data structure for a node that satisfies a given property.
        
    dijkstras_algorithm(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords) -> list
        Algorithm for searching a tree data structure for a node that satisfies a given property. Supports weighted movement cost.
        
    a_star_algorithm(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords) -> list
        Modified version of Dijkstra’s Algorithm that is optimized for a single destination. It prioritizes paths that seem to be leading closer to a goal.
        
        
    Raises:
    -------
    TypeError: 
        If q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the q, r or s coordinates attributes.
        
    ConstraintViolation: 
        If the q+r+s=0 constraint is violated.
        
    Returns:
    --------
    GraphMatrix(object): 
        Two-dimensional, directed, weighted graph, stored in a Dictionary.
    """
    def __init__(self, tile_grp:list|set):
        # contains all directional movement costs --------------------------- #
        self.matrix_dict = dict()
        # contains all coordinates connected to another coordinate ---------- #
        self.matrix_coords = set()
        
        # creating a set with all connections ------------------------------- #
        edges = set()
        
        for tile in tile_grp:
            tile_qrs = container_or_object(tile, 3, return_obj_type="Tuple")
            t_nbors_tuple = neighbors((tile_qrs[0], tile_qrs[1], tile_qrs[2]))
            for nbor in t_nbors_tuple:
                nbor_qrs = (nbor[0], nbor[1], nbor[2])
                for t in tile_grp:
                    t_coords = container_or_object(t, 3, return_obj_type="Tuple")
                    if t_coords[0] == nbor[0] and t_coords[1] == nbor[1] and t_coords[2] == nbor[2]:
                        edges.add((tile_qrs, nbor_qrs, tile.movement_cost, t.movement_cost))
                        
        for edge in edges:
            # movement_cost defined by the tile moved onto ------------------ #
            # movement_cost if possible from edge[0] to edge[1] ------------- #
            if edge[0] in self.matrix_dict.keys():
                self.matrix_dict[edge[0]].update({edge[1]:edge[3]})
            else:
                self.matrix_dict.update({edge[0]:{edge[1]:edge[3]}})
            # movement_cost if possible from edge[1] to edge[0] ------------- #
            if edge[1] in self.matrix_dict.keys():
                self.matrix_dict[edge[1]].update({edge[0]:edge[2]})
            else:
                self.matrix_dict.update({edge[1]:{edge[0]:edge[2]}})
            # add edge coordinats to set connected coordinates -------------- #
            if edge[2] >= 0:
                self.matrix_coords.add(edge[0])
            if edge[3] >= 0:
                self.matrix_coords.add(edge[1])
                                      
        
    def update_entry(self, from_coord:object|tuple|HexCoords, 
                     to_coord:object|tuple|HexCoords, movement_cost:int|float) -> None:
        """
        Add or update a one-directional entry in the adjacency matrix.
        """
        from_c = container_or_object(from_coord, 3)
        to_c = container_or_object(to_coord, 3)
        if self.matrix_dict[from_c]:
            self.matrix_dict[from_c].update({to_c:movement_cost})
        else:
            self.matrix_dict.update({from_c:{to_c:movement_cost}})
        
        
    def del_entry(self, from_coord:object|tuple|HexCoords, 
                  to_coord:object|tuple|HexCoords) -> None:
        """
        Delete a one-directional entry in the adjacency matrix. Does not raise 
        an Error or Warning if no entry matching the input exists.
        """
        from_c = container_or_object(from_coord, 3)
        to_c = container_or_object(to_coord, 3)
        if self.matrix_dict[from_c][to_c]:
            del self.matrix_dict[from_c][to_c]
        if not self.matrix_dict[from_c]:
            del self.matrix_dict[from_c]
            
            
    def connected(self, from_coord:object|tuple|HexCoords) -> set:
        """
        Return all connected coordinates. Returns None, in case of there aren't 
        being any.
        """
        from_c = container_or_object(from_coord, 3)
        try:
            connected = set(self.matrix_dict[from_c].keys())
        except KeyError:
            connected = None
            
        return connected
        
    
    def get_movement_cost(self, from_coord:object|tuple|HexCoords, 
                          to_coord:object|tuple|HexCoords) -> int|float:
        """
        Get the movement cost from one Object or coordinate to another.
        """
        from_c = container_or_object(from_coord, 3)
        to_c = container_or_object(to_coord, 3)
        try:
            movement_cost = self.matrix_dict[from_c][to_c]
        except KeyError:
            movement_cost = -1
        
        return movement_cost
    
    
    # graph based path finding algorithms ----------------------------------- #
    def breadth_first_search(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords, *, test_accessibility:bool=False) -> list:
        """
        Algorithm for searching a tree data structure for a node that satisfies a 
        given property. It starts at the tree root and explores all nodes at the 
        present depth prior to moving on to the nodes at the next depth level. 
        
        Parameters:
        -----------
        start : Object | Tuple | HexCoords
            A Tuple consisting of an Integer or Float for the q, r and s value,
            or an Object having a q, r and s attribute, the assigned values being 
            an Integer or Float. Needs to adhere to zero constraint.
            
        goal : Object | Tuple | HexCoords
            A Tuple consisting of an Integer or Float for the q, r and s value,
            or an Object having a q, r and s attribute, the assigned values being 
            an Integer or Float. Needs to adhere to zero constraint.
            
        test_accessibility : Boolean, optional
            If True, tests if start and goal are connected to other tiles,
            this is to minimize the likelihood of running a pathfinding algorithm,
            that either returns an invalid path or no path.
        
        Raises:
        -------
        TypeError: 
            If q, r or s is not an Integer or a Float. If a passed Tuple has
            too many or too few individual values.
            
        AttributeError: 
            If an Object is passed, but is missing the q, r or s coordinates attributes.
            
        ConstraintViolation: 
            If the q+r+s=0 constraint is violated.
        
        Returns:
        --------
        path(List): A List containing all tiles from start to goal coordinate.
        """
        start = container_or_object(start, 3, return_obj_type="Tuple")
        goal = container_or_object(goal, 3, return_obj_type="Tuple")
        
        # test accessibility ------------------------------------------------ #
        if test_accessibility:
            if start not in self.matrix_coords or goal not in self.matrix_coords:
                return None
        
        frontier = list()
        frontier.append(start)
        came_from = dict() # path A->B is stored as came_from[B] == A
        came_from[start] = None

        while frontier:
            current = frontier.pop(0)
            
            if current == goal:
                break
            else:
                for nbor in neighbors(current):
                    if nbor not in came_from.keys():
                        # movement_cost from row to column not 0 ------------ #
                        if nbor in self.connected(current):
                            if self.get_movement_cost(current, nbor) >= 0:
                                frontier.append(nbor)
                                came_from[nbor] = current
                                
        # if goal not reached and no more frontier tiles left return None --- #
        else:
            return None
        
        # follow the path from goal to start in came_from ------------------- #
        current = goal 
        path = list()
        while current != start: 
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        
        return path


    def dijkstras_algorithm(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords, *, test_accessibility:bool=False) -> list:
        """
        Algorithm for searching a tree data structure for a node that satisfies a 
        given property. It starts at the tree root and explores all nodes at the 
        present depth prior to moving on to the nodes at the next depth level. 
        Supports weighted movement cost.
        
        Parameters:
        -----------
        start : Object | Tuple | HexCoords
            A Tuple consisting of an Integer or Float for the q, r and s value,
            or an Object having a q, r and s attribute, the assigned values being 
            an Integer or Float. Needs to adhere to zero constraint.
            
        goal : Object | Tuple | HexCoords
            A Tuple consisting of an Integer or Float for the q, r and s value,
            or an Object having a q, r and s attribute, the assigned values being 
            an Integer or Float. Needs to adhere to zero constraint.
            
        test_accessibility : Boolean, optional
            If True, tests if start and goal are connected to other tiles,
            this is to minimize the likelihood of running a pathfinding algorithm,
            that either returns an invalid path or no path.
        
        Raises:
        -------
        TypeError: 
            If q, r or s is not an Integer or a Float. If a passed Tuple has
            too many or too few individual values.
            
        AttributeError: 
            If an Object is passed, but is missing the q, r or s coordinates attributes.
            
        ConstraintViolation: 
            If the q+r+s=0 constraint is violated.
        
        Returns:
        --------
        path(List): A List containing all tiles from start to goal coordinate.
        """
        start = container_or_object(start, 3, return_obj_type="Tuple")
        goal = container_or_object(goal, 3, return_obj_type="Tuple")
        
        # test accessibility ------------------------------------------------ #
        if test_accessibility:
            if start not in self.matrix_coords or goal not in self.matrix_coords:
                return None
        
        frontier = list()
        frontier.append((start, 0))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        
        # while not all tiles have been procesed, pop first tile from list -- #
        while frontier:
            current = frontier.pop(0)
            
            # if current qrs_coords equal goal coords, break out of loop ---- #
            if current[0] == goal:
                break
            # else execute loop --------------------------------------------- #
            else:
                for nbor in neighbors(current[0]):
                    if self.get_movement_cost(current[0], nbor) >= 0:
                        new_cost = cost_so_far[current[0]] + self.get_movement_cost(current[0], nbor)
                        if nbor not in cost_so_far or new_cost < cost_so_far[nbor]:
                            cost_so_far[nbor] = new_cost
                            came_from[nbor] = current[0]
                            frontier.append((nbor, new_cost))
                            frontier.sort(key= lambda x:x[1] in frontier)
                            
        # if goal not reached and no more frontier tiles left return None --- #
        else:
            return None
                        
        # follow the path from goal to start in came_from ------------------- #
        current = goal 
        path = list()
        while current != start: 
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        
        return path
                   

    def a_star_algorithm(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords, *, test_accessibility:bool=False) -> list:
        """
        Modified version of Dijkstra’s Algorithm that is optimized for a single 
        destination. It prioritizes paths that seem to be leading closer to a goal.
        
        Parameters:
        -----------
        start : Object | Tuple | HexCoords
            A Tuple consisting of an Integer or Float for the q, r and s value,
            or an Object having a q, r and s attribute, the assigned values being 
            an Integer or Float. Needs to adhere to zero constraint.
            
        goal : Object | Tuple | HexCoords
            A Tuple consisting of an Integer or Float for the q, r and s value,
            or an Object having a q, r and s attribute, the assigned values being 
            an Integer or Float. Needs to adhere to zero constraint.
            
        test_accessibility : Boolean, optional
            If True, tests if start and goal are connected to other tiles,
            this is to minimize the likelihood of running a pathfinding algorithm,
            that either returns an invalid path or no path.
            
        Raises:
        -------
        TypeError: 
            If q, r or s is not an Integer or a Float. If a passed Tuple has
            too many or too few individual values.
            
        AttributeError: 
            If an Object is passed, but is missing the q, r or s coordinates attributes.
            
        ConstraintViolation: 
            If the q+r+s=0 constraint is violated.
        
        Returns:
        --------
        path(List): A List containing all tiles from start to goal coordinate.
        """
        start = container_or_object(start, 3, return_obj_type="Tuple")
        goal = container_or_object(goal, 3, return_obj_type="Tuple")
        
        # test accessibility ------------------------------------------------ #
        if test_accessibility:
            if start not in self.matrix_coords or goal not in self.matrix_coords:
                return None
        
        frontier = list()
        frontier.append((start, 0))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        
        # while not all tiles have been procesed, pop first tile from list -- #
        while frontier:
            current = frontier.pop(0)
            
            # if current qrs_coords equal goal coords, break out of loop ---- #
            if current[0] == goal:
                break
            # else execute loop --------------------------------------------- #
            else:
                for nbor in neighbors(current[0]):
                    if self.get_movement_cost(current[0], nbor) >= 0:
                        new_cost = cost_so_far[current[0]] + self.get_movement_cost(current[0], nbor)
                        if nbor not in cost_so_far or new_cost < cost_so_far[nbor]:
                            cost_so_far[nbor] = new_cost
                            came_from[nbor] = current[0]
                            priority = new_cost + distance(goal, nbor)
                            frontier.append((nbor, priority))
                            frontier.sort(key= lambda x:x[1] in frontier)
        
        # if goal not reached and no more frontier tiles left return None --- #
        else:
            return None
                        
        # follow the path from goal to start in came_from ------------------- #
        current = goal 
        path = list()
        while current != start: 
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        
        return path
               

# helper functions ---------------------------------------------------------- #
def float_to_int(num_in:int|float) -> int|float:
    """
    Returns an Integer if passed an Integer or if passed a Float with its
    decimal being zero. Returns a Float if passed a Float, with a non zero
    decimal.
    
    Parameters:
    -----------
    num_in : Integer | Float
        An Integer or a Float to be cast as Integer if decimal is zero.
    
    Raises:
    -------
    TypeError: If num_in is not of type Integer or a Float.
    
    Returns:
    --------
    num_in(Integer|Float): num_in as Float if non zero decimal, else as Integer.
    """
    if isinstance(num_in, int):
        return num_in
    elif isinstance(num_in, float):
        if num_in.is_integer():
            return int(num_in)
        else:
            return num_in
    else:
        raise TypeError("num_in needs to be of type Integer or Float.") 


def container_or_object(container_or_object:object|tuple|RectCoords|HexCoords|list|dict, 
                    expected_len:2|3, *, return_obj_type:str="Tuple") -> tuple|RectCoords|HexCoords|list|dict:
    """
    Returns a Tuple or a Namedtuple of predefined length, when passed an Object
    or a Tuple. Tests whether the Tuple is of the desired length and/or if the 
    Object contains the predefined coordinate variables x, y for 2-dimensional
    and q, r and s for 3-dimensional coordinate systems. Helper function to 
    catch divergence from desired coordinate shape as early as possible in
    hexlogic functions.
    
    Parameters:
    -----------
    container_or_object : Object | Tuple | RectCoords | HexCoords
        Object having either x and y, or q, r and s attributes, with Integers 
        or Floats as values. Or a Tuple or Namedtuple with length equivalent to 
        the selected dimension. q, r and s need to fullfill the zero constraint 
        for Hexagonal Coordinates.
    
    expected_len : 2 | 3
        Integer for the number of axis of the cartesian coordinate system,
        in case of 3, q + r + s = 0, constraint is enforced.
        
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as RectCoords(Namedtuple) or 
        HexCoords(Namedtuple), if 'Tuple' as a Tuple of shape (x, y) or (q, r, s), 
        if 'List' as a List of length 2 or 3 and if 'Dict' returns a Dictionary, 
        with the axis as keys.
    
    Raises:
    -------
    TypeError: 
        If x, y, q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    ValueError:
        If a different value than 2 or 3 is passed as expected_len.
        
    AttributeError: 
        If an Object is passed, but is missing the coordinates attributes 
        for the selected dimension.
        
    ConstraintViolation: 
        If the selected coordinate system is 3-dimensional and the 
        q+r+s=0 constraint is violated.
    
    Returns:
    --------
    coordinates(Tuple|RectCoords|HexCoords) : 
        Coordinates for the selected dimension in a Tuple or childclass.
    """
    # rectangular coordinates ----------------------------------------------- #
    if expected_len == 2:
        if isinstance(container_or_object, tuple):
            if len(container_or_object) == 2:
                x, y = container_or_object
            else:
                raise TypeError("container_or_object needs to be either an Object having attributes x and y or a Tuple of length 2")
        elif isinstance(container_or_object, (int, float, complex, str, list, range, bytes, 
                               bytearray, memoryview, bool, dict, set, frozenset)):
            raise TypeError("container_or_object needs to be either an Object having attributes x and y or a Tuple of length 2")
        else:
            x = getattr(container_or_object, "x")
            y = getattr(container_or_object, "y")
            
        if return_obj_type.lower() == "tuple":
            rect_coords = (x, y)
        elif return_obj_type.lower() == "coords":
            rect_coords = RectCoords(x, y)
        elif return_obj_type.lower() == "list":
            rect_coords = [x, y]
        elif return_obj_type.lower() == "dict":
            rect_coords = {"x":x, "y":y}
            
        return rect_coords

    # cube coordinates ------------------------------------------------------ #
    elif expected_len == 3:
        if isinstance(container_or_object, tuple):
            if len(container_or_object) == 3:
                q, r, s = container_or_object
                test_type_and_constraints = HexCoords(q, r, s)
                del test_type_and_constraints
            else:
                raise TypeError("container_or_object needs to be either an Object having attributes q, r and s or a Tuple of length 3")
        elif isinstance(container_or_object, (int, float, complex, str, list, range, bytes, 
                               bytearray, memoryview, bool, dict, set, frozenset)):
            raise TypeError("container_or_object needs to be either an Object having attributes q, r and s or a Tuple of length 3")
        else:
            q = getattr(container_or_object, "q")
            r = getattr(container_or_object, "r")
            s = getattr(container_or_object, "s")
            test_type_and_constraints = HexCoords(q, r, s)
            del test_type_and_constraints

        if return_obj_type.lower() == "tuple":
            hex_coords = (q, r, s)
        elif return_obj_type.lower() == "coords":
            hex_coords = HexCoords(q, r, s)
        elif return_obj_type.lower() == "list":
            hex_coords = [q, r, s]
        elif return_obj_type.lower() == "dict":
            hex_coords = {"q":q, "r":r, "s":s}

        return hex_coords
    
    # other integer than 2 or 3 not supported ------------------------------- #
    else:
        raise ValueError("Only 2 or 3 axis coordinate systems supported.")


# Hexlogic functions -------------------------------------------------------- #
def linint(a:int|float, b:int|float, t:int|float) -> int|float:
    """
    Linear interpolation returns point at t of distance between point a and 
    point b on a line.
    
    Parameters:
    -----------
    a : Integer | Float
        A real numeric value, representing a point on a line.
        
    b : Integer | Float
        A real numeric value, representing a point on a line.
        
    t : Integer | Float
        Real number denominating the fractional distance between a and b.
        t * 100 = distance between a and b in percent.
        
    Raises:
    -------
    TypeError: If a, b or t is not an Integer or Float.
        
    Returns:
    --------
    linint(real_number): Linear interpolation t part of the way from a to b.
    """
    if not isinstance(a, int|float):
        raise TypeError("a needs to be either of type Integer or type Float.")
    if not isinstance(b, int|float):
        raise TypeError("b needs to be either of type Integer or type Float.")
    if not isinstance(t, int|float):
        raise TypeError("t needs to be either of type Integer or type Float.")
    
    linint = a + (b - a) * t * 1.0
            
    return int(linint) if linint.is_integer() else linint
    
    
def rect_linint(xy_a:object|tuple|RectCoords, xy_b:object|tuple|RectCoords, 
                t:int|float, *, return_obj_type:str="Tuple") -> tuple|RectCoords|list|dict:
    """
    Linear interpolation returns point at t distance between a and b in
    a rectangular cartesian coordinates system. x and y representing the 
    respective coordinate along the x and y axis of a rectangular coordinate 
    system.
        
    Parameters:
    -----------
    xy_a : Tuple | RectCoords | Object
        A Tuple or childclass consisting of an Integer or Float for the x and y 
        value, or an Object having a x and y attribute, the assigned values 
        being an Integer or Float. 
        
    xy_b : Tuple | RectCoords | Object
        A Tuple or childclass consisting of an Integer or Float for the x and y 
        value, or an Object having a x and y attribute, the assigned values 
        being an Integer or Float. 
        
    t : Integer | Float
        Real number denominating the fractional distance between a and b.
        t * 100 = distance between a and b in percent.
        
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as RectCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (x, y), if 'List' as a List of length 2 and 
        if 'Dict' returns a Dictionary, with the axis as keys.
        
    Raises:
    -------
    TypeError: 
        If xy_a or xy_b is not a Tuple or subclass with 2 values, being Integer 
        or Float respectively.
    
    AttributeError: 
        If xy_a and/or xy_b is an Object xy_a or xy_b is missing a x or y attribute.
        
    Returns:
    --------
    rect_linint(Tuple|RectCoords|List|Dictionary): 
        Linear interpolation t part of the way from a to b.
    """
    (x_a, y_a) = container_or_object(xy_a, 2)
    (x_b, y_b) = container_or_object(xy_b, 2)
        
    x = linint(x_a, x_b, t)
    y = linint(y_a, y_b, t)
    
    if return_obj_type.lower() == "tuple":
        rect_linint = (x, y)
    elif return_obj_type.lower() == "coords":
        rect_linint = RectCoords(x, y)
    elif return_obj_type.lower() == "list":
        rect_linint = [x, y]
    elif return_obj_type.lower() == "dict":
        rect_linint = {"x":x, "y":y}
        
    return rect_linint
    

def cube_linint(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords, 
                t:int|float, *, return_obj_type:str="Tuple") -> tuple|HexCoords|list|dict:
    """
    Returns the hextile coordinates of a point situated at t part of the way 
    from obj_a to obj_b.
        
    Parameters:
    -----------
    obj_a : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    obj_b : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    t : Integer | Float
        Real number denominating the fractional distance between a and b.
        t * 100 = distance between a and b in percent.
        
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as HexCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (q, r, s), if 'List' as a List of length 3 and 
        if 'Dict' returns a Dictionary, with the axis as keys.
        
    Raises:
    -------
    TypeError: 
        If obj_a or obj_b is not a Tuple or subclass with 3 values, being Integer 
        or Float respectively.
        
    AttributeError: 
        If at least one of the parameters is an Object and one of the Objects 
        is missing an q, r or s attribute.
        
    ConstraintViolation: 
        If the q+r+s=0 constraint is violated, by one of the function parameters.
        
    Returns:
    --------
    linint_coords(Tuple|RectCoords|List|Dictionary): 
        The hextile coordinates of a point situated at the t part of the way 
        from obj_a to obj_b.
    """
    
    (q_a, r_a, s_a) = container_or_object(obj_a, 3)
    (q_b, r_b, s_b) = container_or_object(obj_b, 3)
    
    if not isinstance(t, int|float):
        raise TypeError("t needs to be of type Integer or Float.")
        
    q = linint(q_a, q_b, t)
    r = linint(r_a, r_b, t)
    s = linint(s_a, s_b, t)
    
    if return_obj_type.lower() == "tuple":
        linint_coords = (q, r, s)
    elif return_obj_type.lower() == "coords":
        linint_coords = HexCoords(q, r, s)
    elif return_obj_type.lower() == "list":
        linint_coords = [q, r, s]
    elif return_obj_type.lower() == "dict":
        linint_coords = {"q":q, "r":r, "s":s}
        
    return linint_coords


def round_container(container:dict|list|set|tuple|RectCoords, *,
                d:int=0) -> dict|list|set|tuple|RectCoords:
    """
    Rounds each number in a container to the specified decimal, if None is 
    specified to the nearest Integer. For Dictionaries rounds each value or
    each value in a container, assigned as a value. Does not work for nested 
    Dictionaries.
    
    Parameters:
    -----------
    container : Dictionary | List | Set | Tuple | RectCoords
        Built-in container or derived childclass.
        
    d : Integer, optional
        Number of decimals to round to, passed to built-in round function.
    
    Raises:
    -------
    TypeError: 
        If a different Object type is passed than a built in container or 
        derived childclass thereof.
    
    Returns:
    --------
    container(dict|list|set|tuple|RectCoords): 
        Returns a container with each Float in it rounded to d decimal points.
    """
    # case: container is list|set|tuple rounds every int|float in it -------- #
    if isinstance(container, list|set|tuple):
        rndd_lst = [round(x,d) if isinstance(x, float) else x for x in container]
        if isinstance(container, list):
            return rndd_lst
        elif isinstance(container, set):
            return set(rndd_lst)
        elif isinstance(container, tuple):
            return tuple(rndd_lst)
    # case: container is dict rounds every int|float in it, or nested in ---- #
    # list|set|tuple -------------------------------------------------------- #
    elif isinstance(container, dict):
        for key in container.keys():
            if isinstance(container[key], float):
                container[key] = round(container[key],d)
            elif isinstance(container[key], list|set|tuple):
                rndd_lst = [round(x,d) if isinstance(x, float) else x for x in container[key]]
                if isinstance(container[key], list):
                    container[key] = rndd_lst
                elif isinstance(container[key], set):
                    container[key] = set(rndd_lst)
                elif isinstance(container[key], tuple):
                    container[key] = tuple(rndd_lst)
        return container
    else:
        raise TypeError("""container needs to be a general purpose built in 
                        container, Dict, List, Set or Tuple or a childclass""")
        

def round_hex(qrs:tuple|HexCoords, *, return_obj_type:str="Tuple") -> tuple|HexCoords|list|dict:
    """
    Rounds each of the coordinates to the nearest Integer. 
        
    Parameters:
    -----------
    qrs : Tuple | HexCoords
        A Tuple or a Namedtuple containing 3 real numerical values.
        
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as HexCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (q, r, s), if 'List' as a List of length 3 and 
        if 'Dict' returns a Dictionary, with the axis as keys.
        
    Raises:
    -------
    TypeError:
        If the Tuple contains different values than Integers or Float.
        
    ConstraintViolation: 
        If the q+r+s=0 constraint is violated and the return is HexCoords.
        
    Returns:
    --------
    rounded_qrs(Tuple|RectCoords|List|Dictionary): 
        The input Tuple, each element rounded to the nearest Integer. 
    """
    q_f, r_f, s_f = qrs
        
    q = round(q_f)
    r = round(r_f)
    s = round(s_f)

    q_diff = abs(q - q_f)
    r_diff = abs(r - r_f)
    s_diff = abs(s - s_f)

    if q_diff > r_diff and q_diff > s_diff:
        q = -r-s
    elif r_diff > s_diff:
        r = -q-s
    else:
        s = -q-r
        
    if return_obj_type.lower() == "tuple":
        rounded_qrs = (q, r, s)
    elif return_obj_type.lower() == "coords":
        rounded_qrs = HexCoords(q, r, s)
    elif return_obj_type.lower() == "list":
        rounded_qrs = [q, r, s]
    elif return_obj_type.lower() == "dict":
        rounded_qrs = {"q":q, "r":r, "s":s}
        
    return rounded_qrs


def get_xy(obj:object, *, return_obj_type:str="Tuple") -> tuple|RectCoords|list|dict:
    """
    Returns values of attributes x and y of obj as Tuple, RectCoords, List or Dictionary.
    
    Parameters:
    -----------
    obj : Object
        An Object having attributes x and y, values being Integer or Float.
        
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as RectCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (x, y), if 'List' as a List of length 2 and 
        if 'Dict' returns a Dictionary, with the axis as keys.
        
    Raises:
    -------
    TypeError:
        If values returned from Object attributes are not Integer or Float.
        
    AttributeError: 
        If obj is missing x or y as attribute.
        
    Returns:
    --------
    xy(Tuple|RectCoords|List|Dictionary): The values of attributes x, y of obj.
    """
    x = getattr(obj, "x")
    y = getattr(obj, "y")
    
    if not isinstance(x, int|float):
        raise TypeError("obj returned a different type than Integer or Float as value for x")
                            
    if not isinstance(y, int|float):
        raise TypeError("obj returned a different type than Integer or Float as value for y")
            
    if return_obj_type.lower() == "tuple":
        xy = (x, y)
    elif return_obj_type.lower() == "coords":
        xy = RectCoords(x, y)
    elif return_obj_type.lower() == "list":
        xy = [x, y]
    elif return_obj_type.lower() == "dict":
        xy = {"x":x,"y":y}
        
    return xy


def set_xy(obj:object, x:int|float, y:int|float) -> None:
    """
    Set x and y attribute of obj to specified values.
    
    Parameters:
    -----------
    obj : Object
        An Object having attributes x and y, values being Integer or Float.
        
    x : Integer | Float
        The value the x-coordinate is to be set to.
        
    y : Integer | Float
        The value the y-coordinate is to be set to.
        
    Raises:
    -------
    TypeError: 
        If x or y is not an Integer or Float.
        
    Returns:
    --------
    None
    """
    
    if not isinstance(x, int|float):
        raise TypeError("x needs to be of type Integer or Float")
    if not isinstance(y, int|float):
        raise TypeError("y needs to be of type Integer or Float")

    setattr(obj, "x", x)
    setattr(obj, "y", y)
        
    
def get_qrs(obj:object, *, return_obj_type:str="Tuple") -> tuple|HexCoords|list|dict:
    """
    Returns values of attributes q, r and s of obj as Tuple.
        
    Parameters:
    -----------
    obj : object
        An Object having attributes q, r, s, values being Integer or Float. If 
        set to return HexCoords, needs to adhere to zero constraint.
        
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as HexCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (q, r, s), if 'List' as a List of length 3 and 
        if 'Dict' returns a Dictionary, with the axis as keys.
        
    Raises:
    -------
    AttributeError: 
        If obj is missing q, r or s as attribute.
    
    ConstraintViolation: 
        If set to return HexCoords and the q+r+s=0 constraint is violated.
        
    Returns:
    --------
    qrs(Tuple|HexCoords|List|Dictionary): 
        The values of attributes q, r, s of obj as Tuple or NamedTuple.
    """

    q = getattr(obj, "q")
    r = getattr(obj, "r")
    s = getattr(obj, "s")
            
    if return_obj_type.lower() == "tuple":
        qrs = (q, r, s)
    elif return_obj_type.lower() == "coords":
        qrs = HexCoords(q, r, s)
    elif return_obj_type.lower() == "list":
        qrs = [q, r, s]
    elif return_obj_type.lower() == "dict":
        qrs = {"q":q, "r":r, "s":s}
        
    return qrs
    

def set_qrs(obj:object, q:int|float, r:int|float, s:int|float) -> None:
    """
    Set q, r and s attribute of obj to specified values. Input needs to adhere 
    to zero constraint.
        
    Parameters:
    -----------
    obj : Object
        An Object intended to be located on a hexagonal grid.
        
    q : Integer | Float
        The value the q-coordinate is to be set to, needs to adhere to zero-
        constraint.
        
    r : Integer | Float
        The value the r-coordinate is to be set to, needs to adhere to zero-
        constraint.
        
    s : Integer | Float
        The value the s-coordinate is to be set to, needs to adhere to zero-
        constraint.
        
    Raises:
    -------
    TypeError: 
        If q, r or s is not an Integer or Float.
    
    ConstraintViolation: 
        If the q+r+s=0 constraint is violated.
        
    Returns:
    --------
    None
    """ 
    test_type_and_constraints = HexCoords(q, r, s)
    del test_type_and_constraints
    
    setattr(obj, "q", q)
    setattr(obj, "r", r)
    setattr(obj, "s", s)
    

def hex_to_pixel(qrs:object|tuple|HexCoords, *, tile_width:int=64, tile_height:int=64, 
                 return_obj_type:str="Tuple") -> tuple|RectCoords|list|dict:
    """
    Converts cube coordinates to pixel coordinates. 
    
    Parameters:
    -----------
    qrs : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    tile_width : Integer, optional
        Specifies the width of a hexagon tile in pixel.
    
    tile_height : Integer, optional
        Specifies the height of a hexagon tile in pixel.
    
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as HexCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (q, r, s), if 'List' as a List of length 3 and 
        if 'Dict' returns a Dictionary, with the axis as keys.
            
    Raises:
    -------
    TypeError: 
        If x, y, q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the coordinates attributes 
        for the selected dimension.
        
    ConstraintViolation: 
        If the selected coordinate system is 3-dimensional, but the 
        q + r + s = 0 constraint is violated.
        
    Returns:
    --------
    xy(Tuple|RectCoords|List|Dictionary): 
        The input coordinates of hexagon qrs converted to a 2-axis coordinates 
        system xy.
    """
    (q, r, s) = container_or_object(qrs, 3)
    
    test_type_and_constraints = HexCoords(q, r, s)
    del test_type_and_constraints
        
    x = round(((4/3)*q - (2/3)*r - (2/3)*s) * tile_width * 0.375)
    y = round((r - s) * tile_height * 0.5)
        
    if return_obj_type.lower() == "tuple":
        xy = (x, y)
    elif return_obj_type.lower() == "coords":
        xy = RectCoords(x, y)
    elif return_obj_type.lower() == "list":
        xy = [x, y]
    elif return_obj_type.lower() == "dict":
        xy = {"x":x,"y":y}
        
    return xy
    

def pixel_to_hex(xy:object|tuple|RectCoords, *, tile_width:int=64, tile_height:int=64,
                 return_obj_type:str="Tuple") -> tuple|HexCoords|list|dict:
    """
    Converts pixel coordinates to cube coordinates.
        
    Parameters:
    -----------
    xy : Object | Tuple | RectCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being 
        an Integer or Float. Needs to adhere to zero constraint.
        
    tile_width : Integer, optional
        Specifies the width of a hexagon tile in pixel.
    
    tile_height : Integer, optional
        Specifies the height of a hexagon tile in pixel.
    
    return_obj_type : String, optional
        If 'Coords', returns the rect_linint as HexCoords(Namedtuple), if 
        'Tuple' as a Tuple of shape (q, r, s), if 'List' as a List of length 3 
        and if 'Dict' returns a Dictionary, with the axis as keys.
        
    Raises:
    -------
    TypeError: 
        If x or y is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the x or y coordinate attribute.
        
    Returns:
    --------
    qrs(Tuple|RectCoords|List|Dictionary): 
        The input cartesian coordinates Tuple of xy converted to a 
        cube coordinates system qrs.
    """

    x, y = container_or_object(xy, 2)
        
    q = round((x / 2) / tile_width * (8 / 3))
    r = round((y / 2 - x / 4) / tile_height * 2)
    s = round(-q-r)
        
    if return_obj_type.lower() == "tuple":
        qrs = (q, r, s)
    elif return_obj_type.lower() == "coords":
        qrs = HexCoords(q, r, s)
    elif return_obj_type.lower() == "list":
        qrs = [q, r, s]
    elif return_obj_type.lower() == "dict":
        qrs = {"q":q, "r":r, "s":s}
        
    return qrs
    

def neighbors(qrs:object|tuple|HexCoords) -> set:
    """
    Returns a Tuple of coordinates of neighboring hexagons.
        
    Parameters:
    -----------
    qrs : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    Raises:
    -------
    TypeError: 
        If q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the q, r or s coordinate attributes.
        
    ConstraintViolation: 
        If the q + r + s = 0 constraint is violated.
        
    Returns:
    --------
    nbors(Set): 
        A Set containing all cube coordinates neighboring the input Object
        or Tuple.
    """
    q, r, s = container_or_object(qrs, 3)
    
    nbors = ((q+1,r,s-1), (q+1,r-1,s), (q,r-1,s+1), (q-1,r,s+1), (q-1,r+1,s), (q,r+1,s-1))
        
    return nbors
    

def distance(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> int|float:
    """
    Returns distance from one Object to another in a cube coordinate system.
        
    Parameters:
    -----------
    obj_a : Object | Tuple | Object
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    obj_b : Object | Tuple | Object
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    Raises:
    -------
    TypeError: 
        If q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the q, r or s coordinate attributes.
        
    ConstraintViolation: 
        If the q + r + s = 0 constraint is violated.
        
    Returns:
    --------
    ab_dist(Integer|Float): The distance between obj_a and obj_b in hexagon tiles.
    """
    (a_q, a_r, a_s) = container_or_object(obj_a, 3)
    (b_q, b_r, b_s) = container_or_object(obj_b, 3)
        
    q_diff = abs(a_q - b_q)
    r_diff = abs(a_r - b_r)
    s_diff = abs(a_s - b_s)
    ab_dist = float_to_int(max(q_diff, r_diff, s_diff))
        
    return ab_dist
    

def in_range(obj:object|tuple|HexCoords, n:int) -> set:
    """
    Returns a Set containing the cube coordinates of every hexagon in distance 
    n from obj.
        
    Parameters:
    -----------
    obj : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being an 
        Integer or Float. Needs to adhere to zero constraint.
        
    n : Integer
        An Integer limiting the distance to n moves from the obj.
        
    Raises:
    -------
    TypeError: 
        If q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the q, r or s coordinates 
        attributes.
        
    ConstraintViolation: 
        If the q + r + s = 0 constraint is violated.
        
    Returns:
    --------
    hex_in_range(Set): 
        A Set containing all cube coordinates within distance n from obj.
    """
    (o_q, o_r, o_s) = container_or_object(obj, 3)
    
    if not isinstance(n, int|float):
        raise TypeError("n needs to be an Integer, fractional distances not supported")
    elif isinstance(n, float):
        if not n.is_integer():
            raise TypeError("n needs to be an Integer, fractional distances not supported")

    hex_in_range = set()
        
    for q in range(-n, n+1):
        for r in range(-n, n+1):
            for s in range(-n, n+1):
                if q + r + s == 0:
                    hex_in_range.add((o_q+q, o_r+r, o_s+s))
                
    return hex_in_range
    

def line_draw(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> tuple:
    """
    Draws a line from one hexagon to another, returns a Tuple containing the 
    hexagons with the center closest to the line.
        
    Parameters:
    -----------
    obj_a : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being 
        an Integer or Float. Needs to adhere to zero constraint.
        
    obj_a : Object | Tuple | HexCoords
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being 
        an Integer or Float. Needs to adhere to zero constraint.
        
    Raises:
    -------
    TypeError: 
        If q, r or s is not an Integer or a Float. If a passed Tuple has
        too many or too few individual values.
        
    AttributeError: 
        If an Object is passed, but is missing the q, r or s coordinates 
        attributes.
        
    ConstraintViolation: 
        If the q+r+s=0 constraint is violated.
        
    Returns:
    --------
    hex_line_coords(Tuple): 
        A Tuple containing all cube cordinates from obj_a to obj_b inclusive.
    """
    (q_a, r_a, s_a) = container_or_object(obj_a, 3)
    (q_b, r_b, s_b) = container_or_object(obj_b, 3)
    
    inp_a = HexCoords(q_a, r_a, s_a)
    inp_b = HexCoords(q_b, r_b, s_b)
    
    ab_dist = distance(inp_a, inp_b)
        
    hex_line_lst = list()
        
    for i in range(0, ab_dist + 1):
        
        try:
            qrs_f = cube_linint(obj_a, obj_b, 1.0/ab_dist * i)
            
        except ZeroDivisionError:
            qrs_f = cube_linint(obj_a, obj_b, 0)
            
        item = round_hex(qrs_f)
        hex_line_lst.append(item)
    
    hex_line_coords = tuple(hex_line_lst)
        
    return hex_line_coords
    

def dist_lim_flood_fill(start_obj:object|tuple|HexCoords, n:int, obj_grp:list|set, 
                        *, movement_var:str="movement_cost") -> set:
    """
    All cube coordinates within n distance from an Object, factoring in movement_var 
    (variable if -1 blocks object traversability).
        
    Parameters:
    -----------
    start_obj : Tuple | Object
        A Tuple consisting of an Integer or Float for the q, r and s value,
        or an Object having a q, r and s attribute, the assigned values being 
        an Integer or Float. Needs to adhere to zero constraint.
        
    n : Integer
        The number of moves from start Object to fill.
        
    obj_grp : List | Set | SpriteGroup
        A container containing Objects in a cube coordinate system (tiles in tilemap).
        They need to adhere to the zero constraint.
        
    movement_var : String, optional
        Variable name of the variable, that Objects in obj_grp should contain to, 
        allow a block of object traversability. The movement is blocked if the 
        movement cost is -1.
        
    Raises:
    -------
    TypeError: 
        If the q, r or s coordinate in the start_obj or one of the items in the 
        obj_grp , being either a Tuple, Namedtuple or an Object having q, r or s 
        attributes, is not an Integer or Float. If n is not an Integer.
        
    AttributeError: 
        If one of the Objects is missing an q, r or s attribute.
        
    ConstraintViolation: 
        If the q + r + s = 0 constraint is violated.
        
    Returns:
    --------
    visited(Set): A Set containing all cube cordinates within distance n 
    from start_obj.
    """
    start = container_or_object(start_obj, 3)
    
    if not isinstance(n, int|float):
        raise TypeError("""n, representing the number of moves from the 
                           start coordinates needs to be and Integer or a Float
                           without a fractal part.""")
    
    if isinstance(n, float):
        if not n.is_integer:
            raise TypeError("""n, representing the number of moves from the 
                               start coordinates needs to be and Integer or a Float
                               without a fractal part.""")
                               
    for obj in obj_grp:
        for coord in ["q", "r", "s"]:
            if not hasattr(obj, coord):
                raise AttributeError(str(obj) + ", is missing the " + str(coord) + " attribute.")
            if not isinstance(getattr(obj, coord), int or float):
                raise TypeError(coord, "of obj", obj, "must be either an Integer or Float.")
        
    visited = set()
    visited.add(start)
    fringes = []
    fringes.append([start])
    
    if n > 0:
        for i in range(1,n+1):
            fringes.append([])
            for coords in fringes[i-1]:
                for j in range(0,6):
                    nbor_coords = neighbors(coords)[j]
                    # get corresponding object to nbor_coords from obj_grp -- #
                    nbor_obj = None
                    for obj in obj_grp:
                            if (obj.q, obj.r, obj.s) == nbor_coords:
                                nbor_obj = obj
                    blocked = getattr(nbor_obj, movement_var, 1) == -1
                    if nbor_coords not in visited:
                        if not blocked:
                            visited.add(nbor_coords)
                            fringes[i].append(nbor_coords)
    
    return visited


