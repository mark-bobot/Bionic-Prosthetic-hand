"""Torque/travel screen for fixed two-groove drums; no differential assumed."""
import argparse
import json
import math
from pathlib import Path

GROUPS = {"thumb": ("thumb",), "index_middle": ("index", "middle"),
          "ring_little": ("ring", "little")}

def number(value, name, zero=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0 or (not zero and value == 0)):
        raise ValueError(name + " must be finite and " + ("nonnegative" if zero else "positive"))
    return float(value)

def screen(data):
    margin = number(data["load_margin"], "load_margin")
    if margin < 1:
        raise ValueError("load_margin must be at least 1")
    result = {"status": "MEASUREMENTS_REQUIRED", "human_use_approved": False, "groups": {},
              "notes": ["Full-route actuator-end forces include friction: do not derate twice.",
                        "Sum of individual peaks is conservative only over the measured common stroke.",
                        "Fixed grooves cannot adapt to one finger contacting an object first.",
                        "This is a calculation, not release, temperature, strength or fitting evidence."]}
    for group, fingers in GROUPS.items():
        cfg = data["groups"][group]
        fields = ["effective_radius_mm", "usable_sweep_deg", "allowed_torque_Nm"]
        vals = {}
        missing = []
        if not isinstance(cfg.get("servo_model"), str) or not cfg["servo_model"].strip():
            missing.append(group + ".servo_model")
        for field in fields:
            if cfg.get(field) is None:
                missing.append(group + "." + field)
            else:
                vals[field] = number(cfg[field], field)
        rows = []
        for finger in fingers:
            row = data["fingers"][finger]
            checked = {}
            for field in ["peak_force_N", "closure_travel_mm", "maximum_tested_travel_mm"]:
                if row.get(field) is None:
                    missing.append(finger + "." + field)
                else:
                    checked[field] = number(row[field], finger + "." + field, zero=field != "peak_force_N")
            rows.append(checked)
        if missing:
            result["groups"][group] = {"status": "MEASUREMENTS_REQUIRED", "missing": missing}
            continue
        radius = vals["effective_radius_mm"]
        travel = max(row["closure_travel_mm"] for row in rows)
        max_travel = min(row["maximum_tested_travel_mm"] for row in rows)
        torque = margin * sum(row["peak_force_N"] for row in rows) * radius / 1000
        available = radius * math.radians(vals["usable_sweep_deg"])
        overlap = travel <= max_travel
        passed = overlap and travel <= available and torque <= vals["allowed_torque_Nm"]
        confirmed = (cfg.get("servo_and_sweep_confirmed") is True and
                     all(data["fingers"][f].get("full_route_measured") is True for f in fingers))
        result["groups"][group] = {
            "status": ("SCREEN_PASS" if confirmed else "CALIBRATION_OR_ROUTE_REQUIRED") if passed else "SCREEN_FAIL",
            "required_torque_with_margin_Nm": torque,
            "allowed_torque_Nm": vals["allowed_torque_Nm"],
            "common_take_up_required_mm": travel,
            "common_take_up_maximum_tested_mm": max_travel,
            "travel_available_mm": available,
            "common_travel_interval_exists": overlap,
            "friction_factor_applied": False}
    states = [row["status"] for row in result["groups"].values()]
    if "SCREEN_FAIL" in states:
        result["status"] = "SCREEN_FAIL"
    elif all(s == "SCREEN_PASS" for s in states):
        result["status"] = "SCREEN_PASS"
    elif "MEASUREMENTS_REQUIRED" not in states:
        result["status"] = "CALIBRATION_OR_ROUTE_REQUIRED"
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("measurements", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = screen(json.loads(args.measurements.read_text()))
    except (KeyError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
    raise SystemExit(0 if report["status"] == "SCREEN_PASS" else 2)
