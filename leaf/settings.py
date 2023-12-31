import numpy as np

RNG = np.random.default_rng(seed=0)  # Random Number Generator

"""Settings for generating plots."""

SOURCE_DIR = "../results"
RESULTS_DIR = "../results"
EXPERIMENTS = []
EXPERIMENT_TITLES = []

COLORS = {
    "cloud": "#34495e",  # '#e48064',
    "fog": '#e74c3c',
    "fog_static": '#c0392b',
    "wan": '#3498db',
    "wifi": '#2ecc71',
    "cctv": '#0c6f68',
    "v2i": '#c9bc02',
}
"""Simulation duration and intervals in simulated seconds"""
SIMULATION_TIME = 360 * 24
UPDATE_MOBILITY_INTERVAL = 1
POWER_MEASUREMENT_INTERVAL = 1
UPDATE_WIFI_CONNECTIONS_INTERVAL = 60

"""Compute nodes"""
FOG_CU = 400000  # CUs are equivalent to MIPS (million instructions per second) in this experiment
FOG_MAX_POWER = 240
FOG_STATIC_POWER = 100
FOG_UTILIZATION_THRESHOLD = 0.85

CLOUD_CU = np.inf
CLOUD_WATT_PER_CU = 700e-6

"""Network (Latency is only used for determining shortest paths in the routing)"""
WAN_BANDWIDTH = np.inf
WAN_LATENCY = 100
WAN_WATT_PER_BIT_UP = 6658e-9
WAN_WATT_PER_BIT_DOWN = 20572e-9

WIFI_BANDWIDTH = 75
WIFI_LATENCY = 10
WIFI_TAXI_TO_TL_WATT_PER_BIT = 300e-9
WIFI_TL_TO_TL_WATT_PER_BIT = 100e-9
WIFI_RANGE = 300  # e.g. Cisco Aironet 1570 Series

ETHERNET_BANDWIDTH = 1e9
ETHERNET_LATENCY = 1
ETHERNET_WATT_PER_BIT = 0
DATA_CENTER_ENERGY = 1.3
ACTIVE_DEVICE_FACTOR = 0.5
USERS_PER_LINE = 2.3 # AVERAGE NUMBER OF PEOPLE IN THE UK THAT USE THE SAME CONNECTION
DEVICE_PER_USER_ON_LINE = 6.9 # Average per Capita Devices and Connections FOR THE UK
TRANSMISSION_RATE = 15.56 #7GB/HR FOR HD ON A 50 INCH TV

STATIC_CORE_ENERGY = 1.5
STATIC_ACCESS_ENERGY = 5

IDLE_FACTOR_ALLOCATION = 3

DYNAMIC_CORE_ENERGY = 0.03
DYNAMIC_ACCESS_ENERGY = 0.02

BASELOAD_ROUTER = 10

TOTAL_STATIC_ENERGY= 3*((STATIC_CORE_ENERGY + STATIC_ACCESS_ENERGY)/(USERS_PER_LINE*DEVICE_PER_USER_ON_LINE*ACTIVE_DEVICE_FACTOR))
TOTAL_DYNAMIC_ENERGY = TRANSMISSION_RATE*((DYNAMIC_CORE_ENERGY + ((DYNAMIC_ACCESS_ENERGY/WIFI_BANDWIDTH)*100)))
HOME_ROUTER_ENERGY = (BASELOAD_ROUTER)/(USERS_PER_LINE*DEVICE_PER_USER_ON_LINE*ACTIVE_DEVICE_FACTOR)

STATIC_MOBILE_CORE_ENERGY = 0.2
STATIC_MOBILE_ACCESS_ENERGY = 1


DYNAMIC_MOBILE_CORE_ENERGY = 0.03
DYNAMIC_MOBILE_ACCESS_ENERGY = 1.5

TRANSMISSION_RATE_MOBILE = 6.67 #3GB/HR FOR HD ON A 50 INCH TV
TOTAL_MOBILE_ENERGY = (STATIC_MOBILE_CORE_ENERGY+STATIC_MOBILE_ACCESS_ENERGY + (DYNAMIC_MOBILE_CORE_ENERGY+DYNAMIC_MOBILE_ACCESS_ENERGY)*TRANSMISSION_RATE_MOBILE)