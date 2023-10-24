# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 14:48:51 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# add parent directory ------------------------------------------------------ #
import sys
sys.path.append("..")
# imports from parent directory --------------------------------------------- #
import hexlogic as hl
from hexlogic import RectCoords
from hexlogic import HexCoords
from hexlogic import ConstraintViolation
# built-in libraries -------------------------------------------------------- #
import unittest
from unittest.mock import Mock


# unittests ----------------------------------------------------------------- #
def testgrp_generator(center_obj:object|tuple|HexCoords, radius:int, override_coords:tuple=False) -> set:
    """
    Generate a set containing objects with q, r and s attributes to simulate a 
    coordinate groups or a SpriteGroup allow unittests on more complex functions.
    Override coordinates must be formatted as follows: 
    (q, r, s, {attribute_name : override_value})
    """
    # obj_grp containing all objects with 2 dist from start ----------------- #
    obj_grp = list()
    # coords of all objects with distance 2 from start_obj ------------------ #
    all_coords = list(hl.in_range(center_obj, radius))
    # add objects to obj_grp ------------------------------------------------ #
    for coords in all_coords:
        # generate generic object ------------------------------------------- #
        obj = Mock()
        obj.q = coords[0]
        obj.r = coords[1]
        obj.s = coords[2]
        obj.block = False
        obj.movement_cost = 1
        obj_grp.append(obj)
    # generate list as basis to modify obj_grp ------------------------------ #
    index_to_override = list()
    if override_coords:
        for i in range(len(obj_grp)):
            for o_coords in override_coords:
                if o_coords[0] == obj_grp[i].q and o_coords[1] == obj_grp[i].r and o_coords[2] == obj_grp[i].s :
                    index_to_override.append([i, o_coords[3]])
    # modify generic objects with override ---------------------------------- #             
    for override in index_to_override:
        for key in override[1].keys():
            if override[1][key] != "del":
                setattr(obj_grp[override[0]], key, override[1][key])
            else:
                delattr(obj_grp[override[0]], key)
        
    return obj_grp


def testgrp_teardown(test_grp:list) -> None:
    """
    NOT WORKING Clean dispose of the Mock objects in test_grp and test_grp. NOT WORKING
    """
    for obj in test_grp:
        obj.dispose()
    del test_grp


# Tests for test specific functions ----------------------------------------- #
class TestTestgrpGenerator(unittest.TestCase):
    """
    Includes a test of testgrp_teardown in the tearDown section of the unittest 
    for simplicity reasons. testgrp_teardown NOT WORKING
    """
    def setUp(self):
        self.test_grp = testgrp_generator((0, 0, 0), 1, ((1, -1, 0, {"block":True} ), (-1, 1, 0, {"s":"0"} )))
        self.control = {(-1, 0, 1, False), (0, -1, 1, False), (1, 0, -1, False), (0, 0, 0, False), (-1, 1, "0", False), (1, -1, 0, True), (0, 1, -1, False)}
    
    def test_attributes(self):
        self.test_set = {(obj.q, obj.r, obj.s, obj.block) for obj in self.test_grp}
        self.assertEqual(self.test_set, self.control)
    
    def tearDown(self):
        testgrp_teardown(self.test_grp)
        del self.control
        del self.test_set


# Test RectCoords ----------------------------------------------------------- #
class TestRectCoords(unittest.TestCase):
    
    def setUp(self):
        self.rc_test_obj_2 = RectCoords(2, 5)
    
    def test_error(self):
        with self.assertRaises(TypeError):
            rc_test_obj_0 = RectCoords("2", 5)
            rc_test_obj_1 = RectCoords(2, "5")
    
    def test_attributes(self):
        self.assertIs(self.rc_test_obj_2.x, 2)
        self.assertIs(self.rc_test_obj_2.y, 5)
            
    def tearDown(self):
        del self.rc_test_obj_2
        

# Test HexCoords ------------------------------------------------------------ #
class TestHexCoords(unittest.TestCase):
    
    def setUp(self):
        self.hc_test_obj_4 = HexCoords(1, -1, 0)
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hc_test_obj_0 = HexCoords("1", -1, 0)
            hc_test_obj_1 = HexCoords(1, "-1", 0)
            hc_test_obj_2 = HexCoords(1, -1, "0")
            
        with self.assertRaises(ConstraintViolation):
            hc_test_obj_3 = HexCoords(1, -1, 1)
    
    def test_attributes(self):
        self.assertIs(self.hc_test_obj_4.q, 1)
        self.assertIs(self.hc_test_obj_4.r, -1)
        self.assertIs(self.hc_test_obj_4.s, 0)
        
    def tearDown(self):
        del self.hc_test_obj_4
        
        
# Test GraphMatrix ---------------------------------------------------------- #
class TestGraphMatrix(unittest.TestCase):
    
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.test_grp_0 = testgrp_generator((0, 0, 0), 2, ((0, -1, 1, {"r":"-1"} ), 
                                                          (1, -1, 0, {"movement_cost":3} ) ))
        # AttributeError ---------------------------------------------------- #
        self.test_grp_1 = testgrp_generator((0, 0, 0), 2, ((-1, -1, 2, {"r":"del"} ), 
                                                          (0, 1, -1, {"movement_cost":7} ) ))
        # ConstraintViolation ----------------------------------------------- #
        self.test_grp_2 = testgrp_generator((0, 0, 0), 2, ((-1, -1, 2, {"q":-3} ), 
                                                          (0, 1, -1, {"movement_cost":7} ) ))
        # test input expected output ---------------------------------------- #
        self.test_grp_3 = testgrp_generator((0, 0, 0), 1, ((0, -1, 1, {"movement_cost":2} ), 
                                                          (1, -1, 0, {"movement_cost":3} ), 
                                                          (-1, 1, 0, {"movement_cost":4} ) ))
        control_rows = {(-1, 0, 1): [0, 2, 0, 1, 4, 0, 0], 
                        (0, -1, 1): [1, 0, 0, 1, 0, 3, 0],
                        (1, 0, -1): [0, 0, 0, 1, 0, 3, 1],
                        (0, 0, 0): [1, 2, 1, 0, 4, 3, 1],
                        (-1, 1, 0): [1, 0, 0, 1, 0, 0, 1],
                        (1, -1, 0): [0, 2, 1, 1, 0, 0, 0],
                        (0, 1, -1): [0, 0, 1, 1, 4, 0, 0]
                        }
        columns = [(-1, 0, 1), (0, -1, 1), (1, 0, -1), (0, 0, 0), (-1, 1, 0), (1, -1, 0), (0, 1, -1)]
        
        self.control_dict = dict()
        
        for key in control_rows.keys():
            for i in range(len(control_rows[key])):
                f = key
                t = columns[i]
                mc = control_rows[key][i]
                if mc > 0:
                    if f in self.control_dict.keys():
                        self.control_dict[f].update({t:mc})
                    else:
                        self.control_dict.update({f:{t:mc}})
    
    def test_error(self):
        with self.assertRaises(TypeError):
            test_matrix_0 = hl.GraphMatrix(self.test_grp_0)
        
        with self.assertRaises(AttributeError):
            test_matrix_1 = hl.GraphMatrix(self.test_grp_1)
        
        with self.assertRaises(ConstraintViolation):
            test_matrix_2 = hl.GraphMatrix(self.test_grp_2)
    
    def test_attributes(self):
        test_matrix_3 = hl.GraphMatrix(self.test_grp_3)
        self.assertEqual(test_matrix_3.matrix_dict, self.control_dict)
    
    def tearDown(self):
        del self.test_grp_0
        del self.test_grp_1
        del self.test_grp_2
        del self.test_grp_3
        

# Test FloatOrInt ----------------------------------------------------------- #
class TestFloatToInt(unittest.TestCase):
    
    def setUp(self):
        self.fti_0 = hl.float_to_int(1)
        self.fti_1 = hl.float_to_int(2.0)
        self.fti_2 = hl.float_to_int(3.4)
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.float_to_int("3")
    
    def test_inout(self):
        self.assertEqual(self.fti_0, 1.0)
        self.assertIsInstance(self.fti_0, int)
        self.assertEqual(self.fti_1, 2.0)
        self.assertIsInstance(self.fti_1, int)
        self.assertEqual(self.fti_2, 3.4)
        self.assertIsInstance(self.fti_2, float)
        
    def tearDown(self):
        del self.fti_0
        del self.fti_1
        del self.fti_2
        

# Test TupleOrObject -------------------------------------------------------- #
class TestTupleOrObject(unittest.TestCase):
    
    def setUp(self):
        self.obj_0 = Mock()
        self.obj_0.x = 1
        self.obj_0.y = 1
        self.obj_0.q = 2
        self.obj_0.r = -2
        self.obj_0.s = 0
        self.obj_1 = Mock()
        self.obj_1.x = 1
        del self.obj_1.y
        self.obj_1.q = 2
        self.obj_1.r = -2
        self.obj_1.s = "0"
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.tuple_or_object(self.obj_1, 3)
            hl.tuple_or_object((1, 0, -1), 2)
            hl.tuple_or_object(2, 2)
        with self.assertRaises(AttributeError):
            hl.tuple_or_object(self.obj_1, 2)
        with self.assertRaises(ConstraintViolation):
            hl.tuple_or_object(HexCoords(1, 2, 3), 3)
        
    def test_inout(self):
        # Object 2dim as input ---------------------------------------------- #
        self.assertEqual(hl.tuple_or_object(self.obj_0, 2), (1, 1))
        self.assertEqual(hl.tuple_or_object(self.obj_0, 2, return_coords_obj=True), RectCoords(1, 1))
        # Object 3dim as input ---------------------------------------------- #
        self.assertEqual(hl.tuple_or_object(self.obj_0, 3), (2, -2, 0))
        self.assertEqual(hl.tuple_or_object(self.obj_0, 3, return_coords_obj=True), HexCoords(2, -2, 0))
        # Tuple 2dim as input ----------------------------------------------- #
        self.assertEqual(hl.tuple_or_object((2, 3), 2), (2, 3))
        self.assertEqual(hl.tuple_or_object((2, 3), 2, return_coords_obj=True), RectCoords(2, 3))
        # Tuple 3dim as input ----------------------------------------------- #
        self.assertEqual(hl.tuple_or_object((3, 0, -3), 3), (3, 0, -3))
        self.assertEqual(hl.tuple_or_object((3, 0, -3), 3, return_coords_obj=True), HexCoords(3, 0, -3))
        # RectCoords as input ----------------------------------------------- #
        self.assertEqual(hl.tuple_or_object(RectCoords(2, 3), 2), (2, 3))
        self.assertEqual(hl.tuple_or_object(RectCoords(2, 3), 2, return_coords_obj=True), RectCoords(2, 3))
        # HexCoords as input ------------------------------------------------ #
        self.assertEqual(hl.tuple_or_object(HexCoords(3, 0, -3), 3), (3, 0, -3))
        self.assertEqual(hl.tuple_or_object(HexCoords(3, 0, -3), 3, return_coords_obj=True), HexCoords(3, 0, -3))
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        

# TestLinint ---------------------------------------------------------------- #
class TestLinint(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.linint(1, "2", 0.5)
            hl.linint("1", 2, 0.5)
            hl.linint(1, 2, "0.5")
            
    def test_inout(self):
        self.assertEqual(hl.linint(1, 2, 0.5), 1.5)


# TestCartesianLinint ------------------------------------------------------- #
class TestRectLinint(unittest.TestCase):
    
    def setUp(self):
        self.obj_0 = Mock()
        self.obj_0.x = 0
        self.obj_0.y = 0
        self.obj_1 = Mock()
        self.obj_1.x = 5
        self.obj_1.y = 5
        self.obj_2 = Mock()
        self.obj_2.x = 2
        del self.obj_2.y
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.rect_linint((-3,1,1), (2,3), 0.5)
            hl.rect_linint((-3,1), (2,3,0), 0.5)
            hl.rect_linint((-1), (2,3), 0.5)
            hl.rect_linint((-3,1), (3), 0.5)
            hl.rect_linint({"1":-3,"2":1}, (3), 0.5)
            hl.rect_linint({"1":-3,"2":1}, (3), (0.5))
            
        with self.assertRaises(AttributeError):
            hl.rect_linint(self.obj_0, self.obj_2, 0.2)
            
    def test_inout(self):
        self.assertEqual(hl.rect_linint(self.obj_0, self.obj_1, 0.2), (1, 1))
        self.assertEqual(hl.rect_linint((-3,1), (2,3), 0.5), (-0.5, 2))
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()


# TestCubeLinint ------------------------------------------------------------ #
class TestCubeLinint(unittest.TestCase):
    
    def setUp(self):
        # Tuple and Object -------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 2
        self.obj_0.r = -2
        self.obj_0.s = 0
        self.obj_1 = Mock()
        self.obj_1.q = -1
        self.obj_1.r = -1
        self.obj_1.s = 2
        # assertRaises TypeError, ConstraintViolation ----------------------- #
        self.obj_2 = Mock()
        self.obj_2.q = 3
        self.obj_2.r = -2
        del self.obj_2.s
        self.obj_3 = Mock()
        self.obj_3.q = "3"
        self.obj_3.r = -2
        self.obj_3.s = -1
        # HexCoords and Object ---------------------------------------------- #
        self.obj_4 = Mock()
        self.obj_4.q = 2
        self.obj_4.r = 0
        self.obj_4.s = -2
        self.obj_5 = Mock()
        self.obj_5.q = 2
        self.obj_5.r = -3
        self.obj_5.s = 1
        # Object and Tuple | HexCoords | Object ----------------------------- #
        self.obj_6 = Mock()
        self.obj_6.q = -1
        self.obj_6.r = 1
        self.obj_6.s = 0
        self.obj_7 = Mock()
        self.obj_7.q = -2
        self.obj_7.r = 1
        self.obj_7.s = 1
        self.obj_8 = Mock()
        self.obj_8.q = 1
        self.obj_8.r = -3
        self.obj_8.s = 2
        self.obj_9 = Mock()
        self.obj_9.q = 0
        self.obj_9.r = -1
        self.obj_9.s = 1
        self.obj_10 = Mock()
        self.obj_10.q = 1
        self.obj_10.r = 1
        self.obj_10.s = -2
        
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.cube_linint((1, 0, -1), self.obj_3, 1)
            hl.cube_linint((2, -2, 0), "(-3, 0, 3)", 0.5)
        
        with self.assertRaises(AttributeError):
            hl.cube_linint(self.obj_2, (2, 0, -2), 0.2)
        
        with self.assertRaises(ConstraintViolation):
            hl.cube_linint((1, 0, -2), self.obj_0, 0.5)
    
    def test_inout(self):
        # Tuple and Tuple --------------------------------------------------- #
        self.assertEqual(hl.cube_linint((-2, 0, 2), (2, 0, -2), 0.5), (0, 0, 0))
        self.assertEqual(hl.cube_linint((0, -1, 1), (0, 1, -1), 0.5, return_coords_obj=True), HexCoords(0, 0, 0))
        # Tuple and HexCoords ----------------------------------------------- #
        self.assertEqual(hl.cube_linint((2, -1, -1), HexCoords(-1, 2, -1), 1), (-1, 2, -1))
        self.assertEqual(hl.cube_linint((-2, 2, 0), HexCoords(0, 2, -2), 0.5, return_coords_obj=True), HexCoords(-1, 2, -1))
        # Tuple and Object -------------------------------------------------- #
        self.assertEqual(hl.cube_linint((0, 0, 0), self.obj_0, 0.5), (1, -1, 0))
        self.assertEqual(hl.cube_linint((-1, 1, 0), self.obj_1, 0.5, return_coords_obj=True), HexCoords(-1, 0, 1))
        # HexCoords and Tuple ----------------------------------------------- #
        self.assertEqual(hl.cube_linint(HexCoords(0, 2, -2), (0, 0, 0), 0.5), (0, 1, -1))
        self.assertEqual(hl.cube_linint(HexCoords(0, 1, -1), (2, -1, -1), 0.5, return_coords_obj=True), HexCoords(1, 0, -1))
        # HexCoords and HexCoords ------------------------------------------- #
        self.assertEqual(hl.cube_linint(HexCoords(-2, 2, 0), HexCoords(0, -2, 2), 0.5), (-1, 0, 1))
        self.assertEqual(hl.cube_linint(HexCoords(-1, -1, 2), HexCoords(1, 1, -2), 0.5, return_coords_obj=True), HexCoords(0, 0, 0))
        # Hex Coords and Object --------------------------------------------- #
        self.assertEqual(hl.cube_linint(HexCoords(-2, 0, 2), self.obj_4, 0.25), (-1, 0, 1))
        self.assertEqual(hl.cube_linint(HexCoords(1, -2, 1), self.obj_5, 1, return_coords_obj=True), HexCoords(2, -3, 1))
        # Object and Tuple -------------------------------------------------- #
        self.assertEqual(hl.cube_linint(self.obj_6, (3, -3, 0), 0.75), (2, -2, 0))
        self.assertEqual(hl.cube_linint(self.obj_7, (2, -3, 1), 0.25, return_coords_obj=True), HexCoords(-1, 0, 1))
        # Object and Hexcoords ---------------------------------------------- #
        self.assertEqual(hl.cube_linint(self.obj_8, HexCoords(3, -3, 0), 0.5), (2, -3, 1))
        self.assertEqual(hl.cube_linint(self.obj_9, HexCoords(0, -3, 3), 0.5, return_coords_obj=True), HexCoords(0, -2, 2))
        # Object and Object ------------------------------------------------- #
        self.assertEqual(hl.cube_linint(self.obj_10, self.obj_8, 0.75), (1, -2, 1))
        self.assertEqual(hl.cube_linint(self.obj_5, self.obj_7, 0.5, return_coords_obj=True), HexCoords(0, -1, 1))
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()
        self.obj_4.dispose()
        self.obj_5.dispose()
        self.obj_6.dispose()
        self.obj_7.dispose()
        self.obj_8.dispose()
        self.obj_9.dispose()
        self.obj_10.dispose()


# TestRoundContainer -------------------------------------------------------- #
class TestRoundContainer(unittest.TestCase):
    """
    Interim solution until round_container in final form.
    """
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.round_container(3.42, 1)
    
    def test_inout(self):
        self.assertEqual(hl.round_container({"a":2, "b": 4.4, "c":"d"}, d=0), {"a":2, "b": 4, "c":"d"})
        self.assertEqual(hl.round_container(["a", "b", 3, 4.32, 2.19], d=1), ["a", "b", 3, 4.3, 2.2])
        self.assertEqual(hl.round_container({"a", 4.29, 0.92}, d=1), {"a", 4.3, 0.9})
        self.assertEqual(hl.round_container(("a", 2, 5.4), d=0), ("a", 2, 5))
        self.assertEqual(hl.round_container(RectCoords(1.2, 2.7), d=0), RectCoords(1, 3))


# TestRoundHex -------------------------------------------------------------- #
class TestRoundHex(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.round_hex((2, 0, "-2"))
            hl.round_hex((2, "0", -2))
            hl.round_hex(HexCoords("2", 0, -2))
        
        with self.assertRaises(ConstraintViolation):
            hl.round_hex((2, 2, 3), return_coords_obj=True)
            hl.round_hex(HexCoords(2, 2, 3), return_coords_obj=True)
    
    def test_inout(self):
        self.assertEqual(hl.round_hex((1.2, 3.1, -4.3)), (1, 3, -4))
        self.assertEqual(hl.round_hex((1.2, 3.1, -4.3), return_coords_obj=True), HexCoords(1, 3, -4))
        self.assertEqual(hl.round_hex(HexCoords(0.9, 1.8, -2.7)), HexCoords(1, 2, -3))
        self.assertEqual(hl.round_hex(HexCoords(0.9, 1.8, -2.7), return_coords_obj=True), HexCoords(1, 2, -3))


# TestGetxy ----------------------------------------------------------------- #  
class TestGetxy(unittest.TestCase):
    
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.x = 5
        self.obj_0.y = "6"
        # AttributeError ---------------------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.x = 5
        del self.obj_1.y
        # test input expected output ---------------------------------------- #
        self.obj_2 = Mock()
        self.obj_2.x = 1
        self.obj_2.y = 2
        self.obj_3 = Mock()
        self.obj_3.x = 3
        self.obj_3.y = 4
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.get_xy(self.obj_0)
            hl.get_xy(self.obj_0, return_coords_obj=True)
        
        with self.assertRaises(AttributeError):
            hl.get_xy(self.obj_1)
            hl.get_xy(self.obj_1, return_coords_obj=True)
    
    def test_inout(self):
        self.assertEqual(hl.get_xy(self.obj_2), (1, 2))
        self.assertEqual(hl.get_xy(self.obj_3, return_coords_obj=True), RectCoords(3, 4))
    
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()


# TestSetxy ----------------------------------------------------------------- #
class TestSetxy(unittest.TestCase):
    
    def setUp(self):
        self.obj_0 = Mock()
        del self.obj_0.x
        del self.obj_0.y
        self.obj_1 = Mock()
        del self.obj_1.x
        del self.obj_1.y
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.set_xy(self.obj_0, 1, "2")
            hl.set_xy(self.obj_1, "3", 4)
    
    def test_inout(self):
        self.obj_0.x = 9
        self.obj_0.y = 9
        hl.set_xy(self.obj_0, 1, 2)
        self.assertEqual(self.obj_0.x, 1)
        self.assertEqual(self.obj_0.y, 2)
        
        self.obj_1.x = 9
        self.obj_1.y = 9
        hl.set_xy(self.obj_1, 3, 4)
        self.assertEqual(self.obj_1.x, 3)
        self.assertEqual(self.obj_1.y, 4)
    
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()


# TestGetqrs ---------------------------------------------------------------- #
class TestGetqrs(unittest.TestCase):
    
    def setUp(self):
        self.obj_0 = Mock()
        self.obj_0.q = 1
        self.obj_0.r = 1
        self.obj_0.s = -2
        self.obj_1 = Mock()
        self.obj_1.q = 1
        self.obj_1.r = 1
        del self.obj_1.s
        
    def test_error(self):
        with self.assertRaises(AttributeError):
            hl.get_qrs(self.obj_1)
    
    def test_inout(self):
        self.assertEqual(hl.get_qrs(self.obj_0), (1, 1, -2))
        self.assertEqual(hl.get_qrs(self.obj_0, return_coords_obj=True), HexCoords(1, 1, -2))
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()


# TestSetqrs ---------------------------------------------------------------- #
class TestSetqrs(unittest.TestCase):
    
    def setUp(self):
        self.obj_0 = Mock()
        del self.obj_0.q
        del self.obj_0.r
        del self.obj_0.s
        
    def test_error(self):
        
        with self.assertRaises(TypeError):
            hl.set_qrs(self.obj_0, 1, 0, "-1")
        
        with self.assertRaises(ConstraintViolation):
            hl.set_qrs(self.obj_0, 1, 1, 0)
    
    def test_inout(self):
        hl.set_qrs(self.obj_0, 1, 2, -3)
        self.assertEqual(self.obj_0.q, 1)
        self.assertEqual(self.obj_0.r, 2)
        self.assertEqual(self.obj_0.s, -3)
        
    def tearDown(self):
        self.obj_0.dispose()


# TestHexToPixel ------------------------------------------------------------ #
class TestHexToPixel(unittest.TestCase):
    
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 1
        self.obj_0.r = -3
        self.obj_0.s = "2"
        # AttributeError ---------------------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.q = 3
        self.obj_1.r = 0
        del self.obj_1.s
        # test input expected output ---------------------------------------- #
        self.obj_2 = Mock()
        self.obj_2.q = 3
        self.obj_2.r = -3
        self.obj_2.s = 0
        self.obj_3 = Mock()
        self.obj_3.q = 2
        self.obj_3.r = -1
        self.obj_3.s = -1
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.hex_to_pixel(self.obj_0)
        with self.assertRaises(AttributeError):
            hl.hex_to_pixel(self.obj_1)
        with self.assertRaises(ConstraintViolation):
            hl.hex_to_pixel((2, 0, -1))
    
    def test_inout(self):
        self.assertEqual(hl.hex_to_pixel((-1, -1, 2)), (-48, -96))
        self.assertEqual(hl.hex_to_pixel((-2, 1, 1), return_coords_obj=True), RectCoords(-96, 0))
        self.assertEqual(hl.hex_to_pixel(HexCoords(2, -3, 1)), (96, -128))
        self.assertEqual(hl.hex_to_pixel(HexCoords(-2, 2, 0), return_coords_obj=True), RectCoords(-96, 64))
        self.assertEqual(hl.hex_to_pixel(self.obj_2), (144, -96))
        self.assertEqual(hl.hex_to_pixel(self.obj_3, return_coords_obj=True), RectCoords(96, 0))
    
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()


# TestPixelToHex ------------------------------------------------------------ #
class TestPixelToHex(unittest.TestCase):
    
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.x = -48
        self.obj_0.y = "-96"
        # AttributeError ---------------------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.x = -96
        del self.obj_1.y
        # test input expected output ---------------------------------------- #
        self.obj_2 = Mock()
        self.obj_2.x = 144
        self.obj_2.y = -96
        self.obj_3 = Mock()
        self.obj_3.x = 96
        self.obj_3.y = 0
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.pixel_to_hex(self.obj_0)
        with self.assertRaises(AttributeError):
            hl.pixel_to_hex(self.obj_1)
    
    def test_inout(self):
        self.assertEqual(hl.pixel_to_hex((-48, -96)), (-1, -1, 2))
        self.assertEqual(hl.pixel_to_hex((-96, 0), return_coords_obj=True), HexCoords(-2, 1, 1))
        self.assertEqual(hl.pixel_to_hex((96, -128)), (2, -3, 1))
        self.assertEqual(hl.pixel_to_hex((-96, 64), return_coords_obj=True), HexCoords(-2, 2, 0))
        self.assertEqual(hl.pixel_to_hex(self.obj_2), (3, -3, 0))
        self.assertEqual(hl.pixel_to_hex(self.obj_3, return_coords_obj=True), HexCoords(2, -1, -1))
    
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()


# TestNeighbors ------------------------------------------------------------- #
class TestNeighbors(unittest.TestCase):
    
    def setUp(self):
        self.obj_0 = Mock()
        self.obj_0.q = 1
        self.obj_0.r = -2
        del self.obj_0.s
        self.obj_1 = Mock()
        self.obj_1.q = -1
        self.obj_1.r = 0
        self.obj_1.s = 1
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.neighbors([1, 0, -1])
        
        with self.assertRaises(AttributeError):
            hl.neighbors(self.obj_0)
        
        with self.assertRaises(ConstraintViolation):
            hl.neighbors((1, 0, -2))
    
    def test_inout(self):
        self.assertEqual(hl.neighbors((1, -2, 1)), ((2, -2, 0), (2, -3, 1), (1, -3, 2), (0, -2, 2), (0, -1, 1), (1, -1, 0)))
        self.assertEqual(hl.neighbors(HexCoords(0, -1, 1)), ((1, -1, 0), (1, -2, 1), (0, -2, 2), (-1, -1, 2), (-1, 0, 1), (0, 0, 0)))
        self.assertEqual(hl.neighbors(self.obj_1), ((0, 0, 0), (0, -1, 1), (-1, -1, 2), (-2, 0, 2), (-2, 1, 1), (-1, 1, 0)))
    
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()


# TestDistance -------------------------------------------------------------- #
class TestDistance(unittest.TestCase):
    
    def setUp(self):
        # AttributeError ---------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 1
        self.obj_0.r = -2
        del self.obj_0.s
        # test input expected output ---------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.q = 1
        self.obj_1.r = 0
        self.obj_1.s = -1
        self.obj_2 = Mock()
        self.obj_2.q = 1
        self.obj_2.r = 1
        self.obj_2.s = -2
        self.obj_3 = Mock()
        self.obj_3.q = -2
        self.obj_3.r = 1
        self.obj_3.s = 1
        self.obj_4 = Mock()
        self.obj_4.q = 0
        self.obj_4.r = 0
        self.obj_4.s = 0
        self.obj_5 = Mock()
        self.obj_5.q = 2
        self.obj_5.r = -1
        self.obj_5.s = -1

    def test_error(self):
        with self.assertRaises(TypeError):
            hl.distance((0, 1, -1), ("2", -1, -1))
        
        with self.assertRaises(AttributeError):
            hl.distance((0, 0, 0), self.obj_0)
        
        with self.assertRaises(ConstraintViolation):
            hl.distance((0, -1, 2), (-2, 0, 2))
    
    def test_inout(self):
        # obj_a is Tuple ---------------------------------------------------- #
        self.assertEqual(hl.distance((3, -3, 0), (-1, 1, 0)), 4)
        self.assertEqual(hl.distance((0, -2, 2), HexCoords(0, 1, -1)), 3)
        self.assertEqual(hl.distance((-2, 0, 2), self.obj_1), 3)
        # obj_a is HexCoords ------------------------------------------------ #
        self.assertEqual(hl.distance(HexCoords(-2, 2, 0), (0, 2, -2)), 2)
        self.assertEqual(hl.distance(HexCoords(-1, -1, 2), HexCoords(0, -1, 1)), 1)
        self.assertEqual(hl.distance(HexCoords(1, -2, 1), self.obj_2), 3)
        # obj_a is Object --------------------------------------------------- #
        self.assertEqual(hl.distance(self.obj_3, (0, 0, 0)), 2)
        self.assertEqual(hl.distance(self.obj_4, HexCoords(2, -1, -1)), 2)
        self.assertEqual(hl.distance(self.obj_3, self.obj_5), 4)
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()
        self.obj_4.dispose()
        self.obj_5.dispose()


# TestInRange --------------------------------------------------------------- #
class TestInRange(unittest.TestCase):
    
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 1
        self.obj_0.r = "-1"
        self.obj_0.s = 0
        # AttributeError ---------------------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.q = 3
        self.obj_1.r = -2
        del self.obj_1.s
        self.obj_2 = Mock()
        self.obj_2.q = 0
        self.obj_2.r = 1
        self.obj_2.s = -1
        
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.in_range(self.obj_0, 1)
            hl.in_range([1, 0, -1], 2)
        
        with self.assertRaises(AttributeError):
            hl.in_range(self.obj_1, 1)
        
        with self.assertRaises(ConstraintViolation):
            hl.in_range((1, 0, -2), 3)
    
    def test_inout(self):
        self.assertEqual(hl.in_range((1, -2, 1), 1), {(2, -2, 0), (0, -1, 1), (1, -2, 1), (1, -3, 2), (2, -3, 1), (1, -1, 0), (0, -2, 2)})
        self.assertEqual(hl.in_range(HexCoords(-1, 0, 1), 3), {(-1, -3, 4), (0, -1, 1), (-1, -1, 2), (-2, 1, 1), (-2, 3, -1), (-1, 3, -2), (1, -2, 1), (-4, 2, 2), (-3, 0, 3), (2, -1, -1), (-2, 0, 2), (0, 2, -2), (-4, 1, 3), (1, 0, -1), (2, 0, -2), (0, -3, 3), (-2, -2, 4), (1, -3, 2), (-4, 0, 4), (-1, 1, 0), (1, -1, 0), (2, -2, 0), (-1, 0, 1), (-1, 2, -1), (0, 0, 0), (2, -3, 1), (-2, -1, 3), (-1, -2, 3), (0, 1, -1), (0, -2, 2), (-3, -1, 4), (-3, 3, 0), (-2, 2, 0), (-4, 3, 1), (1, 1, -2), (-3, 1, 2), (-3, 2, 1)})
        self.assertEqual(hl.in_range(self.obj_2, 2), {(2, 1, -3), (0, -1, 1), (-2, 1, 1), (-2, 3, -1), (-1, 3, -2), (0, 3, -3), (2, -1, -1), (0, 2, -2), (1, 0, -1), (2, 0, -2), (-1, 1, 0), (1, -1, 0), (-1, 0, 1), (-1, 2, -1), (0, 0, 0), (0, 1, -1), (1, 2, -3), (-2, 2, 0), (1, 1, -2)})
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()


# TestLineDraw -------------------------------------------------------------- #
class TestLineDraw(unittest.TestCase):
    
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 1
        self.obj_0.r = "-2"
        self.obj_0.s = 1
        # AttributeError ---------------------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.q = 3
        del self.obj_1.r
        self.obj_1.s = -1
        # test input expected output ---------------------------------------- #
        self.obj_2 = Mock()
        self.obj_2.q = 3
        self.obj_2.r = -2
        self.obj_2.s = -1
        self.obj_3 = Mock()
        self.obj_3.q = 2
        self.obj_3.r = 0
        self.obj_3.s = -2
        self.obj_4 = Mock()
        self.obj_4.q = 1
        self.obj_4.r = 1
        self.obj_4.s = -2
        self.obj_5 = Mock()
        self.obj_5.q = -1
        self.obj_5.r = -1
        self.obj_5.s = 2
        self.obj_6 = Mock()
        self.obj_6.q = 2
        self.obj_6.r = -3
        self.obj_6.s = 1
        self.obj_7 = Mock()
        self.obj_7.q = -2
        self.obj_7.r = 1
        self.obj_7.s = 1
        
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.line_draw(self.obj_0, self.obj_1)
        
        with self.assertRaises(AttributeError):
            hl.line_draw(self.obj_2, self.obj_1)
        
        with self.assertRaises(ConstraintViolation):
            hl.line_draw(HexCoords(0, 0, 0), (1, -3, 1))
    
    def test_inout(self):
        # obj_a is Tuple ---------------------------------------------------- #
        self.assertEqual(hl.line_draw((0, 3, -3), (2, 0, -2)), ((0, 3, -3), (1, 2, -3), (1, 1, -2), (2, 0, -2)))
        self.assertEqual(hl.line_draw((-2, 2, 0), HexCoords(3, -3, 0)), ((-2, 2, 0), (-1, 1, 0), (0, 0, 0), (1, -1, 0), (2, -2, 0), (3, -3, 0)))
        self.assertEqual(hl.line_draw((-1, -1, 2), self.obj_3), ((-1, -1, 2), (0, -1, 1), (0, 0, 0), (1, 0, -1), (2, 0, -2)))
        # obj_a is HexCoords ------------------------------------------------ #
        self.assertEqual(hl.line_draw(HexCoords(-2, 2, 0), (2, 0, -2)), ((-2, 2, 0), (-1, 2, -1), (0, 1, -1), (1, 0, -1), (2, 0, -2)))
        self.assertEqual(hl.line_draw(HexCoords(-1, 2, -1), HexCoords(2, -3, 1)), ((-1, 2, -1), (0, 1, -1), (0, 0, 0), (1, -1, 0), (1, -2, 1), (2, -3, 1)))
        self.assertEqual(hl.line_draw(HexCoords(0, -2, 2), self.obj_4), ((0, -2, 2), (0, -1, 1), (0, 0, 0), (1, 0, -1), (1, 1, -2)))
        # obj_a is Object --------------------------------------------------- #
        self.assertEqual(hl.line_draw(self.obj_5, (1, 1, -2)), ((-1, -1, 2), (0, -1, 1), (0, 0, 0), (0, 1, -1), (1, 1, -2)))
        self.assertEqual(hl.line_draw(self.obj_6, HexCoords(0, 2, -2)), ((2, -3, 1), (2, -2, 0), (1, -1, 0), (1, 0, -1), (0, 1, -1), (0, 2, -2)))
        self.assertEqual(hl.line_draw(self.obj_7, self.obj_3), ((-2, 1, 1), (-1, 1, 0), (0, 0, 0), (1, 0, -1), (2, 0, -2)))
        
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()
        self.obj_4.dispose()
        self.obj_5.dispose()
        self.obj_6.dispose()
        self.obj_7.dispose()


# TestDistLimFloodFill ------------------------------------------------------ #
class TestDistLimFloodFill(unittest.TestCase):
    """
    Test dependent on in_range function.
    """
    def setUp(self):
        # TypeError --------------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 0
        self.obj_0.r = 0
        self.obj_0.s = 0
        self.obj_0.block = False
        self.test_grp_0 = testgrp_generator((0, 0, 0), 1, ((1, -1, 0, {"q":"-1"} ), (-1, 1, 0, {"s":"0"} )))
        # AttributeError ---------------------------------------------------- #
        self.obj_1 = Mock()
        self.obj_1.q = 0
        self.obj_1.r = 0
        del self.obj_1.s
        self.obj_1.block = False
        self.test_grp_1 = testgrp_generator((0, 0, 0), 1, ((1, -1, 0, {"q":"del"} ), (-1, 1, 0, {"s":"del"} )))
        # ConstraintViolation ----------------------------------------------- #
        self.obj_2 = Mock()
        self.obj_2.q = 0
        self.obj_2.r = 0
        self.obj_2.s = -1
        self.obj_2.block = False
        self.test_grp_2 = testgrp_generator((0, 0, 0), 1, ((1, -1, 0, {"q":0} ), (-1, 1, 0, {"s":"1"} )))
        # test input expected output ---------------------------------------- #
        self.obj_3 = Mock()
        self.obj_3.q = 0
        self.obj_3.r = 0
        self.obj_3.s = 0
        self.obj_3.block = False
        self.test_grp_3 = testgrp_generator((0, 0, 0), 2, ((0, -1, 1, {"block":True} ), 
                                                          (1, -1, 0, {"block":True} ), 
                                                          (-1, 1, 0, {"block":True} ), 
                                                          (1, 1, -2, {"block":True} ) ))
        self.test_grp_4 = testgrp_generator((0, 0, 0), 2, ((2, 0, -2, {"block":True} ), 
                                                             (1, 1, -2, {"block":True} ), 
                                                             (0, 2, -2, {"block":True} ), 
                                                             (-1, 0, 1, {"block":True} ) ))
        
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.dist_lim_flood_fill(self.obj_3, 1, self.test_grp_0)
            hl.dist_lim_flood_fill(self.obj_0, 1, self.test_grp_3)
        
        with self.assertRaises(AttributeError):
            hl.dist_lim_flood_fill(self.obj_3, 1, self.test_grp_1)
            hl.dist_lim_flood_fill(self.obj_0, 1, self.test_grp_3)
        
        with self.assertRaises(ConstraintViolation):
            hl.dist_lim_flood_fill(self.obj_2, 1, self.test_grp_3)
            hl.dist_lim_flood_fill(self.obj_3, 1, self.test_grp_2)
    
    def test_inout(self):
        self.assertEqual(hl.dist_lim_flood_fill(self.obj_3, 2, self.test_grp_3, block_var="block"), 
                         {(-1, 0, 1), (1, 0, -1), (-1, -1, 2), (-2, 1, 1), (-1, 2, -1), (0, 0, 0), (2, 0, -2), (2, -1, -1), (0, 2, -2), (0, 1, -1), (-2, 0, 2)})
        self.assertEqual(hl.dist_lim_flood_fill(self.obj_3, 2, self.test_grp_4, block_var="block"), 
                         {(2, -2, 0), (1, 0, -1), (0, -1, 1), (-1, -1, 2), (-2, 1, 1), (-1, 2, -1), (0, 0, 0), (1, -2, 1), (-1, 1, 0), (2, -1, -1), (-2, 2, 0), (1, -1, 0), (0, 1, -1), (0, -2, 2)})
    
    def tearDown(self):
        self.obj_0.dispose()
        self.obj_1.dispose()
        self.obj_2.dispose()
        self.obj_3.dispose()
    
    
# TestBreadthFirstSearch ---------------------------------------------------- #
class TestBreadthFirstSearch(unittest.TestCase):
    """
    Test depends on GraphMatrix object.
    """
    def setUp(self):
        # AttributeError ---------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 0
        self.obj_0.r = 0
        del self.obj_0.s
        # test input expected output ---------------------------------------- #
        self.test_grp_3 = testgrp_generator((0, 0, 0), 5, ( (2, 0, -2, {"movement_cost":0} ), 
                                                          (1, 1, -2, {"movement_cost":0} ), 
                                                          (0, 2, -2, {"movement_cost":0} ), 
                                                          (-1, 3, -2, {"movement_cost":0} ),
                                                          (-2, 4, -2, {"movement_cost":0} ),
                                                          (-3, 5, -2, {"movement_cost":0} ),
                                                          (-4, 6, -2, {"movement_cost":0} ),
                                                          (-3, 1, 2, {"movement_cost":0} ),
                                                          (-2, 0, 2, {"movement_cost":0} ),
                                                          (-1, -1, 2, {"movement_cost":0} ),
                                                          (0, -2, 2, {"movement_cost":0} ),
                                                          (1, -3, 2, {"movement_cost":0} ),
                                                          (2, -4, 2, {"movement_cost":0} ),
                                                          (3, -5, 2, {"movement_cost":0} )
                                                          ))
        self.graph_matrix_3 = hl.GraphMatrix(self.test_grp_3)
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.breadth_first_search((0, 5, "-5"), (0, -5, 5), self.graph_matrix_3)
        
        with self.assertRaises(AttributeError):
            hl.breadth_first_search(self.obj_0, (0, -5, 5), self.graph_matrix_3)
        
        with self.assertRaises(ConstraintViolation):
            hl.breadth_first_search((1, 5, -5), (0, -5, 5), self.graph_matrix_3)
    
    def test_inout(self):
        self.assertEqual(hl.breadth_first_search((0, 5, -5), (0, -5, 5), self.graph_matrix_3), 
                         [(0, 5, -5), (1, 4, -5), (2, 3, -5), (3, 2, -5), (3, 1, -4), (3, 0, -3), 
                          (3, -1, -2), (2, -1, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-2, 1, 1), 
                          (-3, 2, 1), (-4, 2, 2), (-4, 1, 3), (-3, 0, 3), (-2, -1, 3), (-1, -2, 3), 
                          (0, -3, 3), (0, -4, 4), (0, -5, 5)])
    
    def tearDown(self):
        self.obj_0.dispose()
        del self.test_grp_3
        del self.graph_matrix_3
    
    
# TestDijekstrasAlgorithm --------------------------------------------------- #
class TestDijekstrasAlgorithm(unittest.TestCase):
    """
    Test depends on GraphMatrix object.
    """
    def setUp(self):
        # AttributeError ---------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 0
        self.obj_0.r = 0
        del self.obj_0.s
        # test input expected output ---------------------------------------- #
        self.test_grp_3 = testgrp_generator((0, 0, 0), 5, ( (2, 0, -2, {"movement_cost":0} ), 
                                                          (1, 1, -2, {"movement_cost":0} ), 
                                                          (0, 2, -2, {"movement_cost":0} ), 
                                                          (-1, 3, -2, {"movement_cost":0} ),
                                                          (-2, 4, -2, {"movement_cost":0} ),
                                                          (-3, 5, -2, {"movement_cost":0} ),
                                                          (-4, 6, -2, {"movement_cost":0} ),
                                                          (-3, 1, 2, {"movement_cost":0} ),
                                                          (-2, 0, 2, {"movement_cost":0} ),
                                                          (-1, -1, 2, {"movement_cost":0} ),
                                                          (0, -2, 2, {"movement_cost":0} ),
                                                          (1, -3, 2, {"movement_cost":0} ),
                                                          (2, -4, 2, {"movement_cost":0} ),
                                                          (3, -5, 2, {"movement_cost":0} )
                                                          ))
        self.graph_matrix_3 = hl.GraphMatrix(self.test_grp_3)
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.dijkstras_algorithm((0, 5, "-5"), (0, -5, 5), self.graph_matrix_3)
        
        with self.assertRaises(AttributeError):
            hl.dijkstras_algorithm(self.obj_0, (0, -5, 5), self.graph_matrix_3)
        
        with self.assertRaises(ConstraintViolation):
            hl.dijkstras_algorithm((1, 5, -5), (0, -5, 5), self.graph_matrix_3)
    
    def test_inout(self):
        self.assertEqual(hl.dijkstras_algorithm((0, 5, -5), (0, -5, 5), self.graph_matrix_3),
                         [(0, 5, -5), (1, 4, -5), (2, 3, -5), (3, 2, -5), (3, 1, -4), 
                          (3, 0, -3), (3, -1, -2), (2, -1, -1), (1, -1, 0), (0, -1, 1), 
                          (-1, 0, 1), (-2, 1, 1), (-3, 2, 1), (-4, 2, 2), (-4, 1, 3), 
                          (-3, 0, 3), (-2, -1, 3), (-1, -2, 3), (0, -3, 3), (0, -4, 4), 
                          (0, -5, 5)])
                         
    
    def tearDown(self):
        self.obj_0.dispose()
        del self.test_grp_3
        del self.graph_matrix_3
    
    
# TestAStarAlgorithm -------------------------------------------------------- #
class TestAStarAlgorithm(unittest.TestCase):
    """
    Test depends on GraphMatrix object.
    """
    def setUp(self):
        # AttributeError ---------------------------------------------------- #
        self.obj_0 = Mock()
        self.obj_0.q = 0
        self.obj_0.r = 0
        del self.obj_0.s
        # test input expected output ---------------------------------------- #
        self.test_grp_3 = testgrp_generator((0, 0, 0), 5, ( (2, 0, -2, {"movement_cost":0} ), 
                                                          (1, 1, -2, {"movement_cost":0} ), 
                                                          (0, 2, -2, {"movement_cost":0} ), 
                                                          (-1, 3, -2, {"movement_cost":0} ),
                                                          (-2, 4, -2, {"movement_cost":0} ),
                                                          (-3, 5, -2, {"movement_cost":0} ),
                                                          (-4, 6, -2, {"movement_cost":0} ),
                                                          (-3, 1, 2, {"movement_cost":0} ),
                                                          (-2, 0, 2, {"movement_cost":0} ),
                                                          (-1, -1, 2, {"movement_cost":0} ),
                                                          (0, -2, 2, {"movement_cost":0} ),
                                                          (1, -3, 2, {"movement_cost":0} ),
                                                          (2, -4, 2, {"movement_cost":0} ),
                                                          (3, -5, 2, {"movement_cost":0} )
                                                          ))
        self.graph_matrix_3 = hl.GraphMatrix(self.test_grp_3)
    
    def test_error(self):
        with self.assertRaises(TypeError):
            hl.a_star_algorithm((0, 5, "-5"), (0, -5, 5), self.graph_matrix_3)
        
        with self.assertRaises(AttributeError):
            hl.a_star_algorithm(self.obj_0, (0, -5, 5), self.graph_matrix_3)
        
        with self.assertRaises(ConstraintViolation):
            hl.a_star_algorithm((1, 5, -5), (0, -5, 5), self.graph_matrix_3)
    
    def test_inout(self):
        self.assertEqual(hl.a_star_algorithm((0, 5, -5), (0, -5, 5), self.graph_matrix_3),
                         [(0, 5, -5), (1, 4, -5), (2, 3, -5), (3, 2, -5), (3, 1, -4), 
                          (3, 0, -3), (3, -1, -2), (2, -1, -1), (1, -1, 0), (0, -1, 1), 
                          (-1, 0, 1), (-2, 1, 1), (-3, 2, 1), (-4, 2, 2), (-4, 1, 3), 
                          (-3, 0, 3), (-2, -1, 3), (-1, -2, 3), (0, -3, 3), (0, -4, 4), 
                          (0, -5, 5)])
    
    def tearDown(self):
        self.obj_0.dispose()
        del self.test_grp_3
        del self.graph_matrix_3
    

# run unittests ------------------------------------------------------------- #
unittest.main()

