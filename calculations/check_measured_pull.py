"""Screen measured, actuator-end pulls without counting routing friction twice.

Run: python calculations/check_measured_pull.py measurements.json
Measurements are required; the empty template cannot produce a passing result.
"""
import argparse,json,math
from pathlib import Path

CHANNELS=('thumb','index_middle','ring_little')
def positive(value,label,allow_zero=False):
 if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0 or (value==0 and not allow_zero):
  raise ValueError(label+' must be a finite '+('non-negative' if allow_zero else 'positive')+' number')
 return float(value)

def screen(data):
 # Electrical/thermal and clinical suitability are deliberately outside this calculation.
 result={'status':'MEASUREMENTS_REQUIRED','channels':{},'limits':['Torque/travel screening only; no runtime, thermal, structural or fitted-use acceptance.','For an equaliser, measure the assembled pair at its input, with the actual return bands and full route.','Use the lowest measured loaded supply voltage; the owned generic servos are unidentified.']}
 r=positive(data['effective_spool_radius_mm'],'effective_spool_radius_mm')
 angle=positive(data['calibrated_sweep_deg'],'calibrated_sweep_deg')
 margin=positive(data['load_margin'],'load_margin')
 if margin<1:raise ValueError('load_margin must be at least 1')
 slack=positive(data['slack_allowance_mm'],'slack_allowance_mm',True)
 torque=positive(data['screen_torque_Nm'],'screen_torque_Nm')
 theta=math.radians(angle)
 for name in CHANNELS:
  m=data['channels'][name]
  if m.get('peak_input_force_N') is None or m.get('required_input_travel_mm') is None:
   result['channels'][name]={'status':'MEASUREMENTS_REQUIRED'};continue
  f=positive(m['peak_input_force_N'],name+' force')
  travel=positive(m['required_input_travel_mm'],name+' travel',True)
  # Gauge point is where the disconnected servo pulls: all downstream losses are included.
  required_torque=margin*f*r/1000
  min_radius=(travel+slack)/theta
  max_radius=1000*torque/(margin*f)
  travel_available=r*theta
  passed=required_torque<=torque and travel+slack<=travel_available
  result['channels'][name]={'status':'SCREEN_PASS' if passed else 'SCREEN_FAIL',
   'required_torque_with_margin_Nm':required_torque,'screen_torque_Nm':torque,
   'travel_available_mm':travel_available,'travel_with_slack_mm':travel+slack,
   'minimum_radius_for_travel_mm':min_radius,'maximum_radius_for_force_mm':max_radius,
   'radius_interval_exists':min_radius<=max_radius,
   'nominal_radius_mm':r,'friction_factor_applied':False}
 statuses=[v['status'] for v in result['channels'].values()]
 if 'SCREEN_FAIL' in statuses:result['status']='SCREEN_FAIL'
 elif all(s=='SCREEN_PASS' for s in statuses):
  result['status']='SCREEN_PASS' if data.get('servo_and_sweep_confirmed') is True else 'CALIBRATION_REQUIRED'
 result['servo_and_sweep_confirmed']=data.get('servo_and_sweep_confirmed') is True
 return result

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('measurements',type=Path);parser.add_argument('--output',type=Path)
 args=parser.parse_args()
 try:report=screen(json.loads(args.measurements.read_text()))
 except (ValueError,KeyError,TypeError) as e:parser.error(str(e))
 text=json.dumps(report,indent=2)+'\n'
 if args.output:args.output.write_text(text)
 print(text,end='')
