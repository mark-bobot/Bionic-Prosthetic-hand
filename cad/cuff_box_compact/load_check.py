"""Internal motor-box reaction scenarios, not predicted loads on a wearer."""
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parent;O=R/'exports'
c=json.loads((O/'checks.json').read_text())
old=json.loads((R.parent/'cuff_box/exports/checks.json').read_text())
eta=.6;force=10;radius=.0123
moment=sum(p['z_mm'] for p in c['ports_local_mm'])*force/eta/1000
oldmoment=sum(p['z_mm']+10 for p in old['ports_local_mm'])*force/eta/1000
j={'scope':'Quasistatic free body of the motor box: five parallel cords with equal tensions. Internal tendon forces also react at the palm; these moments are not net wearer/joint loads.',
   'assumed_hand_tendon_force_each_N':force,'assumed_routing_efficiency':eta,
   'pair_motor_torque_Nm':2*radius*force/eta,'thumb_motor_torque_Nm':radius*force/eta,
   'five_exit_tensions_sum_N':5*force/eta,
   'new_box_pitch_reaction_about_mount_plane_Nm':moment,
   'equivalent_56mm_mount_couple_N':moment/.056,
   'old_box_pitch_reaction_about_cuff_crown_Nm':oldmoment,
   'geometric_lever_reduction_percent':100*(1-moment/oldmoment),
   'takeup_at_assumed_160deg_mm':radius*1000*math.radians(160),
   'enclosure_height_reduction_percent':100*(1-c['box_body_size_mm'][2]/old['box_body_size_mm'][2]),
   'limitations':['Actual cord angles and loads unknown.','No material strength, bolt load sharing, fatigue, local skin pressure or suspension rating established.','The arm carrier also receives palm/tendon reactions; do not treat this internal box reaction as the overall wearer torque.'],
   'geometry_report_sha256':hashlib.sha256((O/'checks.json').read_bytes()).hexdigest()}
(O/'load_checks.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
