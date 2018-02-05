from .scale import Scale

from typing import Dict, List, Union


Parameters = Dict[str, Union[str, int, float]]

class Configuration:
    def __init__(self):
        self.time_scale = None      # type: Scale
        self.space_scales = []      # type: List[Scale]
        self.parameters = {}        # type: Parameters


def merge_configuration(
        base_configuration: Configuration,
        overriding_configuration: Configuration
        ) -> Configuration:
    new_conf = Configuration()

    new_conf.time_scale = base_configuration.time_scale
    new_conf.space_scales = base_configuration.space_scales

    if overriding_configuration.time_scale:
        new_conf.time_scale = overriding_configuration.time_scale

    if overriding_configuration.space_scales:
        new_conf.space_scales = overriding_configuration.space_scales

    new_conf.parameters = _merge_parameters(
            base_configuration.parameters, overriding_configuration.parameters)

    return new_conf


def _merge_parameters(
        base_dict: Parameters,
        overriding_dict: Parameters
        ) -> Parameters:
    merged_dict = dict()

    for key in base_dict:
        merged_dict[key] = base_dict[key]

    for key in overriding_dict:
        merged_dict[key] = overriding_dict[key]

    return new_dict
