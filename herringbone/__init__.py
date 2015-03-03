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

    def points(self):
        """
        Return a list of herringbone pattern points.

        :return: list of points as `(x, y)` tuples.
        :rtype: list
        """
        result = []

        # Steps to increase y-coordinate
        delta_y = [0.25, 0.75, 0.25, 0.75]
        # Value indicating row index: 0, 1, 2, 3
        y_index = 0
        # For each row, start x-coordinate at distance, depending on y-index
        x_offset = [0.25, 1.25, 0, 1]

        # Start first row
        y = self.lower_left[1]
        while y <= self.upper_right[1]:
            # First x-coordinate in row
            x = x_offset[y_index] * self.distance + self.lower_left[0]

            while x <= self.upper_right[0]:
                # Append point coordinates to list
                result.append((x, y))
                # Increase x-coordinate
                x += 2 * self.distance

            # Increase y-coordinate
            y += delta_y[y_index] * self.distance
            # Increase y-index cyclicly
            y_index = (y_index + 1) % 4

        return result