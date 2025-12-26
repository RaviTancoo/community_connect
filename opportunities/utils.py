from geopy.geocoders import Nominatim

def geocode_location(location_name):
    """
    Convert a location string into latitude and longitude using Nominatim.
    """
    geolocator = Nominatim(user_agent="community_connect")
    loc = geolocator.geocode(location_name)
    if loc:
        return loc.latitude, loc.longitude
    return None, None
