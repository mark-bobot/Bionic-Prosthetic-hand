"""Forearm-integrated component layout. CC BY 4.0; mm. Unfitted prototype."""
from pathlib import Path
import json,sys,math
import cadquery as cq
import trimesh
R=Path(__file__).resolve().parent;O=R/'exports';O.mkdir(exist_ok=True)
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def cyl(d,h,x,y,z):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))
def bore_y(d,l,x,y,z):return cq.Workplane('XZ').circle(d/2).extrude(l,both=True).translate((x,y,z))
# Stations: y, half width, half height. Forearm axis runs +Y toward wrist; +Z dorsal.
stations=[(-295,40,36),(-175,38,34),(-158,47,47),(-153,49,51),(-80,49,51),(-70,44,43),(-30,42,43),(-16,37,30)]
def loft(st):
 w=cq.Workplane('XY')
 last=st[0][0]
 for i,(y,rx,rz) in enumerate(st):
  if i:w=w.workplane(offset=y-last)
  w=w.ellipse(rx,rz);last=y
 return w.loft(ruled=True).rotate((0,0,0),(1,0,0),-90).translate((0,st[0][0],8))
outer=loft(stations)
lumen=loft([(-297,35,32),(-160,27,25)])
# The residual-limb space stops at -160. A 3 mm bulkhead separates it from equipment.
air=loft([(-157,44,44)]+[(y,rx-3,rz-3) for y,rx,rz in stations[3:-1]]+[(-21,35,31)])
body=outer.cut(lumen).cut(air)
# Forearm opening is rearward; split shell along the sides for service and donning.
upper=body.intersect(box(130,320,100,0,-150,8.2))
lower=body.intersect(box(130,320,100,0,-150,-92.2))
# Joining bosses lie in/outside the shell wall, never within the reserved socket.
for y,rx in [(-275,39.7),(-210,38.6),(-145,49),(-98,49),(-48,41.3)]:
 for x in [-rx+1,rx-1]:
  upper=upper.union(cyl(6,6,x,y,8.2)).cut(cyl(3.4,9,x,y,7))
  lower=lower.union(cyl(6,6,x,y,1.8)).cut(cyl(3.4,9,x,y,0))
upper=upper.cut(lumen);lower=lower.cut(lumen)
# The independently strapped electrode reaches the empty socket through a lower window.
lower=lower.cut(box(34,49,55,0,-220,-60).edges('|Z').fillet(3))
# Embedded servo shelf, below the motors and above the battery; bonded into side walls.
shelf=box(90,83,2,0,-120.5,-13).intersect(outer)
for x,y in [(-25,-128),(0,-118),(25,-128)]:
 seat=box(24,44.6,6,x,y,-11).cut(box(21,41.6,7,x,y,-11))
 shelf=shelf.union(seat)
 for dx in [-11.7,11.7]:shelf=shelf.cut(box(2.5,12,8,x+dx,y,-15))
lower=lower.union(shelf)
# Battery cradle joins the lower shell. Two under-floor tunnels accept 10 mm straps;
# reserve at most 0.8 mm strap thickness in the 1 mm gap below the servo shelf.
battery_cradle=box(38,74,7,0,-115,-40).edges('|Z').fillet(2)
battery_cradle=battery_cradle.cut(box(34,72,8,0,-115,-36)).intersect(outer)
lower=lower.union(battery_cradle)
for y in [-141,-90]:
 lower=lower.cut(box(44,12,1.5,0,y,-39.2))
 for x in [-17.8,17.8]:lower=lower.cut(box(2.2,12,8,x,y,-39.2))
# Electronics tray beneath the forward tendon mechanism; seated on four integral bosses.
tray=box(48,53,2,0,-52,-26).edges('|Z').fillet(3)
tray=tray.intersect(air)
for x in [-21,21]:
 for y in [-72,-32]:
  # Posts extend to the exterior surface and are clipped to the shell outline.
  post=cyl(7,22,x,y,-48).intersect(outer)
  lower=lower.union(post).cut(cyl(3.4,28,x,y,-49))
  tray=tray.cut(cyl(3.4,4,x,y,-27))
# Reference bought-part envelopes; body/ear/shaft and cable allowances require measurement.
components={}
spool=cq.importers.importStep(str(R.parent/'compact/exports/single_groove_spool.step'))
for i,(x,y) in enumerate([(-25,-128),(0,-118),(25,-128)]):
 components[f'servo_{i}']=box(20,40.6,30,x,y,-11).union(box(24,55,4,x,y,11))
 components[f'spool_{i}']=spool.translate((x,y+(-10 if i!=1 else 10),24))
components['battery']=box(32,70,22,0,-115,-36)
components['Nano']=box(18,45,8,-14,-52,-23)
components['EMG_conditioner']=box(22,35,10,12,-47,-23)
components['logic_regulator']=box(12.7,10.2,4,26,-73,-15)
components['fuse_allowance']=box(12,24,12,-22,-92,-26)
components['distribution_allowance']=box(12,18,10,22,-90,-24)
# Controls sit in a shallow recess in the upper arm shell, above the tendon cassette.
components['main_switch_allowance']=box(16,20,20,-13,-64,24)
components['arm_switch_allowance']=box(10,10,12,13,-64,32)
well=box(50,34,20,0,-64,44).edges('|Z').fillet(4).cut(box(46,30,22,0,-64,47).edges('|Z').fillet(2)).intersect(outer)
upper=upper.cut(box(46,30,30,0,-64,44).edges('|Z').fillet(2)).union(well)
for x,d in [(-13,12.2),(13,6.2)]:upper=upper.cut(cyl(d,6,x,-64,43))
upper=upper.cut(box(17,21,20.5,-13,-64,23.5)).cut(box(11,11,12.5,13,-64,31.5))
lower=lower.cut(box(22,12,10,-34,-34,-24))
# Independent probe is visible through the socket window; no rigid contact-pressure screw.
carrier=cq.importers.importStep(str(R.parent/'arm_interface/exports/emg_band_carrier.step')).rotate((0,0,0),(1,0,0),3).translate((0,-220,-28.45))
probe=box(22,35,6,0,0,2).rotate((0,0,0),(1,0,0),3).translate((0,-220,-28.45))
# Side seam cable passage stays outside the reserved residual-limb volume.
upper=upper.cut(bore_y(4,39,34,-192,8));lower=lower.cut(bore_y(4,39,34,-192,8))
# Two internal equaliser lanes, plus a lower thumb lane, replacing the top cassette.
mechanism=box(68,70,2,0,-54,0).edges('|Z').fillet(4)
for x in [-32.5,0,32.5]:mechanism=mechanism.union(box(3,66,8,x,-54,2))
for y in [-87.5,-20.5]:mechanism=mechanism.union(box(62,3,8,0,y,2))
for x in [-16,16]:mechanism=mechanism.cut(bore_y(2.2,5,x,-87.5,6))
for x in [-26,-6,6,26]:mechanism=mechanism.cut(bore_y(2.2,5,x,-20.5,6))
# Removable shallow cover retains the bars. Screw bosses outside bar swept footprints.
cover=box(68,70,2,0,-54,10).edges('|Z').fillet(4)
for x in [0]:
 for y in [-86,-21]:
  mechanism=mechanism.union(cyl(8,8,x,y,2)).cut(cyl(3.4,13,x,y,-1))
  # Top-loaded M3 nut, captured by the cover; short bolt ends above the thumb lane.
  nut_pocket=cq.Workplane('XY').polygon(6,6.6).extrude(2.5).translate((x,y,7.6))
  mechanism=mechanism.cut(nut_pocket)
  cover=cover.cut(cyl(3.4,4,x,y,9))
eq=cq.importers.importStep(str(R.parent/'exports/pair_equaliser.step'))
bars={'index_middle_equaliser':eq.translate((-16,-37,3)),'ring_little_equaliser':eq.translate((16,-37,3))}
# Thumb lane below the centre wall; it does not share the pair-bar plane.
thumb_track=box(12,70,2,0,-54,-11).union(box(2,70,9,-5,-54,-9)).union(box(2,70,9,5,-54,-9))
thumb_slider=box(6,12,4,0,-37,-8).edges('|Z').fillet(1.5)
for y in [-41,-33]:thumb_slider=thumb_slider.cut(cyl(2.4,6,0,y,-9))
mechanism=mechanism.union(thumb_track)
# Connect the thumb track to the upper base with rear/end bridges.
for y in [-86,-22]:mechanism=mechanism.union(box(12,4,12,0,y,-10))
for y in [-86,-22]:mechanism=mechanism.cut(bore_y(2.2,5,0,y,-6))
# Raise the pair-bar plane above the original receiver plate.
mechanism=mechanism.translate((0,0,6));cover=cover.translate((0,0,6));thumb_slider=thumb_slider.translate((0,0,6))
bars={n:p.translate((0,0,6)) for n,p in bars.items()}
# Mount the whole mechanism on two support crossbars in lower shell.
for y in [-82,-26]:
 cross=box(110,7,3,0,y,3).cut(box(12,9,5,0,y,2)).intersect(outer)
 lower=lower.union(cross)
 for x in [-30,30]:
  lower=lower.cut(cyl(3.4,8,x,y,1));mechanism=mechanism.cut(cyl(3.4,5,x,y,5))
  # Clear screw insertion from above and keep heads outside equaliser sweep samples.
  mechanism=mechanism.cut(cyl(6.4,10,x,y,8))
# Retain source palm/fingers and assemble the thumb at its original palm joint.
from thumb_mount import receiver,thumb_proximal,thumb_distal
receiver=receiver.cut(box(12,24,10,0,-26,-5))
# Relieve the forearm front around the existing receiver; mount with original M4 centres.
upper=upper.cut(receiver);lower=lower.cut(receiver)
front_support=box(90,16,4,0,-24,-4).cut(box(12,18,6,0,-24,-5)).intersect(outer)
lower=lower.union(front_support)
for x in [-18,18]:lower=lower.cut(cyl(4.4,12,x,-24,-8))
# Five tendon ports through the front bulkhead; their flexible paths need bench installation.
for x,z in [(-26,12),(-6,12),(6,12),(26,12),(0,0)]:
 upper=upper.cut(bore_y(2.2,8,x,-18,z));lower=lower.cut(bore_y(2.2,8,x,-18,z))
# Clearance around the removable mechanism, retaining its underside seating faces.
upper=upper.cut(mechanism).cut(cover);lower=lower.cut(mechanism).cut(cover)
# External strap slots on the socket, outside the lumen.
for y in [-265,-190]:
 for x in [-38,38]:
  tab=box(10,26,4,x,y,3.8).edges('|Z').fillet(2)
  lower=lower.union(tab).cut(box(3,20,7,x,y,2))
lower=lower.cut(lumen)
parts={'forearm_lower':lower,'forearm_upper':upper,'electronics_tray':tray,
 'internal_tendon_base':mechanism,'internal_tendon_cover':cover,'thumb_slider':thumb_slider,'palm_receiver':receiver}
report={'status':'Unfitted forearm-integrated prototype; residual-to-wrist length assumed',
 'stations_y_rx_rz_mm':stations,'socket_lumen_y_mm':[-295,-160],
 'reserved_residual_end_to_wrist_mm':160,'components':{},'parts':{},'collisions':[],'lumen_intrusions':[]}
for n,p in parts.items():
 if len(p.solids().vals())!=1:
  print(n,[(round(q.Volume(),3),tuple(round(v,2) for v in q.Center().toTuple())) for q in p.solids().vals()],flush=True)
 assert p.val().isValid() and len(p.solids().vals())==1,(n,len(p.solids().vals()))
 b=p.val().BoundingBox();q=p.translate((0,0,-b.zmin))
 for ext in ['step','stl']:cq.exporters.export(q,str(O/f'{n}.{ext}'),tolerance=.08,angularTolerance=.15)
 m=trimesh.load_mesh(O/f'{n}.stl');assert m.is_watertight and m.volume>0,n
 report['parts'][n]={'watertight':True,'size_mm':m.extents.tolist(),'assembly_zmin_mm':b.zmin}
# Read corrected open hand (thumb and added receiver supplied above).
hand=cq.importers.importStep(str(O/'corrected_fingers.step'))
models={**parts,**components,**bars,'EMG_carrier':carrier,'electrode_envelope':probe,'hand':hand,'thumb_proximal':thumb_proximal,'thumb_distal':thumb_distal}
for n,p in components.items():
 b=p.val().BoundingBox();report['components'][n]={'bounds_mm':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]}
items=list(models.items())
for i,(n,p) in enumerate(items):
 if n not in ['forearm_lower','forearm_upper']:
  v=p.intersect(lumen).val().Volume()
  if v>.001:report['lumen_intrusions'].append([n,v])
 for nn,q in items[i+1:]:
  a,b=p.val().BoundingBox(),q.val().BoundingBox()
  if any(min(getattr(a,k+'max'),getattr(b,k+'max'))-max(getattr(a,k+'min'),getattr(b,k+'min'))<=1e-5 for k in 'xyz'):continue
  v=p.intersect(q).val().Volume()
  if v>.001:report['collisions'].append([n,nn,v])
(R/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'parts':report['parts'],'collisions':report['collisions'],'lumen_intrusions':report['lumen_intrusions']},indent=2),flush=True)
assert not report['collisions'] and not report['lumen_intrusions']
for label,omit in [('complete',set()),('open',{'forearm_upper','internal_tendon_cover'})]:
 ass=cq.Compound.makeCompound([p.val() for n,p in models.items() if n not in omit])
 cq.exporters.export(ass,str(O/f'{label}_forearm.step'))
 sys.path.insert(0,str(R.parent/'bionic'))
 from render import render
 if '--no-preview' not in sys.argv:
  render(O/f'{label}_forearm.step',O/f'{label}_preview.png',title=f'Forearm-integrated Phoenix — {label} CAD')
