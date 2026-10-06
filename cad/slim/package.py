"""Package the optional smaller-part candidate without changing the baseline manifest."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
R=Path(__file__).resolve().parents[2]
for p in ['cad/slim/checks.json','cad/slim/integration_checks.json']:
 assert not json.loads((R/p).read_text())['collisions'],p
selected={
 'cad/slim/exports/compact_base.stl':1,'cad/slim/exports/compact_tray.stl':1,
 'cad/slim/exports/feedthrough_lid.stl':1,'cad/slim/exports/complete_slim_candidate.step':None,
 'cad/compact/exports/single_groove_spool.stl':3,'cad/exports/pair_equaliser.stl':2,
 'cad/arm_interface/exports/emg_band_carrier.stl':1,
 'cad/bionic/exports/socket_dorsal.stl':1,'cad/bionic/exports/socket_ventral_door.stl':1,
 'cad/bionic/exports/fixed_palm_receiver.stl':1,'cad/bionic/exports/tendon_cassette_base.stl':1,
 'cad/bionic/exports/tendon_cassette_cover.stl':1,'cad/bionic/exports/thumb_line_slider.stl':1,
 'cad/bionic/exports/wrist_guide_comb.stl':1,
}
files={p:{'quantity':q,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()} for p,q in selected.items()}
manifest={'version':'0.3.0-layout','entrypoint':'cad/slim/README.md',
 'status':'Optional smaller-part candidate; actual servo fit and power system unverified','selected_files':files}
(R/'cad/slim/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
paths=set(filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')))
paths.add('cad/slim/manifest.json')
target=Path('/tmp/Bionic-Prosthetic-hand-0.3.0-layout.zip')
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(paths):
  if (R/p).is_file():z.write(R/p,'Bionic-Prosthetic-hand/'+p)
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(f'{len(paths)} files; verified {target}')
