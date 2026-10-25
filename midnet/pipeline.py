from pathlib import Path
import shutil, yaml, json
from .utils import require, write_json
from .brief import parse_brief
from .subtitles import make_srt
from .assets import inventory
from .render import render
from .cards import make_thumbnail
from .qc import check

def locate_audio(inp):
    for ext in ('wav','mp3','m4a','aac','flac'):
        p=inp/f'audio.{ext}'
        if p.exists(): return p
    media=[p for p in inp.iterdir() if p.suffix.lower() in {'.wav','.mp3','.m4a','.aac','.flac'}]
    return media[0] if media else None

def produce(root,input_dir='input',output_dir='production'):
    root=Path(root); inp=root/input_dir; out=root/output_dir; out.mkdir(parents=True,exist_ok=True)
    require('ffmpeg'); require('ffprobe')
    cfg=yaml.safe_load((root/'config/production.yaml').read_text())
    brief=parse_brief(inp/'brief.md')
    if brief['validation_errors']: raise ValueError('; '.join(brief['validation_errors']))
    audio=locate_audio(inp)
    if not audio: raise FileNotFoundError('Add narration as input/audio.wav or input/audio.mp3')
    report={'pipeline':'MidNet News Video Producer 1.0','input_audio':str(audio),'brief':{'titles':brief['titles'],'resource_names':brief['resources']}}
    srt=out/'subtitles.srt'; report['subtitles']=make_srt(brief['english'],audio,srt)
    assets=inventory(inp/'src',inp/'src/sources.json'); report['assets']=assets
    video=out/'newsVideo.mp4'; report['render']=render(audio,srt,assets,root/'brand/logo/midnet-news-logo-hd.png',brief['english'],video,root/'workspace',cfg)
    bgs=[a['path'] for a in assets if a.get('kind')=='image' and not a.get('error')]
    thumbs=[]
    for i in range(3):
        p=out/f'newsThumbnail{i+1}.png'; make_thumbnail(p,brief['thumbnail_ideas'][i],brief['titles'][i],root/'brand/logo/midnet-news-logo-hd.png',bgs[i%len(bgs)] if bgs else None); thumbs.append(p)
    (out/'uploadInfo.txt').write_text('\n'.join([f'TITLE {i+1}: {t}' for i,t in enumerate(brief['titles'])])+'\n\nDESCRIPTION:\n'+brief['description']+'\n',encoding='utf-8')
    source_lines=['MIDNET NEWS SOURCE RECORD','']+[f"- {a['filename']} | source: {a.get('source','USER-PROVIDED / NOT RECORDED')} | license: {a.get('license','NOT RECORDED')} | archive: {a.get('archive',False)}" for a in assets]
    if not assets: source_lines.append('- No external visual assets used; branded motion cards only.')
    (out/'sourceRecord.txt').write_text('\n'.join(source_lines),encoding='utf-8')
    report['qc']=check(video,srt,thumbs); report['status']=report['qc']['status']
    write_json(out/'productionReport.json',report)
    return report
