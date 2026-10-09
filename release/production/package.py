"""Verify and freeze the selected bottom-drive bench kit; never grant fitted-use approval."""
from pathlib import Path
import argparse,hashlib,json,zipfile
R=Path(__file__).resolve().parents[2];D=R/'release/production';C=R/'cad/bottom_drive';O=C/'exports'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def create(output):
 checks=json.loads((O/'checks.json').read_text())
 for group,root in [('source_sha256',R),('output_sha256',O)]:
  for name,digest in checks[group].items():require(sha(root/name)==digest,'Stale CAD evidence: '+name)
 for key in ['collisions_mm3','ear_keepout_intersections_mm3','adapter_intersections_mm3','lumen_intersections_mm3']:
  require(not checks[key],key)
 require(len(checks['hand_pose_checks'])==13,'Missing motion samples')
 require(all(not p['box_intersections_mm3'] for p in checks['hand_pose_checks']),'Motion failure')
 require(len(checks['parts'])==7 and sum(p['quantity'] for p in checks['parts'].values())==8,'Wrong kit')
 for report in ['mount_checks.json','drum_hardware_checks.json']:
  data=json.loads((O/report).read_text())
  for name,digest in data['source_sha256'].items():
   path=C/name if (C/name).exists() else O/name
   require(sha(path)==digest,'Stale hardware evidence: '+name)
  require(not data.get('collisions_mm3',[]),'Hardware collision')
  require(all(v['swept_head_base_intersection_mm3']<.001 for v in data.get('rows',[])),'Drum sweep collision')
 selected={}
 for name,info in checks['parts'].items():
  require(info['one_valid_solid'] and info['watertight'],name)
  for ext in ['stl','step']:selected[str((O/f'{name}.{ext}').relative_to(R))]=info['quantity']
 for path in [O/'complete.step',O/'complete_preview.png',O/'drive_detail_preview.png',O/'routing_comparison.png',O/'checks.json',O/'mount_checks.json',O/'drum_hardware_checks.json',O/'routing_comparison.json',C/'README.md',C/'profile.json',R/'BUILD.md',R/'LICENSE.md',R/'firmware/README.md',D/'README.md',D/'readiness.json',D/'software_checks.txt',Path(__file__)]:
  selected[str(path.relative_to(R))]=None
 for path in (R/'firmware/ProstheticHand').iterdir():
  if path.is_file():selected[str(path.relative_to(R))]=None
 readiness=json.loads((D/'readiness.json').read_text())
 manifest={'status':'BENCH_ENGINEERING_KIT_ONLY_NOT_PRODUCTION_APPROVAL','selected_design':'cad/bottom_drive','intended_use':readiness['intended_use'],'production_ready':False,'open_gates':readiness['gates'],'files':{n:{'quantity':q,'sha256':sha(R/n),'bytes':(R/n).stat().st_size} for n,q in sorted(selected.items())},'source_note':'Full CAD regeneration requires repository sources, including upstream Phoenix and imported forearm/sizing modules. This selected kit contains exports and firmware, not every historical CAD source.'}
 (D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 output.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
  for name in sorted(selected):z.write(R/name,name)
  z.write(D/'manifest.json','release/production/manifest.json')
 with zipfile.ZipFile(output) as z:
  require(z.testzip() is None,'Corrupt ZIP')
  for name,info in manifest['files'].items():require(hashlib.sha256(z.read(name)).hexdigest()==info['sha256'],'ZIP content mismatch')
 print(f'Verified {len(selected)} selected files: {output}')
 print('Fitted-use / production readiness: BLOCKED; physical and fitting evidence incomplete.')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=Path('/tmp/Bionic-bottom-drive-engineering-kit.zip'));a.add_argument('--require-production',action='store_true')
 args=a.parse_args();create(args.output)
 if args.require_production:raise SystemExit(2)
