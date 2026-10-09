"""Inverted motor cartridge with low tendon exits; original Phoenix hand unmodified. CC BY 4.0."""
from pathlib import Path
import argparse,hashlib,json,math,sys
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
import numpy as np
import trimesh
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'forearm'))
from hand import models as original_hand, posed
from thumb_mount import posed_thumb
sys.path.insert(0,str(R.parent/'sizing'))
from adapter import receiver as make_receiver
from arm_adapter import make_arm_adapter
sys.path.insert(0,str(R.parent/'bionic'))
from render import render


def box(w,l,h,x=0,y=0,z=0):
    return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))

def cyl(d,h,x,y,z):
    return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))

def rounded(w,l,h,x,y,z,r=5):
    return box(w,l,h,x,y,z).edges('|Z').fillet(r)

def along_y(radius,y0,y1,x,z):
    return cq.Solid.makeCylinder(radius,y1-y0,cq.Vector(x,y0,z),cq.Vector(0,1,0))

def bounds(s):
    b=s.BoundingBox();return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]

def overlap(a,b):
    aa,bb=a.BoundingBox(),b.BoundingBox()
    if any(min(getattr(aa,k+'max'),getattr(bb,k+'max'))-max(getattr(aa,k+'min'),getattr(bb,k+'min'))<=1e-6 for k in 'xyz'):return 0.
    p=a.intersect(b);assert p.isValid();return max(0,p.Volume())

def spool(grooves):
    h=4.2 if grooves==1 else 7.2
    p=cyl(24,h,0,0,0)
    for z in ([0,3] if grooves==1 else [0,3,6]):p=p.union(cyl(28,1.2,0,0,z))
    p=p.cut(cyl(6,20,0,0,-1))
    for x in [-8,8]:p=p.cut(cq.Workplane('XY').center(x,0).slot2D(5,2.3).extrude(20).translate((0,0,-1)))
    for z in ([2.1] if grooves==1 else [2.1,5.1]):
        p=p.cut(cq.Workplane('YZ').center(0,z).circle(.7).extrude(32,both=True))
    return p.val()


def build(profile_path,out):
    p=json.loads(profile_path.read_text())
    for k,v in p.items():
        if k.endswith('_mm') or k.endswith('_percent'):
            if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0:raise ValueError(k)
    if p['servo_body_height_mm']<20:raise ValueError('This layout requires a servo height of at least 20 mm; reroute if smaller.')
    if p['servo_ear_width_allowance_mm']<p['servo_body_width_mm'] or p['servo_ear_length_allowance_mm']<p['servo_body_length_mm']:raise ValueError('Ear allowance cannot be smaller than the body')
    if not .5*p['servo_body_length_mm']>p['shaft_offset_mm']:raise ValueError('Shaft must lie over the reference case')
    out.mkdir(parents=True,exist_ok=True)
    h=p['servo_body_height_mm'];sz=4+h+p['shaft_projection_allowance_mm']+p['horn_height_allowance_mm']
    height=max(sz+10,48)+3;roof=height-4
    deck=p['cuff_axis_z_mm']+p['adapter_inner_radius_mm']+p['adapter_wall_mm']
    centre_y=-56
    base=rounded(94,96,4,0,centre_y,0)
    walls=rounded(94,96,roof-4,0,centre_y,4).cut(rounded(88,90,roof,0,centre_y,4,r=2))
    base=base.union(walls)
    # Four M4 posts join the case to the rigid adapter instead of strap ears.
    mount_xy=[(x,y) for x in [-34,34] for y in [-86,-30]]
    for x,y in mount_xy:
        base=base.cut(cyl(4.4,8,x,y,-1))
        countersink=cq.Solid.makeCone(2.2,4.4,2.2,cq.Vector(x,y,1.8),cq.Vector(0,0,1))
        base=base.cut(cq.Workplane('XY').newObject([countersink]))
    stations=[('index_middle',-28,-46,1,2),('thumb',0,-56,-1,1),('ring_little',28,-46,1,2)]
    components={};ear_keepouts={};cords={};ports=[];upper_seats=[];tie_slots=[];motor_mounts=[]
    for name,x,y,direction,grooves in stations:
        w,l=p['servo_body_width_mm'],p['servo_body_length_mm']
        seat=box(w+5,l+5,4,x,y,4).cut(box(w+1,l+1,6,x,y,4))
        for dy in [-l/2,l/2]:seat=seat.cut(box(10,8,6,x,y+dy,4))
        upper_seats.append(seat.rotate((x,0,height/2),(x,1,height/2),180).val())
        # Two removable ties per servo; their buckles stay inside the enclosure.
        for yy in [y-9,y+9]:
            for xx in [x-(w/2+2),x+(w/2+2)]:tie_slots.append((xx,yy))
        body=box(w,l,h,x,y,4)
        # An illustrative ear position; full ear-footprint keep-out is checked separately.
        ears=box(p['servo_ear_width_allowance_mm'],p['servo_ear_length_allowance_mm'],2.5,x,y,4+20.55)
        for dx in [-5,5]:
            for dy in [-24.75,24.75]:
                ears=ears.cut(cyl(4.5,4,x+dx,y+dy,4+20.05))
                motor_mounts.append((x+dx,y+dy))
        shaft=cyl(p['shaft_diameter_allowance_mm'],p['shaft_projection_allowance_mm'],x,y+direction*p['shaft_offset_mm'],4+h)
        components[name+'_servo_reference']=body.union(ears).union(shaft).rotate((x,0,height/2),(x,1,height/2),180).val()
        ear_keepouts[name]=ears.rotate((x,0,height/2),(x,1,height/2),180).val()
        s=spool(grooves).translate((x,y+direction*p['shaft_offset_mm'],sz)).rotate((x,0,height/2),(x,1,height/2),180)
        components[name+'_spool']=s
        tangent_x=x+12.3;shaft_y=y+direction*p['shaft_offset_mm']
        for groove,local_z in enumerate([2.1] if grooves==1 else [2.1,5.1]):
            exit_z=height-(sz+(.5 if groove==0 else 6.6))
            ports.append({'group':name,'groove':groove,'x_mm':tangent_x,'y_mm':-8,'z_mm':exit_z})
            start=cq.Vector(tangent_x,shaft_y,height-(sz+local_z));end=cq.Vector(tangent_x,-14,exit_z)
            delta=end-start
            cords[f'{name}_cord_{groove}']=cq.Solid.makeCylinder(.3,delta.Length,start,delta.normalized())
    # Five lined cord exits: tube seats stop at a shoulder, rather than falling into the box.
    for port in ports:
        x,z=port['x_mm'],port['z_mm']
        pad=box(8,6,5.8,x,-11,z-2.9)
        base=base.union(pad)
    for port in ports:
        x,z=port['x_mm'],port['z_mm']
        base=base.cut(cq.Workplane('XY').newObject([along_y(.75,-15,-7,x,z)]))
        base=base.cut(cq.Workplane('XY').newObject([along_y(2.2,-12,-7,x,z)]))
    # Rear vertical carrier keeps the footprint short; two accessible floor screws hold it.
    carrier=box(80,2,38,0,-99.5,6).union(box(80,12,2,0,-95,4))
    # A stepped top leaves the lid switches clear while supporting the taller Nano.
    carrier=carrier.cut(box(35,4,25,-9.5,-99.5,28))
    for x in [-36,36]:
        base=base.cut(cyl(3.4,9,x,-95,-1)).cut(cq.Workplane('XY').polygon(6,6.6).extrude(2.5).translate((x,-95,0)))
        carrier=carrier.cut(cyl(3.4,8,x,-95,2))
    components.update({
      'Nano_reference':box(45,8,18,-16,-94,8).val(),
      'EMG_conditioner_reference':box(22,10,35,21,-93,8).val(),
      'logic_regulator_reference':box(12.7,4,10.2,-34,-95,30).val(),
      'power_distribution_allowance':box(14,6,8,0,-20,5).val(),
      'main_switch_allowance':box(20,16,20,-17,-92,roof-20).val(),
      'arm_switch_allowance':box(10,10,12,0,-95,roof-12).val(),
    })
    # Carrier tie slots flank each board; no invented PCB mounting-hole pattern.
    for x,z in [(-39,17),(8,17),(8,34),(34,17),(34,34),(-39,33),(-28,33)]:
        carrier=carrier.cut(box(2,6,5,x,-99.5,z))
    # Cable entries have space for measured grommets; power comes from an external fused supply.
    base=base.cut(cq.Workplane('XY').newObject([along_y(4,-12,-6,0,20)]))
    sidehole=cq.Solid.makeCylinder(4,8,cq.Vector(42,-93,30),cq.Vector(1,0,0))
    base=base.cut(cq.Workplane('XY').newObject([sidehole]))
    bosses=[(-41.5,-82),(41.5,-82),(-41.5,-13),(26,-13)]
    for x,y in bosses:
        base=base.union(cyl(8,roof,x,y,0)).cut(cyl(3.4,roof+2,x,y,-1))
        base=base.cut(cq.Workplane('XY').polygon(6,6.6).extrude(2.5).translate((x,y,0)))
    lid=rounded(94,96,4,0,centre_y,roof)
    for shape in upper_seats:lid=lid.union(cq.Workplane("XY").newObject([shape]))
    # Ties are no longer the primary hanging restraint. Four M3 through-bolts
    # per motor use the drawing's 49.5 x 10 mm ear-hole pattern.
    ear_top=height-(4+20.55)
    motor_heads={}
    for i,(x,y) in enumerate(motor_mounts):
        lid=lid.union(cyl(7,roof-ear_top,x,y,ear_top))
        lid=lid.cut(cyl(3.4,height-ear_top+2,x,y,ear_top-1))
        lid=lid.cut(cq.Workplane('XY').center(x,y).polygon(6,6.6).extrude(3).translate((0,0,height-2.6)))
        # Diameter 6 x 3 mm pan-head allowance below each mounting ear.
        motor_heads[f'motor_M3_head_{i}']=cyl(6,3,x,y,ear_top-5.5).val()
    components.update(motor_heads)
    # Locate the lid with four short tabs rather than a ring that could hit the boards.
    for x,y,w,l in [(-43,-56,1.5,18),(43,-56,1.5,18),(35,-99.5,14,1.5),(0,-12.5,14,1.5)]:
        lid=lid.union(box(w,l,2,x,y,roof-2))
    for x,y in bosses:lid=lid.cut(cyl(3.4,9,x,y,roof-3))
    for x,y,d in [(-17,-92,12.2),(0,-95,6.2)]:lid=lid.cut(cyl(d,10,x,y,roof-3))
    for x in [-14,0,14]:
        lid=lid.cut(cq.Workplane('XY').center(x,-15).slot2D(10,2.5,angle=0).extrude(5).translate((0,0,roof-1)))
    parts={'box_base':base.val(),'box_lid':lid.val(),'rear_board_carrier':carrier.val()}
    named={**parts,**components,**cords}
    collisions=[]
    items=list(named.items())
    for i,(n,a) in enumerate(items):
        for nn,b in items[i+1:]:
            v=overlap(a,b)
            if v>.001:collisions.append([n,nn,v])
    keepout_hits=[]
    for n,a in ear_keepouts.items():
        for nn,b in {**parts,**{k:v for k,v in components.items() if not k.startswith(n)}}.items():
            v=overlap(a,b)
            if v>.001:keepout_hits.append([n,nn,v])
    report={'status':'UNFITTED_LOW_TENDON_INVERTED_MOTOR_CARTRIDGE','profile':p,
      'box_body_size_mm':[94,96,height],'box_deck_global_z_mm':deck,
      'lid_underside_local_z_mm':roof,'original_upright_spool_base_local_z_mm':sz,'paired_drum_lowest_local_z_mm':height-sz-7.2,
      'motor_mount_holes_local_xy_mm':motor_mounts,'motor_ear_top_local_z_mm':ear_top,'ports_local_mm':ports,'collisions_mm3':collisions,'ear_keepout_intersections_mm3':keepout_hits,
      'parts':{},'components':{n:bounds(s) for n,s in components.items()},
      'scope':'Original hand and arm adapter unchanged. Motors inverted inside case; cords exit low, on the outside of the arm shell. No claimed measured force improvement, horn fit, strength or wearer fit.'}
    print('Collisions',collisions,'Keep-outs',keepout_hits,flush=True)
    (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not collisions and not keepout_hits,'Resolve packaging intersections'
    print_parts={**parts,'two_groove_drum':spool(2),'thumb_drum':spool(1)}
    for n,shape in print_parts.items():
        assert shape.isValid() and len(shape.Solids())==1,n
        b=shape.BoundingBox();q=shape.translate((0,0,-b.zmin))
        for ext in ['step','stl']:cq.exporters.export(q,str(out/f'{n}.{ext}'),tolerance=.08,angularTolerance=.15)
        mesh=trimesh.load_mesh(out/f'{n}.stl');assert mesh.is_watertight and mesh.volume>0,n
        report['parts'][n]={'one_valid_solid':True,'watertight':True,'assembly_local_zmin_mm':b.zmin,'size_mm':mesh.extents.tolist(),'quantity':2 if n=='two_groove_drum' else 1}
    # Export a physical carrier, sized by explicit placeholder dimensions.
    arm=make_arm_adapter(p,deck)
    receiver=make_receiver(p['hand_scale_percent']/100).val()
    arm=arm.cut(receiver).cut(receiver.translate((0,0,.2)))
    global_named={n:s.translate((0,0,deck)) for n,s in named.items()}
    global_named.update({'arm_adapter':arm,'palm_receiver':receiver})
    for n,shape in [('arm_adapter',arm),('palm_receiver',receiver)]:
        assert shape.isValid() and len(shape.Solids())==1,n
        zmin=shape.BoundingBox().zmin
        for ext in ['step','stl']:cq.exporters.export(shape.translate((0,0,-zmin)),str(out/f'{n}.{ext}'),tolerance=.08,angularTolerance=.15)
        mesh=trimesh.load_mesh(out/f'{n}.stl');assert mesh.is_watertight and mesh.volume>0,n
        report['parts'][n]={'one_valid_solid':True,'watertight':True,'assembly_global_zmin_mm':zmin,'size_mm':mesh.extents.tolist(),'quantity':1}
    interfaces=[]
    for n,s in [('arm_adapter',arm),('palm_receiver',receiver)]:
        for nn,q in global_named.items():
            if nn==n:continue
            v=overlap(s,q)
            if v>.001:interfaces.append([n,nn,v])
    report['adapter_intersections_mm3']=interfaces
    print('Adapter intersections',interfaces,flush=True)
    (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not interfaces
    lumen=along_y(p['adapter_inner_radius_mm'],-24-p['adapter_length_mm'],-44,0,p['cuff_axis_z_mm'])
    report['lumen_intersections_mm3']={n:overlap(s,lumen) for n,s in global_named.items() if overlap(s,lumen)>.001}
    assert not report['lumen_intersections_mm3'],report['lumen_intersections_mm3']
    source_hand={n:s.val().scale(p['hand_scale_percent']/100) for n,s in {**original_hand,**posed_thumb()}.items()}
    report['hand_pose_checks']=[]
    for t in [v/12 for v in range(13)]:
        mcp,pip,tr,tp=60*t,10+60*t,-60-30*t,10+30*t
        posed_parts={n:q.val().scale(p['hand_scale_percent']/100) for n,q in {**posed(mcp,pip),**posed_thumb(tr,tp)}.items()}
        hits=[]
        for n,a in posed_parts.items():
            for nn,b in global_named.items():
                v=overlap(a,b)
                if v>.001:hits.append([n,nn,v])
        report['hand_pose_checks'].append({'MCP':mcp,'PIP':pip,'thumb_root':tr,'thumb_tip':tp,'box_intersections_mm3':hits})
        assert not hits
    # The exact original flat guard is retained separately, without nonlinear deformation.
    source=R.parent/'phoenix_v3/exports/original_arm_guard.step'
    guard=cq.importers.importStep(str(source)).val()
    cq.exporters.export(guard,str(out/'original_flat_gauntlet_reference.step'))
    palette=[{'bounds':bounds(s),'color':[62,132,112]} for n,s in global_named.items() if 'reference' in n]
    palette += [{'bounds':bounds(s),'color':[184,127,62]} for n,s in global_named.items() if 'spool' in n]
    for mode,omit in [('complete',set()),('open',{'box_lid'}),('box_only',set()),('drive_detail',set())]:
        show={n:s for n,s in global_named.items() if n not in omit}
        if mode in ['complete','open']:show.update(source_hand)
        elif mode=='box_only':show={n:s for n,s in show.items() if n not in ['arm_adapter','palm_receiver']}
        else:show={n:s for n,s in show.items() if any(k in n for k in ['servo_reference','spool','cord_'])}
        file=out/f'{mode}.step';cq.exporters.export(cq.Compound.makeCompound(list(show.values())),str(file))
        actual=cq.importers.importStep(str(file)).solids().vals()
        for n,s in show.items():
            matches=[a for a in actual if np.allclose(bounds(a),bounds(s),atol=.0001,rtol=0)]
            assert len(matches)==1,(mode,n)
        render(file,out/f'{mode}_preview.png',title=f'Phoenix v3 · bottom tendon drive · {mode.replace("_"," ")}',solid_colors=palette,view=(-145,-25) if mode=='drive_detail' else (-145,28))
    axis_checks=[]
    for name,x,y,direction,grooves in stations:
        axes=[]
        for shape,radius in [(components[name+'_servo_reference'],p['shaft_diameter_allowance_mm']/2),(components[name+'_spool'],12)]:
            found=[]
            for f in shape.Faces():
                if f.geomType()=='CYLINDER':
                    c=BRepAdaptor_Surface(f.wrapped).Cylinder();axis=c.Axis();q=axis.Location()
                    if abs(c.Radius()-radius)<1e-5 and abs(axis.Direction().Z())>.99:found.append((q.X(),q.Y()))
            assert found,name
            assert all(np.allclose(found[0],v,atol=1e-5) for v in found)
            axes.append(found[0])
        error=math.dist(*axes);assert error<1e-5
        axis_checks.append({'group':name,'axis_error_mm':error,'reference_servo_axis_xy':axes[0],'drum_axis_xy':axes[1]})
    report['shaft_axis_checks']=axis_checks
    report['transmission']={'paired_drive':'Two separate grooves per paired servo; fixed coupled take-up, no floating equaliser',
      'effective_radius_mm':12.3,'ideal_travel_at_assumed_160deg_mm':12.3*math.radians(160),
      'candidate_motor':'FT5425BL replacement','evaluated_supply_V':[6,7.4,8.4],'owned_motor_fit_verified':False}
    report['source_sha256']={(str(q.relative_to(R.parent.parent)) if q.is_relative_to(R.parent.parent) else str(q)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [Path(__file__),profile_path,R.parent/'upstream/phoenix_v3.step',R.parent/'forearm/hand.py',R.parent/'forearm/thumb_mount.py',R/'arm_adapter.py',R.parent/'sizing/adapter.py']}
    report['output_sha256']={q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in out.iterdir() if q.suffix in ['.step','.stl','.png']}
    (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Exported bottom-drive cartridge, seven print types and 13 sampled hand poses.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=R/'profile.json')
    parser.add_argument('--output',type=Path,default=R/'exports')
    a=parser.parse_args();build(a.profile.resolve(),a.output.resolve())
