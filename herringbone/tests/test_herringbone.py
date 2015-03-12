# Copyright 2014 Florenz A.P. Hollebrandse
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from herringbone import Herringbone
import numpy.testing as nt
import numpy as np


class TestHerringBone(unittest.TestCase):
    dtype = [('x', '<f4'), ('y', '<f4'), ('x_grid', '<i4'), ('y_grid', '<i4'), ('m', '<i4')]

    def test_empty_herringbone(self):
        hb = Herringbone((0, 0), (0, 0), 1)
        nt.assert_array_equal(hb.points, np.array([], dtype=self.dtype))

    def test_row_count(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        self.assertEqual(hb.row_count(), 2)

    def test_row_count_2(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 2)
        self.assertEqual(hb.row_count(), 1)

    def test_column_count(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        self.assertEqual(hb.column_count(), 2)

    def test_column_count_2(self):
        hb = Herringbone((0, 0), (2.5, 2.5), 2)
        self.assertEqual(hb.column_count(), 2)

    def test_single_unit_herringbone(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (1.25, 0.25, 1, 0, 0),
                                    (0, 1.00, 0, 1, 0),
                                    (1, 1.25, 1, 1, 0)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_two_unit_herringbone(self):
        hb = Herringbone((0, 0), (3.25, 1.25), 1)
        expected_points = np.array([(0.25, 0.00, 0, 0, 0),
                                    (2.25, 0.00, 2, 0, 0),
                                    (1.25, 0.25, 1, 0, 0),
                                    (3.25, 0.25, 3, 0, 0),
                                    (0.00, 1.00, 0, 1, 0),
                                    (2.00, 1.00, 2, 1, 0),
                                    (1.00, 1.25, 1, 1, 0),
                                    (3.00, 1.25, 3, 1, 0)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_four_unit_herringbone(self):
        hb = Herringbone((0, 0), (3.25, 3.25), 1)
        expected_points = np.array([(0.25, 0.00, 0, 0, 0),
                                    (2.25, 0.00, 2, 0, 0),
                                    (1.25, 0.25, 1, 0, 0),
                                    (3.25, 0.25, 3, 0, 0),
                                    (0.00, 1.00, 0, 1, 0),
                                    (2.00, 1.00, 2, 1, 0),
                                    (1.00, 1.25, 1, 1, 0),
                                    (3.00, 1.25, 3, 1, 0),

                                    (0.25, 2.00, 0, 2, 0),
                                    (2.25, 2.00, 2, 2, 0),
                                    (1.25, 2.25, 1, 2, 0),
                                    (3.25, 2.25, 3, 2, 0),
                                    (0.00, 3.00, 0, 3, 0),
                                    (2.00, 3.00, 2, 3, 0),
                                    (1.00, 3.25, 1, 3, 0),
                                    (3.00, 3.25, 3, 3, 0)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_single_square_herringbone(self):
        hb = Herringbone((0, 0), (1, 1), 1)
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (0.00, 1, 0, 1, 0)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_east_west(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_order='EAST_WEST')
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (1.25, 0.25, 1, 0, 1),
                                    (0, 1.00, 0, 1, 2),
                                    (1, 1.25, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_north_south(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_order='NORTH_SOUTH')
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (0, 1.00, 0, 1, 1),
                                    (1.25, 0.25, 1, 0, 2),
                                    (1, 1.25, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_z_shape(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_shape='Z')
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (1.25, 0.25, 1, 0, 1),
                                    (0, 1.00, 0, 1, 2),
                                    (1, 1.25, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_s_shape(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_shape='S')
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (1.25, 0.25, 1, 0, 1),
                                    (1, 1.25, -1, 1, 2),
                                    (0, 1.00, 0, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_s_shape_north_south(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_shape='S', sort_order='NORTH_SOUTH')
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (0, 1.00, 0, 1, 1),
                                    (1, 1.25, 1, -1, 2),
                                    (1.25, 0.25, 1, 0, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_first_sw(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_first='SW')
        expected_points = np.array([(0.25, 0, 0, 0, 0),
                                    (1.25, 0.25, 1, 0, 1),
                                    (0, 1.00, 0, 1, 2),
                                    (1, 1.25, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_first_se(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_first='SE')
        expected_points = np.array([(1.25, 0.25, 0, 0, 0),
                                    (0.25, 0, 1, 0, 1),
                                    (1, 1.25, 0, 1, 2),
                                    (0, 1.00, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_first_nw(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_first='NW')
        expected_points = np.array([(0, 1.00, 0, 0, 0),
                                    (1, 1.25, 1, 0, 1),
                                    (0.25, 0, 0, 1, 2),
                                    (1.25, 0.25, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_first_ne(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_first='NE')
        expected_points = np.array([(1, 1.25, 0, 0, 0),
                                    (0, 1.00, 1, 0, 1),
                                    (1.25, 0.25, 0, 1, 2),
                                    (0.25, 0, 1, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_first_nw_s_shape(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_first='NW', sort_shape='S')
        expected_points = np.array([(0, 1.00, 0, 0, 0),
                                    (1, 1.25, 1, 0, 1),
                                    (1.25, 0.25, -1, 1, 2),
                                    (0.25, 0, 0, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)

    def test_sort_first_ne_s_shape(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        hb.sort(sort_first='NE', sort_shape='S')
        expected_points = np.array([(1, 1.25, 0, 0, 0),
                                    (0, 1, 1, 0, 1),
                                    (0.25, 0, -1, 1, 2),
                                    (1.25, 0.25, 0, 1, 3)],
                                   dtype=self.dtype)
        nt.assert_array_equal(hb.points, expected_points)
