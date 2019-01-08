from functools import reduce

from .zip_code_zones import ZIP_ZONES
from .state_zip_ranges import ZIP_CODE_RANGES_BY_STATE
from .state_info import StateAcronyms, StateName
from models.zip_objects import State


def __group_region_by_zip_start(accum, curr):
    index = ZIP_ZONES[curr]
    if accum[index] is None:
        accum[index] = []
    accum[index].append(curr);
    return accum


def get_state_zip_zone(state_acronym):
    if state_acronym in ZIP_ZONES:
        return ZIP_ZONES[state_acronym]


def get_state_zip_range(state_acronym):
    if state_acronym in ZIP_CODE_RANGES_BY_STATE.keys():
        return ZIP_CODE_RANGES_BY_STATE[state_acronym]


def generate_state_obj_list():
    state_name_list = list(StateName.__members__)
    state_acronym_list = list(StateAcronyms.__members__)
    state_list = {}

    for idx, val in enumerate(state_acronym_list):
        state_list[val] = State(state_name_list[idx],state_acronym_list[idx])
    return state_list


STATE_ACRONYM_GROUPED_BY_ZIP = reduce(__group_region_by_zip_start, ZIP_ZONES, [None] * 10)
