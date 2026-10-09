"""Dimensioned side schematic; external route shown only as a direction arrow."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
R=Path(__file__).resolve().parent
fig,axes=plt.subplots(1,2,figsize=(11,6))
fig.patch.set_facecolor('#f5f4ef')
for ax,title,inv in zip(axes,['Previous: drums above motors','New: drums below motors'],[False,True]):
 ax.set_facecolor('#f5f4ef');ax.set_aspect('equal');ax.axis('off')
 ax.add_patch(Rectangle((0,0),96,54.9,facecolor='#dce5df',edgecolor='#375149',lw=2))
 case_z=20.9 if inv else 4
 drum_z=5.8 if inv else 41.9
 ax.add_patch(Rectangle((24,case_z),40.6,30,facecolor='#75a48e',edgecolor='#375149'))
 ax.add_patch(Rectangle((41,drum_z),28,7.2,facecolor='#d1a065',edgecolor='#755131'))
 ax.text(44,case_z+15,'Motor',ha='center',va='center',fontsize=11)
 for z in ([6.4,12.5] if inv else [42.4,48.5]):
  ax.plot([69,96],[z,z],color='#9b6128',lw=2)
  ax.add_patch(FancyArrowPatch((96,z),(109,z),arrowstyle='->',mutation_scale=12,color='#9b6128',lw=2))
 ax.plot([-3,98],[-3,-3],color='#556d77',lw=5)
 ax.text(48,-8,'Arm-adapter mounting plane',ha='center',va='top',fontsize=9)
 ax.text(48,68,title,ha='center',fontsize=12,weight='bold')
 ax.text(48,60,'12.5 / 6.4 mm exits' if inv else '42.4 / 48.5 mm exits',ha='center',fontsize=10)
 ax.text(48,-21,'Drum radius stays 12.3 mm',ha='center',fontsize=10)
 ax.set_xlim(-7,115);ax.set_ylim(-28,76)
fig.text(.5,.075,'Same ideal pull and travel. Lower routing may reduce rubbing; actual friction must be measured.',ha='center',fontsize=10)
fig.text(.5,.035,'Side schematic only. Cords remain outside the arm shell. Dimensions in mm.',ha='center',fontsize=9,color='#755131')
fig.subplots_adjust(left=.03,right=.97,top=.96,bottom=.17,wspace=.13)
fig.savefig(R/'exports/routing_comparison.png',dpi=170)
