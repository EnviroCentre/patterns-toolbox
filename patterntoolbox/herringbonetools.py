# -*- coding: utf-8 -*-

# Copyright 2015 Florenz A. P. Hollebrandse
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
import math
import herringbone


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

        param4 = arcpy.Parameter(
            displayName="Sort order",
            name="sort_order",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4.filter.list = ["EAST_WEST", "NORTH_SOUTH"]
        param4.value = param4.filter.list[0]

        param5 = arcpy.Parameter(
            displayName="Sort shape",
            name="sort_shape",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param5.filter.list = ["S", "Z"]
        param5.value = param5.filter.list[0]

        param6 = arcpy.Parameter(
            displayName="Sort first point",
            name="sort_first",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param6.filter.list = ["SW", "NW", "NE", "SE"]
        param6.value = param6.filter.list[0]

        return [param0, param1, param2, param3, param4, param5, param6]

    def execute(self, parameters, messages):
        grid_distance = parameters[1].value

        extent_features = parameters[0].valueAsText
        desc = arcpy.Describe(extent_features)
        spatial_ref = desc.spatialReference
        lower_left = (math.ceil(desc.extent.XMin / grid_distance) * grid_distance,
                      math.ceil(desc.extent.YMin / grid_distance) * grid_distance)
        upper_right = (desc.extent.XMax, desc.extent.YMax)

        out_features = parameters[2].valueAsText
        clip_extents = parameters[3].value
        sort_order = parameters[4].valueAsText.upper()
        sort_shape = parameters[5].valueAsText.upper()
        sort_first = parameters[6].valueAsText.upper()

        arcpy.AddMessage("Lower left corner: {}".format(lower_left))
        arcpy.AddMessage("Upper right corner: {}".format(upper_right))
        arcpy.AddMessage("Grid distance: {}".format(grid_distance))

        # Create pattern
        pattern = herringbone.Herringbone(lower_left, upper_right, grid_distance)
        pattern.sort(sort_order, sort_shape, sort_first)

        # Convert to feature class
        # pattern.points also as m-values, but NumPyArrayToFeatureClass has a bug and can't create PointM features
        arcpy.da.NumPyArrayToFeatureClass(pattern.points[['x', 'y', 'm']], 'in_memory/all_points', ('x', 'y'), spatial_ref)

        # Clip if necessary
        if clip_extents:
            arcpy.AddMessage("Clipping features and saving to point feature class {}.".format(out_features))
            arcpy.Clip_analysis('in_memory/all_points', extent_features, 'in_memory/clipped_features')
            # Clip destroys sort order
            arcpy.Sort_management('in_memory/clipped_features', out_features, 'm')
            arcpy.Delete_management('in_memory/clipped_features')
        else:
            arcpy.AddMessage("Saving output point feature class to {}.".format(out_features))
            arcpy.CopyFeatures_management('in_memory/all_points', out_features)

        arcpy.Delete_management('in_memory/all_points')
