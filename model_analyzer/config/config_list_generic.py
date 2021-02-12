# Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .config_value import ConfigValue
from model_analyzer.constants import \
    MODEL_ANALYZER_SUCCESS, MODEL_ANALYZER_FAILURE

from copy import deepcopy


class ConfigListGeneric(ConfigValue):
    """
    A generic list.
    """

    def __init__(self,
                 type_,
                 preprocess=None,
                 required=False,
                 validator=None,
                 output_mapper=None):
        """
        Create a new list of numeric values.

        Parameters
        ----------
        type_ : ConfigValue
            The type of elements in the list
        preprocess : callable
            Function be called before setting new values.
        required : bool
            Whether a given config is required or not.
        validator : callable or None
            A validator for the final value of the field.
        output_mapper: callable
            This callable unifies the output value of this field.
        """

        # default validator
        if validator is None:

            def validator(x):
                return type(x) is list and len(x) > 0

        super().__init__(preprocess, required, validator, output_mapper)

        self._type = type_
        self._cli_type = str
        self._value = []
        self._output_mapper = output_mapper

    def set_value(self, value):
        """
        Set the value for this field.

        Parameters
        ----------
        value : object
            The value for this field.
        """

        type_ = self._type

        new_value = []
        if type(value) is list:
            for item in value:
                list_item = deepcopy(type_)
                status = list_item.set_value(item)
                if status == MODEL_ANALYZER_SUCCESS:
                    new_value.append(list_item)
                else:
                    return MODEL_ANALYZER_FAILURE
        else:
            return MODEL_ANALYZER_FAILURE

        return super().set_value(new_value)