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
import os.path


class PointsToRoute(object):
    def __init__(self):
        self.label = "Points to route"
        self.description = "Create a route (polyline) from a pattern of points"
        self.canRunInBackground = True

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="Points",
            name="point_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param0.filter.list = ["Point"]

        param1 = arcpy.Parameter(
            displayName="Output features",
            name="out_features",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        return [param0, param1]

    def execute(self, parameters, messages):
        point_features = parameters[0].valueAsText
        desc = arcpy.Describe(point_features)
        spatial_ref = desc.spatialReference
        out_features = parameters[1].valueAsText

        points = arcpy.da.FeatureClassToNumPyArray(point_features, ('SHAPE@X', 'SHAPE@Y'))

        arcpy.CreateFeatureclass_management(*os.path.split(out_features), geometry_type="POLYLINE",
                                            spatial_reference=spatial_ref)

        cursor = arcpy.da.InsertCursor(out_features, ["SHAPE@"])
        polyline = arcpy.Polyline(arcpy.Array([arcpy.Point(*row) for row in points]))

        cursor.insertRow([polyline])
