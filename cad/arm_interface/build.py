"""Right-arm open saddle and independently strapped EMG carrier. NOT a fitted socket.
CadQuery 2.8.0. mm. CC BY 4.0. Limb dimensions are placeholder fixture geometry.
"""
from pathlib import Path
import json
import numpy as np
from matplotlib.colors import to_rgb
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parent;O=R/'exports';O.mkdir(exist_ok=True)
P=json.loads((R/'parameters.json').read_text())
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def envelope(extra=0):
 return (cq.Workplane('XY').ellipse(P['distal_inner_width_mm']/2+extra,P['distal_inner_depth_mm']/2+extra)
   .workplane(offset=P['length_mm']).ellipse(P['proximal_inner_width_mm']/2+extra,P['proximal_inner_depth_mm']/2+extra)
   .loft().rotate((0,0,0),(1,0,0),90).translate((0,P['distal_y_mm'],P['centre_z_mm'])))
outer=envelope(P['wall_mm']);inner=envelope()
saddle=outer.cut(inner).cut(box(140,200,100,0,-95,P['open_edge_z_mm']-100))
# Dorsal ribs support the component housing; interior is cut again below.
for x in [-20,20]:saddle=saddle.union(box(10,114,34,x,-95,-30))
# Match existing 25 mm webbing slots in the compact housing (at global y=-45,-140).
for y in [-45,-140]:
 saddle=saddle.union(box(88,32,8 if y==-45 else 4,0,y,-4 if y==-45 else 0).edges('|Z').fillet(3))
 for x in [-40,40]:saddle=saddle.cut(box(3,26,12,x,y,-6))
# Independent support-strap ears along open ventral edges; 20 mm webbing.
for y in [-60,-140]:
 for x in [-35,35]:
  saddle=saddle.union(box(24,28,4,x,y,-44).edges('|Z').fillet(3))
  saddle=saddle.cut(box(3.5,22,8,42 if x>0 else -42,y,-46))
saddle=saddle.cut(inner)
# Front bridge steps below the existing wrist-cradle plate, retaining its strap-slot floor.
saddle=saddle.cut(box(78,24,6,0,-24,0))
# Separate probe carrier. Smooth soft retention across its BACK; contacts face out.
# Manufacturer board outline 22x35; thickness/contact protrusion must be measured.
w=P['electrode_board_width_mm'];l=P['electrode_board_length_mm']
carrier=box(w+8,l+8,2).edges('|Z').fillet(3)
wall=box(w+8,l+8,5,0,0,2).edges('|Z').fillet(3).cut(box(w+2,l+2,6,0,0,2))
carrier=carrier.union(wall)
# Open connector exit at one short end; verify real plug and bend radius.
carrier=carrier.cut(box(14,10,8,0,(l+8)/2,2))
for x in [-19,19]:
 carrier=carrier.union(box(12,28,2,x).edges('|Z').fillet(2))
 carrier=carrier.cut(box(3,22,4,-21 if x<0 else 21,0,-1))
# Cable-tie strain relief on back-side tab, away from electrode contact surface.
carrier=carrier.union(box(16,12,2,0,-(l+8)/2-4).edges('|Z').fillet(2))
for x in [-5,5]:carrier=carrier.cut(box(2.5,7,4,x,-(l+8)/2-4,-1))
parts={'right_open_saddle':saddle,'emg_band_carrier':carrier}
report={'status':P['status'],'parameters':P,'parts':{},'collisions':[]}
for name,p in parts.items():
 assert len(p.solids().vals())==1 and p.val().isValid(),name
 z=p.val().BoundingBox().zmin;q=p.translate((0,0,-z))
 cq.exporters.export(q,str(O/f'{name}.step'));cq.exporters.export(q,str(O/f'{name}.stl'),tolerance=.08,angularTolerance=.15)
 m=trimesh.load_mesh(O/f'{name}.stl');assert m.is_watertight and m.volume>0,name
 report['parts'][name]={'watertight':True,'size_mm':m.extents.tolist(),'volume_mm3':float(m.volume)}
# Assembly coords preserve the current Phoenix/housing datums.
pod=cq.importers.importStep(str(R.parent/'compact/exports/compact_assembly.step')).rotate((0,0,0),(0,0,1),180).translate((0,-30,4))
probe=box(w,l,P['electrode_thickness_assumed_mm'],0,0,2)
probe_pos=(0,-105,-78)
positioned_carrier=carrier.translate(probe_pos);positioned_probe=probe.translate(probe_pos)
shapes={'saddle':saddle,'housing':pod,'probe_carrier':positioned_carrier,'probe_envelope':positioned_probe}
for i,(n,p) in enumerate(shapes.items()):
 for nn,q in list(shapes.items())[i+1:]:
  v=p.intersect(q).val().Volume()
  if v>1e-4:report['collisions'].append([n,nn,v])
assert not report['collisions'],report['collisions']
# Check no hard geometry enters the unlined placeholder lumen; not a tissue-pressure check.
assert saddle.intersect(inner).val().Volume()<1e-4
report['interface']='Two existing 25 mm housing slots per station align with saddle slots; straps omitted'
report['skin_contact']='Probe shown separately under open side; vertical position and real contact protrusion unverified'
report['wrist_lock']='Not added; existing free pivot is not a load-approved connection'
(R/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
hand=cq.importers.importStep(str(R.parent/'phoenix_v3/exports/phoenix_motorised_reference.step'))
for n in ['saddle','probe_carrier','probe_envelope']:
 v=shapes[n].intersect(hand).val().Volume()
 assert v<1e-4,(n,'existing assembly',v)
report['existing_assembly_collision_check']='Passed for all new parts against full existing assembly'
(R/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
assembly=cq.Assembly(name='right_arm_unfitted_concept')
assembly.add(hand,name='existing_phoenix_and_housing')
for n in ['saddle','probe_carrier','probe_envelope']:assembly.add(shapes[n],name=n)
cq.exporters.export(assembly.toCompound(),str(O/'right_arm_reference.step'))
# Two views of attachment geometry. Phantom is a dimension reference, not a patient model.
fig=plt.figure(figsize=(13,7));
for panel,angle in enumerate([(25,-55),(-35,-55)],1):
 ax=fig.add_subplot(1,2,panel,projection='3d');faces=[];colors=[]
 for p,col in [(saddle,'#657d89'),(positioned_carrier,'#d5a04d'),(positioned_probe,'#b9bfc5')]:
  v,f=p.val().tessellate(.5);v=[a.toTuple() for a in v]
  tri=np.array([[v[j] for j in t] for t in f]);norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12)
  light=np.array([-.3,-.5,1]);light/=np.linalg.norm(light);shade=.4+.6*np.abs(norm@light)
  faces.extend(tri);colors.extend(np.array(to_rgb(col))[None,:]*shade[:,None])
 ax.add_collection3d(Poly3DCollection(faces,facecolors=colors,edgecolors='none'))
 ax.set(xlim=(-55,55),ylim=(-180,-15),zlim=(-85,10));ax.set_box_aspect((110,165,95));ax.view_init(*angle)
 ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_zlabel('mm')
 ax.set_title('Dorsal housing support' if panel==1 else 'Open underside and separate EMG carrier')
fig.suptitle('Right forearm attachment concept — placeholder dimensions, no fitted socket or wrist lock')
fig.tight_layout();fig.savefig(O/'arm_interface_preview.png',dpi=150);plt.close(fig)
print(json.dumps(report,indent=2))
