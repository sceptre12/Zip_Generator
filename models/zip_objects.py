from app.configs.constants.generator_functions import get_state_zip_zone, get_state_zip_range
from config.user_config import ZIP_CODE_WEBSITE


class JsonFormatter:
    def __init__(self):
        self.json_format = {}

    def set_json(self):
        self.json_format = {**self.__dict__}

    def get_json(self):
        self.set_json()
        return self.json_format


class Coordinates(JsonFormatter):
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long


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
    def __init__(self, zip_code, link, state, zip_type, city, county):
        self.zip_code = zip_code
        self.link = ZIP_CODE_WEBSITE + link
        self.state = state
        self.city = city
        self.county = county
        self.zip_type = zip_type
        self.bordering_zips = []
        self.coordinates = None
        self.population = None
        self.area = None

    def add_coords(self, lat, long):
        self.coordinates = Coordinates(lat, long)

    def add_population(self, population, pop_density):
        self.population = Population(population, pop_density)

    def add_area(self, land_area, water_area, radius_coverage):
        self.area = Area(land_area, water_area, radius_coverage)

    def add_bordering_zips(self, zip_code):
        self.bordering_zips.append(zip_code)

    def __str__(self): return self.zip_code

    def __repr__(self): return self.__str__()

    def get_json(self):
        self.json_format = super(ZipCode, self).get_json()
        self.json_format['coordinates'] = self.coordinates.get_json() if self.coordinates is not None else None
        self.json_format['population'] = self.population.get_json() if self.population is not None else None
        self.json_format['area'] = self.area.get_json() if self.area is not None else None
        return self.json_format


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
