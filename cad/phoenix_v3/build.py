"""Phoenix v3 motorisation study. Upstream geometry CC BY 4.0; attribution in README.
Keep source bodies unchanged. Repositioning only in reference assembly. mm.
"""
from pathlib import Path
import hashlib,json,math,tempfile,sys
import cadquery as cq
import trimesh
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parent;O=R/'exports';O.mkdir(exist_ok=True)
source=R.parent/'upstream/phoenix_v3.step'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='3d7086af7fd8a3b8f33ca87d8af6b10bdc7fc9038eb923bf920633acd7227620'
S=cq.importers.importStep(str(source)).solids().vals();assert len(S)==32
# Deterministic source-solid indices, checked against the original STEP product groups.
N={0:'original_arm_guard',1:'original_palm_left',2:'original_palm_right',22:'proximal_finger_a',23:'proximal_finger_b',24:'proximal_thumb',25:'proximal_finger_c',26:'proximal_finger_d',27:'distal_thumb',28:'distal_long_a',29:'distal_short_a',30:'distal_short_b',31:'distal_long_b'}
for i in range(3,16):N[i]=f'original_pin_or_spacer_{i:02d}'
for i in range(16,22):N[i]=f'original_tensioner_part_{i:02d}'
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_parts':{},'reference_collisions':[], 'notes':['Source solids retain their geometry and source scale.','Assembly pose is a study, not verified pin insertion or travel.']}
if '--assembly-only' in sys.argv:
 report['source_parts']=json.loads((R/'checks.json').read_text())['source_parts']
else:
 for i,n in N.items():
  p=S[i];assert p.isValid()
  # Exports retain source layout coordinates; no scale or shape modification.
  cq.exporters.export(p,str(O/f'{n}.step'))
  with tempfile.TemporaryDirectory() as tmp:
   trial=Path(tmp)/'trial.stl';cq.exporters.export(p,str(trial),tolerance=.06,angularTolerance=.12)
   m=trimesh.load_mesh(trial)
  # Source print meshes are obtained from the official release; conversion is diagnostic only.
  (O/f'{n}.stl').unlink(missing_ok=True)
  report['source_parts'][n]={'source_solid':i,'cad_valid':True,'watertight':bool(m.is_watertight),'volume_mm3':p.Volume()}
# Recover exact centres from cylindrical joint faces, rather than rounded drawings.
def joint(i,r,y_region=None):
 out=[]
 for f in S[i].Faces():
  if f.geomType()!='CYLINDER':continue
  c=f._geomAdaptor().Cylinder();a=c.Axis();q=a.Location();b=f.BoundingBox()
  if abs(c.Radius()-r)<1e-4 and abs(a.Direction().X())>.99:
   if y_region and not(y_region[0]<q.Y()<y_region[1]):continue
   out.append(((b.xmin+b.xmax)/2,q.Y(),q.Z()))
 assert out,(i,r)
 return out[0]
pivot=joint(2,3,(-95,-85));Y=pivot[1];ZMIN=S[2].BoundingBox().zmin
# The MCP spacing comes from the source's knuckle/pin cylinder coordinates.
X=126.591 # fixed layout datum only; absolute translation does not alter fit
palm=cq.Workplane('XY').newObject([S[2]]).translate((-X,-Y,-ZMIN))
models={'phoenix_palm_right':palm}
# Finger roots are 14 mm apart, with the original stagger in the palm.
# Use exact common MCP Y/Z recovered from source cylinder faces.
mcps=[]
for f in S[2].Faces():
 if f.geomType()!='CYLINDER':continue
 c=f._geomAdaptor().Cylinder();q=c.Axis().Location()
 if abs(c.Radius()-2.5)<1e-4 and abs(c.Axis().Direction().X())>.99 and -25<q.Y()<-5:
  b=f.BoundingBox();mcps.append((b.xmin,b.xmax,q.Y(),q.Z()))
# Slot centres between adjoining knuckle faces, four original joint positions.
def root_target(yval,xval):
 a=min(mcps,key=lambda t:abs(t[2]-yval)+abs(t[0]-xval))
 return (a[1]+3,a[2],a[3])
targets=[root_target(-10.94,101.59),root_target(-10.94,108.59),root_target(-14.94,128.59),root_target(-20.94,142.59)]
for name,pi,di,t in zip(['index','middle','ring','little'],[23,25,22,26],[28,31,30,29],targets):
 root=joint(pi,2.3);tip=joint(pi,2.375)
 shift=tuple(t[j]-root[j] for j in range(3))
 prox=cq.Workplane('XY').newObject([S[pi]]).translate(shift).translate((-X,-Y,-ZMIN))
 # Distal root is the middle of its two pin-bearing bore sections (radius 2.25).
 entries=[]
 for f in S[di].Faces():
  if f.geomType()=='CYLINDER':
   c=f._geomAdaptor().Cylinder();q=c.Axis().Location()
   if abs(c.Radius()-2.25)<1e-4:
    b=f.BoundingBox();entries.append(((b.xmin+b.xmax)/2,q.Y(),q.Z()))
 dr=(min(a[0] for a in entries)+max(a[0] for a in entries))/2,entries[0][1],entries[0][2]
 dest=tuple(tip[j]+shift[j] for j in range(3))
 dist=cq.Workplane('XY').newObject([S[di]]).translate(tuple(dest[j]-dr[j] for j in range(3))).translate((-X,-Y,-ZMIN))
 models[name+'_proximal']=prox;models[name+'_distal']=dist
# Thumb root along the actual oblique bore. Centre of 2.7 mm radius coaxial sections.
thumbfaces=[]
for f in S[2].Faces():
 if f.geomType()=='CYLINDER':
  c=f._geomAdaptor().Cylinder();q=c.Axis().Location();d=c.Axis().Direction()
  if abs(c.Radius()-2.7)<1e-4 and abs(d.Z())<.01:thumbfaces.append((q.X(),q.Y(),q.Z()))
T=tuple(sum(p[j] for p in thumbfaces)/len(thumbfaces) for j in range(3))
pr=joint(24,2.3);pt=joint(24,2.375)
def thumbtransform(p):return p.translate(tuple(-v for v in pr)).rotate((0,0,0),(0,0,1),130).translate(T).translate((-X,-Y,-ZMIN))
models['thumb_proximal']=thumbtransform(cq.Workplane('XY').newObject([S[24]]))
# Thumb distal root centre follows its two coaxial pin bores.
droot=(40.756,11.934,6.882) # source-layout datum; refined from cylinder sections below
entries=[]
for f in S[27].Faces():
 if f.geomType()=='CYLINDER':
  c=f._geomAdaptor().Cylinder();q=c.Axis().Location()
  if abs(c.Radius()-2.25)<1e-4:
   b=f.BoundingBox();entries.append(((b.xmin+b.xmax)/2,q.Y(),q.Z()))
droot=((min(a[0] for a in entries)+max(a[0] for a in entries))/2,entries[0][1],entries[0][2])
models['thumb_distal']=thumbtransform(cq.Workplane('XY').newObject([S[27]]).translate(tuple(pt[j]-droot[j] for j in range(3))))
# Thumb pose is exploded because the oblique source joint orientation remains unresolved.
# Do not remove original material just to make an assumed assembly pose fit.
for n in ['thumb_proximal','thumb_distal']:models[n]=models[n].translate((-22,0,12))
report['thumb_pose']='Exploded 22 mm lateral and 12 mm upward; joint orientation not validated'
# New wrist cradle references the existing 6 mm bores; no drilling of the palm.
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
cz=pivot[2]-ZMIN
cradle=box(74,22,4,0,-24)
for x in [-35,35]:
 ear=cq.Workplane('YZ').circle(8).extrude(4).translate((x-2,0,cz)).union(box(4,26,4,x,-13))
 bore=cq.Workplane('YZ').circle(3.2).extrude(6).translate((x-3,0,cz))
 cradle=cradle.union(ear.cut(bore))
for x in [-18,18]:cradle=cradle.cut(cq.Workplane('XY').center(x,-24).circle(2.2).extrude(6).translate((0,0,-1)))
assert len(cradle.solids().vals())==1 and cradle.val().isValid()
printcradle=cradle.translate((0,0,-cradle.val().BoundingBox().zmin))
cq.exporters.export(printcradle,str(O/'phoenix_wrist_cradle.step'));cq.exporters.export(printcradle,str(O/'phoenix_wrist_cradle.stl'),tolerance=.06,angularTolerance=.12)
m=trimesh.load_mesh(O/'phoenix_wrist_cradle.stl');assert m.is_watertight and m.volume>0
models['wrist_cradle']=cradle
# Component housing is kept behind the hand; a spacer keeps the cradle base below it.
pod=cq.importers.importStep(str(R.parent/'compact/exports/compact_assembly.step')).rotate((0,0,0),(0,0,1),180).translate((0,-30,4))
models['compact_housing']=pod
# Static pair intersections are recorded, not hidden. Assembly isn't print-in-place.
items=list(models.items())
for i,(n,p) in enumerate(items):
 for nn,q in items[i+1:]:
  a,b=p.val().BoundingBox(),q.val().BoundingBox()
  if any(min(getattr(a,k+'max'),getattr(b,k+'max'))-max(getattr(a,k+'min'),getattr(b,k+'min'))<=1e-5 for k in 'xyz'):continue
  v=p.intersect(q).val().Volume()
  if v>1e-4:report['reference_collisions'].append([n,nn,v])
report['contacts_below_0_001_mm3']=[x for x in report['reference_collisions'] if x[2]<.001]
report['reference_collisions']=[x for x in report['reference_collisions'] if x[2]>=.001]
assert not report['reference_collisions'],report['reference_collisions']
report['cradle']={'watertight':True,'pivot_bore_mm':6.4,'pivot_z_mm':cz,'scale':'upstream only; regenerate after sizing'}
(R/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
ass=cq.Assembly(name='phoenix_v3_motorisation_reference')
for n,p in models.items():ass.add(p,name=n)
cq.exporters.export(ass.toCompound(),str(O/'phoenix_motorised_reference.step'))
# Render actual source geometry, not a substitute hand.
fig=plt.figure(figsize=(11,14));ax=fig.add_subplot(111,projection='3d');faces=[];colors=[]
for n,p in models.items():
 c='#526f7c' if n=='compact_housing' else '#d09a46' if n=='wrist_cradle' else '#bac6cd'
 for solid_index,s in enumerate(p.solids().vals()):
  # Exterior view: omit internal envelope boxes and tray so they do not show through the cover.
  if n=='compact_housing' and solid_index not in [0,2]:continue
  if n=='compact_housing':c='#425761' if solid_index==0 else '#9aabb3'
  v,f=s.tessellate(.6);v=[a.toTuple() for a in v];tri=np.asarray([[v[j] for j in ff] for ff in f])
  norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12)
  light=np.array([-.3,-.5,1]);light/=np.linalg.norm(light);bright=.45+.55*np.abs(norm@light)
  faces.extend(tri);colors.extend(np.asarray(to_rgb(c))[None,:]*bright[:,None])
ax.add_collection3d(Poly3DCollection(faces,facecolor=colors,edgecolor='none'))
ax.set_xlim(-110,55);ax.set_ylim(-180,150);ax.set_zlim(-10,75);ax.set_box_aspect((165,330,85));ax.view_init(53,-65)
ax.set_title('Phoenix v3 + rounded motor housing\nThumb exploded for joint review; socket and wrist lock unfinished',fontsize=13);ax.set_axis_off();fig.tight_layout();fig.savefig(O/'phoenix_preview.png',dpi=160)
print(json.dumps({'source_parts':len(N),'non_watertight_source_parts':[n for n,r in report['source_parts'].items() if not r['watertight']],'reference_collisions':report['reference_collisions']},indent=2))
