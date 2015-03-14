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


class AddLabelsTool(object):
    def __init__(self):
        self.label = "Add labels"
        self.description = "Add a field with incremental point labels"
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
            displayName="Label prefix",
            name="prefix",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        return [param0, param1]

    def execute(self, parameters, messages):
        point_features = parameters[0].valueAsText
        prefix = parameters[1].valueAsText
        if not prefix:
            prefix = ''
        field_name = "label"

        feature_count = int(arcpy.GetCount_management(point_features).getOutput(0))
        digits = int(math.floor(math.log(feature_count, 10))) + 1
        expression = '"' + prefix + '{:0' + str(digits) + 'd}".format(index())'
        code_block = \
"""i = 0

def index():
    global i
    i += 1
    return i
"""

        arcpy.AddField_management(point_features, field_name, "TEXT", field_length=12)
        arcpy.CalculateField_management(point_features, field_name, expression, "PYTHON_9.3", code_block)

