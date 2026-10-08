"""Scale-aware Phoenix receiver; fixed forearm bolts, resized hand interface. CC BY 4.0."""
from pathlib import Path
import sys
import cadquery as cq
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'forearm'))
from hand import models,pivot,ZMIN


def box(w,l,h,x=0,y=0,z=0):
    return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))


def receiver(scale):
    if not .9 <= scale <= 1.4:
        raise ValueError('Receiver generator currently supports 90–140% design studies only; not a validated fitting range')
    # Keep the housing-side bolt pattern, seating plane and centre slider clearance.
    p=box(74,22,4,0,-24)
    for side in [-1,1]:
        # Taper between the fixed rear plate and resized wrist ears, in the XY plane.
        points=[(side*31,-26),(side*37,-26),(side*37,-15),(side*(35*scale+2),-5),
                (side*(35*scale+2),0),(side*(35*scale-2),0),(side*(35*scale-2),-5),(side*31,-15)]
        stem=cq.Workplane('XY').polyline(points).close().extrude(4)
        x=side*35*scale;cz=(pivot[2]-ZMIN)*scale
        ear=cq.Workplane('YZ').circle(8*scale).extrude(4).translate((x-2,0,cz))
        # Source wrist bore scales with the original printed palm; clearance stays 0.4 mm.
        bore=cq.Workplane('YZ').circle((6*scale+.4)/2).extrude(6).translate((x-3,0,cz))
        p=p.union(stem).union(ear.cut(bore))
    # Four-mm plate underneath the palm, unchanged thickness and bought fastener sizes.
    plate=box(70*scale,52*scale,4,0,17*scale,-8).edges('|Z').fillet(4)
    front=box(70*scale,15*scale,8,0,-6*scale,-4).intersect(box(200,100,30,0,35,-15))
    p=p.union(plate).union(front).union(box(74,4,8,0,-13,-4))
    for x in [-24*scale,31*scale]:
        slot=cq.Workplane('XY').center(x,16*scale).slot2D(22,3,angle=90).extrude(7).translate((0,0,-10))
        p=p.cut(slot)
    for x in [-18*scale,18*scale]:
        p=p.union(cq.Workplane('XY').center(x,32*scale).circle(5).extrude(4).translate((0,0,-4)))
        p=p.cut(cq.Workplane('XY').center(x,32*scale).circle(2.2).extrude(15).translate((0,0,-10)))
    palm=cq.Workplane('XY').newObject([models['phoenix_palm_right'].val().scale(scale)])
    p=p.cut(palm).cut(palm.translate((0,0,-.3)))
    # Keep the original native-thumb relief, with its XY footprint following the hand.
    p=p.cut(box(20*scale,32*scale,16,-39*scale,38*scale,-12).edges('|Z').fillet(2))
    for x in [-18,18]:
        p=p.cut(cq.Workplane('XY').center(x,-24).circle(2.2).extrude(16).translate((0,0,-8)))
        # One-mm recess: 8 x 2.5 mm head allowance finishes at Z=5.5, below the cassette.
        p=p.cut(cq.Workplane('XY').center(x,-24).circle(4.2).extrude(10).translate((0,0,3)))
    p=p.cut(box(12,24,12,0,-26,-6))
    return p

if __name__=='__main__':
    import json
    scale=json.loads((R/'profile.json').read_text())['hand_scale_percent']/100
    p=receiver(scale)
    print('solids',len(p.solids().vals()),'valid',p.val().isValid(),flush=True)
    cq.exporters.export(p,'/tmp/resized_receiver_probe.step')
