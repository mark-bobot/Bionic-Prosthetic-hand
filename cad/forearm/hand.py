"""Corrected Phoenix placement from source geometry; CC BY 4.0."""
from pathlib import Path
import hashlib,json
import cadquery as cq
R=Path(__file__).resolve().parent;O=R/'exports'
source=R.parent/'upstream/phoenix_v3.step'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='3d7086af7fd8a3b8f33ca87d8af6b10bdc7fc9038eb923bf920633acd7227620'
S=cq.importers.importStep(str(source)).solids().vals()
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
# Distals lie dorsal-side down in the upstream printing layout.
# A 10 degree PIP rest bend clears their original extension-stop surfaces.
PIP_REST=10
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
for name,pi,di,t in zip(['index','middle','ring','little'],[23,25,22,26],[30,31,28,29],targets):
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
 dist=(cq.Workplane('XY').newObject([S[di]])
 .rotate(dr,(dr[0],dr[1]+1,dr[2]),180)
 .rotate(dr,(dr[0]+1,dr[1],dr[2]),-PIP_REST)
 .translate(tuple(dest[j]-dr[j] for j in range(3))).translate((-X,-Y,-ZMIN)))
 models[name+'_proximal']=prox;models[name+'_distal']=dist


def posed(mcp_angle=0,pip_angle=PIP_REST):
 out={'phoenix_palm_right':palm}
 for name,t in zip(['index','middle','ring','little'],targets):
  root=(t[0]-X,t[1]-Y,t[2]-ZMIN)
  pi={'index':23,'middle':25,'ring':22,'little':26}[name]
  sr=joint(pi,2.3);st=joint(pi,2.375)
  pip=tuple(root[j]+st[j]-sr[j] for j in range(3))
  out[name+'_proximal']=models[name+'_proximal'].rotate(root,(root[0]+1,root[1],root[2]),-mcp_angle)
  out[name+'_distal']=models[name+'_distal'].rotate(pip,(pip[0]+1,pip[1],pip[2]),-(pip_angle-PIP_REST)).rotate(root,(root[0]+1,root[1],root[2]),-mcp_angle)
 return out

if __name__=='__main__':
 import sys
 if '--check-motion' in sys.argv:
  # Record hinge axes and verify flexion goes toward the palm (-Z), not the dorsum.
  checks=[]
  for name,t in zip(['index','middle','ring','little'],targets):
   root=(t[0]-X,t[1]-Y,t[2]-ZMIN)
   p=models[name+'_proximal'];d=models[name+'_distal']
   pi={'index':23,'middle':25,'ring':22,'little':26}[name]
   sr=joint(pi,2.3);st=joint(pi,2.375)
   pip=tuple(root[j]+st[j]-sr[j] for j in range(3))
   for angle in [0,15,30,45,60]:
    # At MCP-only and combined MCP/PIP angles, check the same adjacent source surfaces.
    for pip_angle in [PIP_REST,max(PIP_REST,angle)]:
     pp=p.rotate(root,(root[0]+1,root[1],root[2]),-angle)
     dd=d.rotate(pip,(pip[0]+1,pip[1],pip[2]),-(pip_angle-PIP_REST)).rotate(root,(root[0]+1,root[1],root[2]),-angle)
     hit=[pp.intersect(palm).val().Volume(),dd.intersect(palm).val().Volume(),pp.intersect(dd).val().Volume()]
     checks.append({'finger':name,'mcp':angle,'pip':pip_angle,'overlap_mm3':hit})
  print(json.dumps({'poses':len(checks),'max_overlap_mm3':max(max(q['overlap_mm3']) for q in checks)},indent=2))
  (O/'finger_motion_diagnostic.json').write_text(json.dumps(checks,indent=2)+'\n')
 for name,shapes in [('corrected_fingers',models),('partial_flexion_fingers',posed(45,15))]:
  cq.exporters.export(cq.Compound.makeCompound([p.val() for p in shapes.values()]),str(O/(name+'.step')))
