"""Original-proportion hand sizing and adjustable limb keep-out study. CC BY 4.0.
This does not scale hardware, generate a fitted socket, or accept a resized assembly.
"""
from pathlib import Path
import argparse, hashlib, json, sys
import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from sizing import evaluate, validate

R = Path(__file__).resolve().parent
F = R.parent / 'forearm'
sys.path.insert(0, str(F))
from hand import models
from thumb_mount import posed_thumb


def bounds(s):
    b = s.BoundingBox()
    return [b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax]


def envelope(e):
    w = cq.Workplane('XY').ellipse(e['proximal_width_mm']/2, e['proximal_depth_mm']/2)
    w = w.workplane(offset=e['distal_end_y_mm']-e['opening_y_mm']).ellipse(e['distal_width_mm']/2, e['distal_depth_mm']/2)
    return w.loft(ruled=True).rotate((0,0,0),(1,0,0),-90).translate((0,e['opening_y_mm'],e['axis_z_mm'])).val()


def overlap(a, b):
    aa, bb = a.BoundingBox(), b.BoundingBox()
    if any(min(getattr(aa,k+'max'),getattr(bb,k+'max')) - max(getattr(aa,k+'min'),getattr(bb,k+'min')) <= 1e-6 for k in 'xyz'):
        return 0.0
    return a.intersect(b).Volume()


def make_preview(out, hand, fixed, env, report, baseline, profile):
    # Orthographic projections of actual CAD triangles, not an imagined hand silhouette.
    def project(ax, shapes, color, scale=1, shift=0, side=False, alpha=1):
        polygons=[]
        for shape in shapes:
            vertices, faces=shape.tessellate(.7)
            v=np.array([p.toTuple() for p in vertices])*scale
            coords=np.column_stack((v[:,1]+shift,v[:,2])) if side else np.column_stack((v[:,0]+shift,v[:,1]))
            polygons.extend(coords[np.asarray(faces)])
        ax.add_collection(PolyCollection(polygons, facecolors=color, edgecolors='none', alpha=alpha, rasterized=True))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig=plt.figure(figsize=(15,10),facecolor='#f8fafb')
    grid=fig.add_gridspec(2,2,height_ratios=[1.25,1],width_ratios=[1.4,1],hspace=.42,wspace=.25)
    ax=fig.add_subplot(grid[0,:])
    scales=profile['comparison_scales_percent']
    maxs=max(scales)/100
    for i,pct in enumerate(scales):
        shift=i*145*maxs
        project(ax,hand.values(),'#7897a5',pct/100,shift)
        length=baseline['wrist_to_middle_tip_mm']*pct/100
        ax.text(shift,-25,f'{pct:g}%\n{length:.1f} mm CAD wrist → middle tip',ha='center',va='top',fontsize=10)
        ax.plot([shift-45*maxs,shift+45*maxs],[0,0],c='#b76e38',lw=.8,ls='--')
        # Same anatomical shape, a different uniformly scaled joint/feature layout.
    ax.set_aspect('equal');ax.autoscale_view();ax.set_axis_off()
    ax.set_title('Original Phoenix v3 proportions • corrected fingertips at every scale',loc='left',pad=16,fontweight='bold')
    ax=fig.add_subplot(grid[1,0])
    project(ax,fixed,'#a7afb6',side=True)
    project(ax,[s.scale(profile['hand_scale_percent']/100) for s in hand.values()],'#7897a5',side=True)
    # Draw a keep-out section outline, so equipment intrusion stays visible.
    e=profile['limb_clearance_envelope'];z=e['axis_z_mm'];a=e['opening_y_mm'];b=e['distal_end_y_mm']
    ax.fill([a,b,b,a],[z-e['proximal_depth_mm']/2,z-e['distal_depth_mm']/2,z+e['distal_depth_mm']/2,z+e['proximal_depth_mm']/2],color='#e7b15d',alpha=.7)
    for y,label in [(a,'Opening'),(b,'Limb end'),(0,'CAD wrist')]:
        ax.axvline(y,c='#7d643c',ls='--',lw=.8)
        ax.text(y,67,label,ha='center',fontsize=9)
    ax.annotate('',xy=(b,-68),xytext=(0,-68),arrowprops={'arrowstyle':'<->','color':'#7d643c'})
    ax.text(b/2,-74,f'{-b:g} mm design gap',ha='center',va='top')
    ax.set_aspect('equal');ax.autoscale_view();ax.set_ylim(-90,90)
    ax.set_xlabel('Y / mm (towards fingertips)');ax.set_ylabel('Z / mm (dorsal up)')
    ax.set_title('Side projection • sizing context, receiver omitted',loc='left',fontsize=11,fontweight='bold')
    ax=fig.add_subplot(grid[1,1]);ax.set_axis_off()
    screen=report['travel_screen']
    text=(f"Selected example: {report['hand_scale_percent']:g}%\n"
          f"Hand CAD length: {report['projected_cad_wrist_to_middle_tip_mm']:.1f} mm\n"
          f"Palm section width: {report['palm_section_width_mm']:.1f} mm\n\n"
          "Motors, battery and electronics keep their size.\n"
          "Arm envelope dimensions are independent controls.\n"
          "Different hand scale needs a new wrist adapter.\n\n"
          f"Envelope/assembly overlaps: {len(report['envelope_intersections_with_existing_assembly_mm3'])}\n"
          f"3 candidate servos alone: {report['servo_mass_only_g']:.1f} g\n"
          f"Ideal fixed-spool take-up: {screen['ideal_takeup_mm']:.1f} mm\n"
          "Real tendon force and stroke still need measuring.")
    ax.text(0,1,text,va='top',linespacing=1.5,fontsize=11,color='#263c48')
    fig.suptitle('Adjustable sizing study — no wearer dimensions supplied',x=.07,ha='left',fontsize=20,fontweight='bold',color='#263c48')
    fig.text(.07,.02,'Examples are not adult/child sizes or validated fit. Gold is reserved limb/liner space, not a fitted socket. CAD wrist ≠ anatomical wrist until registered.',fontsize=9,color='#576875')
    fig.savefig(out/'sizing_preview.png',dpi=145,bbox_inches='tight');plt.close(fig)


def build(profile_path, output):
    profile=validate(json.loads(profile_path.read_text()));output.mkdir(parents=True,exist_ok=True)
    scale=profile['hand_scale_percent']/100
    hand={n:p.val() for n,p in {**models,**posed_thumb()}.items()}
    # A reproducible CAD breadth station, not total hand spread or a clinical landmark.
    section=models['phoenix_palm_right'].intersect(cq.Workplane('XY').box(300,.1,200).translate((0,60,0))).val()
    baseline={'wrist_to_middle_tip_mm':hand['middle_distal'].BoundingBox().ymax,
              'palm_section_width_mm':section.BoundingBox().xlen,'palm_section_y_mm':60}
    report=evaluate(profile,baseline);report['baseline_geometry_mm']=baseline
    selected={n:s.scale(scale) for n,s in hand.items()}
    assert len(selected)==11 and all(s.isValid() for s in selected.values())
    cq.exporters.export(cq.Compound.makeCompound(list(selected.values())),str(output/'scaled_hand.step'))
    # Recover the fixed shell/hardware from the verified baseline without importing build.py.
    check=json.loads((F/'checks.json').read_text())
    receiver=cq.importers.importStep(str(F/'exports/palm_receiver.step')).translate((0,0,check['parts']['palm_receiver']['assembly_zmin_mm'])).val()
    all_solids=cq.importers.importStep(str(F/'exports/complete_forearm.step')).solids().vals()
    omitted=list(hand.values())+[receiver]
    fixed=[]
    for solid in all_solids:
        if not any(np.allclose(bounds(solid),bounds(s),atol=.0001,rtol=0) for s in omitted):fixed.append(solid)
    assert len(all_solids)-len(fixed)==12
    env=envelope(profile['limb_clearance_envelope']);assert env.isValid()
    cq.exporters.export(env,str(output/'limb_clearance_envelope.step'))
    print('Checking adjustable limb envelope against the baseline assembly...',flush=True)
    report['envelope_intersections_with_existing_assembly_mm3']=[
        {'solid_index':i,'volume_mm3':v} for i,s in enumerate(all_solids)
        if (v:=overlap(env,s))>.001]
    print('Checking resized hand against fixed housing and hardware...',flush=True)
    report['hand_intersections_with_fixed_assembly_mm3']=[
        {'hand_part':n,'fixed_solid_index':i,'volume_mm3':v}
        for n,s in selected.items() for i,p in enumerate(fixed) if (v:=overlap(s,p))>.001]
    report['interface_status']='BASELINE_INTERFACE_ONLY' if report['existing_receiver_matches_hand_scale'] else 'RESIZED_RECEIVER_REQUIRED'
    report['hardware_scale_percent']=100
    # Check STEP round-trip dimensions and volume scaling for every corrected hand part.
    imported=cq.importers.importStep(str(output/'scaled_hand.step')).solids().vals()
    report['export_checks']={}
    for n,s in selected.items():
        matches=[p for p in imported if np.allclose(bounds(p),bounds(s),atol=.0001,rtol=0)]
        assert len(matches)==1,n
        p=matches[0]
        assert p.isValid(),n
        assert abs(p.Volume()/hand[n].Volume()-scale**3)<scale**3*.001,n
        report['export_checks'][n]={'valid':p.isValid(),'bounds_mm':bounds(p),'volume_ratio':p.Volume()/hand[n].Volume()}
    report['scope']='Independent hand and keep-out STEP studies. No regenerated socket, receiver, pins, complete fitted assembly, or force/fit acceptance.'
    make_preview(output,hand,fixed,env,report,baseline,profile)
    report['sha256']={str(p.relative_to(R.parent.parent)) if p.is_relative_to(R.parent.parent) else p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [profile_path,Path(__file__),R/'sizing.py',F/'hand.py',F/'thumb_mount.py',F/'exports/complete_forearm.step',R.parent/'upstream/phoenix_v3.step']}
    report['output_sha256']={n:hashlib.sha256((output/n).read_bytes()).hexdigest() for n in ['scaled_hand.step','limb_clearance_envelope.step','sizing_preview.png']}
    (output/'sizing_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','hand_scale_percent','projected_cad_wrist_to_middle_tip_mm','palm_section_width_mm','interface_status','hand_intersections_with_fixed_assembly_mm3','envelope_intersections_with_existing_assembly_mm3']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=R/'profile.json')
    parser.add_argument('--output',type=Path,default=R/'exports')
    args=parser.parse_args();build(args.profile.resolve(),args.output.resolve())
