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

import arcpy
import arcpy.da
import herringbone
import math
import numpy


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
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        param3 = arcpy.Parameter(
            displayName="Clip to extent",
            name="clip_extent",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")
        param3.value = True

        return [param0, param1, param2, param3]

    def execute(self, parameters, messages):
        grid_distance = parameters[1].value

        extent_features = parameters[0].valueAsText
        desc = arcpy.Describe(extent_features)
        spatial_ref = desc.spatialReference
        lower_left = (desc.extent.XMin - math.fmod(desc.extent.XMin, grid_distance),
                      desc.extent.YMin - math.fmod(desc.extent.YMin, grid_distance))
        upper_right = (desc.extent.XMax - math.fmod(desc.extent.XMax, grid_distance) + grid_distance,
                       desc.extent.YMax - math.fmod(desc.extent.YMax, grid_distance) + grid_distance)

        out_features = parameters[2].valueAsText
        clip_extents = parameters[3].value

        arcpy.AddMessage("Lower left corner: {}".format(lower_left))
        arcpy.AddMessage("Upper right corner: {}".format(upper_right))
        arcpy.AddMessage("Grid distance: {}".format(grid_distance))

        pattern = herringbone.Herringbone(lower_left=lower_left,
                                          upper_right=upper_right,
                                          distance=grid_distance)

        point_array = numpy.array(pattern.points(),
                                  numpy.dtype([
                                      ('x', numpy.float32),
                                      ('y', numpy.float32),
                                      ('x_grid', numpy.float32),
                                      ('y_grid', numpy.float32)
                                  ]))
        arcpy.da.NumPyArrayToFeatureClass(point_array, 'in_memory/all_points', ('x', 'y'),
                                          spatial_ref)

        if clip_extents:
            arcpy.AddMessage("Clipping features and saving to point feature class {}.".format(out_features))
            arcpy.Clip_analysis('in_memory/all_points', extent_features, out_features)
        else:
            arcpy.AddMessage("Saving output point feature class to {}.".format(out_features))
            arcpy.CopyFeatures_management('in_memory/all_points', out_features)

        arcpy.Delete_management('in_memory/all_points')
