"""Unit conversions, insufficient stroke, and unmeasured-input regression checks."""
import copy,importlib.util,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sizing',R/'calculations/check_measured_pull.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a=json.loads((R/'calculations/measured_pull_template.json').read_text())
assert m.screen(a)['status']=='MEASUREMENTS_REQUIRED'
# Analytic fixture: 20 N at 10 mm, margin 1.5 -> 0.3 Nm; 180 deg -> pi*10 mm.
a.update(servo_and_sweep_confirmed=True,effective_spool_radius_mm=10,calibrated_sweep_deg=180,screen_torque_Nm=.31,slack_allowance_mm=0)
for c in a['channels'].values():c.update(peak_input_force_N=20,required_input_travel_mm=30)
r=m.screen(a);assert r['status']=='SCREEN_PASS'
assert math.isclose(r['channels']['thumb']['required_torque_with_margin_Nm'],.3)
assert math.isclose(r['channels']['thumb']['travel_available_mm'],10*math.pi)
b=copy.deepcopy(a);b['servo_and_sweep_confirmed']=False
assert m.screen(b)['status']=='CALIBRATION_REQUIRED'
b=copy.deepcopy(a);b['channels']['thumb']['required_input_travel_mm']=40
assert m.screen(b)['status']=='SCREEN_FAIL'
assert not m.screen(b)['channels']['thumb']['radius_interval_exists']
b=copy.deepcopy(a);b['channels']['thumb']['peak_input_force_N']=30
assert m.screen(b)['status']=='SCREEN_FAIL'
b=copy.deepcopy(a);b['channels']['thumb']['peak_input_force_N']=None
assert m.screen(b)['status']=='MEASUREMENTS_REQUIRED'
for bad in [0,-1,float('nan'),float('inf'),True]:
 b=copy.deepcopy(a);b['effective_spool_radius_mm']=bad
 try:m.screen(b)
 except ValueError:pass
 else:raise AssertionError(bad)
print('Measured-pull sizing checks passed; no hardware measurements fabricated.')
