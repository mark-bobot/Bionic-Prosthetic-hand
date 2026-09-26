"""Editable add-on CAD. Units: mm. CC BY 4.0; see root LICENSE.md.
Run with CadQuery 2.8.0. This carrier does not alter the Phoenix mesh.
"""
from pathlib import Path
import json
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'exports'; OUT.mkdir(exist_ok=True)
# Body envelope is from DS3225 data; allowance and strap retention are design choices.
BODY_L,BODY_W,BODY_H=40.,20.,40.5
CLEARANCE=.5
PITCH=34.
PLATE_L,PLATE_W,BASE=76.,110.,4.
WALL=3.
RADIUS=12.             # Radius to groove floor, not including tendon thickness.
CENTRES=[-PITCH,0,PITCH]

def box(x,y,z,cx=0,cy=0,cz=0):
 return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate((cx,cy,cz))
def hole(part,d,x,y,z=-1,h=100):
 return part.cut(cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z)))

plate=box(PLATE_L,PLATE_W,BASE).edges('|Z').fillet(3)
for y in CENTRES:
 outer=box(BODY_L+2*CLEARANCE+2*WALL,BODY_W+2*CLEARANCE+2*WALL,11,cy=y,cz=BASE)
 inner=box(BODY_L+2*CLEARANCE,BODY_W+2*CLEARANCE,12,cy=y,cz=BASE)
 plate=plate.union(outer.cut(inner))
 # Cable opening at the rear end, through the short retaining wall.
 plate=plate.cut(box(8,8,8,cx=23,cy=y,cz=BASE))
 # One 4.8 mm cable tie passes under the floor and over the rear of each body.
 for dy in [-16,16]: plate=plate.cut(box(5.6,3,BASE+2,cx=12,cy=y+dy,cz=-1))
# Four 25 mm strap slots. The base sits over padding; straps go round a test fixture/cuff.
for x in [-32,32]:
 for y in [-31,31]: plate=plate.cut(box(3,26,BASE+2,cx=x,cy=y,cz=-1))

# Two winding grooves. Use one per servo, feeding paired groups via equalisers.
spool=cq.Workplane('XY').circle(RADIUS).extrude(12)
for z in [0,5.25,10.5]:
 spool=spool.union(cq.Workplane('XY').circle(RADIUS+2).extrude(1.5).translate((0,0,z)))
spool=hole(spool,6,0,0) # Tool access to the metal horn retaining screw.
# Bolt to an actual metal horn. No printed servo spline.
for x in [-8,8]:
 spool=spool.cut(cq.Workplane('XY').center(x,0).slot2D(5,2.3,angle=0).extrude(14).translate((0,0,-1)))
# Radial anchor holes for knots, one in each groove.
for z in [3.4,8.6]:
 spool=spool.cut(cq.Workplane('YZ').center(0,z).circle(1).extrude(30,both=True))

# Tie-on fairlead: PTFE tubes press through horizontal 2.2 mm bores.
fairlead=box(14,20,8)
for y in [-4,4]: fairlead=fairlead.cut(cq.Workplane('YZ').center(y,4).circle(1.1).extrude(20,both=True))
for y in [-8,8]: fairlead=fairlead.cut(box(6,2,10,cy=y,cz=-1))

equaliser=box(26,8,4).edges('|Z').fillet(2)
for x in [-10,0,10]: equaliser=hole(equaliser,2.4,x,0)

parts={'pair_equaliser':equaliser,'servo_carrier':plate,'two_groove_spool':spool,'tendon_fairlead':fairlead}
report={}
for name,p in parts.items():
 assert len(p.solids().vals())==1, name
 assert p.val().isValid(),name
 cq.exporters.export(p,str(OUT/f'{name}.step'))
 cq.exporters.export(p,str(OUT/f'{name}.stl'),tolerance=.06,angularTolerance=.15)
 mesh=trimesh.load_mesh(OUT/f'{name}.stl')
 assert mesh.is_watertight and mesh.volume>0,name
 report[name]={'bounds_mm':mesh.extents.tolist(),'volume_mm3':float(mesh.volume),'watertight':bool(mesh.is_watertight)}

# Assembly is an envelope check only: rectangular reference motors and separate spools.
assembly=cq.Assembly(name='forearm_carrier')
assembly.add(plate,name='carrier',color=cq.Color(.2,.4,.55))
render=[(plate,'#557e97')]
for i,y in enumerate(CENTRES):
 motor=box(BODY_L,BODY_W,BODY_H,cy=y,cz=BASE)
 assert motor.intersect(plate).val().Volume()<1e-5
 assembly.add(motor,name=f'servo_envelope_{i}',color=cq.Color(.18,.18,.18))
 # Shaft offset is a layout assumption; verify on actual unit before assembly.
 mounted=spool.translate((-10,y,BASE+BODY_H+3))
 assembly.add(mounted,name=f'spool_{i}',color=cq.Color(.9,.55,.18))
 render.extend([(motor,'#333d46'),(mounted,'#eba647')])
cq.exporters.export(assembly.toCompound(),str(OUT/'carrier_assembly.step'))
fig=plt.figure(figsize=(12,8),facecolor='#f6f7f8'); ax=fig.add_subplot(111,projection='3d')
for shape,col in render:
 verts,faces=shape.val().tessellate(.3)
 xyz=[v.toTuple() for v in verts]
 ax.add_collection3d(Poly3DCollection([[xyz[j] for j in face] for face in faces],facecolor=col,edgecolor='none',alpha=1))
ax.set_xlim(-45,45); ax.set_ylim(-60,60); ax.set_zlim(0,65); ax.set_box_aspect((90,120,65)); ax.view_init(30,-55)
ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_zlabel('mm')
ax.set_title('Three-servo forearm carrier — reference fit',fontsize=17,pad=20)
fig.text(.08,.05,'76 × 110 mm base · 40 × 20 × 40.5 mm servo envelopes\nMetal horns, straps, wiring and tendons omitted. Physical fit is untested.',fontsize=11)
fig.savefig(OUT/'carrier_preview.png',dpi=160);plt.close(fig)
(ROOT/'cad_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

# Dimensioned top-view drawing of the carrier itself.
fig,ax=plt.subplots(figsize=(8,10));
mesh=trimesh.load_mesh(OUT/'servo_carrier.stl')
from matplotlib.collections import PolyCollection
ax.add_collection(PolyCollection(mesh.triangles[:,:,:2],facecolors='#d5e6ef',edgecolors='#59788a',linewidths=.15))
ax.set_xlim(-43,43);ax.set_ylim(-60,60);ax.set_aspect('equal');ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_title('Carrier top view — 76 × 110 mm')
fig.savefig(OUT/'carrier_top.png',dpi=150);plt.close(fig)
