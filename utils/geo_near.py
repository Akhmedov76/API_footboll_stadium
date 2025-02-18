from geopy.distance import geodesic


def calculate_distance(stadion_lan, stadion_lot, user_lan, user_lon):
    stadion_coordinates = (stadion_lan, stadion_lot)
    user_coordinates = (user_lan, user_lon)
    return geodesic(stadion_coordinates, user_coordinates).km
