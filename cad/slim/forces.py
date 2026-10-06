"""Candidate torque/current screen; manufacturer ratings are not enclosure acceptance."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parent
rows=[]
for voltage,stall,rated,current in [(6,20.5,6.8,3.4),(7.4,25,8.3,4.4),(8.4,28.5,9.5,5)]:
 allowance=min(.4*stall,rated)
 rows.append({'voltage_V':voltage,'stall_kgcm':stall,'rated_kgcm':rated,'screen_allowance_kgcm':allowance,
  'paired_tendon_N_each_at_60pct':.6*allowance*.0980665/(2*1.5*.0123),
  'thumb_tendon_N_at_60pct':.6*allowance*.0980665/(1.5*.0123),
  'three_servo_stall_A':3*current})
result={'source':'https://www.feetechrc.com/Data/feetechrc/upload/file/20210810/6376418710101296552903409.pdf',
 'assumptions':{'working_fraction_cap':.4,'separate_load_margin':1.5,'routing_efficiency':.6,'effective_radius_mm':12.3},
 'rows':rows,'takeup_at_160deg_mm':12.3*math.radians(160),
 'housing_height_reduction_pct':100*(60-50)/60,'housing_and_cassette_height_reduction_pct':100*(73-63)/73,
 'limitations':['Manufacturer rated torque is a cap, not a verified enclosed continuous-duty allowance.',
 'Battery voltage and sag change available torque; use the lowest measured operating voltage.',
 'No fingertip force, runtime, current limiting or structural acceptance is established.']}
(R/'forces.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
