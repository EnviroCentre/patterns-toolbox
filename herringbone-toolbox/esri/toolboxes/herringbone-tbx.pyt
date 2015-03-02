# -*- coding: utf-8 -*-

# Copyright 2015 EnviroCentre
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import arcpy
import herringbone


class Toolbox(object):
    def __init__(self):
        self.label = "Herringbone"
        self.alias = "Herringbone"
        self.tools = [CreateHerringboneTool]


class CreateHerringboneTool(object):
    def __init__(self):
        self.label = "Create herringbone"
        self.description = "Creates a herringbone grid pattern"
        self.canRunInBackground = True

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="Extent",
            name="extent_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param0.filter.list = ["Polygon"]

        param1 = arcpy.Parameter(
            displayName="Grid distance",
            name="grid_distance",
            datatype="Double",
            parameterType="Required",
            direction="Input")
        param1.filter.type = "Range"
        param1.filter.list = [0.001, 9e10]

        param2 = arcpy.Parameter(
            displayName="Output features",
            name="out_features",
            datatype="GPFeatureLayer",
            parameterType="Derived",
            direction="Output")

        return [param0, param1, param2]

    def execute(self, parameters, messages):
        bounds = parameters[0].value.hullRectangle.split(' ')
        grid_distance = parameters[1].value
        out_features = parameters[2].valueAsText

        arcpy.addMessage("Creating herringbone pattern.")
        arcpy.addMessage("Lower left corner: {}".format(bounds[:2]))
        arcpy.addMessage("Upper right corner: {}".format(bounds[2:]))
        arcpy.addMessage("Grid distance: {}".format(grid_distance))

        pattern = herringbone.Herringbone(lower_left=bounds[:2],
                                          upper_right=bounds[2:],
                                          distance=grid_distance)

        pointGeoms = [arcpy.PointGeometry(arcpy.Point(point[0],
                                                      point[1]))
                      for point in pattern.points()]

        arcpy.addMessage("Saving output point feature class to {}".format(out_features))
        arcpy.CopyFeatures_management(pointGeoms, out_features)
