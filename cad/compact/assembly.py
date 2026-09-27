"""Combine validated subassemblies. Original prototype, CC BY 4.0."""
from pathlib import Path
import json
import numpy as np
from matplotlib.colors import to_rgb
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parent;O=R/'exports'
hand=cq.importers.importStep(str(O/'minimal_hand_assembly.step'))
pod=cq.importers.importStep(str(O/'compact_assembly.step')).rotate((0,0,0),(0,0,1),180).translate((0,-12,0))
collisions=[]
for i,a in enumerate(hand.solids().vals()):
 for j,b in enumerate(pod.solids().vals()):
  ba,bb=a.BoundingBox(),b.BoundingBox()
  if any(min(getattr(ba,axis+'max'),getattr(bb,axis+'max'))-max(getattr(ba,axis+'min'),getattr(bb,axis+'min'))<=1e-6 for axis in 'xyz'):continue
  v=a.intersect(b).Volume()
  if v>1e-5:collisions.append([i,j,v])
assert not collisions,collisions
ass=cq.Assembly(name='minimal_hand_and_housing_unfitted');ass.add(hand,name='hand');ass.add(pod,name='housing')
shape=ass.toCompound();cq.exporters.export(shape,str(O/'complete_reference_assembly.step'))
b=shape.BoundingBox()
report={'hand_housing_collisions':collisions,'reference_assembly_bounds_mm':[b.xlen,b.ylen,b.zlen], 'socket':'absent', 'tendon_routing':'not complete'}
(R/'assembly_checks.json').write_text(json.dumps(report,indent=2)+'\n')
# Exterior visual, with closed lid; no arm or socket invented for illustration.
fig=plt.figure(figsize=(10,14));ax=fig.add_subplot(111,projection='3d');faces=[];colors=[]
for p,c in [(pod,'#506974'),(hand,'#c2cace')]:
 for solid in p.solids().vals():
  v,f=solid.tessellate(.7);v=[a.toTuple() for a in v]
  triangles=np.asarray([[v[k] for k in ff] for ff in f])
  normals=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
  light=np.array([-.3,-.5,1.]);light/=np.linalg.norm(light)
  brightness=.45+.55*np.abs(normals@light)
  faces.extend(triangles);colors.extend(np.array(to_rgb(c))[None,:]*brightness[:,None])
ax.add_collection3d(Poly3DCollection(faces,facecolor=colors,edgecolor='none'))
ax.set_xlim(-90,50);ax.set_ylim(-165,160);ax.set_zlim(-35,70);ax.set_box_aspect((140,325,105));ax.view_init(48,-65)
ax.set_title('Minimal hand + enclosed components\nUnfitted prototype — socket and tendon routing unfinished',fontsize=14)
ax.set_axis_off();fig.tight_layout();fig.savefig(O/'complete_preview.png',dpi=160);plt.close(fig)
print(json.dumps(report,indent=2))
