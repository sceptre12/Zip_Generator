from config.constants.generator_functions import get_state_zip_zone, get_state_zip_range
from config.user_config import ZIP_CODE_WEBSITE

from .base_model import JsonFormatter


class Area(JsonFormatter):
    def __init__(self, land_area, water_area, radius_coverage):
        self.land_area = land_area
        self.water_area = water_area
        self.radius_coverage = radius_coverage


class Population(JsonFormatter):
    def __init__(self, population, pop_density):
        self.population = population
        self.pop_density = pop_density


class State:
    def __init__(self,state_name,state_acronym):
        self.state_name = state_name
        self.state_acronym = state_acronym

    def __str__(self):
        return self.state_name + " " + self.state_acronym

    def __repr__(self):
        return self.__str__()


class ZipCode(JsonFormatter):
    def __init__(self, zip_code=None, link=None, state=None, zip_type=None, city=None, county=None):
        self.zip_code = zip_code
        self.link = ZIP_CODE_WEBSITE + link if link is not None else None
        self.state = state
        self.city = city
        self.county = county
        self.zip_type = zip_type
        self.bordering_zips = []

    def __str__(self): return self.zip_code

    def __repr__(self): return self.__str__()

    def get_json(self):
        return super(ZipCode, self).get_json()


class StateInfo:
    def __init__(self, state):
        self.state = state
        self.zip_codes = []
        self.zip_zone = get_state_zip_zone(self.state.state_acronym)
        self.zip_ranges = get_state_zip_range(self.state.state_acronym)

    def add_zip(self, zip_code):
        self.zip_codes.append(zip_code)

    def get_json_zips(self):
        return map(lambda zip_c: zip_c.get_json(), self.zip_codes)
