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


class TestHerringBone(unittest.TestCase):
    def test_empty_herringbone(self):
        hb = Herringbone((0, 0), (0, 0), 1)
        self.assertEqual(hb.points(), [])

    def test_single_unit_herringbone(self):
        hb = Herringbone((0, 0), (1.25, 1.25), 1)
        expected_points = [(0.25, 0,    0, 0),
                           (1.25, 0.25, 1, 0),
                           (0,    1.00, 0, 1),
                           (1,    1.25, 1, 1)]
        self.assertEqual(hb.points(), expected_points)

    def test_two_unit_herringbone(self):
        hb = Herringbone((0, 0), (3.25, 1.25), 1)
        expected_points = [(0.25, 0.00, 0, 0),
                           (2.25, 0.00, 2, 0),
                           (1.25, 0.25, 1, 0),
                           (3.25, 0.25, 3, 0),
                           (0.00, 1.00, 0, 1),
                           (2.00, 1.00, 2, 1),
                           (1.00, 1.25, 1, 1),
                           (3.00, 1.25, 3, 1)]
        self.assertEqual(hb.points(), expected_points)

    def test_four_unit_herringbone(self):
        hb = Herringbone((0, 0), (3.25, 3.25), 1)
        expected_points = [(0.25, 0.00, 0, 0),
                           (2.25, 0.00, 2, 0),
                           (1.25, 0.25, 1, 0),
                           (3.25, 0.25, 3, 0),
                           (0.00, 1.00, 0, 1),
                           (2.00, 1.00, 2, 1),
                           (1.00, 1.25, 1, 1),
                           (3.00, 1.25, 3, 1),

                           (0.25, 2.00, 0, 2),
                           (2.25, 2.00, 2, 2),
                           (1.25, 2.25, 1, 2),
                           (3.25, 2.25, 3, 2),
                           (0.00, 3.00, 0, 3),
                           (2.00, 3.00, 2, 3),
                           (1.00, 3.25, 1, 3),
                           (3.00, 3.25, 3, 3)]
        self.assertEqual(hb.points(), expected_points)

    def test_single_square_herringbone(self):
        hb = Herringbone((0, 0), (1, 1), 1)
        expected_points = [(0.25, 0, 0, 0),
                           (0.00, 1, 0, 1)]
        self.assertEqual(hb.points(), expected_points)