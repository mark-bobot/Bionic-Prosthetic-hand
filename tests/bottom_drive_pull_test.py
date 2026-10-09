"""Independent force/travel examples and rejection of incomplete or invalid evidence."""
import copy
import importlib.util
import json
import math
from pathlib import Path
R = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pull", R / "calculations/check_bottom_drive_pull.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
data = json.loads((R / "calculations/bottom_drive_pull_template.json").read_text())
assert m.screen(data)["status"] == "MEASUREMENTS_REQUIRED"
for g in data["groups"].values():
    g.update(servo_model="synthetic test only", effective_radius_mm=10, usable_sweep_deg=180, allowed_torque_Nm=.31,
             servo_and_sweep_confirmed=True)
for f in data["fingers"].values():
    f.update(peak_force_N=10, closure_travel_mm=30, maximum_tested_travel_mm=31,
             full_route_measured=True)
r = m.screen(data)
assert r["status"] == "SCREEN_PASS" and r["human_use_approved"] is False
assert math.isclose(r["groups"]["index_middle"]["required_torque_with_margin_Nm"], .3)
assert math.isclose(r["groups"]["thumb"]["required_torque_with_margin_Nm"], .15)
assert math.isclose(r["groups"]["index_middle"]["travel_available_mm"], math.pi * 10)
b = copy.deepcopy(data)
b["fingers"]["index"].update(closure_travel_mm=22, maximum_tested_travel_mm=25)
assert m.screen(b)["status"] == "SCREEN_FAIL"  # Equal-travel incompatibility.
b = copy.deepcopy(data)
b["groups"]["thumb"]["usable_sweep_deg"] = 90
assert m.screen(b)["status"] == "SCREEN_FAIL"
b = copy.deepcopy(data)
b["fingers"]["ring"]["peak_force_N"] = 20
assert m.screen(b)["status"] == "SCREEN_FAIL"
for key in ["full_route_measured"]:
    b = copy.deepcopy(data)
    b["fingers"]["thumb"][key] = False
    assert m.screen(b)["status"] == "CALIBRATION_OR_ROUTE_REQUIRED"
b = copy.deepcopy(data)
b["groups"]["thumb"]["servo_and_sweep_confirmed"] = False
assert m.screen(b)["status"] == "CALIBRATION_OR_ROUTE_REQUIRED"
b = copy.deepcopy(data)
b["fingers"]["thumb"]["peak_force_N"] = None
assert m.screen(b)["status"] == "MEASUREMENTS_REQUIRED"
for bad in [False, -1, float("nan"), float("inf"), 0]:
    b = copy.deepcopy(data)
    b["groups"]["thumb"]["effective_radius_mm"] = bad
    try:
        m.screen(b)
    except ValueError:
        pass
    else:
        raise AssertionError(bad)
print("PASS: paired torque, unequal travel, short sweep, overload, missing/unconfirmed data, invalid numbers")
