"""Freeze the prototype package; stdlib only. Run at repository root."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
R=Path(__file__).resolve().parents[1]
selected={
'cad/compact/exports/compact_base.stl':1,'cad/compact/exports/compact_tray.stl':1,
'cad/compact/exports/compact_lid.stl':1,'cad/compact/exports/single_groove_spool.stl':3,
'cad/exports/pair_equaliser.stl':2,'cad/exports/tendon_fairlead.stl':3,
'cad/phoenix_v3/exports/phoenix_wrist_cradle.stl':1,
'cad/arm_interface/exports/right_open_saddle.stl':1,'cad/arm_interface/exports/emg_band_carrier.stl':1,
'cad/arm_interface/exports/right_arm_reference.step':None,
'firmware/ProstheticHand/ProstheticHand.ino':None,
'firmware/ProstheticHand/HandControl.h':None,'firmware/ProstheticHand/EMGFilters.h':None,
'firmware/ProstheticHand/EMGFilters.cpp':None}
for p in ['cad/compact/checks.json','cad/arm_interface/checks.json','cad/phoenix_v3/checks.json']:
 d=json.loads((R/p).read_text());assert not d.get('collisions',d.get('reference_collisions',[])),p
for p in selected:assert (R/p).is_file(),p
files={p:{'quantity':q,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'bytes':(R/p).stat().st_size} for p,q in selected.items()}
manifest={'version':'0.1.0-prototype','status':'Bench-development package; unfinished mechanics and unfitted arm interface',
 'entrypoint':'BUILD.md','selected_files':files,'fairlead_quantity':'Up to three; mounting/path unresolved',
 'open_gates':['Measured servo/battery/switch/electrode fit','Thumb joint orientation','Wrist lock and axle retention',
 'Restrained equalisers, tendon routing and manual release','Physical force, electrical and thermal testing','Individual socket and suspension fit']}
(R/'release/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
paths=sorted(set(filter(None,tracked))|{'BUILD.md','release/package.py','release/manifest.json'})
target=Path('/tmp/Bionic-Prosthetic-hand-0.1.0-prototype.zip')
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for p in paths:
  if (R/p).is_file():z.write(R/p,'Bionic-Prosthetic-hand/'+p)
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(f'{len(paths)} files; ZIP verified: {target}')
