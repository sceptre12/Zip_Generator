
def triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


def smoothen_value(val):
    '''
    This takes in a float and adjusts the precision of this float val
    :param val:
    :return:
    '''
    import numpy as np
    return float(np.format_float_positional(val, precision=15))


# A function to check whether point P(x, y)
# lies inside the triangle formed by
# A(x1, y1), B(x2, y2) and C(x3, y3)
def is_point_inside_triangle(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = smoothen_value(triangle_area(x1, y1, x2, y2, x3, y3))

    # Calculate area of triangle PBC
    A1 = smoothen_value(triangle_area(x, y, x2, y2, x3, y3))

    # Calculate area of triangle PAC
    A2 = smoothen_value(triangle_area(x1, y1, x, y, x3, y3))

    # Calculate area of triangle PAB
    A3 = smoothen_value(triangle_area(x1, y1, x2, y2, x, y))

    # Check if sum of A1, A2 and A3
    # is same as A
    return A == (A1 + A2 + A3)


def is_point_wrapper(args):
    return is_point_inside_triangle(*args)


def get_simplicies(triangle_coordinates):
    from scipy.spatial import Delaunay
    return Delaunay(triangle_coordinates).simplices
