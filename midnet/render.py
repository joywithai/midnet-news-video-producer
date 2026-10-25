from pathlib import Path
from PIL import Image
from .utils import run, media_duration
from .cards import make_card

def render(audio,srt,assets,logo,english,out,workspace,cfg):
    workspace=Path(workspace); frames=workspace/'cards'; frames.mkdir(parents=True,exist_ok=True)
    dur=media_duration(audio); interval=float(cfg['visuals']['seconds_per_asset']); count=max(1,int(dur//interval)+1)
    valid=[a for a in assets if a.get('kind')=='image' and not a.get('error')]
    title=english.split('.')[0].strip()[:100] or 'MidNet News'
    cards=[]
    for i in range(count):
        bg=valid[i%len(valid)]['path'] if valid else None
        p=frames/f'card_{i:03}.png'; make_card(p,title,'Truth First. News That Matters.',logo,bg); cards.append(p)
    concat=workspace/'cards.txt'; lines=[]
    for p in cards: lines += [f"file '{p.as_posix()}'",f'duration {interval}']
    lines += [f"file '{cards[-1].as_posix()}'"]
    concat.write_text('\n'.join(lines),encoding='utf-8')
    subtitle_filter=f"subtitles={Path(srt).as_posix()}:force_style='FontName=DejaVu Sans,FontSize=26,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101820,BorderStyle=1,Outline=2,Shadow=0,MarginV=42,Alignment=2'"
    cmd=['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-vf',subtitle_filter+',scale=1920:1080,format=yuv420p','-r',str(cfg['video']['fps']),'-c:v','libx264','-preset',cfg['video']['preset'],'-crf',str(cfg['video']['crf']),'-c:a','aac','-b:a','192k','-shortest',str(out)]
    run(cmd); return {'duration':dur,'card_count':count,'used_user_visuals':len(valid)}
