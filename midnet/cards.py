from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import textwrap
NAVY=(7,26,51); NAVY2=(18,54,90); RED=(215,25,32); WHITE=(255,255,255); SILVER=(201,210,220)
def font(size,bold=True):
    candidates=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
def contain(im, box):
    im=im.copy(); im.thumbnail(box,Image.Resampling.LANCZOS); return im
def make_card(path,title,subtitle='',logo=None,background=None,size=(1920,1080)):
    W,H=size
    canvas=Image.new('RGB',size,NAVY); d=ImageDraw.Draw(canvas)
    for y in range(H):
        t=y/H; c=tuple(round(NAVY[i]*(1-t)+NAVY2[i]*t) for i in range(3)); d.line((0,y,W,y),fill=c)
    if background and Path(background).exists():
        try:
            bg=Image.open(background).convert('RGB'); scale=max(W/bg.width,H/bg.height); bg=bg.resize((round(bg.width*scale),round(bg.height*scale)),Image.Resampling.LANCZOS); left=(bg.width-W)//2; top=(bg.height-H)//2; bg=bg.crop((left,top,left+W,top+H)); bg=bg.filter(ImageFilter.GaussianBlur(1)); canvas=Image.blend(bg,canvas,0.32); d=ImageDraw.Draw(canvas)
        except Exception: pass
    d.rectangle((0,0,W,18),fill=RED); d.polygon([(0,H-170),(W,H-250),(W,H),(0,H)],fill=(5,18,35))
    wrap='\n'.join(textwrap.wrap(title,28)[:3]); f=font(82); d.multiline_text((110,270),wrap,font=f,fill=WHITE,spacing=17,stroke_width=2,stroke_fill=(0,0,0))
    if subtitle: d.text((115,690),subtitle[:85],font=font(34),fill=SILVER)
    d.rectangle((110,218,360,232),fill=RED)
    if logo and Path(logo).exists():
        lg=Image.open(logo).convert('RGBA'); lg=contain(lg,(210,210)); canvas.paste(lg,(W-lg.width-54,54),lg)
    canvas.save(path,quality=96)
def make_thumbnail(path,idea,title,logo=None,background=None):
    make_card(path,title,idea,logo,background,(1280,720))
