"""Check fixed bolt interfaces at the receiver generator's sizing boundaries."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'cad/sizing'))
from adapter import receiver
from build_adapter import verify_bores

rows=[]
for scale in [.9,1.4]:
    shape=receiver(scale).val()
    assert shape.isValid() and len(shape.Solids())==1
    interface=verify_bores(shape,scale)
    rows.append({'scale_percent':scale*100,'one_valid_solid':True,'interface':interface})
    print('Boundary geometry and fixed bolt interface pass:',scale*100,flush=True)
for invalid in [.89,1.41,float('nan')]:
    try:receiver(invalid)
    except ValueError:pass
    else:raise AssertionError(('Unsupported scale accepted',invalid))
print(json.dumps({'scope':'Solid and bore geometry only; full assemblies at boundary scales are not validated.','sizes':rows},indent=2))
