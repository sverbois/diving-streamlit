import pandas as pd
import pytest

import utils

AIR_PRICES = {3: 3.0, 15: 6.0, 24: 8.0}


@pytest.mark.parametrize(
    ("args", "expected"),
    [((15, 200, 50, 45, 15.0), 20.0), ((12, 230, 60, 38, 22.5), 16.518218623481783)],
)
def test_compute_rmv(args, expected):
    assert utils.compute_rmv(*args) == pytest.approx(expected)


@pytest.mark.parametrize(("ppo2", "o2", "expected"), [(1.6, 40, 30), (1.4, 32, 34), (1.6, 100, 6), (1.2, 21, 47)])
def test_compute_mod(ppo2, o2, expected):
    assert utils.compute_mod(ppo2, o2) == expected


@pytest.mark.parametrize(("ppo2", "depth", "expected"), [(1.6, 30, 40), (1.4, 40, 28), (1.6, 3, 100), (1.0, 68, 13)])
def test_best_mix(ppo2, depth, expected):
    assert utils.best_mix(ppo2, depth) == expected


@pytest.mark.parametrize(("o2", "depth", "expected"), [(32, 40, 1.6), (21, 20, 0.63), (40, 68, 3.12)])
def test_compute_ppo2(o2, depth, expected):
    assert utils.compute_ppo2(o2, depth) == expected


@pytest.mark.parametrize(("o2", "depth", "expected"), [(32, 40, 33), (21, 20, 20), (40, 68, 49)])
def test_equivalent_air_depth(o2, depth, expected):
    assert utils.equivalent_air_depth(o2, depth) == expected


@pytest.mark.parametrize(("ppo2", "expected"), [(0.9, 35), (1.0, 40), (1.1, 45), (1.6, 70)])
def test_max_normoxic_depth(ppo2, expected):
    assert utils.max_normoxic_depth(ppo2, 0.20) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    [((45, 30, 1.6), (29, 14)), ((60, 30, 1.4), (20, 35)), ((70, 24, 1.6), (20, 46)), ((40, 24, 1.1), (22, 24))],
)
def test_best_trimix(args, expected):
    assert utils.best_trimix(*args) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ((15, 50, 200, 0, 0, 21, 21), {"he": 0.0, "air": 2250.0, "o2": 0.0}),
        ((12, 30, 220, 0, 35, 21, 18), {"he": 924.0, "air": 1210.6329113924048, "o2": 145.36708860759518}),
        ((24, 0, 200, 0, 0, 21, 32), {"he": 0.0, "air": 4131.645569620253, "o2": 668.3544303797471}),
        ((10, 100, 200, 20, 45, 21, 21), {"he": 700.0, "air": 113.92405063291139, "o2": 186.07594936708858}),
    ],
)
def test_get_missing_gases(args, expected):
    assert utils.get_missing_gases(*args) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("missing", "cylinder_volume", "expected"),
    [
        ({"he": 0, "air": 2250, "o2": 0}, 15, 6.0),
        ({"he": 0, "air": 2250, "o2": 0}, 24, 8.0),
        ({"he": 0, "air": 0, "o2": 0}, 10, 6.0),
        ({"he": 924, "air": 1210, "o2": 145}, 12, 3.0),
    ],
)
def test_filling_base_cost(missing, cylinder_volume, expected):
    assert utils.filling_base_cost(missing, cylinder_volume, mix_price=3.0, air_prices=AIR_PRICES) == expected


@pytest.mark.parametrize(("args", "expected"), [((40, 20), 178.88543819998318), ((0, 0), 0.0)])
def test_compute_q(args, expected):
    assert utils.compute_q(*args) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("q", "expected"),
    [
        (0, "Recreational"),
        (199.9, "Recreational"),
        (200, "Sport"),
        (350, "Technical"),
        (499, "Technical"),
        (500, "Expedition"),
    ],
)
def test_category_for_q(q, expected):
    assert utils.category_for_q(q) == expected


@pytest.mark.parametrize(
    ("q", "expected"),
    [
        (100, "1/1,000,000"),
        (101, "1/100,000"),
        (300, "1/10,000"),
        (400, "1/1,000"),
        (450, "2/100"),
        (600, "10/100"),
        (601, "??/100"),
    ],
)
def test_dci_risq_for_q(q, expected):
    assert utils.dci_risq_for_q(q) == expected


def test_dive_plan():
    levels = pd.DataFrame([{"depth": 40, "duration": 5}, {"depth": 20, "duration": 10}])

    profile = utils.build_dive_profile(levels, descent_speed=20, ascent_speed=10, stop_depth=6, stop_duration=5)
    plan = utils.add_gas_consumption(profile, rmv=20, cylinder_volume=15, cylinder_pressure=200)

    assert list(plan["type"]) == ["constant", "descent", "constant", "ascent", "constant", "ascent", "deco", "ascent"]
    assert list(plan["depth"]) == pytest.approx([0, 20, 40, 30, 20, 13, 6, 0])
    assert list(plan["end_depth"]) == pytest.approx([0, 40, 40, 20, 20, 6, 6, 0])
    assert list(plan["duration"]) == pytest.approx([0, 2, 5, 2, 10, 1.4, 5, 0.6])
    assert list(plan["consumption"]) == pytest.approx([0, 120, 500, 160, 600, 64.4, 160, 12])
    assert list(plan["runtime"]) == pytest.approx([0, 2, 7, 9, 19, 20.4, 25.4, 26])
    assert list(plan["pressure"]) == pytest.approx([200, 192, 158.6666667, 148, 108, 103.7066667, 93.04, 92.24])
