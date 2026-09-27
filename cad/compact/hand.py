"""Original minimal two-joint tendon hand, experimental geometry, CC BY 4.0.
Both handed variants exported. No fitted socket. Units mm.
"""
from pathlib import Path
import json, math
import cadquery as cq
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parent;O=R/'exports'
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def axle(d,w,x=0,y=0,z=6):return cq.Workplane('YZ').circle(d/2).extrude(w).translate((x-w/2,y,z))
def bore_y(d,l,x=0,y=0,z=2):return cq.Workplane('XZ').circle(d/2).extrude(l).translate((x,y+l,z))
def fork(y):
 p=None
 for x in [-6,6]:
  cheek=axle(10,4,x,y).union(box(4,10,12,x,y-5))
  p=cheek if p is None else p.union(cheek)
 return p.cut(axle(3.2,30,0,y))
def root():return axle(10,7.2).union(box(7.2,10,12,0,5)).cut(axle(3.2,30))
def proximal(L):
 p=root().union(box(16,L-16,12,0,L/2)).union(fork(L))
 p=p.cut(bore_y(2.2,L-16,0,8,2))
 for y in [12,L-12]:p=p.cut(axle(2,22,0,y,10))
 return p

def distal(L):
 body=box(16,L-8,12,0,(L+8)/2).edges('|Z').fillet(4)
 p=root().union(body).cut(bore_y(2.2,L-14,0,8,2))
 p=p.cut(axle(2.4,22,0,L-6,2)).cut(axle(2,22,0,12,10))
 return p
# Fingers bend toward -Z (palm side). Thumb is abducted and rotated for opposition.
def thumbplace(p):
 return p.translate((0,0,-6)).rotate((0,0,0),(0,1,0),-45).rotate((0,0,0),(0,0,1),50).translate((-47,25,6))
outline=[(-28,0),(28,0),(40,24),(40,72),(-40,72),(-40,24)]
palm=cq.Workplane('XY').polyline(outline).close().extrude(12)
for x in [-27,-9,9,27]:palm=palm.union(fork(78).translate((x,0,0)))
# Thumb clevis has a proximal bridge which overlaps the side of the palm.
thumbmount=fork(0).union(box(16,18,12,0,-18)).cut(axle(2,24,0,-14,10))
palm=palm.union(thumbplace(thumbmount))
# Palm-side relief for opposed thumb at 60 degrees, with clearance allowance.
palm=palm.cut(box(5,22,7.5,-39.5,35,-.5))
# Tendon exit/feed-through channels: straight palm lanes ending below MCP axes.
for x in [-27,-9,9,27]:palm=palm.cut(bore_y(2.2,65,x,8,2))
# Two M4 wrist plate holes, explicitly a prototype pattern, not a commercial connector.
for x in [-18,18]:palm=palm.cut(cq.Workplane('XY').center(x,10).circle(2.2).extrude(15))
# Dorsal elastic anchors, one per long finger.
for x in [-27,-9,9,27]:palm=palm.cut(cq.Workplane('XY').center(x,65).circle(1.2).extrude(15))
parts={'minimal_palm_right':palm,'minimal_palm_left':palm.mirror('YZ')}
layout=[('index',-27,35,30),('middle',-9,40,32),('ring',9,37,30),('little',27,28,25)]
models={'palm':palm}
for n,x,L,D in layout:
 parts[n+'_proximal']=proximal(L);parts[n+'_distal']=distal(D)
 models[n+'_proximal']=parts[n+'_proximal'].translate((x,78,0))
 models[n+'_distal']=parts[n+'_distal'].translate((x,78+L,0))
parts['thumb_distal']=distal(45)
models['thumb']=thumbplace(parts['thumb_distal'])
# Removable flat wrist bridge. Underside assembly is at Z=-4..0.
plate=box(48,34,4,0,4,-4).edges('|Z').fillet(3)
for x in [-18,18]:
 for y in [-6,10]:plate=plate.cut(cq.Workplane('XY').center(x,y).circle(2.2).extrude(6).translate((0,0,-5)))
parts['wrist_bridge']=plate.translate((0,0,4));models['wrist_bridge']=plate
report={'parts':{},'static_collisions':[], 'motion_checks':[], 'status':'Experimental hand; socket and physical validation absent'}
for n,p in parts.items():
 assert len(p.solids().vals())==1,(n,len(p.solids().vals()))
 assert p.val().isValid(),n
 # Parts with tilted thumb geometry are not promised support-free.
 b=p.val().BoundingBox();printpart=p.translate((0,0,-b.zmin))
 cq.exporters.export(printpart,str(O/f'{n}.step'));cq.exporters.export(printpart,str(O/f'{n}.stl'),tolerance=.06,angularTolerance=.12)
 m=trimesh.load_mesh(O/f'{n}.stl');assert m.is_watertight and m.volume>0,n
 report['parts'][n]={'size_mm':m.extents.tolist(),'watertight':True}
for i,(n,p) in enumerate(models.items()):
 for nn,pp in list(models.items())[i+1:]:
  v=p.intersect(pp).val().Volume()
  if v>1e-5:report['static_collisions'].append([n,nn,v])
# Sample synchronized MCP/PIP flexion poses; not exhaustive swept-volume validation.
for angle in [0,15,30,45,60]:
 for n,x,L,D in layout:
  prox=parts[n+'_proximal'].rotate((0,0,6),(1,0,6),-angle).translate((x,78,0))
  dist=parts[n+'_distal'].rotate((0,0,6),(1,0,6),-angle).translate((0,L,0)).rotate((0,0,6),(1,0,6),-angle).translate((x,78,0))
  for a,b,aa,bb in [('palm',n+'_proximal',palm,prox),(n+'_proximal',n+'_distal',prox,dist),('palm',n+'_distal',palm,dist)]:
   v=aa.intersect(bb).val().Volume()
   if v>1e-5:report['motion_checks'].append({'angle':angle,'parts':[a,b],'volume_mm3':v})
for angle in [0,15,30,45,60]:
 thumb=thumbplace(parts['thumb_distal'].rotate((0,0,6),(1,0,6),-angle))
 v=thumb.intersect(palm).val().Volume()
 if v>1e-5:report['motion_checks'].append({'angle':angle,'parts':['thumb','palm'],'volume_mm3':v})
(R/'hand_checks.json').write_text(json.dumps(report,indent=2)+'\n')
assert not report['static_collisions'],report['static_collisions']
assert not report['motion_checks'],report['motion_checks']
ass=cq.Assembly(name='minimal_hand_right_unfitted')
for n,p in models.items():ass.add(p,name=n)
cq.exporters.export(ass.toCompound(),str(O/'minimal_hand_assembly.step'))
fig=plt.figure(figsize=(11,10));ax=fig.add_subplot(111,projection='3d');faces=[];colors=[]
for n,p in models.items():
 c='#617b88' if n=='palm' else '#d0d7d9'
 v,f=p.val().tessellate(.5);v=[a.toTuple() for a in v]
 faces.extend([[v[j] for j in ff] for ff in f]);colors.extend([c]*len(f))
ax.add_collection3d(Poly3DCollection(faces,facecolor=colors,edgecolor='none'))
ax.set_xlim(-95,50);ax.set_ylim(-15,160);ax.set_zlim(-35,30);ax.set_box_aspect((145,175,65));ax.view_init(60,-70)
ax.set_title('Minimal tendon hand — geometry prototype\nTwo joints per finger; opposed hinged thumb; no socket')
ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_zlabel('mm')
fig.savefig(O/'minimal_hand_preview.png',dpi=160);plt.close(fig)
print(json.dumps({'parts':len(parts),'static_collisions':report['static_collisions'],'motion_collisions':report['motion_checks']},indent=2))
