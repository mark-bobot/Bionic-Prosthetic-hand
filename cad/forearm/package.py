"""Package the current forearm candidate with explicit selection and SHA-256 hashes."""
from pathlib import Path
import hashlib, json, subprocess, zipfile
R = Path(__file__).resolve().parents[2]
cad = R / 'cad/forearm'
check = json.loads((cad / 'checks.json').read_text())
motion = json.loads((cad / 'motion_checks.json').read_text())
assert not check['collisions'] and not check['lumen_intrusions']
assert all(p['watertight'] for p in check['parts'].values())
assert not motion['partial_finger_collisions']
assert max(motion['shell_lumen_overlap_mm3'].values()) < .001
assert all(max(p['overlap_mm3'].values()) < .001 for p in motion['mechanism_poses'])
assert motion['full_flexion_accepted'] is False
selected = {f'cad/forearm/exports/{n}.stl': 1 for n in check['parts']}
selected.update({
    'cad/forearm/exports/complete_forearm.step': None,
    'cad/compact/exports/single_groove_spool.stl': 3,
    'cad/exports/pair_equaliser.stl': 2,
    'cad/arm_interface/exports/emg_band_carrier.stl': 1,
})
manifest = {
    'version': '0.4.0-forearm', 'entrypoint': 'cad/forearm/README.md',
    'status': 'Unfitted design candidate; deeper source PIP flexion and power parts unresolved',
    'selected_files': {p: {'quantity': q, 'sha256': hashlib.sha256((R / p).read_bytes()).hexdigest()}
                       for p, q in selected.items()},
    'validation_files': {str(p.relative_to(R)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [cad/'checks.json', cad/'motion_checks.json',
                                   cad/'exports/finger_motion_diagnostic.json']},
}
(cad / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
paths = set(filter(None, subprocess.check_output(['git', 'ls-files', '-z'], cwd=R).decode().split('\0')))
paths.add('cad/forearm/manifest.json')
assert set(selected).issubset(paths), 'Stage new files before packaging.'
target = Path('/tmp/Bionic-Prosthetic-hand-0.4.0-forearm.zip')
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(paths):
        if (R / p).is_file(): z.write(R / p, 'Bionic-Prosthetic-hand/' + p)
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
print(f'{len(paths)} files; verified {target}')
