ADMIN_EMAIL = "sebastien.verbois@gmail.com"

PPO2_VALUES = (0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6)
DEFAULT_PPO2_INDEX = 6
CYLINDER_VOLUMES = (10, 12, 14, 15, 16, 17, 18, 20, 24)
DEFAULT_CYLINDER_VOLUME_INDEX = 3

END_DEPTHS = (24, 30)
MIN_O2_IN_NORMOXIC_TRIMIX = 0.20

DECO_DEPTH = 6  # m
SAFETY_STOP_DURATION = 5  # min
ASCENT_SPEED = 10  # m/min

MIX_PRICE = 3.0  # €, flat fee when more than one gas is added
O2_PRICE = 0.025  # €/L
HE_PRICE = 0.08  # €/L
AIR_PRICES = {3: 3.0, 15: 6.0, 24: 8.0}  # € per air fill, keyed by the largest cylinder volume (L) it covers
