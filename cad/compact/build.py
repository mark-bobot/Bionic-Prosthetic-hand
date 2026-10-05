"""Original compact packaging study. mm. CC BY 4.0. Not a fitted socket.
Run using CadQuery 2.8.0 after ../build.py. Actual servo model remains unknown.
"""
from pathlib import Path
import json, math
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parent;O=R/'exports';O.mkdir(exist_ok=True)
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def cyl(d,h,x,y,z):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))
def rounded(w,l,h,x,y,z,r=12):return box(w,l,h,x,y,z).edges('|Z').fillet(r)
base=rounded(94,160,4,0,68,0)
# Low motor retainers; rear cables and removable ties. Outer ears remain above walls.
for x in [-28,0,28]:
 wall=box(27,47,11,x,20,4).cut(box(21,41,12,x,20,4))
 wall=wall.cut(box(10,8,9,x,43,4))
 base=base.union(wall)
 for dy in [-5,45]:base=base.cut(box(6,3,6,x,dy,-1))
# Thin full guard. Cover is held using four through screws/nuts.
wall=rounded(94,160,58,0,68,4).cut(rounded(88,154,59,0,68,4,r=9))
base=base.union(wall)
bosses=[(-41,52),(41,52),(-41,140),(41,140)]
for x,y in bosses:
 base=base.union(cyl(8,58,x,y,4)).cut(cyl(3.4,70,x,y,-1))
 base=base.cut(cq.Workplane('XY').polygon(6,6.6).extrude(2.5).translate((x,y,0)))
# Side electrode and rear USB access, and front tendon exit window.
base=base.cut(box(18,8,12,-22,147,35))
base=base.cut(box(8,16,12,46,115,34))
base=base.cut(box(78,8,18,0,-11,43))
# Removable electronics tray above battery, with M3 through bolts to underside nuts.
tray=box(74,68,2,0,106,30)
posts=[(-35,76),(35,76),(-35,136),(35,136)]
for x,y in posts:
 base=base.union(cyl(6,26,x,y,4)).cut(cyl(3.4,35,x,y,-1))
 base=base.cut(cq.Workplane('XY').polygon(6,6.6).extrude(2.5).translate((x,y,0)))
 tray=tray.cut(cyl(3.4,5,x,y,29))
# Wire passage on the right side of tray, away from board footprints.
tray=tray.cut(box(9,22,4,31,109,29))
C={
 'battery':([70,32,22],0,112,7,'#d5a451'),
 'servo_regulator':([40.6,20.3,7.6],-12,60,7,'#697ac3'),
 'fuse_holder':([14,28,12],25,66,7,'#af7963'),
 'distribution':([12,20,14],-22,83,7,'#af7963'),
 'capacitor':([10,10,20],0,80,7,'#af7963'),
 'Nano':([18,45,19],-22,109,33,'#32988e'),
 'EMG':([22,35,10],7,115,33,'#32988e'),
 'logic_regulator':([12.7,10.2,4],20,86,33,'#697ac3'),
 'main_switch':([16,20,20],23,58.1,42,'#aa5767'),
 'arm_switch':([10,10,12],23,74,50,'#aa5767'),
}
for name,(sz,x,y,z,c) in C.items():
 if z==7:base=base.union(box(sz[0]-2,sz[1]-2,2,x,y,4))
# Battery strap through base, 10 mm webbing.
for y in [93,131]:base=base.cut(box(12,2,6,0,y,-1))
# Four fixture slots remain outside battery footprint. This is not a skin interface.
for x in [-40,40]:
 for y in [15,110]:base=base.cut(box(3,26,6,x,y,-1))
# Wrist bridge prototype pattern, matching hand.py after assembly rotation.
for x in [-18,18]:base=base.cut(cyl(4.4,6,x,-6,-1))
# Smooth rear roof: original 65 mm at motors, falling to 59 mm over rear boards.
def roof_cap(offset=0):
 points=[(y,62+3*math.cos(math.pi*(y-100)/30)) for y in range(125,99,-5)]
 profile=(cq.Workplane('YZ').moveTo(-30,-10).lineTo(170,-10).lineTo(170,59)
          .lineTo(130,59).spline(points,includeCurrent=True,tangents=[(-1,0),(-1,0)])
          .lineTo(-30,65).close().extrude(120).translate((-60,0,offset)))
 return profile
outer_cap=roof_cap();inner_cap=roof_cap(-3)
base=base.intersect(inner_cap)
lid=rounded(94,160,70,0,68,0).intersect(outer_cap).cut(inner_cap)
# Recess switch panel by 5 mm; switch bodies move down with its mounting face.
lid=lid.cut(rounded(28,46,12,23,66,56,r=4))
well=rounded(28,46,8,23,66,57,r=4).cut(rounded(24,42,7,23,66,60,r=2))
lid=lid.union(well)
for name in ['main_switch','arm_switch']:
 sz,x,y,z,c=C[name];C[name]=(sz,x,y,z-5,c)
# Counterbores assume heads <= 6 mm diameter and <= 2 mm high; verify thin seats.
for x,y in bosses:
 top=65 if y<100 else 59
 lid=lid.cut(cyl(3.4,12,x,y,top-10)).cut(cyl(6.4,2.2,x,y,top-2))
for name,d in [('main_switch',12.2),('arm_switch',6.2)]:
 _,x,y,_,_=C[name];lid=lid.cut(cyl(d,6,x,y,56))
# Rounded ventilation slots arranged as two compact groups.
def vent(x,y,length,z=54):
 return cq.Workplane('XY').center(x,y).slot2D(length,2.5,angle=90).extrude(14).translate((0,0,z))
for x in [-28,-22,-16,-10]:lid=lid.cut(vent(x,61,18))
for x in [-28,0,28]:lid=lid.cut(vent(x,22,18))
# Inspect the selected screw head and switch bushing lengths on a fit coupon.
models={n:box(*sz,x,y,z) for n,(sz,x,y,z,c) in C.items()}
spool=cq.importers.importStep(str(R.parent/'exports/two_groove_spool.step'))
for i,x in enumerate([-28,0,28]):
 # Ear envelope is an explicit layout allowance, not an identified servo specification.
 models[f'servo_{i}']=box(20,40,40.5,x,20,4).union(box(24,54,6,x,20,34))
 models[f'spool_{i}']=spool.translate((x,30 if i==1 else 10,47.5))
# Export valid parts at Z=0. Curved lid needs slicer orientation/support review.
parts={'compact_base':base,'compact_tray':tray.translate((0,0,-30)), 'compact_lid':lid.translate((0,0,-56))}
report={'component_envelopes':C,'checks':{},'collisions':[],'socket_status':'Not designed: mounting use and arm dimensions required','profile':{'outer_corner_radius_mm':12,'front_height_mm':65,'rear_height_mm':59,'switch_recess_mm':5,'cover_vertical_thickness_mm':3}}
for n,p in parts.items():
 assert len(p.solids().vals())==1 and p.val().isValid(),n
 cq.exporters.export(p,str(O/f'{n}.step'));cq.exporters.export(p,str(O/f'{n}.stl'),tolerance=.08,angularTolerance=.15)
 m=trimesh.load_mesh(O/f'{n}.stl');assert m.is_watertight and m.volume>0,n
 report['checks'][n]={'size_mm':m.extents.tolist(),'watertight':True,'volume_mm3':float(m.volume)}
fixtures={'base':base,'tray':tray,'lid':lid}
allshapes={**fixtures,**models}
for i,(n,p) in enumerate(allshapes.items()):
 for nn,pp in list(allshapes.items())[i+1:]:
  v=p.intersect(pp).val().Volume()
  if v>1e-5:report['collisions'].append([n,nn,v])
(R/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
assert not report['collisions'],report['collisions']
assembly=cq.Assembly(name='compact_pack_unfitted')
for n,p in allshapes.items():assembly.add(p,name=n)
cq.exporters.export(assembly.toCompound(),str(O/'compact_assembly.step'))
# Transparent view shows the stacking study; all colours are reference envelopes.
fig=plt.figure(figsize=(10,12));ax=fig.add_subplot(111,projection='3d');faces=[];colors=[]
for n,p in allshapes.items():
 if n=='lid':continue
 if n=='base':color=(.3,.4,.47,.16)
 elif n=='tray':color=(.6,.65,.68,.25)
 elif n.startswith('servo'):color='#303d45'
 elif n.startswith('spool'):color='#dfad50'
 else:color=C[n][4]
 v,f=p.val().tessellate(.65);v=[vv.toTuple() for vv in v]
 faces.extend([[v[j] for j in ff] for ff in f]);colors.extend([color]*len(f))
ax.add_collection3d(Poly3DCollection(faces,facecolor=colors,edgecolor='none'))
ax.set_xlim(-50,50);ax.set_ylim(-15,150);ax.set_zlim(0,68);ax.set_box_aspect((100,165,68));ax.view_init(55,-65)
ax.set_title('Rounded housing — cover removed\n94 × 160 mm; 65 mm motor end / 59 mm rear; arm interface pending')
ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_zlabel('mm')
fig.savefig(O/'compact_preview.png',dpi=160);plt.close(fig)
print(json.dumps({'checks':report['checks'],'collisions':report['collisions']},indent=2))
