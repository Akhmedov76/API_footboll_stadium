from scipy.spatial import distance
from math import sin, cos, sqrt, atan2, radians


def get_distance(point1, point2):
    R = 6371
    lat1 = radians(point1[0])
    lon1 = radians(point1[1])
    lat2 = radians(point2[0])
    lon2 = radians(point2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Example
# point1 = (52.2296756, 21.0122287)
# point2 = (48.856614, 2.3522219)
#
# distance_in_km = get_distance(point1, point2)
# print(f"Distance  {point1} and {point2}  {distance_in_km} km")
