import itertools
from .base_model import JsonFormatter
from utility.util import is_point_inside_triangle


class Communities(JsonFormatter):
    def __init__(self,zip_code,zip_coords):
        from scipy.spatial import Delaunay
        self.tri = Delaunay(zip_coords)
        self.communities = [Community(zip_code,zip_coords,simplices,index) for index, simplices in enumerate(self.tri.simplices)]

    def get_json(self):
        return [community.get_json() for community in self.communities]


class Community(JsonFormatter):
    def __init__(self,zip_code,zip_coords, simplices,index):
        self.zip_code = zip_code
        self.simplicy_index = index
        self.simplicy = simplices
        self.boundary_coordinates = list(map(lambda idx: zip_coords[idx],simplices))
        self.neighboring_communities = []
        self.users = []

    def is_point_valid(self,point):
        '''
        Returns true or false depending on if the point is inside of the triangle
        :param point:
        :return:
        '''
        return is_point_inside_triangle(list(map(lambda x: abs(x), list(itertools.chain(self.boundary_coordinates,point)))))


class ZipCodes(JsonFormatter):
    def __init__(self,zip_code,state,state_abrv,city,county):
        self.zip_code = zip_code
        self.state = state
        self.state_abrv = state_abrv
        self.city = city
        self.county = county
        self.bordering_zips = []
