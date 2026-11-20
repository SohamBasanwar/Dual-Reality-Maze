from pathlib import Path
import json,math,textwrap
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;P=R/'previews';T=P/'part-thumbnails'
parts=[r for r in json.loads((R/'scene.json').read_text()) if not r['component']]
font=lambda n,b=False:ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
groups=[('Full name engraved','Soham Basanwar', '#bfe5cf'),('SB engraved','SB','#c8d9ef'),('No physical lettering','Unmarked','#e8d3b2')]
width=2400;cw=380;ch=335;cols=6;gap=16;x0=20
all_heights=[]
for title,prefix,color in groups:
    subset=sorted([r for r in parts if r['personalization'].startswith(prefix)],key=lambda r:(r['role'],r['name']))
    all_heights.append((title,prefix,color,subset,110+math.ceil(len(subset)/cols)*(ch+gap)))
canvas=Image.new('RGB',(width,180+sum(a[4] for a in all_heights)+100),'#121923');draw=ImageDraw.Draw(canvas)
draw.text((24,20),'DUAL-REALITY MAZE / REVISION 10',font=font(38,True),fill='#efd0a0')
draw.text((24,74),f'{len(parts)} printed assembly parts — actual CAD meshes, not electrical components',font=font(26),fill='#eeeeee')
draw.text((24,115),'Each part is enlarged to fit its card. Sizes are not comparable between cards.',font=font(23),fill='#b9c2cd')
y=180
for title,prefix,color,subset,h in all_heights:
    group=Image.new('RGB',(width,h),'#121923');gd=ImageDraw.Draw(group)
    gd.text((24,18),f'{title}  /  {len(subset)} parts',font=font(33,True),fill=color)
    gd.text((24,62),'Soham Basanwar appears in every assembly-part filename and parts-list entry.',font=font(22),fill='#b9c2cd')
    for i,r in enumerate(subset):
        x=x0+(i%cols)*(cw+gap);yy=110+(i//cols)*(ch+gap)
        gd.rounded_rectangle((x,yy,x+cw,yy+ch),12,fill='#26303c')
        img=Image.open(T/(r['role']+'-'+r['name']+'.png')).convert('RGB');img.thumbnail((cw-12,240))
        group.paste(img,(x+(cw-img.width)//2,yy+5))
        gd.text((x+12,yy+245),r['role'].upper(),font=font(19,True),fill=color)
        for j,line in enumerate(textwrap.wrap(r['name'].replace('_',' '),27)):
            gd.text((x+12,yy+273+j*24),line,font=font(21),fill='#f5f5f5')
    group.save(P/('printed-parts-'+('full-name' if prefix.startswith('Soham') else 'sb' if prefix=='SB' else 'unmarked')+'.png'))
    canvas.paste(group,(0,y));y+=h
draw.text((24,y+22),'Unmarked: optical, thin, tiny or fit-sensitive parts. Test coupons are cropped samples, not additional assembly parts.',font=font(22),fill='#b9c2cd')
draw.text((24,y+56),'One selected reveal dome and one diffuser/mask per enclosure are counted. Optional roof alternatives are substitutions.',font=font(22),fill='#b9c2cd')
canvas.save(P/'printed-parts-all.png')
print('Inventory sheets:',len(parts),'assembly parts; no electronic reference blocks.')
