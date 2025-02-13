from geopy.distance import geodesic


def calculate_distance(starion_lan, stadion_lot, user_lan, user_lon):
    stadion_coordinates = (starion_lan, stadion_lot)
    user_coordinates = (user_lan, user_lon)
    return geodesic(stadion_coordinates, user_coordinates).km
