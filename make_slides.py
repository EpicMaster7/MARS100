from pathlib import Path
import json, math
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR

root=Path(__file__).parent
R=json.loads((root/'results.json').read_text())
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
BG='071522';CARD='12283B';CARD2='182F42';TEXT='EDF4FA';MUTED='ADC2D1';GOLD='F5C86C';CYAN='71CDDD';GREEN='6BD6AE';CORAL='FF9387'
def col(hex):return RGBColor.from_string(hex)
def shape(sl,x,y,w,h,fill,line=None,r=0):
    sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=col(fill);sh.line.fill.background() if line is None else None
    if line:sh.line.color.rgb=col(line)
    if r:
        try:sh.adjustments[0]=.10
        except:pass
    return sh
def text(sl,x,y,w,h,s,size=18,color=TEXT,bold=False,align=None,font='Aptos',margin=0):
    tb=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=tb.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_top=Inches(margin);tf.margin_bottom=Inches(margin);tf.margin_left=Inches(margin);tf.margin_right=Inches(margin)
    p=tf.paragraphs[0];p.text=s;p.font.name=font;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=col(color)
    if align:p.alignment=align
    return tb
def slidebg():
    sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=col(BG);return sl
def footer(sl,n,src='MARS/100 · Conceptual model · Hypothetical costs & probabilities'):
    shape(sl,.57,7.04,12.18,.013,'294257');text(sl,.58,7.13,11.7,.21,src,10,MUTED);text(sl,12.37,7.12,.35,.20,f'{n:02}',10,MUTED,align=PP_ALIGN.RIGHT)
def tag(sl,s):text(sl,.65,.38,9,.3,s.upper(),12,GOLD,True)
def heading(sl,s,desc=None):text(sl,.65,.86,12.0,.76,s,34,TEXT,True);desc and text(sl,.67,1.64,11.95,.55,desc,16,MUTED)
def ellipse(sl,x,y,w,h,stroke,width=1.5):
    e=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(y),Inches(w),Inches(h));e.fill.background();e.line.color.rgb=col(stroke);e.line.width=Pt(width)
    return e

# 1
s=slidebg();tag(s,'Aerospace · mission architecture');text(s,.67,1.32,7.0,2.15,'100 TONNES\nTO MARS.',48,TEXT,True)
text(s,.70,3.55,6.0,.9,'Which delivery architecture minimizes cost without sacrificing the entire mission?',22,MUTED)
shape(s,.68,5.29,5.55,.59,CARD,line='2F4F61',r=1);text(s,.87,5.41,5.10,.32,'GOAL: ≥100t landed at ≥95% modeled reliability',14,GREEN,True)
# orbit art
ellipse(s,7.00,1.0,5.3,5.3,'446F85',1.6);ellipse(s,7.80,1.79,3.7,3.7,CYAN,1.6)
sl=s
sh=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(9.42),Inches(3.40),Inches(.49),Inches(.49));sh.fill.solid();sh.fill.fore_color.rgb=col(GOLD);sh.line.fill.background()
sh=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(11.41),Inches(3.4),Inches(.17),Inches(.17));sh.fill.solid();sh.fill.fore_color.rgb=col(CYAN);sh.line.fill.background()
sh=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(6.98),Inches(3.58),Inches(.20),Inches(.20));sh.fill.solid();sh.fill.fore_color.rgb=col(CORAL);sh.line.fill.background()
text(s,10.19,3.48,1.4,.3,'SUN',11,GOLD,True);text(s,11.23,3.98,1.5,.3,'EARTH',11,CYAN,True);text(s,6.72,3.98,1.2,.3,'MARS',11,CORAL,True)
footer(s,1)

# 2
s=slidebg();tag(s,'The design problem');heading(s,'One goal. Three competing strategies.','How should a mission team deliver an ambitious cargo target to the Martian surface?')
items=[('A','DIRECT','4 × 25t','Four smaller launches with no orbital refueling.','71CDDD'),('B','REFUEL','1 × 100t','One large lander supported by four tanker launches.','F5C86C'),('C','REDUNDANT','6 × 25t','Six smaller landers across two launch windows; two can fail.','6BD6AE')]
for i,(letter,name,qty,ex,clr) in enumerate(items):
 x=.67+i*4.25;shape(s,x,2.45,3.88,3.76,CARD,line='284658',r=1)
 text(s,x+.23,2.72,3.27,.32,letter+'  /  '+name,12,clr,True)
 text(s,x+.24,3.27,3.34,.65,qty,34,TEXT,True)
 text(s,x+.24,4.12,3.3,1.10,ex,17,MUTED)
 text(s,x+.23,5.70,3.35,.34,'Mars surface delivery',12,clr)
text(s,.67,6.47,12,.36,'Success is not only a question of how much cargo is launched. Failure modes and redundancy matter.',17,TEXT)
footer(s,2)

#3
s=slidebg();s.shapes.add_picture(str(root/'hohmann_transfer.png'),0,0,width=prs.slide_width,height=prs.slide_height)
# chart already contains title/labels; no extra footer

#4
s=slidebg();tag(s,'Rocket equation');heading(s,'Propellant is the architectural bottleneck.','Backwards mass sizing from the Martian surface to low Earth orbit.')
shape(s,.68,2.32,5.85,3.35,CARD,r=1);shape(s,6.81,2.32,5.85,3.35,CARD,r=1)
text(s,.95,2.58,5.2,.30,'25t DIRECT LANDER',13,CYAN,True);text(s,.95,3.15,5.2,.81,'139t',42,TEXT,True)
text(s,.95,4.14,5.17,.62,'Required mass before trans-Mars injection',17,MUTED)
text(s,.95,5.02,5.1,.38,'Within assumed 150t orbital capacity',14,GREEN,True)
text(s,7.12,2.58,4.9,.30,'100t REFUELED LANDER',13,GOLD,True);text(s,7.12,3.15,5.2,.81,'448t',42,TEXT,True)
text(s,7.12,4.14,5.1,.67,'Required mass before trans-Mars injection',17,MUTED)
text(s,7.12,5.02,4.95,.38,'4 additional propellant tanker flights',14,GOLD,True)
text(s,.79,6.15,12,.48,'Mass ratio = exp( Δv / (g₀ × Isp) )      •      TMI: 3.59 km/s      •      Terminal descent: assumed 0.60 km/s',17,TEXT)
footer(s,4,'Assumed dry mass and EDL model, not engineering-validated lander sizing')

#5
s=slidebg();s.shapes.add_picture(str(root/'architecture_comparison.png'),0,0,width=prs.slide_width,height=prs.slide_height)

#6
s=slidebg();s.shapes.add_picture(str(root/'design_space.png'),0,0,width=prs.slide_width,height=prs.slide_height)

#7
s=slidebg();tag(s,'Sensitivity · research limits');heading(s,'The answer depends on the assumptions.','Reliability estimates can shift the preferred fleet size.')
shape(s,.69,2.24,6.08,3.73,CARD,line='2B5360',r=1)
text(s,1.00,2.58,5.45,.32,'A useful sensitivity threshold',14,GREEN,True)
text(s,1.00,3.13,5.3,.81,'86.4%',39,TEXT,True)
text(s,1.00,4.14,5.3,1.06,'Minimum assumed small-lander EDL success for six landers to clear a 95% campaign target.',17,MUTED)
shape(s,7.02,2.24,5.62,3.73,CARD,line='2B5360',r=1)
text(s,7.32,2.58,4.9,.32,'The critical limitation',14,CORAL,True)
text(s,7.32,3.15,4.89,2.45,'Mars landing systems able to deliver 25t or 100t remain conceptual. Failure events could be correlated, undermining the model\'s assumed reliability gain.',20,TEXT)
text(s,.74,6.43,11.95,.32,'Next: correlated failures → refined EDL mass → date-specific ephemerides → credible cost ranges',16,GOLD,True)
footer(s,7,'NASA NTRS 2022 SAC21 and 2026 Mars EDL chapter; hypothetical scenario model')

#8
s=slidebg();tag(s,'Takeaways');heading(s,'How would a mission architect think?')
lessons=[('01','CONSTRAINTS CHANGE THE WINNER','The cheapest standalone design fails the 95% model reliability test.'),('02','REDUNDANCY IS NOT FREE','Six independent landers improve modeled success, but require more launches and two windows.'),('03','UNKNOWN TECHNOLOGY DOMINATES','Real Mars EDL capability, dry mass and common-mode risk matter more than tiny orbital refinements.')]
for i,(num,ttl,desc) in enumerate(lessons):
 y=2.03+i*1.43;shape(s,.72,y,11.91,1.20,CARD,r=1);text(s,1.02,y+.19,1.03,.49,num,24,GOLD,True);text(s,2.02,y+.13,9.87,.30,ttl,16,TEXT,True);text(s,2.02,y+.56,9.85,.57,desc,14,MUTED)
text(s,.74,6.60,11.9,.31,'Conceptual trade study, not a flight-qualified mission or a verified cost forecast.',14,CORAL)
footer(s,8)

prs.save(root/'walkthrough.pptx');print('wrote',len(prs.slides),'slides')
