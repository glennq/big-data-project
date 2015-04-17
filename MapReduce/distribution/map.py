#!/usr/bin/python
import sys
from geopy.geocoders import Nominatim
import random
from sets import Set
regions = Set(["Marble Hill", "Inwood", "Fort George", "Hudson Heights", "West Harlem", "Hamilton Heights", "Manhattanville", "Morningside Heights", "Central Harlem", "Harlem", "Strivers' Row", "Astor Row", "Sugar Hill", "Marcus Garvey Park", "Mount Morris Historical District", "Le Petit Senegal", "East Harlem", "Silk Stocking District", "Lenox Hill", "Carnegie Hill", "Yorkville", "Upper West Side", "Upper East Side", "Manhattan Valley", "Bloomingdale District", "Lincoln Square", "Columbus Circle", "Sutton Place", "Rockefeller Center", "Diamond District", "Theater District", "Turtle Bay", "Midtown East", "Midtown", "Tudor City", "Little Brazil", "Times Square", "Hudson Yards", "Midtown West", "Hell's Kitchen","San Juan Hill", "Clinton", "Garment District", "Koreatown", "Murray Hill", "Tenderloin", "Madison Square", "Flower District", "Brookdale", "Hudson Yards", "Kips Bay", "Rose Hill", "NoMad", "Peter Cooper Village", "Chelsea", "Flatiron District", "Toy District", "Photo District", "Gramercy Park", "Stuyvesant Square", "Union Square", "Stuyvesant Town", "Little Germany", "Alphabet City and Littleoisaida", "East Village", "Greenwich Village", "NoHo", "Bowery", "West Village", "Lower East Side", "SoHo", "Nolita", "Little Italy", "Chinatown", "Financial District", "Five Points", "Cooperative Village", "Two Bridges", "Tribeca", "Civic Center", "Radio Row", "South Street Seaport Historical District", "Battery Park City", "Meatpacking District", "Waterside Plaza", "Astoria", "Corona", "East Elmhurst", "Elmhurst", "Forest Hills", "Fresh Pond", "Glendale", "Hunters Point", "Jackson Heights", "Long Island City", "Maspeth", "Middle Village", "Rego Park", "Ridgewood", "Sunnyside", "Woodside", "Bayside", "Bellerose", "College Point", "Douglaston", "Flushing", "Pomonok", "Floral Park", "Fresh Meadows", "Fort Totten", "Glen Oaks", "Kew Gardens Hills", "Kew Gardens", "Little Neck", "Whitestone", "The Hole", "Howard Beach", "Ozone Park", "Richmond Hill", "Woodhaven", "Southeastern Queens[edit]", "Bellaire", "Briarwood", "Brookville", "Cambria Heights", "Hollis Hills", "Hollis", "Holliswood", "Jamaica", "Jamaica Estates", "Jamaica Hills", "Laurelton", "Meadowmere", "Queens Village", "Rochdale Village", "Rosedale", "Saint Albans", "South Jamaica", "Springfield Gardens", "Warnerville", "Arverne", "Bayswater", "Belle Harbor", "Breezy Point", "Broad Channel", "Edgemere", "Far Rockaway", "Hammels", "Neponsit", "Rockaway Beach", "Rockaway Park", "Roxbury", "Seaside", "Bedford-Stuyvesant", "Boerum Hill", "Carroll Gardens", "Cobble Hill", "Brooklyn Heights", "Brownsville", "City Line", "Clinton Hill", "Crown Heights", "Cypress Hills", "Downtown Brooklyn", "DUMBO", "East New York", "Fort Greene", "Gowanus", "Greenwood Heights", "Highland Park", "New Lots", "Ocean Hill", "Park Slope", "Prospect Heights", "RAMBO", "Spring Creek", "Starrett City", "Stuyvesant Heights", "Sunset Park", "Vinegar Hill", "Weeksville", "Windsor Terrace", "Wingate", "Bergen Beach", "Canarsie", "Flatlands", "Georgetown", "Marine Park", "Mill Basin", "Brighton Beach", "Coney Island", "Gerritsen Beach", "Gravesend", "Homecrest", "Madison", "Manhattan Beach", "Plum Beach", "Seagate", "Sheepshead Bay", "Bay Ridge", "Borough Park", "Dyker Heights", "New Utrecht", "Ditmas Park", "East Flatbush", "Farragut", "Fiske Terrace", "Flatbush", "Kensington", "Prospect Lefferts Gardens", "Prospect Park South", "Bedford Park", "Belmont", "Fordham", "Kingsbridge", "Marble Hill", "Norwood", "Riverdale", "University Heights", "Woodlawn", "Downtown Bronx", "East Tremont", "Highbridge", "Hunts Point", "Longwood", "Melrose", "Morris Heights", "Morrisania", "Mott Haven", "The Hub", "Tremont", "West Farms", "Allerton", "Baychester", "Bronxdale", "City Island", "Co-op City", "Eastchester", "Edenwald", "Indian Village", "Laconia", "Olinville", "Morris Park", "Pelham Gardens", "Pelham Parkway", "Van Nest", "Wakefield", "Williamsbridge", "Bruckner", "Castle Hill", "Clason Point", "Country Club", "Edgewater Park", "Harding Park", "Parkchester", "Park Versailles", "Westchester Heights", "Pelham Bay", "Soundview", "Schuylerville", "Throggs Neck", "Unionport", "Westchester Square"])

def changeLongitudeLatitudeToAddress(longitude, latitude, recursionTimes):
    '''chaneg longitude and latitude of a place to its address'''

    if recursionTimes > 4:
        return 

    geolocator = Nominatim()
    address_str = str(latitude) + ", " + str(longitude)
    location = geolocator.reverse(address_str)
    address = location.address.split(",")
    address = map(deleteWhiteSpace, address)
    for item in address:
        if item in regions:
            return item
    
    n = random.randint(1, 4)
    
    if n == 1:
        return changeLongitudeLatitudeToAddress(longitude + 0.1, latitude, recursionTimes + 1)
    elif n == 2:
        return changeLongitudeLatitudeToAddress(longitude - 0.1, latitude, recursionTimes + 1)
    elif n == 3:
        return changeLongitudeLatitudeToAddress(longitude, latitude + 0.1, recursionTimes + 1)
    elif n == 4:
        return changeLongitudeLatitudeToAddress(longitude, latitude - 0.1, recursionTimes + 1)


def deleteWhiteSpace(str):
    """docstring for deleteWhiteSpace"""
    return str.strip()


for line in sys.stdin:
    line = line.strip()
    unpack = line.split(",")
    if len(unpack[0]) == 9:
        continue
    try:
        medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag, pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude = unpack

        pick_year, pick_time = pickup_datetime.split()
        pick_y, pick_m, pick_d = pick_year.split("-")
        pick_h = pick_time.split(":")[0]

        drop_year, drop_time = dropoff_datetime.split()
        drop_y, drop_m, drop_d = drop_year.split("-")
        drop_h = drop_time.split(":")[0]

        pickupRegion = " "
        dropoffRegion = " "
        
        pickupRegion = changeLongitudeLatitudeToAddress(float(pickup_longitude), float(pickup_latitude), 0)
        #dropoffRegion = changeLongitudeLatitudeToAddress(float(dropoff_longitude), float(dropoff_latitude), 0)

        if pickupRegion is not None:
            print pickupRegion + "," + pick_y + "," + pick_m + "," + pick_d + "," + pick_h + "\t" + pickup_longitude + "\t" + pickup_latitude
        # if dropoffRegion is not None:
        #     print dropoffRegion + "\t" + drop_y + "," + drop_m + "\t" + drop_d + "\t" + drop_h + "\t" + dropoff_longitude + "\t" + dropoff_latitude
    except:
        pass
