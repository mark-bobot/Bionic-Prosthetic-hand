"""Integrated forearm prototype, revision B. Run after build.py.
CC BY 4.0. Published PCB outlines + explicitly assumed component heights.
"""
from pathlib import Path
import json, math
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parent; O=R/'exports'
def box(l,w,h,x=0,y=0,z=0):
 return cq.Workplane('XY').box(l,w,h,centered=(True,True,False)).translate((x,y,z))
def cyl(d,h,x,y,z):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))
# The bay begins at the existing plate's x=38 edge. 1 mm overlap joins bases.
base=cq.importers.importStep(str(O/'servo_carrier.step'))
bay=box(121,110,4,97.5)
base=base.union(bay)
wall=box(120,110,34,98,0,4).cut(box(114,104,35,98,0,4))
base=base.union(wall)
# Four M3 through-bolts into captive hex nuts. Nut insertion is from underside.
bosses=[(42,-46),(149,-46),(42,46),(149,46)]
for x,y in bosses:
 base=base.union(cyl(8,34,x,y,4))
 base=base.cut(cyl(3.4,43,x,y,-1))
 nut=cq.Workplane('XY').polygon(6,6.6).extrude(2.5).translate((x,y,0))
 base=base.cut(nut)
# COMPONENT RECORD: outer installed envelopes, not exact manufacturer CAD.
components={
 'Nano':dict(size=[45,18,19],centre=[70,31],z=7,source='Arduino outline; installed height assumed',color='#26888b'),
 'EMG':dict(size=[35,22,10],centre=[117,31],z=7,source='DFRobot outline; component height assumed',color='#2c9790'),
 'servo_regulator':dict(size=[40.6,20.3,7.6],centre=[68,0],z=7,source='Pololu published assembled envelope, excluding added connectors',color='#5264bb'),
 'logic_regulator':dict(size=[12.7,10.2,4],centre=[104,0],z=7,source='Pololu outline; 4 mm height allowance',color='#5264bb'),
 'battery':dict(size=[70,32,22],centre=[82,-32],z=7,source='Assumed protected pack envelope; no exact pack selected',color='#d9a54b'),
 'fuse_holder':dict(size=[14,28,12],centre=[135,-32],z=7,source='Assumed insulated inline holder',color='#ba7867'),
 'distribution':dict(size=[12,20,14],centre=[140,0],z=7,source='Assumed insulated soldered distribution block',color='#ba7867'),
 'capacitor':dict(size=[10,10,20],centre=[123,0],z=7,source='Assumed 1000 uF radial capacitor envelope',color='#ba7867'),
 'main_switch':dict(size=[16,20,20],centre=[145,31],z=18,source='Assumed 12 mm panel-bushing switch; body below lid',color='#a34655'),
 'arm_switch':dict(size=[10,10,12],centre=[145,-14],z=26,source='Assumed 6 mm panel-bushing switch; body below lid',color='#a34655'),
}
# Low mounting pads avoid inventing PCB mounting-hole positions.
# Adhesive-backed nonconductive hook-and-loop fixes boards to pads; lid retains nothing.
for name,c in components.items():
 if name.endswith('switch'):continue
 l,w,h=c['size'];x,y=c['centre']
 base=base.union(box(l-2,w-2,2,x,y,4))
 # Envelope starts at 7 mm: allow 1 mm insulating mounting tape above the pad.
# Battery pocket lips; 0.5 mm end clearance and a removable soft strap.
# Lips at ends only, clear of the lid screw boss at x42,y-46.
for x in [45.5,118.5]:
 base=base.union(box(2,28,6,x,-32,4))
# Battery strap floor slots, 10 mm strap. No rigid compression of the cell pouch.
for y in [-50,-14]:base=base.cut(box(12,2,5,82,y,-.5))
# A second strap station supports the electronics end of the longer base.
for y in [-28,28]:base=base.cut(box(3,26,5,151,y,-.5))
# Lid vents provide airflow; pads insulate the board undersides.
# Pass-through between motor area and electronics. Upper slot has lid-open access.
base=base.cut(box(7,18,14,39,0,10))
# USB access at the motor-side wall and electrode cable at outer side.
base=base.cut(box(7,14,12,39,31,10))
base=base.cut(box(16,7,10,117,53.5,9))
# Wire guides in the corridors, not in component footprints.
for x,y in [(94,14),(94,-12),(150,14),(52,14)]:
 base=base.union(box(2,4,5,x,y,4))
# Removable vented lid and underside locating lip.
lid=box(120,110,3,98,0,38)
lip=box(113.2,103.2,2,98,0,36).cut(box(109.2,99.2,3,98,0,35.5))
# Keep lip clear of the four bosses; clearance pockets do not touch screw holes.
for x,y in bosses:lip=lip.cut(cyl(10,5,x,y,35))
lip=lip.cut(box(18,22,3,145,31,35.5))
lid=lid.union(lip)
for x,y in bosses:lid=lid.cut(cyl(3.4,8,x,y,35))
# Switch holes, capacitor/board ventilation and cable exit clearance.
for d,x,y in [(12.2,145,31),(6.2,145,-14)]:lid=lid.cut(cyl(d,8,x,y,35))
for x in [52,58,64,70,76,82]: lid=lid.cut(box(2,18,8,x,0,35))
for x in [102,110,118,126]:lid=lid.cut(box(2,14,8,x,31,35))
# Clearance in lip at side cable opening.
lid=lid.cut(box(16,7,3,117,53.5,35.5))
assert base.intersect(lid).val().Volume()<1e-5, 'base/lid clash'
# Flat exterior face on print bed; locating lip points upward.
parts={'integrated_base':base,'electronics_lid':lid.rotate((0,0,0),(1,0,0),180).translate((0,0,41))}
checks={}
for n,p in parts.items():
 assert len(p.solids().vals())==1,(n,len(p.solids().vals()))
 assert p.val().isValid(),n
 cq.exporters.export(p,str(O/f'{n}.step'))
 cq.exporters.export(p,str(O/f'{n}.stl'),tolerance=.08,angularTolerance=.15)
 m=trimesh.load_mesh(O/f'{n}.stl'); assert m.is_watertight and m.volume>0,n
 checks[n]={'size_mm':m.extents.tolist(),'watertight':bool(m.is_watertight),'volume_mm3':float(m.volume)}
models={}
for n,c in components.items():
 l,w,h=c['size'];x,y=c['centre'];models[n]=box(l,w,h,x,y,c['z'])
collisions=[]
for n,m in models.items():
 for fixture,shape in [('base',base),('lid',lid)]:
  volume=m.intersect(shape).val().Volume()
  if volume>1e-5:collisions.append([n,fixture,volume])
for i,(n,m) in enumerate(models.items()):
 for name,other in list(models.items())[i+1:]:
  volume=m.intersect(other).val().Volume()
  if volume>1e-5:collisions.append([n,name,volume])
assert not collisions,collisions
assembly=cq.Assembly(name='integrated_forearm_rev_b')
assembly.add(base,name='base',color=cq.Color(.22,.42,.55))
assembly.add(lid,name='lid',color=cq.Color(.6,.7,.77,.5))
render=[(base,'#5b8299')]
for n,m in models.items():
 assembly.add(m,name=n);render.append((m,components[n]['color']))
spool=cq.importers.importStep(str(O/'two_groove_spool.step'))
for i,y in enumerate([-34,0,34]):
 motor=box(40,20,40.5,0,y,4);drum=spool.translate((-10,y,47.5))
 assert motor.intersect(base).val().Volume()<1e-5
 assert drum.intersect(base).val().Volume()<1e-5
 assembly.add(motor,name=f'servo_{i}');assembly.add(drum,name=f'spool_{i}')
 render.extend([(motor,'#333d46'),(drum,'#eaaa41')])
cq.exporters.export(assembly.toCompound(),str(O/'integrated_assembly.step'))
checks['component_collisions']=collisions
checks['components']=components
checks['overall_envelope_mm']=[196,110,59.5]
(R/'integration_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
# Clear labelled layout; lid omitted for access to parts.
fig,ax=plt.subplots(figsize=(14,8));ax.set_aspect('equal');ax.set_xlim(-45,167);ax.set_ylim(-62,65)
ax.add_patch(Rectangle((-38,-55),196,110,facecolor='#e7edf1',edgecolor='#456578',linewidth=2))
ax.plot([38,38],[-55,55],color='#456578',lw=2)
for n,c in components.items():
 l,w,h=c['size'];x,y=c['centre'];ax.add_patch(Rectangle((x-l/2,y-w/2),l,w,facecolor=c['color'],alpha=.75))
 label={'servo_regulator':'5 V servo\nregulator','logic_regulator':'logic\nreg.','distribution':'power\nblock','capacitor':'cap','fuse_holder':'fuse','main_switch':'main\nswitch','arm_switch':'arm'}.get(n,n)
 ax.text(x,y,label,ha='center',va='center',fontsize=9,color='white' if n!='battery' else '#172c39')
for i,y in enumerate([-34,0,34]):
 ax.add_patch(Rectangle((-20,y-10),40,20,facecolor='#394650'));ax.text(0,y,['thumb','index + middle','ring + little'][i],ha='center',va='center',color='white',fontsize=9)
# Suggested routing corridors; representative routing space, not real cable CAD.
ax.plot([41,94,94,150],[-12,-12,14,14],color='#e16f35',lw=2,ls='--')
ax.set_title('Revision B • integrated component layout (lid removed)',fontsize=18,pad=18)
ax.set_xlabel('mm');ax.set_ylabel('mm');ax.grid(alpha=.12)
fig.text(.1,.025,'196 × 110 mm base · dashed line: wiring corridor · battery and switch sizes are assumed envelopes',fontsize=11)
fig.savefig(O/'integrated_layout.png',dpi=160);plt.close(fig)
fig=plt.figure(figsize=(14,8));ax=fig.add_subplot(111,projection='3d')
faces=[];colors=[]
for p,col in render:
 v,f=p.val().tessellate(.5);v=[t.toTuple() for t in v]
 faces.extend([[v[j] for j in t] for t in f]);colors.extend([col]*len(f))
ax.add_collection3d(Poly3DCollection(faces,facecolor=colors,edgecolor='none',zsort='average'))
ax.set_xlim(-40,160);ax.set_ylim(-58,58);ax.set_zlim(0,65);ax.set_box_aspect((200,116,65));ax.view_init(60,-66)
ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_zlabel('mm');ax.set_title('Integrated forearm pack • cover removed',fontsize=18)
fig.text(.1,.03,'Reference envelopes shown. No physical fit, wiring bend-radius or thermal validation yet.',fontsize=11)
fig.savefig(O/'integrated_preview.png',dpi=160);plt.close(fig)
print(json.dumps({k:v for k,v in checks.items() if k!='components'},indent=2))
