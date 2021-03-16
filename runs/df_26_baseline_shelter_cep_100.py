import os
import csv
import numpy as np
from random import *
from math import *
import operator
import pickle

# BASELINE VALUES FOR DF-26 INTERMEDIATE-RANGE BALLISTIC MISSILE ATTACK
# FROM TRANSPORTER ERECTOR LAUNCHERS (TELS) BASED ON MAINLAND CHINA
#
# CIRCULAR ERROR PROBABLE (CEP): 100 M
#
# UNITARY WARHEADS
# ASSURED KILL IF HIT WITHIN LETHAL RADIUS OF TARGET
#
# MISSILES SENT: 100, TO 120 PARKING SPOTS AT ANDERSON AFB
# MONTE CARLO ITERATIONS: 200

df_26_targets = []


parking_spots = os.path.expanduser(
    '/Users/stevenli/Desktop/Winter 2021/GOVT 85.12/Paper/gov90-monte-carlo-master/data/Baseline.csv')

with open(parking_spots) as csvDataFile:
    csvReader = csv.reader(csvDataFile, )
    for row in csvReader:

        split = row[0].split(",")
        lat = float(split[0])
        lon = float(split[1])
        df_26_targets.append([lat, lon])

# HELPER FUNCTIONS


def ft_to_m(feet):

    return feet / 3.2808


def lb_to_kg(lb):

    return lb / 2.2046226218


def lethal_radius_m(yield_kg):

    # yield in kg
    # radius in m

    m = ft_to_m(20)
    kg = lb_to_kg(1)

    lethal_radius = m * (yield_kg / kg)**(1. / 3.)
    return lethal_radius  # (m)


def area_of_circle_m(radius):

    return pi * (radius**2)

# RETURN THE COORDINATES OF A GIVEN POINT (RADIUS (m), THETA (degrees))
# RELATIVE TO THE ANOTHER POINT'S COORDINATES


def haversine_location(lat1, lon1, radius, theta):

    r_earth = 6372800

    dx = radius * cos(theta)
    dy = radius * sin(theta)

    lat2 = lat1 + (dy / r_earth) * (180 / 3.14)
    lon2 = lon1 + (dx / r_earth) * (180 / 3.14) / cos(lat1 * 3.14 / 180)

    return(lat2, lon2)

# CALCULATE THE DISTANCE (m) BETWEEN TWO COORDINATES


def haversine_distance(lat1, lon1, lat2, lon2):

    R = 6372.8 * 1000  # earth radius in meters

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))

    return R * c

# RAPIDLY DEPLOYABLE SHELTER DATA

df_26_dist_radius_ft = 450  # from Heginbotham
df_26_dist_radius_m = ft_to_m(df_26_dist_radius_ft)

# VARIABLE DF-26 IRBM DATA

df_26_sspk = 0.90
df_26_cep_m = 100
df_26_sent = 100
yield_kg = 1500

# df_26_sspk = [0.70, 0.90]  # assumption from Heginbotham
# df_26_cep_m = [30, 300]  # m
# df_26 payload = [1200,1800]


# MONTE CARLO SIMULATION

monte_carlo_iterations = 200

sigma = df_26_cep_m / 0.675  # getting normal distribution from CEP
mu = 0

df_26_leaker_iterations = {}

# FOR EACH NUMBER OF LEAKERS POSSIBLE ...

for df_26_leaker_n in range(0, df_26_sent+1):

    print(df_26_leaker_n)

    df_26_success = []  # list to record success value each iteration of simulation

    # RUN SIMULATION OF CJ-20 ALCMS TARGETING AIRCRAFT

    for monte_carlo_iteration in range(0, monte_carlo_iterations):

        shuffle(df_26_targets)  # ! leaked missiles have "random" targets

        df_26_n = 0  # current missile

        df_26_hit_locations = []  # locations of all missile hits

        # ITERATE OVER EACH MISSILE OF LEAKED MISSILES
        # TO DETERMINE WHERE EACH MISSILE LANDS

        while df_26_n < df_26_leaker_n:

            # DETERMINE RANDOM LOCATION OF MISSILE FROM NORMAL
            # DISTRIBUTION
            df_26_hit_radius = np.random.normal(mu, sigma, 1)[0]

            # DETERMINE ANGLE RANDOMLY
            df_26_hit_angle = randint(1, 360)

            # DETERMINE WHICH TARGET THE MISSILE IS SENT TO
            current_target = df_26_n % len(df_26_targets)

            # DETERMINE COORDINATES OF TARGET THE MISSILE IS SENT TO
            current_target_lat = df_26_targets[current_target][0]
            current_target_lon = df_26_targets[current_target][1]

            # DETERMINE MISSILE'S GEOGRAPHIC COORDINATES
            df_26_hit_location = haversine_location(
                current_target_lat,
                current_target_lon,
                df_26_hit_radius,
                df_26_hit_angle)

            # RECORD MISSILE'S GEOGRAPHIC COORDINATES
            df_26_hit_locations.append(df_26_hit_location)

            # MOVE ON TO NEXT MISSILE
            df_26_n += 1

        df_26_targets_hits = {}

        # ITERATE OVER CJ-20 TARGETS

        for df_26_target in df_26_targets:

            # DETERMINE CJ-20 TARGET COORDINATES

            df_26_target_loc_lat = df_26_target[0]
            df_26_target_loc_lon = df_26_target[1]

            # ITERATE OVER CJ-20 HIT LOCATIONS

            for df_26_hit_location in df_26_hit_locations:

                # DETERMINE CJ-20 HIT LOCATION'S COORDINATES

                df_26_hit_location_lat = df_26_hit_location[0]
                df_26_hit_location_lon = df_26_hit_location[1]

                # DETERMINE CJ-20 HIT LOCATION'S DISTANCE FROM CURRENT CJ-20
                # TARGET

                df_26_distance_from_df_26_target = haversine_distance(df_26_target_loc_lat,
                                                                      df_26_target_loc_lon,
                                                                      df_26_hit_location_lat,
                                                                      df_26_hit_location_lon
                                                                      )

                # DETERMINE WHETHER MISSILE HIT SUFFICIENTLY CLOSE TO TARGET
                # SUCH THAT THE DISTANCE BETWEEN THE MISSILE AND TARGET IS LESS
                # THAN THE RADIUS OF THE MISSILE'S SUBMUNITION FOOTPRINT RADIUS

                if (df_26_distance_from_df_26_target < lethal_radius_m(yield_kg)):

                    if df_26_target[0] in df_26_targets_hits:
                        df_26_targets_hits[df_26_target[0]] += 1

                    else:
                        df_26_targets_hits[df_26_target[0]] = 1

        df_26_kills = 0

        # CALCULATIONS FOR TARGETS HIT BY CJ-20
        for key, value in df_26_targets_hits.items():

            hits_n = value
            df_26_target_pk = 1 - ((1 - df_26_sspk)**hits_n)
            df_26_kills += df_26_target_pk

        df_26_success.append(df_26_kills)

    df_26_expected_value = sum(df_26_success) / float(len(df_26_success))

    df_26_leaker_iterations[df_26_leaker_n] = df_26_expected_value

pickle.dump(df_26_leaker_iterations, open("df_26_baseline_shelter_cep_100.p", "wb"))