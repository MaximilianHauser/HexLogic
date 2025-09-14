# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 13:32:03 2025

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
from src.hexlogic import hexlogic as hl
from tests.hexlogic_unittest import testgrp_generator

# regular imports ----------------------------------------------------------- #
from unittest.mock import Mock

# examples ------------------------------------------------------------------ #
"""
Printout describing visually and with text the example tileset and it's properties.
"""

                        
print("     +s \               / -r          ")
print("         \      _      /              ")
print("            _ / H \ _                 ")
print("        _ / S \ _ / I \ _             ")
print("      / R \ _ / B \ _ / J \           ")
print("      \ _ / G \ _ / C \ _ /           ")
print("-q __ / Q \ _ / A \ _ / K \ __ +q     ")
print("      \ _ / F \ _ / D \ _ /           ")
print("      / P \ _ / E \ _ / L \           ")
print("      \ _ / O \ _ / M \ _ /           ")
print("          \ _ / N \ _ /               ")
print("              \ _ /                   ")
print("         /              \             ")
print("     +r /                \ -s         ")
print("")
print("")
print("")
print("A: ( q=0, r=0, s=0 )                  ")
print("B: ( q=0, r=-1, s=1 )                 ")
print("C: ( q=1, r=-1, s=0 )                 ")
print("D: ( q=1, r=0, s=-1 )                 ")
print("E: ( q=0, r=1, s=-1 )                 ")
print("F: ( q=-1, r=1, s=0 )                 ")
print("G: ( q=-1, r=0, s=1 )                 ")
print("H: ( q=0, r=-2, s=2 )                 ")
print("I: ( q=1, r=-2, s=1 )                 ")
print("J: ( q=2, r=-2, s=0 )                 ")
print("K: ( q=2, r=-1, s=-1 )                ")
print("L: ( q=2, r=0, s=-2 )                 ")
print("M: ( q=1, r=1, s=-2 )                 ")
print("N: ( q=0, r=2, s=-2 )                 ")
print("O: ( q=-1, r=2, s=-1 )                ")
print("P: ( q=-2, r=2, s=0 )                 ")
print("Q: ( q=-2, r=1, s=1 )                 ")
print("R: ( q=-2, r=0, s=2 )                 ")
print("S: ( q=-1, r=-1, s=2 )                ")
print("")
print("")

"""
Printout of the example tileset and various functions performed on it as examples.
"""
example_grp = testgrp_generator((0, 0, 0), 5, ( (2, 0, -2, {"movement_cost":-1} ), 
                                                  (1, 1, -2, {"movement_cost":-1} ), 
                                                  (0, 2, -2, {"movement_cost":-1} ), 
                                                  (-1, 3, -2, {"movement_cost":-1} ),
                                                  (-2, 4, -2, {"movement_cost":-1} ),
                                                  (-3, 5, -2, {"movement_cost":-1} ),
                                                  (-4, 6, -2, {"movement_cost":-1} ),
                                                  (-3, 1, 2, {"movement_cost":-1} ),
                                                  (-2, 0, 2, {"movement_cost":-1} ),
                                                  (-1, -1, 2, {"movement_cost":-1} ),
                                                  (0, -2, 2, {"movement_cost":-1} ),
                                                  (1, -3, 2, {"movement_cost":-1} ),
                                                  (2, -4, 2, {"movement_cost":-1} ),
                                                  (3, -5, 2, {"movement_cost":-1} )
                                                  ))

print("")
print("Classes:")
print("")
print("class RectCoords(namedtuple('RectCoords', 'x y')):")
rect_coord = hl.RectCoords(18, 3)
print(rect_coord)
print("Coordinates in a rectangular cartesian coordinate system.")
print("")
print("class HexCoords(namedtuple('HexCoords', 'q r s')):")
hex_coord = hl.HexCoords(7, 8, -15)
print(hex_coord)
print("Coordinates in a three-dimensional cartesian coordinate system, limited by the constraint q + r + s = 0.")
print("")
print("class GraphMatrix:")
graph_matrix = hl.GraphMatrix(example_grp)
print(graph_matrix)
print("Creates a GraphMatrix object, containing a directed, weighted graph, from the objects or coordinates contained in tile_grp, organized in a Dictionary.")

print("")
print("")
print("")
print("Functions and Methods:")
print("")
print("def float_to_int(num_in:int|float) -> int|float:")
integer = hl.float_to_int(12.0)
print(integer)
print("Returns an Integer if passed an Integer or if passed a Float with its decimal being zero. Returns a Float if passed a Float, with a non zero decimal.")
print("")
print("def container_or_object(container_or_object:object|tuple|RectCoords|HexCoords|list|dict, expected_len:2|3, return_obj_type:str='Tuple') -> tuple|RectCoords|HexCoords|list|dict:")
ordered_pair = hl.container_or_object((2, -2), 2)
print(ordered_pair)
print("Returns a Tuple or a Namedtuple of predefined length, when passed an Object or a Tuple.")
print("")
print("def linint(a:int|float, b:int|float, t:int|float) -> int|float:")
linear_interpolation = hl.linint(3, 9, 0.5)
print(linear_interpolation)
print("Linear interpolation returns point at t of distance between a and b.")
print("")
print("def rect_linint(xy_a:object|tuple|RectCoords, xy_b:object|tuple|RectCoords, t:int|float, return_obj_type:str='Tuple') -> tuple|RectCoords|list|dict:")
rect_linear_interpolation = hl.rect_linint((3, 3), (9, 9), 0.5)
print(rect_linear_interpolation)
print("Linear interpolation returns point at t of distance between a and b on a cartesian coordinates system.")
print("")
print("def cube_linint(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords, t:int|float, return_obj_type:str='Tuple') -> tuple|HexCoords|list|dict:")
cube_linear_interpolation = hl.cube_linint((3, 6, -9), (-9, 6, 3), 0.5)
print(cube_linear_interpolation)
print("Returns the hextile coordinates of a point situated at t part of the way from obj_a to obj_b.")
print("")
print("def round_container(container:dict|list|set|tuple|RectCoords, d:int=0) -> dict|list|set|tuple|RectCoords:")
rounded_container = hl.round_container([-3.1, 6.2, -2.9, 7.2])
print(rounded_container)
print("Rounds each number in a container to the specified decimal, if None is specified to the nearest Integer.")
print("")
print("def round_hex(qrs:tuple|HexCoords, return_obj_type:str='Tuple') -> tuple|HexCoords|list|dict:")
rounded_hex = hl.round_hex((7.1, 8.2, -15.3))
print(rounded_hex)
print("Rounds each of the coordinates to the nearest Integer.")
print("")

example_object_1 = Mock()
example_object_1.x = 1
example_object_1.y = 2

print("def get_xy(obj:object, return_obj_type:str='Tuple') -> tuple|RectCoords|list|dict:")
x_y = hl.get_xy(example_object_1)
print(x_y)
print("Returns values of attributes x and y of obj as Tuple or RectCoords.")
print("")
print("def set_xy(obj:object, x:int|float, y:int|float) -> None:")
hl.set_xy(example_object_1, 3, 6)
print(example_object_1)
print("Set x and y attribute of obj to specified values.")
print("")

example_object_1.q = 3
example_object_1.r = 6
example_object_1.s = -9

print("def get_qrs(obj:object, return_obj_type:str='Tuple') -> tuple|HexCoords|list|dict:")
q_r_s = hl.get_qrs(example_object_1)
print(q_r_s)
print("Returns values of attributes q, r, s of obj.")
print("")
print("def set_qrs(obj:object, q:int|float, r:int|float, s:int|float) -> None:")
hl.set_qrs(example_object_1, -9, 6, 3)
print(example_object_1)
print("Set q r and s attribute of obj to specified values.")
print("")
print("def hex_to_pixel(qrs:object|tuple|HexCoords, tile_width:int=64, tile_height:int=64, return_obj_type:str='Tuple') -> tuple|RectCoords|list|dict:")
pixel = hl.hex_to_pixel((3, 6, -9))
print(pixel)
print("Converts cube coordinates to pixel coordinates.")
print("")
print("def pixel_to_hex(xy:object|tuple|RectCoords, tile_width:int=64, tile_height:int=64, return_obj_type:str='Tuple') -> tuple|HexCoords|list|dict:")
hex_tuple = hl.pixel_to_hex((144, 480))
print(hex_tuple)
print("Converts pixel coordinates to cube coordinates.")
print("")
print("def get_angle(obj_a:object|tuple|RectCoords|HexCoords, obj_b:object|tuple|RectCoords|HexCoords, expected_len_a:int=3, expected_len_b:int=3, unit:str='deg)' -> float:")
angle = hl.get_angle((3, 6, -9), (-9, 3, 6))
print(angle)
print("Returns the angle from a line through obj_a and abj_b relative to the x-axis of a two dimensional cartesian coordinate system.")
print("")
print("def neighbors(qrs:object|tuple|HexCoords, return_obj_type:str='Tuple') -> set:")
list_neighbors = hl.neighbors((3, 6, -9))
print(list_neighbors)
print("Return a List of coordinates of neighboring hexagons.")
print("")
print("def distance(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords) -> int|float:")
distance = hl.distance((3, 6, -9), (-9, 6, 3))
print(distance)
print("Returns distance from one Object to another in a cube coordinate system.")
print("")
print("def in_range(obj:object|tuple|HexCoords, n:int, return_obj_type:str='Tuple') -> set:")
list_in_range = hl.in_range((3, 6, -9), 1)
print(list_in_range)
print("Returns a Set containing the cube coordinates of every hexagon in distance n from obj.")
print("")
print("def line_draw(obj_a:object|tuple|HexCoords, obj_b:object|tuple|HexCoords, return_obj_type:str='Tuple') -> tuple:")
line = hl.line_draw((3, 6, -9), (-9, 6, 3))
print(line)
print("Draws a line from one hexagon to another, returns a Tuple containing the hexagons with the center closest to the line.")
print("")
print("def dist_lim_flood_fill(start_obj:object|tuple|HexCoords, n:int, obj_grp:list|set, movement_var:str='movement_cost') -> set:")
flood_fill = hl.dist_lim_flood_fill((0, 0, 0), 4, example_grp, movement_var="movement_cost")
print(flood_fill)
print("All cube coordinates within n distance from an Object, factoring in movement_var (variable if 0 blocks object traversability).")
print("")
print("def update_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords, movement_cost:int|float) -> None:")
graph_matrix.update_entry((0, 1, -1), (1, 1, -2), 1)
print(graph_matrix)
print("Add or update a one-directional entry in the adjacency matrix.")
print("")
print("def del_entry(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> None:")
graph_matrix.del_entry((-3, 3, 0), (-3, 2, 1))
print(graph_matrix)
print("Delete a one-directional entry in the adjacency matrix. Does not raise an Error or Warning if no entry matching the input exists.")
print("")
print("def connected(self, from_coord:object|tuple|HexCoords) -> set:")
graph_matrix.connected((-3, 2, 1))
print(graph_matrix)
print("Return all connected coordinates. Returns None, in case of there aren't being any.")
print("")
print("def get_movement_cost(self, from_coord:object|tuple|HexCoords, to_coord:object|tuple|HexCoords) -> int|float:")
m_c = graph_matrix.get_movement_cost((-3, 2, 1), (-2, 2, 0))
print(m_c)
print("Get the movement cost from one Object or coordinate to another.")
print("")
print("def breadth_first_search(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords, test_accessibility:bool=False, return_obj_type:str='Tuple') -> list:")
breadth_first = graph_matrix.breadth_first_search((-3, 0, 3), (3, 0, -3), test_accessibility=False)
print(breadth_first)
print("Algorithm for searching a tree data structure for a node that satisfies a given property.")
print("")
print("def dijkstras_algorithm(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords, test_accessibility:bool=False, return_obj_type:str='Tuple') -> list:")
dijkstras = graph_matrix.dijkstras_algorithm((-3, 0, 3), (3, 0, -3), test_accessibility=False)
print(dijkstras)
print("Supports weighted movement cost.")
print("")
print("def a_star_algorithm(self, start:object|tuple|HexCoords, goal:object|tuple|HexCoords, test_accessibility:bool=False, return_obj_type:str='Tuple') -> list:")
a_star = graph_matrix.a_star_algorithm((-3, 0, 3), (3, 0, -3), test_accessibility=False)
print(a_star)
print("Modified version of Dijkstra’s Algorithm that is optimized for a single destination. It prioritizes paths that seem to be leading closer to a goal.")


