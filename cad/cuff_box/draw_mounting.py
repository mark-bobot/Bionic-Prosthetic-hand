"""Dimensioned mounting schematic; schematic straps are not fitted CAD."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

root=Path(__file__).resolve().parent
r=json.loads((root/'exports/checks.json').read_text())
p=r['profile']; deck=r['box_deck_global_z_mm']; h=r['box_body_size_mm'][2]
crown=p['cuff_axis_z_mm']+p['formed_cuff_outer_radius_mm']
fig,axs=plt.subplots(1,2,figsize=(12,7),gridspec_kw={'width_ratios':[1.25,1]})
fig.patch.set_facecolor('#f4f4ef')
for ax in axs:
    ax.set_facecolor('#f4f4ef');ax.set_aspect('equal');ax.axis('off')
a=axs[0]
a.add_patch(Rectangle((-104,deck),96,h,facecolor='#bacbc3',edgecolor='#263f35',lw=2))
a.add_patch(Rectangle((-80,crown-2),65,2,facecolor='#666666'))
a.text(-50,28,'Original formed cuff: envelope only',ha='center',fontsize=9)
for y in [-63,-30]:
    a.plot([y,y],[crown,deck+3],color='#b17936',lw=5,linestyle='--')
a.annotate('Two strap stations\n33 mm apart',xy=(-63,47),xytext=(-121,7),arrowprops={'arrowstyle':'->'},fontsize=9)
a.add_patch(FancyArrowPatch((-63,15),(-30,15),arrowstyle='<->',mutation_scale=10,color='#333333'))
a.text(-46.5,18,'33 mm',ha='center',fontsize=9)
a.text(-56,83,'3 servos\n+ upright boards',ha='center',va='center',fontsize=12)
a.annotate('Removable lid',xy=(-48,deck+h),xytext=(-84,136),arrowprops={'arrowstyle':'->'},fontsize=9)
a.add_patch(FancyArrowPatch((-108,deck),(-108,deck+h),arrowstyle='<->',mutation_scale=10,color='#333333'))
a.text(-111,deck+h/2,f'{h:g} mm',rotation=90,va='center',ha='right',fontsize=9)
a.annotate('Cords towards hand',xy=(24,108),xytext=(-5,137),arrowprops={'arrowstyle':'->'},fontsize=9)
for z in [deck+53.5,deck+62.5]:
    a.annotate('',xy=(30,z),xytext=(-8,z),arrowprops={'arrowstyle':'->','color':'#a4652d','lw':2})
a.text(-56,151,'SIDE VIEW — LOAD PATH',ha='center',weight='bold',fontsize=12)
a.set_xlim(-132,50);a.set_ylim(-8,159)
b=axs[1]
b.add_patch(Rectangle((-47,-104),94,96,facecolor='#dce4de',edgecolor='#263f35',lw=2))
for x,y,name in [(-28,-46,'Index /\nmiddle'),(0,-56,'Thumb'),(28,-46,'Ring /\nlittle')]:
    b.add_patch(Rectangle((x-10,y-20.3),20,40.6,facecolor='#7ea997',edgecolor='#263f35'))
    b.text(x,y,name,ha='center',va='center',fontsize=8)
for x,w,label in [(-23,18,'Nano'),(4,22,'EMG'),(29,12.7,'5 V')]:
    b.add_patch(Rectangle((x-w/2,-99),w,10,facecolor='#e0bc84',edgecolor='#87663a'))
    b.text(x,-94,label,ha='center',va='center',fontsize=8)
b.annotate('Five tendon exits',xy=(10,-8),xytext=(0,12),ha='center',arrowprops={'arrowstyle':'->'},fontsize=9)
b.text(0,28,'TOP VIEW — NOMINAL LAYOUT',ha='center',weight='bold',fontsize=12)
b.text(0,-115,'94 × 96 mm body\nBattery external',ha='center',va='top',fontsize=10)
b.set_xlim(-64,64);b.set_ylim(-137,40)
fig.text(.5,.07,'Schematic only. Straps, wrist restraint and fitted socket are unresolved. Dimensions in mm.',ha='center',fontsize=10,color='#7c3f31')
fig.text(.5,.035,'Original hand and cuff geometry retained; measure the servos and formed cuff before making the enclosure.',ha='center',fontsize=9)
fig.subplots_adjust(left=.04,right=.97,top=.94,bottom=.15,wspace=.12)
fig.savefig(root/'exports/mounting_schematic.png',dpi=180)
fig.savefig(root/'exports/mounting_schematic.svg')
