"""Run tendon_forces.py first. Optional plot dependency: matplotlib."""
import json, math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
d=json.loads((R/'tendon_forces.json').read_text());a=d['assumptions']
r=[8+i*8/149 for i in range(150)]
fig,ax=plt.subplots(1,2,figsize=(11,4.4),layout='constrained')
for eta in [.4,.6,.8]:
 ax[0].plot(r,[eta*d['working_torque_Nm']/(2*a['load_margin']*v/1000) for v in r],label=f'{eta:.0%} routing efficiency')
ax[0].scatter([a['effective_radius_mm']],[d['sensitivity'][1]['pair_tendon_N_each']],color='#222',zorder=5)
ax[0].set(xlabel='Effective winding radius (mm)',ylabel='Tendon tension per paired finger (N)',title='Force screening limit')
ax[0].legend(frameon=False,fontsize=9)
ax[1].plot(r,[v*math.radians(160) for v in r],color='#277c87')
ax[1].scatter([a['effective_radius_mm']],[d['travel'][2]['take_up_mm']],color='#222')
ax[1].set(xlabel='Effective winding radius (mm)',ylabel='Ideal take-up (mm)',title='Travel at an illustrative 160° sweep')
for axis in ax:
 axis.axvline(a['effective_radius_mm'],color='#444',ls='--',lw=1)
 axis.grid(alpha=.2);axis.spines[['top','right']].set_visible(False)
fig.suptitle('Current spool: 12.3 mm effective radius • 13.4 N per finger at 60% efficiency • 34.3 mm travel',fontsize=11)
fig.savefig(R/'force_travel.png',dpi=160)
