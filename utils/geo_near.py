from geopy.distance import geodesic


def calculate_distance(stadion_lan, stadion_lot, user_lan, user_lon):
    stadion_coordinates = (stadion_lan, stadion_lot)
    user_coordinates = (user_lan, user_lon)
    return geodesic(stadion_coordinates, user_coordinates).km


# Example


# stadion_lan = 52.2296756
# stadion_lot = 21.0122287
# user_lan = 48.856614
# user_lon = 2.3522219
#
# distance_in_km = calculate_distance(stadion_lan, stadion_lot, user_lan, user_lon)
# print(f"Distance from Stadion to User: {distance_in_km} km")