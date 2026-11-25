import pandas as pd

N2_IN_AIR = 0.79
METERS_PER_BAR = 10.0
GAS_CONSTANT = 0.08314  # L·bar/(mol·K)
ZERO_CELSIUS = 273.15  # K
# Divers count gas as cylinder volume × pressure, so gas litres are taken at 1 bar and 20 °C.
SURFACE_PRESSURE = 1.0  # bar
SURFACE_TEMPERATURE = 20.0  # °C


def pressure_at(depth):
    return depth / METERS_PER_BAR + 1.0


def depth_at(pressure):
    return (pressure - 1.0) * METERS_PER_BAR


def kelvin(celsius):
    return celsius + ZERO_CELSIUS


def celsius(kelvin):
    return kelvin - ZERO_CELSIUS


def moles_in(surface_volume):
    return SURFACE_PRESSURE * surface_volume / (GAS_CONSTANT * kelvin(SURFACE_TEMPERATURE))


def surface_volume_of(moles):
    return moles * GAS_CONSTANT * kelvin(SURFACE_TEMPERATURE) / SURFACE_PRESSURE


def ideal_gas_pressure(volume, moles, temperature):
    return moles * GAS_CONSTANT * temperature / volume


def compute_rmv(cylinder_volume, start_pressure, end_pressure, dive_time, mean_depth):
    return (cylinder_volume * (start_pressure - end_pressure)) / (dive_time * pressure_at(mean_depth))


def compute_mod(ppo2_max, o2_percentage):
    return round(depth_at(ppo2_max / (o2_percentage / 100.0)))


def best_mix(ppo2_max, depth):
    return min(100, round(ppo2_max / pressure_at(depth) * 100))


def compute_ppo2(o2_percentage, depth):
    return round(o2_percentage / 100.0 * pressure_at(depth), 2)


def equivalent_air_depth(o2_percentage, depth):
    ppn2 = (100 - o2_percentage) / 100.0 * pressure_at(depth)
    return round(depth_at(ppn2 / N2_IN_AIR))


def max_normoxic_depth(max_ppo2, min_o2_fraction):
    return round(depth_at(max_ppo2 / min_o2_fraction))


def best_trimix(dive_depth, max_end_depth, max_ppo2):
    dive_pressure = pressure_at(dive_depth)
    max_ppn2 = pressure_at(max_end_depth) * N2_IN_AIR
    o2_percentage = min(100, round(max_ppo2 / dive_pressure * 100))
    n2_percentage = min(79, 100 - o2_percentage, round(max_ppn2 / dive_pressure * 100))
    he_percentage = 100 - o2_percentage - n2_percentage
    return o2_percentage, he_percentage


def get_missing_gases(
    cylinder_volume,
    start_pressure,
    end_pressure,
    start_he_percentage,
    end_he_percentage,
    start_o2_percentage,
    end_o2_percentage,
):
    """Return the volume in liters of each gas to add."""
    gas_missing = (end_pressure - start_pressure) * cylinder_volume
    start_n2_percentage = 100 - start_he_percentage - start_o2_percentage
    end_n2_percentage = 100 - end_he_percentage - end_o2_percentage
    missing_he = (
        end_he_percentage / 100.0 * end_pressure * cylinder_volume
        - start_he_percentage / 100.0 * start_pressure * cylinder_volume
    )
    missing_n2 = (
        end_n2_percentage / 100.0 * end_pressure * cylinder_volume
        - start_n2_percentage / 100.0 * start_pressure * cylinder_volume
    )
    missing_air = missing_n2 / N2_IN_AIR
    missing_o2 = gas_missing - (missing_he + missing_air)

    return {
        "he": missing_he,
        "air": missing_air,
        "o2": missing_o2,
    }


def filling_base_cost(missing_gases, cylinder_volume, mix_price, air_prices):
    if sum(1 for volume in missing_gases.values() if volume > 0) > 1:
        return mix_price
    return next(price for max_volume, price in air_prices.items() if cylinder_volume <= max_volume)


def compute_q(depth, time):
    return depth * (time**0.5)


def category_for_q(q):
    if q < 200:
        return "Recreational"
    if q < 350:
        return "Sport"
    if q < 500:
        return "Technical"
    return "Expedition"


def dcs_risk_for_q(q):
    if q <= 100:
        return "1/1,000,000"
    if q <= 200:
        return "1/100,000"
    if q <= 300:
        return "1/10,000"
    if q <= 400:
        return "1/1,000"
    if q <= 450:
        return "2/100"
    if q <= 500:
        return "4/100"
    if q <= 550:
        return "6/100"
    if q <= 600:
        return "10/100"
    return "??/100"


def build_dive_profile(levels: pd.DataFrame, descent_speed, ascent_speed, stop_depth, stop_duration) -> pd.DataFrame:
    """Insert descents, ascents and the final stop between the levels.

    `depth` is the mean depth of a segment (used for consumption), `end_depth` the depth reached at its end.
    """
    stops = [(0, 0), *zip(levels["depth"], levels["duration"]), (stop_depth, stop_duration)]
    rows = []
    for i, (depth, duration) in enumerate(stops):
        is_last = i == len(stops) - 1
        rows.append(
            {"depth": depth, "duration": duration, "type": "deco" if is_last else "constant", "end_depth": depth}
        )
        next_depth = 0 if is_last else stops[i + 1][0]
        diff_depth = next_depth - depth
        rows.append(
            {
                "depth": (depth + next_depth) / 2,
                "duration": diff_depth / descent_speed if diff_depth > 0 else -diff_depth / ascent_speed,
                "type": "descent" if diff_depth > 0 else "ascent",
                "end_depth": next_depth,
            }
        )
    return pd.DataFrame(rows)


def add_gas_consumption(profile: pd.DataFrame, rmv, cylinder_volume, cylinder_pressure) -> pd.DataFrame:
    profile = profile.copy()
    profile["consumption"] = pressure_at(profile["depth"]) * rmv * profile["duration"]
    profile["runtime"] = profile["duration"].cumsum()
    profile["pressure"] = cylinder_pressure - profile["consumption"].cumsum() / cylinder_volume
    return profile
