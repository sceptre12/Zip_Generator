from config.constants.generator_functions import get_state_zip_zone, get_state_zip_range
from config.user_config import ZIP_CODE_WEBSITE
from util import is_point_inside_triangle, get_simplicies
import itertools


class JsonFormatter:
    def __init__(self):
        self.json_format = {}

    def set_json(self):
        self.json_format = {**self.__dict__}

    def get_json(self):
        self.set_json()
        return self.json_format


class Community(JsonFormatter):
    def __init__(self,zip_code,simplex_indices):
        self.zip_code = zip_code  # secondary key
        self.simplex_indices = simplex_indices  # Indices for the Boundaries for the Community
        self.neighbors = []  # List of neighboring communities id's
        self.community_boundaries = []

    def is_point_valid(self,point):
        '''
        Returns true or false depending on if the point is inside of the triangle
        :param point:
        :return:
        '''
        return is_point_inside_triangle(list(map(lambda x: abs(x), list(itertools.chain(self.simplex,point)))))

    # def


class Coordinate(JsonFormatter):
    def __init__(self,zip_code,zip_coordinates,zip_bounds,neighboring_zips):
        self.zip_code = zip_code
        self.zip_coordinates = zip_coordinates
        self.zip_bounds = zip_bounds
        self.neighboring_zips = neighboring_zips
        self.communities = self.create_communities(zip_coordinates)

    def create_community(self,simplicity):
        return Community(self.zip_code,simplicity)

    def create_communities(self,zip_coordinates):
        return list(map(self.create_community,get_simplicies(zip_coordinates)))

    def generate_community_neighbors(self):
        for community in self.communities:
            community




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
        self.coordinates = None
        self.population = None
        self.area = None

    def add_coords(self, coordinate_id):
        self.coordinates = coordinate_id

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
        self.json_format['coordinates'] = self.coordinate if self.coordinate is not None else None
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
