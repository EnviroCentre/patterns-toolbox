# -*- coding: utf-8 -*-

# Copyright 2015 EnviroCentre
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

import math
import numpy as np


class Herringbone(object):
    """
    A herringbone pattern.

    :param tuple lower_left: lower left coordinate of area to create herringbone pattern
    :param tuple upper_right: upper right coordinate of area to create herringbone pattern
    :param float distance: grid square distance
    """

    def __init__(self, lower_left, upper_right, distance):
        """
        Create a herringbone pattern

        :param tuple lower_left: lower left coordinate of area to create herringbone pattern
        :param tupe upper_right: upper right coordinate of area to create herringbone pattern
        :param float distance: grid square distance
        :return: herringbone pattern
        :rtype: :class:`Herringbone`
        """
        self.lower_left = lower_left
        self.upper_right = upper_right
        self.distance = distance
        self.points = self._points_array()

    def row_count(self):
        return int(math.floor(self.upper_right[1] - self.lower_left[1] / self.distance)) + 1

    def column_count(self):
        return int(math.floor(self.upper_right[0] - self.lower_left[0] / self.distance)) + 1

    def _points(self):
        result = []

        # Steps to increase y-coordinate
        delta_y = [0.25, 0.75, 0.25, 0.75]
        # Value indicating row index: 0, 1, 2, 3
        y_index = 0
        # For each row, start x-coordinate at distance, depending on y-index
        x_offset = [0.25, 1.25, 0, 1]

        # Start first row
        y = self.lower_left[1]
        y_grid = 0

        while y <= self.upper_right[1]:
            # First x-coordinate in row
            x_grid = round(x_offset[y_index])
            x = self.lower_left[0] + x_offset[y_index] * self.distance

            while x <= self.upper_right[0]:
                # Append point coordinates to list
                result.append((x, y, x_grid, y_grid))
                # Increase x-coordinate
                x_grid += 2
                x += 2 * self.distance

            # Increase y-coordinate
            y_grid += round(delta_y[y_index])  # Only increase y if delta_y == 0.75
            y += delta_y[y_index] * self.distance
            # Increase y-index cyclicly
            y_index = (y_index + 1) % 4

        return result

    def _points_array(self):
        return np.array(self._points(),
                        np.dtype([
                            ('x', np.float32),
                            ('y', np.float32),
                            ('x_grid', np.int32),
                            ('y_grid', np.int32)
                        ]))

    def sort(self, sort_order='EAST_WEST', sort_shape='Z', sort_first='SW'):
        # principal sort axis
        order = {
            'EAST_WEST': ['y_grid', 'x_grid'],
            'NORTH_SOUTH': ['x_grid', 'y_grid']
        }

        # starting corner
        if sort_first[0] == 'N':
            self.points['y_grid'] *= -1
            self.points['y_grid'] += self.row_count() - 1
        if sort_first[1] == 'E':
            self.points['x_grid'] *= -1
            self.points['x_grid'] += self.column_count() - 1

        # sort shape
        if sort_shape == 'S':
            # x_grid values, every other y_grid, multiply by -1 (and vice verse for NORTH_SOUTH)
            # points['x_grid'][np.fmod(points['y_grid'], 2) == 1]
            self.points[order[sort_order][1]][np.fmod(self.points[order[sort_order][0]], 2) == 1] *= -1

        # actual sorting
        ordered_indices = np.argsort(self.points, order=order[sort_order])
        self.points = self.points[ordered_indices]
