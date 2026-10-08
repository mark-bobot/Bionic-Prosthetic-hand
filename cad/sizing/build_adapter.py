"""Assemble a scale-aware receiver against the fixed forearm candidate. CC BY 4.0."""
from pathlib import Path
import argparse, hashlib, json, sys
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
import numpy as np
import trimesh
from sizing import validate
from adapter import receiver
R=Path(__file__).resolve().parent;F=R.parent/'forearm'
sys.path.insert(0,str(F))
from hand import models,posed,pivot,ZMIN
from thumb_mount import posed_thumb
sys.path.insert(0,str(R.parent/'bionic'))
from render import render


def bounds(s):
    b=s.BoundingBox();return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]


def intersect_volume(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if any(min(getattr(aa,k+'max'),getattr(bb,k+'max'))-max(getattr(aa,k+'min'),getattr(bb,k+'min'))<=1e-6 for k in 'xyz'):
        return 0.0
    v=a.intersect(b)
    assert v.isValid(),'Invalid collision boolean'
    return max(0,v.Volume())


def baseline():
    checks=json.loads((F/'checks.json').read_text())
    closure=json.loads((F/'closure_checks.json').read_text())
    assert closure['all_samples_clear'] and len(closure['samples'])==13
    checksums=json.loads((F/'assembly_checks.json').read_text())
    for n,h in checksums['source_sha256'].items():
        assert hashlib.sha256((F/n).read_bytes()).hexdigest()==h,n
    full=F/'exports/complete_forearm.step'
    assert hashlib.sha256(full.read_bytes()).hexdigest()==checksums['assemblies']['complete_forearm']['sha256']
    original={n:p.val() for n,p in {**models,**posed_thumb()}.items()}
    named={n:cq.importers.importStep(str(F/'exports'/f'{n}.step')).translate((0,0,p['assembly_zmin_mm'])).val()
           for n,p in checks['parts'].items()}
    solids=cq.importers.importStep(str(full)).solids().vals()
    fixed={}
    for i,s in enumerate(solids):
        if any(np.allclose(bounds(s),bounds(p),atol=.0001,rtol=0) for p in [named['palm_receiver'],*original.values()]):continue
        name=next((n for n,p in named.items() if np.allclose(bounds(s),bounds(p),atol=.0001,rtol=0)),f'fixed_component_{i}')
        fixed[name]=s
    assert len(solids)-len(fixed)==12
    return original,fixed,checks


def verify_bores(shape,scale):
    circles=[]
    for face in shape.Faces():
        if face.geomType()=='CYLINDER':
            c=BRepAdaptor_Surface(face.wrapped).Cylinder();p=c.Axis().Location();d=c.Axis().Direction()
            circles.append((c.Radius(),p.X(),p.Y(),p.Z(),d.X(),d.Y(),d.Z()))
    for x in [-18,18]:
        assert any(abs(r-2.2)<1e-5 and abs(xx-x)<1e-5 and abs(y+24)<1e-5 and abs(dz)>.99 for r,xx,y,z,dx,dy,dz in circles)
        assert any(abs(r-4.2)<1e-5 and abs(xx-x)<1e-5 and abs(y+24)<1e-5 and abs(dz)>.99 for r,xx,y,z,dx,dy,dz in circles)
        # Require a full annular footprint around each fixed attachment, below the recess.
        ring=cq.Workplane('XY').center(x,-24).circle(6).circle(3).extrude(3).val()
        assert abs(shape.intersect(ring).Volume()-ring.Volume())<.001
    z=(pivot[2]-ZMIN)*scale
    wrist=[c for c in circles if abs(c[0]-(6*scale+.4)/2)<1e-5 and abs(c[2])<1e-5 and abs(c[3]-z)<1e-5 and abs(c[4])>.99]
    assert len(wrist)>=2
    return {'forearm_bolt_centres_xy_mm':[[-18,-24],[18,-24]],'through_bore_mm':4.4,
            'head_recess_diameter_mm':8.4,'head_recess_depth_mm':1,
            'bearing_material_under_recess_mm':3,'wrist_bore_mm':6*scale+.4,'wrist_axis_yz_mm':[0,z],
            'ear_thickness_mm':4,'outer_ear_span_mm':70*scale+4,
            'scope':'Geometry only. Axle retention, chosen bolts, load capacity and tool access require physical verification.'}


def build(profile_path,out):
    profile=validate(json.loads(profile_path.read_text()));scale=profile['hand_scale_percent']/100
    original,fixed,checks=baseline();out.mkdir(parents=True,exist_ok=True)
    # Existing receiver subtraction left shell material around/above the bolt holes.
    # Clear the actual heads locally, without thinning the new receiver's bearing floor.
    lower=fixed['forearm_lower']
    before_lower_volume=lower.Volume()
    for x in [-18,18]:
        pocket=cq.Workplane('XY').center(x,-24).circle(4.3).extrude(5).translate((0,0,3)).val()
        lower=lower.cut(pocket)
    assert lower.isValid() and len(lower.Solids())==1
    fixed['forearm_lower']=lower
    adapter=receiver(scale).val();assert adapter.isValid() and len(adapter.Solids())==1
    bore_report=verify_bores(adapter,scale)
    hand={n:p.scale(scale) for n,p in original.items()}
    heads={f'M4_head_allowance_{i}':cq.Workplane('XY').center(x,-24).circle(4).extrude(2.5).translate((0,0,3)).val() for i,x in enumerate([-18,18])}
    hits=[]
    for n,p in {'resized_receiver':adapter,**hand,**heads}.items():
        for nn,q in fixed.items():
            v=intersect_volume(p,q)
            if v>.001:hits.append([n,nn,v])
    for n,p in {**hand,**heads}.items():
        v=intersect_volume(p,adapter)
        if v>.001:hits.append([n,'resized_receiver',v])
    report={'hand_scale_percent':scale*100,'status':'UNFITTED_ADAPTER_CANDIDATE',
            'patient_fit_verified':False,'baseline_forearm_version':'0.4.3',
            'lower_shell_change':{'head_pocket_diameter_mm':8.6,'pocket_z_mm':[3,8], 'removed_volume_mm3':before_lower_volume-lower.Volume()},
            'interface':bore_report,'static_collisions_mm3':hits,'closure_samples':[],
            'scope':'Fixed hardware at 100%; scaled original hand, new receiver and two local lower-shell head pockets. No tendon, axle, nut, full fastener, load or fitted socket validation.'}
    print('Static checks:',hits,flush=True)
    # Store failure diagnostics; never present an intersecting assembly as a valid candidate.
    (out/'adapter_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not hits,'Static interference; see adapter_checks.json'
    for step in range(13):
        t=step/12;mcp=60*t;pip=10+60*t;tr=-60-30*t;tp=10+30*t
        moving={n:p.val().scale(scale) for n,p in {**posed(mcp,pip),**posed_thumb(tr,tp)}.items()}
        found=[];maximum=0
        for n,p in moving.items():
            for nn,q in {'resized_receiver':adapter,**fixed,**heads}.items():
                v=intersect_volume(p,q);maximum=max(maximum,v)
                if v>.001:found.append([n,nn,v])
        report['closure_samples'].append({'step':step,'MCP':mcp,'PIP':pip,'thumb_root':tr,'thumb_tip':tp,'maximum_overlap_mm3':maximum,'collisions':found})
        print('Closure sample',step,found,flush=True)
        if step==9 and not found:
            cq.exporters.export(cq.Compound.makeCompound([*moving.values(),adapter]),str(out/'sized_flexion_hand.step'))
    report['all_samples_clear']=all(not v['collisions'] for v in report['closure_samples'])
    (out/'adapter_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['all_samples_clear'],'Sampled interference; see adapter_checks.json'
    # Original-to-original hand intersections transform uniformly with scale; this run
    # checks the resized hand against the added receiver and every fixed assembly solid.
    report['hand_self_motion_scope']='Original hand geometry and 13 pose angles are uniformly scaled. Hand-v-hand booleans are not repeated; see baseline closure_checks.json.'
    zmin=adapter.BoundingBox().zmin
    printable=adapter.translate((0,0,-zmin))
    for ext in ['step','stl']:
        cq.exporters.export(printable,str(out/f'resized_receiver.{ext}'),tolerance=.08,angularTolerance=.15)
    mesh=trimesh.load_mesh(out/'resized_receiver.stl')
    assert mesh.is_watertight and mesh.volume>0
    report['print_parts']={'resized_receiver':{'assembly_zmin_mm':zmin,'watertight':True,'dimensions_mm':mesh.extents.tolist()}}
    lower_zmin=lower.BoundingBox().zmin
    for ext in ['step','stl']:
        cq.exporters.export(lower.translate((0,0,-lower_zmin)),str(out/f'forearm_lower_head_clearance.{ext}'),tolerance=.08,angularTolerance=.15)
    lower_mesh=trimesh.load_mesh(out/'forearm_lower_head_clearance.stl')
    assert lower_mesh.is_watertight and lower_mesh.volume>0
    report['print_parts']['forearm_lower_head_clearance']={'assembly_zmin_mm':lower_zmin,'watertight':True,'dimensions_mm':lower_mesh.extents.tolist()}
    palette=[{'bounds':bounds(adapter),'color':[196,147,70]}]
    for info in checks['components'].values():palette.append({'bounds':info['bounds_mm'],'color':[72,112,113]})
    for mode,omit in [('complete',set()),('open',{'forearm_upper','internal_tendon_cover'})]:
        assembly=cq.Compound.makeCompound([p for n,p in fixed.items() if n not in omit]+[adapter,*hand.values(),*heads.values()])
        target=out/f'sized_{mode}.step';cq.exporters.export(assembly,str(target))
        actual=cq.importers.importStep(str(target)).solids().vals()
        for n,s in {**hand,'resized_receiver':adapter,'forearm_lower_head_clearance':lower}.items():
            matches=[p for p in actual if np.allclose(bounds(p),bounds(s),atol=.0001,rtol=0)]
            assert len(matches)==1 and matches[0].isValid(),(mode,n)
            assert abs(matches[0].Volume()/s.Volume()-1)<.001,(mode,n,'volume')
        render(target,out/f'sized_{mode}_preview.png',title=f'Phoenix v3 · {scale*100:g}% hand · new wrist receiver',solid_colors=palette,view=(-145,28))
    render(out/'sized_flexion_hand.step',out/'sized_flexion_preview.png',title=f'{scale*100:g}% hand · sampled flexion · new receiver',solid_colors=palette,view=(-145,28))
    report['sha256']={str(p.relative_to(R.parent.parent)) if p.is_relative_to(R.parent.parent) else p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [profile_path,Path(__file__),R/'adapter.py',R/'sizing.py',F/'hand.py',F/'thumb_mount.py',F/'exports/complete_forearm.step',F/'closure_checks.json']}
    report['output_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in ['.step','.stl','.png']}
    (out/'adapter_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Validated receiver, two complete exports and 13 closure samples.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=R/'profile.json')
    parser.add_argument('--output',type=Path,default=R/'adapter_exports')
    a=parser.parse_args();build(a.profile.resolve(),a.output.resolve())
