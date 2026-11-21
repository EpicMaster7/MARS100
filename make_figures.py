"""Visualize the existing MARS/100 result bundle. Requires matplotlib."""
import json, math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Circle

root=Path(__file__).resolve().parent
R=json.loads((root/'results.json').read_text()); A=R['assumptions']; comp=R['comparison']; tr=R['trajectory']
BG='#081421'; PANEL='#102439'; TEXT='#eef4fa'; MUTED='#a6b7c9'; GOLD='#f6c768'; CYAN='#6acada'; CORAL='#f48e87'; GREEN='#66d3ae'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED})

def title(fig, heading, sub):
    fig.text(.07,.93,heading,fontsize=25,fontweight='bold',color=TEXT)
    fig.text(.07,.875,sub,fontsize=11,color=MUTED)

def tidy(ax):
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)
    ax.set_axisbelow(True)
    ax.grid(axis='x',color='#ffffff',alpha=.10)

fig=plt.figure(figsize=(14,7.875),facecolor=BG)
title(fig,'100 TONNES TO MARS','A conceptual architecture trade study  |  Illustrative cost and risk assumptions')
ax1=fig.add_axes([.19,.29,.29,.48]);ax2=fig.add_axes([.57,.29,.35,.48]);tidy(ax1);tidy(ax2)
labels=['4 direct landers','1 refueled lander','6 prepositioned landers']
colors=[CYAN,GOLD,GREEN]
y=np.arange(3)
cost=[x['cost_musd'] for x in comp]
p=[100*x['success_probability'] for x in comp]
ax1.barh(y,cost,color=colors,height=.49)
ax1.set_yticks(y,labels,color=TEXT);ax1.invert_yaxis();ax1.set_xlim(0,1250);ax1.set_xlabel('Cost (million USD, assumed)',labelpad=13)
for i,c in enumerate(cost):ax1.text(c+20,i,f'${c:,.0f}M',va='center',color=TEXT,fontweight='bold',fontsize=12)
ax1.set_title('Campaign cost',loc='left',color=TEXT,fontsize=15,pad=15)
ax2.barh(y,p,color=colors,height=.49);ax2.set_yticks(y,['']*3);ax2.invert_yaxis();ax2.set_xlim(0,115)
ax2.axvline(A['min_reliability']*100,ls='--',lw=1.6,color=CORAL)
ax2.text(95,3.12,'95% requirement',ha='center',color=CORAL,fontsize=10)
ax2.set_xlabel('Probability of delivering ≥100t (%)',labelpad=13)
ax2.set_title('Modeled full-delivery probability',loc='left',color=TEXT,fontsize=15,pad=15)
for i,q in enumerate(p):ax2.text(q+2,i,f'{q:.1f}%',va='center',color=TEXT,fontweight='bold',fontsize=12)
fig.text(.07,.15,'BASELINE FINDING',color=GOLD,fontsize=10,fontweight='bold')
fig.text(.07,.097,'Six 25t landers are the least-cost option meeting 95% reliability in this model.',fontsize=15,color=TEXT,fontweight='bold')
fig.text(.07,.045,'Not a flight-ready architecture. Landing systems, launch costs, dry masses and reliability values are hypothetical.',fontsize=10,color=MUTED)
fig.savefig(root/'architecture_comparison.png',dpi=185,facecolor=BG);plt.close(fig)

# Plot a genuine two-body Hohmann orbit, aligned with Earth departure at theta=0.
fig=plt.figure(figsize=(14,7.875),facecolor=BG)
title(fig,'THE PHYSICS: EARTH → MARS','Two-body circular-orbit approximation  |  Hohmann transfer and departure injection')
ax=fig.add_axes([.05,.10,.58,.74],facecolor=BG)
for sp in ax.spines.values():sp.set_visible(False)
ax.set_aspect('equal');ax.set_xlim(-1.78,1.78);ax.set_ylim(-1.61,1.61);ax.set_xticks([]);ax.set_yticks([])
t=np.linspace(0,2*np.pi,400)
re=1;rm=1.523679
ax.plot(re*np.cos(t),re*np.sin(t),color=CYAN,alpha=.5,ls=(0,(3,5)),lw=1.6)
ax.plot(rm*np.cos(t),rm*np.sin(t),color=CORAL,alpha=.5,ls=(0,(3,5)),lw=1.6)
a=(re+rm)/2;e=(rm-re)/(rm+re)
# perihelion (x positive), aphelion (x negative): focus at 0, center offset -ae
th=np.linspace(0,np.pi,200)
r=a*(1-e*e)/(1+e*np.cos(th))
ax.plot(r*np.cos(th),r*np.sin(th),color=GREEN,lw=3)
ax.scatter([0],[0],s=390,c=GOLD,zorder=6)
ax.scatter([re], [0],s=135,c=CYAN,zorder=6)
ax.scatter([-rm],[0],s=135,c=CORAL,zorder=6)
ax.annotate('Sun',(0,0),(.07,-.18),color=TEXT,fontsize=12)
ax.annotate('Earth departure',(1,0),(.62,-.21),color=CYAN,fontsize=12)
ax.annotate('Mars arrival',(-rm,0),(-1.53,-.22),color=CORAL,fontsize=12)
ax.annotate('Transfer arc',(-.25,1.16),(.05,1.35),color=GREEN,fontsize=12,arrowprops={'arrowstyle':'-','color':GREEN})
fig.text(.66,.73,f"{tr['transfer_days']:.0f}",color=TEXT,fontsize=38,fontweight='bold');fig.text(.66,.68,'days transfer',color=MUTED,fontsize=12)
fig.text(.66,.55,f"{tr['tmi_dv_kms']:.2f} km/s",color=TEXT,fontsize=27,fontweight='bold');fig.text(.66,.50,'burn from 300 km LEO to',color=MUTED,fontsize=12);fig.text(.66,.46,'trans-Mars injection (TMI)',color=MUTED,fontsize=12)
fig.text(.66,.32,f"{tr['phase_angle_deg']:.1f}°",color=TEXT,fontsize=29,fontweight='bold');fig.text(.66,.27,'Mars lead angle at launch',color=MUTED,fontsize=12)
fig.text(.66,.13,'~26-month launch cadence',color=GOLD,fontsize=13,fontweight='bold')
fig.text(.06,.04,'Schematic scale uses circular planetary orbits; no date-specific ephemeris, aerothermal entry or powered descent integration.',color=MUTED,fontsize=9)
fig.savefig(root/'hohmann_transfer.png',dpi=185,facecolor=BG);plt.close(fig)

# Design space scatter: all choices colored by size, stars threshold.
fig=plt.figure(figsize=(14,7.875),facecolor=BG)
title(fig,'WHEN DOES REDUNDANCY PAY?','All modeled fleet sizes, with identical physics and cost assumptions')
ax=fig.add_axes([.11,.20,.81,.58]);tidy(ax)
for c in R['design_space']:
    cc=GREEN if c['family']=='small' else GOLD
    ax.scatter([c['cost_musd']],[100*c['success_probability']],s=155 if c['id']=='small_6' else 76,
               color=cc,edgecolor=TEXT if c['id']=='small_6' else 'none',lw=1.7,zorder=4)
    if c['id'] in ('small_4','small_5','small_6','small_7','large_1','large_2','large_3'):
        ax.annotate(c['id'].replace('_',' × '), (c['cost_musd'],100*c['success_probability']),
                    xytext=(5,6),textcoords='offset points',color=TEXT,fontsize=9)
ax.axhline(95,ls='--',color=CORAL,lw=1.8,label='95% target')
ax.set_xlim(400,2100);ax.set_ylim(50,103)
ax.set_xlabel('Campaign cost (million USD, illustrative)',labelpad=14)
ax.set_ylabel('P(≥100t delivered), %',labelpad=14)
ax.legend(facecolor=PANEL,labelcolor=TEXT,loc='lower right')
fig.text(.11,.085,'A large monolithic lander is inexpensive in the assumed model, but one landing failure loses the whole cargo target.',color=TEXT,fontsize=12)
fig.text(.11,.046,'The recommendation depends strongly on independence, lander reliability, launch pricing and mass assumptions.',color=MUTED,fontsize=10)
fig.savefig(root/'design_space.png',dpi=185,facecolor=BG);plt.close(fig)
print('Saved three high-resolution PNG charts')
