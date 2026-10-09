"""Geometry and illustrative friction comparison; no measured force claim."""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parent;O=R/'exports'
a=json.loads((R.parent/'cuff_box_compact/exports/checks.json').read_text())
b=json.loads((O/'checks.json').read_text())
lookup={(p['group'],p['groove']):p for p in a['ports_local_mm']}
ports=[]
for p in b['ports_local_mm']:
 old=lookup[p['group'],p['groove']]
 ports.append(dict(group=p['group'],groove=p['groove'],old_height_mm=old['z_mm'],new_height_mm=p['z_mm'],lowered_by_mm=old['z_mm']-p['z_mm']))
oldmoment=sum(p['old_height_mm'] for p in ports)*10/.6/1000
newmoment=sum(p['new_height_mm'] for p in ports)*10/.6/1000
j={'scope':'Geometric box reactions and illustrative friction sensitivity, not measured external routing, wearer torque or strength.',
 'ports':ports,'unchanged_effective_radius_mm':12.3,'ideal_takeup_at_160deg_mm':12.3*math.radians(160),
 'assumed_hand_tendon_N_each':10,'assumed_efficiency_for_mount_load':.6,
 'old_internal_box_pitch_Nm':oldmoment,'new_internal_box_pitch_Nm':newmoment,
 'internal_pitch_reduction_percent':100*(1-newmoment/oldmoment),
 'friction_example_only':[{'assumed_mu':mu,'assumed_old_contact_deg':90,'assumed_new_contact_deg':45,'driving_tension_reduction_percent':100*(1-math.exp(-mu*math.pi/4))} for mu in [.05,.1,.2]],
 'measured_pull_reduction':None,
 'source_sha256':{str(p.relative_to(R.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),O/'checks.json',R.parent/'cuff_box_compact/exports/checks.json']}}
(O/'routing_comparison.json').write_text(json.dumps(j,indent=2)+'\n')
print('Internal box pitch scenario:',round(oldmoment,3),'->',round(newmoment,3),'Nm')
