from functools import reduce

from .zip_code_zones import ZIP_ZONES
from .state_zip_ranges import ZIP_CODE_RANGES_BY_STATE


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


STATE_ACRONYM_GROUPED_BY_ZIP = reduce(__group_region_by_zip_start, ZIP_ZONES, [None] * 10)
